import whisper
import re


# Load model once (global)
model = whisper.load_model("base")


def analyze_audio(video_path: str):
    try:
        result = model.transcribe(video_path)
        transcript = result["text"]

        # Filler words
        filler_words = ["uh", "um", "like", "you know", "so", "actually"]
        filler_count = 0

        words = re.findall(r'\w+', transcript.lower())

        for word in words:
            if word in filler_words:
                filler_count += 1

        total_words = len(words)

        filler_ratio = filler_count / total_words if total_words > 0 else 0

        return {
            "transcript": transcript,
            "total_words": total_words,
            "filler_count": filler_count,
            "filler_ratio": round(filler_ratio, 2)
        }

    except Exception as e:
        return {"error": str(e)}
