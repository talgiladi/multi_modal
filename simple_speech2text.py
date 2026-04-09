import numpy as np
import soundfile as sf
from transformers import pipeline

# Initialize the speech-to-text pipeline from Hugging Face Transformers.
# Passing raw audio avoids the pipeline's ffmpeg-based file loading path.
pipe = pipeline(
  "automatic-speech-recognition",
  model="openai/whisper-tiny.en",
  chunk_length_s=30,
)

def load_audio(path: str) -> dict:
  audio, sample_rate = sf.read(path, dtype="float32")

  if audio.ndim > 1:
    audio = np.mean(audio, axis=1, dtype=np.float32)

  return {"raw": audio, "sampling_rate": sample_rate}

# Define the path to the audio file that needs to be transcribed.
sample = "sample-meeting.wav"
audio_input = load_audio(sample)
print("audio loaded")
# Perform speech recognition on in-memory audio instead of handing the filename
# to transformers, which removes the ffmpeg system dependency for WAV input.
prediction = pipe(audio_input, batch_size=8)["text"]

print(f"model output: {prediction}")
