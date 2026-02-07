import time

try:
    import pyttsx3
    engine = pyttsx3.init()

    def speak(text):
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            print("[TTS]", text)

except Exception:
    def speak(text):
        print("[TTS]", text)


def listen(prompt=None, timeout=5):
    if prompt:
        speak(prompt)
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if prompt:
                print(prompt)
            audio = r.listen(source, timeout=timeout)
            text = r.recognize_google(audio)
            return text.strip()
    except Exception:
        # Fallback to keyboard input
        if prompt:
            try:
                return input(prompt + " (type): ").strip()
            except Exception:
                return ""
        try:
            return input().strip()
        except Exception:
            return ""
