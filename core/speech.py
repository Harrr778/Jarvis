import speech_recognition as sr
import pyttsx3
import logging

logger = logging.getLogger("jarvis.speech")

class SpeechEngine:
    def __init__(self, config):
        """Инициализация речевого движка"""
        # Настройка синтеза речи
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        
        # Применяем настройки из конфигурации
        voice_index = config.get("voice_index", 0)
        if voice_index < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_index].id)
        
        self.engine.setProperty('rate', config.get("voice_rate", 190))
        
        # Настройка распознавания речи
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = config.get("energy_threshold", 300)
        
        logger.info("Речевой движок инициализирован")
    
    def speak(self, text):
        """Произносит текст"""
        logger.debug(f"Говорю: {text}")
        print(f"Джарвис: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Слушает и распознает речь"""
        try:
            with sr.Microphone() as source:
                print("Слушаю...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                
            print("Распознаю...")
            query = self.recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {query}")
            return query.lower()
        except sr.UnknownValueError:
            logger.warning("Не удалось распознать речь")
            print("Не удалось распознать речь")
            return ""
        except Exception as e:
            logger.error(f"Ошибка при распознавании речи: {e}")
            print(f"Ошибка: {e}")
            return ""