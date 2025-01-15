from faster_whisper import WhisperModel
import os

def transcribeAudio(audio_path):
    # Use CPU with optimized settings since ROCm support might be limited
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="float32",
        cpu_threads=6,  # Adjust based on your CPU cores
        num_workers=2
    )
    
    try:
        segments, _ = model.transcribe(
            audio_path,
            beam_size=5,
            word_timestamps=True,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
        transcriptions = []
        for segment in segments:
            transcriptions.append((segment.text, segment.start, segment.end))
        
        return transcriptions
        
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return []