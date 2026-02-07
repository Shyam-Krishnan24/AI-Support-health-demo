import time

try:
    import pyttsx3
    engine = pyttsx3.init()

    def speak(text):
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            print("[VOICE]", text)

except Exception:
    def speak(text):
        print("[VOICE]", text)


def listen(prompt=None, timeout=5):
    """Listen for voice input with automatic fallback to keyboard input."""
    if prompt:
        speak(prompt)
    
    # Try speech recognition first
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                if prompt:
                    print(prompt)
                audio = r.listen(source, timeout=timeout)
                text = r.recognize_google(audio)
                return text.strip()
        except (OSError, sr.UnknownValueError, sr.RequestError):
            # Microphone unavailable or recognition failed - fall through to keyboard
            pass
    except Exception:
        # speech_recognition not installed - fall through to keyboard
        pass
    
    # Fallback to keyboard input
    try:
        if prompt:
            return input(prompt + " (type): ").strip()
        return input().strip()
    except Exception:
        return ""
