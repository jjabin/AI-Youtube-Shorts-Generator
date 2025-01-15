from faster_whisper import WhisperModel

def transcribeAudio(audio_path):
    # Load the model with explicit compute type
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="float32"  # Explicitly set compute type to float32
    )
    
    # Transcribe the audio
    segments, _ = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True
    )
    
    transcriptions = []
    
    for segment in segments:
        transcriptions.append((segment.text, segment.start, segment.end))
    
    return transcriptions