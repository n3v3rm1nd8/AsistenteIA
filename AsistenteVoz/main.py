import pyaudio
import speech_recognition as sr
import unicodedata, os, pyttsx3, subprocess, time

# Configuración de PyAudio
CHUNK = 1024  # Tamaño del buffer de audio
FORMAT = pyaudio.paInt16  # Formato de audio (16 bits por muestra)
CHANNELS = 1  # Número de canales (mono)
RATE = 44100  # Tasa de muestreo (samples por segundo)

def initialize_recognizer():
    return sr.Recognizer()

def get_default_device_index():
    p = pyaudio.PyAudio()
    default_device_index = p.get_default_input_device_info()['index']
    p.terminate()
    return default_device_index

def capture_audio_from_default_device(duration=5):
    p = pyaudio.PyAudio()
    default_device_index = get_default_device_index()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=default_device_index)
    talk('¿En que puedo ayudarte?')
    print("Escuchando...\n")
    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    audio_data = b''.join(frames)
    return sr.AudioData(audio_data, RATE, 2)

def recognize_speech_from_audio(audio_data, recognizer, language="es-ES"):
    try:
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except Exception as e:
        pass
    
def remove_accents(input_str):
    if input_str == None:
        return ''
    # Normalizar la cadena de texto a su forma descompuesta
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # Filtrar solo los caracteres que no son acentuados
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def talk(textClean):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(textClean)
    engine.runAndWait()

if __name__ == "__main__":
    recognizer = initialize_recognizer()
    text_w_accents = ''
    textClean = ''
    while True:
        try:
            audio_data = capture_audio_from_default_device(duration=5)
            text_w_accents = recognize_speech_from_audio(audio_data, recognizer, language="es-ES")
            textClean = remove_accents(text_w_accents).lower()
            print("Has dicho: " + textClean)

            if 'adios' in textClean:
                talk('Un placer ayudarte, hasta pronto')
                break

            elif 'opera' in textClean:
                talk("Abriendo opera")
                subprocess.Popen("C:\\Users\\<USER>\\AppData\\Local\\Programs\\Opera GX\\opera.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
                time.sleep(1)

            elif 'discord' in textClean:
                talk('Abriendo discord')
                subprocess.Popen("C:\\Users\\<USER>\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
                time.sleep(1)

            elif 'lolis' in textClean:
                talk('Abriendo el genshin impact')
                subprocess.Popen("C:\\Program Files\\HoYoPlay\\launcher.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
                time.sleep(1)

            elif 'valorant' in textClean:
                talk('Abriendo valorant')
                subprocess.Popen("C:\\Riot Games\\Riot Client\\RiotClientServices.exe --launch-product=valorant --launch-patchline=live", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
                time.sleep(1)

            elif 'spotify' in textClean:
                talk('Abriendo Spotify')
                subprocess.Popen("C:\\Users\\<USER>\\AppData\\Roaming\\Spotify\\Spotify.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
                time.sleep(1)

            else:
                talk('Lo siento, no reconozco la instruccion')

        except KeyboardInterrupt:
            print("\nInterrupción del usuario. Terminando el programa.")
            break
        except Exception as e:
            print(f"Se produjo un error en el bucle: {e}")