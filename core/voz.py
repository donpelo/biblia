import pyttsx3
engine = pyttsx3.init()
def leer(texto):
    engine.say(texto)
    engine.runAndWait()
