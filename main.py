import os
import sys
import json
import threading
from core.speech import SpeechEngine
from core.ai_brain import AI
from core.memory import MemorySystem
from modules.system_commands import SystemCommands
from modules.applications import ApplicationManager
from utils.logger import setup_logger

# Настройка путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")
DATA_PATH = os.path.join(BASE_DIR, "data")

# Создаем необходимые директории
os.makedirs(os.path.join(DATA_PATH, "memory"), exist_ok=True)
os.makedirs(os.path.join(DATA_PATH, "logs"), exist_ok=True)
os.makedirs(os.path.join(DATA_PATH, "media"), exist_ok=True)

# Настройка логирования
logger = setup_logger("jarvis", os.path.join(DATA_PATH, "logs", "jarvis.log"))

def load_config():
    """Загружает настройки из файла конфигурации"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файл не найден, создаем базовую конфигурацию
        default_config = {
            "user_name": "",
            "ai": {
                "api_key": "",
                "model": "gpt-4"
            },
            "speech": {
                "voice_rate": 190,
                "voice_index": 0,
                "energy_threshold": 300
            },
            "system": {
                "startup": False,
                "tray_icon": True
            }
        }
        
        # Создаем директорию config, если она не существует
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        
        # Записываем базовую конфигурацию
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        
        return default_config

class Jarvis:
    def __init__(self):
        """Инициализация Джарвиса"""
        logger.info("Инициализация Джарвиса")
        
        # Загрузка конфигурации
        self.config = load_config()
        
        # Инициализация компонентов
        self.memory = MemorySystem(os.path.join(DATA_PATH, "memory"))
        self.speech = SpeechEngine(self.config["speech"])
        self.ai = AI(self.config["ai"], self.memory)
        self.system_commands = SystemCommands()
        self.app_manager = ApplicationManager()
        
        # Флаг работы
        self.running = False
    
    def start(self):
        """Запуск Джарвиса"""
        self.running = True
        
        # Приветствие
        user_name = self.config["user_name"]
        if user_name:
            self.speech.speak(f"Здравствуйте, {user_name}! Джарвис к вашим услугам.")
        else:
            self.speech.speak("Здравствуйте! Я Джарвис, ваш персональный ассистент. Как я могу к вам обращаться?")
            user_name = self.speech.listen()
            if user_name:
                self.config["user_name"] = user_name
                # Сохраняем обновленную конфигурацию
                with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=4)
                self.speech.speak(f"Приятно познакомиться, {user_name}!")
        
        # Основной цикл
        self.main_loop()
    
    def process_command(self, command):
        """Обработка команды"""
        if not command:
            return "Не удалось распознать команду"
        
        # Проверяем системные команды
        if "открой" in command:
            app_name = command.split("открой")[1].strip()
            return self.app_manager.open_application(app_name)
        
        elif "выключи компьютер" in command:
            return self.system_commands.shutdown()
        
        elif "перезагрузи компьютер" in command:
            return self.system_commands.restart()
        
        elif "скриншот" in command:
            return self.system_commands.take_screenshot(os.path.join(DATA_PATH, "media"))
        
        elif "пока" in command or "выход" in command:
            self.running = False
            return "До свидания!"
        
        # Для остальных команд используем ИИ
        return self.ai.process(command)
    
    def main_loop(self):
        """Основной цикл работы"""
        while self.running:
            command = self.speech.listen()
            if command:
                logger.info(f"Получена команда: {command}")
                response = self.process_command(command)
                logger.info(f"Ответ: {response}")
                self.speech.speak(response)
        
        logger.info("Завершение работы Джарвиса")

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.start()