FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/huggingface \
    TRANSFORMERS_CACHE=/opt/huggingface \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=5000

WORKDIR /app

# ffmpeg is installed inside the image so the app does not depend on host
# packages when handling formats that still need codec support.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.docker.txt .

RUN pip install --upgrade pip \
    && pip install --index-url https://download.pytorch.org/whl/cpu torch==2.11.0 \
    && pip install -r requirements.docker.txt

COPY . .

# Preload the Whisper model at build time so runtime does not need to fetch it.
RUN python -c "from transformers import pipeline; pipeline('automatic-speech-recognition', model='openai/whisper-tiny.en', chunk_length_s=30)"

EXPOSE 5000

CMD ["python", "speech2text_app.py"]
