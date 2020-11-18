# deepfake

## Getting started

* Clone the repo
* Go to `frontend` directory
* Open a new terminal, run `npm start` to start the react backend

* Next, go to `backend` directory
* Open a new terminal, run `start.bat` (Windows) or `start.sh` (Linux/Mac) to start the python backend


* Go to `localhost:3000` and try it out

## Inspiration

Deepfakes was inspired by youtube videos that showed, you guessed it — deepfakes! They were professionally created, but our production came very close to their models. Look in the video and see for yourself.

## What it does

Creates a "face-swap" video with a source image and a driving video.

## How we built it

We used React for the frontend and Python for the backend, used `first-order-model` from Github as our main ML model. 

## Challenges we ran into

We could not deploy the ML model because we had no experience in it.

## Accomplishments that we're proud of

We were successfully able to replicate the demos provided in the `first-order-model` repo on GitHub and made a custom frontend for easy user input.

## We learned

We learned how to run an ML model on our computers, and that ML models can also run without a GPU, solely relying on CPU.

## Demo
You can check out our demo on [Devpost](https://devpost.com/software/deepfakes-798voc)
