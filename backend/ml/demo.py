import sys
import os
from scipy.spatial import ConvexHull
from ml.animate import normalize_kp
from ml.modules.keypoint_detector import KPDetector
from ml.modules.generator import OcclusionAwareGenerator
from ml.sync_batchnorm import DataParallelWithCallback
import torch
from skimage import img_as_ubyte
from skimage.transform import resize
import numpy as np
import imageio
from tqdm import tqdm
from argparse import ArgumentParser
import yaml
import matplotlib
matplotlib.use('Agg')


if sys.version_info[0] < 3:
    raise Exception(
        "You must use Python 3 or higher. Recommended version is Python 3.7")


def load_checkpoints(config_path, checkpoint_path, cpu=False):

    with open(config_path) as f:
        config = yaml.load(f)

    generator = OcclusionAwareGenerator(**config['model_params']['generator_params'],
                                        **config['model_params']['common_params'])
    if not cpu:
        generator.cuda()

    kp_detector = KPDetector(**config['model_params']['kp_detector_params'],
                             **config['model_params']['common_params'])
    if not cpu:
        kp_detector.cuda()

    if cpu:
        checkpoint = torch.load(
            checkpoint_path, map_location=torch.device('cpu'))
    else:
        checkpoint = torch.load(checkpoint_path)

    generator.load_state_dict(checkpoint['generator'])
    kp_detector.load_state_dict(checkpoint['kp_detector'])

    if not cpu:
        generator = DataParallelWithCallback(generator)
        kp_detector = DataParallelWithCallback(kp_detector)

    generator.eval()
    kp_detector.eval()

    return generator, kp_detector


def record_progress(filename, current, max):
    with open(filename, 'w') as progressFile:
        progressFile.write(f'{current}/{max}')


def make_animation(progress_file, source_image, driving_video, generator, kp_detector, relative=True, adapt_movement_scale=True, cpu=False):
    with torch.no_grad():
        predictions = []
        source = torch.tensor(source_image[np.newaxis].astype(
            np.float32)).permute(0, 3, 1, 2)
        if not cpu:
            source = source.cuda()
        driving = torch.tensor(np.array(driving_video)[np.newaxis].astype(
            np.float32)).permute(0, 4, 1, 2, 3)
        kp_source = kp_detector(source)
        kp_driving_initial = kp_detector(driving[:, :, 0])

        for frame_idx in tqdm(range(driving.shape[2])):
            driving_frame = driving[:, :, frame_idx]
            if not cpu:
                driving_frame = driving_frame.cuda()
            kp_driving = kp_detector(driving_frame)
            kp_norm = normalize_kp(kp_source=kp_source, kp_driving=kp_driving,
                                   kp_driving_initial=kp_driving_initial, use_relative_movement=relative,
                                   use_relative_jacobian=relative, adapt_movement_scale=adapt_movement_scale)
            out = generator(source, kp_source=kp_source, kp_driving=kp_norm)

            predictions.append(np.transpose(
                out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0])

            record_progress(progress_file, frame_idx+1, driving.shape[2])

    return predictions


def generate(progress_file, config, checkpoint, source_image, driving_video, result_video, relative=True, adapt_scale=True, find_best_frame=True, best_frame=None, cpu=True):
    source_image = imageio.imread(source_image)
    reader = imageio.get_reader(driving_video)
    fps = reader.get_meta_data()['fps']
    driving_video = []
    try:
        for im in reader:
            driving_video.append(im)
    except RuntimeError:
        pass
    reader.close()

    source_image = resize(source_image, (256, 256))[..., :3]
    driving_video = [resize(frame, (256, 256))[..., :3]
                     for frame in driving_video]
    generator, kp_detector = load_checkpoints(
        config_path=config, checkpoint_path=checkpoint, cpu=cpu)

    predictions = make_animation(progress_file, source_image, driving_video, generator, kp_detector,
                                 relative=relative, adapt_movement_scale=adapt_scale, cpu=cpu)
    imageio.mimsave(result_video, [img_as_ubyte(
        frame) for frame in predictions], fps=fps)
