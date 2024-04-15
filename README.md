---
date: 2024-04-15T11:34:08.644896
author: AutoGPT <info@agpt.co>
---

# Text-to-Speech API

The project entails building an endpoint that can accept plain text or SSML formatted input, convert this input into natural-sounding speech audio utilizing Python libraries, and allow the customization of various voice parameters such as voice type, speed, pitch, volume, and potentially other parameters like strategic pauses for enhanced clarity and emotional impact. The preferred Python package for the text-to-speech conversion process is pyttsx3 due to its offline capabilities and extensive customization features, including voice type (neutral preferred), rate (speed), and volume adjustments. Additionally, the generated audio file should be available in MP3 format, which suits the user's needs. Essential insights and requirements gathered from the interview process include the importance of customization in the text-to-speech process to create a more engaging and natural auditory experience. Libraries such as gTTS and SpeechRecognition were also identified as relevant for text-to-speech and speech-to-text conversions but were not selected due to the project's specific requirements and the need for offline functionality.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Text-to-Speech API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
