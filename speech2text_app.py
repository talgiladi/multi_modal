import numpy as np
import gradio as gr
import soundfile as sf
from transformers import pipeline

# Initialize the speech recognition pipeline once at startup so requests can
# reuse the same model instance inside the container.
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny.en",
    chunk_length_s=30,
)

# Function to transcribe audio using the OpenAI Whisper model
def transcript_audio(audio_file):
    a = load_audio(audio_file)
    result = pipe(a, batch_size=8)["text"]
    return result


def load_audio(path: str) -> dict:
    audio, sample_rate = sf.read(path, dtype="float32")

    if audio.ndim > 1:
        audio = np.mean(audio, axis=1, dtype=np.float32)

    return {"raw": audio, "sampling_rate": sample_rate}

# Set up Gradio interface
audio_input = gr.Audio(sources="upload", type="filepath")  # Audio input
output_text = gr.Textbox()  # Text output

# Create the Gradio interface with the function, inputs, and outputs
iface = gr.Interface(
    fn=transcript_audio,
    inputs=audio_input,
    outputs=output_text,
    title="Audio Transcription App",
    description="Upload the audio file",
)

# Launch the Gradio app
iface.launch(server_name="0.0.0.0", server_port=5000)
