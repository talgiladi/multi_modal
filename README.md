# MultiModal Speech-to-Text

This project includes a Docker image for running the Gradio speech-to-text app
without relying on host-level package installs.

## Run with Docker

Build the image:

```bash
docker build -t multimodal-speech2text .
```

Start the app:

```bash
docker run --rm -p 5000:5000 multimodal-speech2text
```

Then open `http://localhost:5000`.

## Run with Docker Compose

```bash
docker compose up --build
```

## What is bundled

- Python runtime
- Python app dependencies
- `ffmpeg` inside the container
- Preloaded `openai/whisper-tiny.en` model during image build

The app listens on port `5000` inside the container.
