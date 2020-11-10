
/**
 * Component to handle file upload. Works for image
 * uploads, but can be edited to work for any file.
 */
import React from "react";

export function FileUpload() {
    // State to store uploaded file
    const [image, setImage] = React.useState("");
    const [video, setVideo] = React.useState("");
    
    // Handles file upload event and updates state
    function handleUploadImage(event) {
      setImage(event.target.files[0]);
    }
    function handleUploadVideo(event) {
      setVideo(event.target.files[0]);
    }
  
    return (
      <form
        method="POST"
        enctype="multipart/form-data"
        name="upload"
        action="http://localhost:8000/upload"
        id="upload-box"
      >
        <label for="image">Image: </label>
        <input id="image" type="file" name="image" onChange={handleUploadImage} />
        <label for="video">Video: </label>
        <input id="video" type="file" name="video" onChange={handleUploadVideo} />
        <div>
          <button class="submitBtn" type="submit">
            Submit
          </button>
        </div>
      </form>
    );
  }
  // http://localhost/upload  parameter image=... 
  // response: {"status": "ok", "url": "http://localhost/get_result?id=13982190321903"}
  // client display loading
  // client pings the "url" every 10 seconds
  // "get_result" will return either {"status": "not ready"} OR {"status": "ready", "url": "http://localhost/videos/13982190321903.mp4"}
  
  /**
   * Component to display thumbnail of image.
   */
  const ImageThumb = ({ image }) => {
    return <img src={URL.createObjectURL(image)} alt={image.name} />;
  };
  