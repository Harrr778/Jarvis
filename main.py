import os
import sys
import json
import threading
from core.speech import SpeechEngine
from core.ai_brain import AI
from core.memory import MemorySystem
from modules.system_commands import SystemCommands
from modules.applications import ApplicationManager
from modules.web_search import WebSearch
from modules.personal_assist import PersonalAssistant
from utils.logger import setup_logger

# Настройка путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")
COMMANDS_PATH = os.path.join(BASE_DIR, "config", "commands.json")
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

def load_commands():
    """Загружает конфигурацию команд"""
    try:
        with open(COMMANDS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Файл конфигурации команд не найден.")
        return {
            "system_commands": {},
            "app_commands": {},
            "search_commands": {},
            "exit_commands": {}
        }

class Jarvis:
    def __init__(self):
        """Инициализация Джарвиса"""
        logger.info("Инициализация Джарвиса")
        
        # Загрузка конфигурации
        self.config = load_config()
        self.commands_config = load_commands()
        
        # Инициализация компонентов
        self.memory = MemorySystem(os.path.join(DATA_PATH, "memory"))
        self.speech = SpeechEngine(self.config["speech"])
        self.ai = AI(self.config["ai"], self.memory)
        self.system_commands = SystemCommands()
        self.app_manager = ApplicationManager()
        self.web_search = WebSearch()
        self.personal_assistant = PersonalAssistant(CONFIG_PATH)
        
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
    
    def find_command_match(self, user_input):
        """Находит соответствующую команду для ввода пользователя"""
        user_input = user_input.lower()
        
        # Проверяем категории команд
        for category, commands in self.commands_config.items():
            for cmd_trigger, cmd_action in commands.items():
                if cmd_trigger in user_input:
                    return category, cmd_action, user_input.replace(cmd_trigger, "").strip()
        
        # Проверяем веб-поиск через регулярные выражения
        search_result = self.web_search.parse_search_intent(user_input)
        if search_result:
            return "web_search", "parse_intent", user_input
            
        # Проверяем запросы для персонального ассистента
        personal_result = self.personal_assistant.parse_intent(user_input)
        if personal_result:
            return "personal", "response", personal_result
        
        # Если не найдено соответствий, используем ИИ
        return "ai", "process", user_input
    
    def process_command(self, command):
        """Обработка команды"""
        if not command:
            return "Не удалось распознать команду"
        
        # Ищем соответствующую команду
        category, action, params = self.find_command_match(command)
        
        logger.info(f"Категория: {category}, Действие: {action}, Параметры: {params}")
        
        # Выполняем действие в соответствии с категорией
        if category == "system_commands":
            method = getattr(self.system_commands, action)
            if action == "take_screenshot":
                return method(os.path.join(DATA_PATH, "media"))
            else:
                return method()
        
        elif category == "app_commands":
            if action == "open_application":
                return self.app_manager.open_application(params)
        
        elif category == "search_commands":
            if action == "search":
                return self.web_search.search(params)
            elif action == "search_recipe":
                return self.web_search.search_recipe(params)
            elif action == "search_video":
                return self.web_search.search_video(params)
        
        elif category == "exit_commands":
            self.running = False
            return "До свидания!"
        
        elif category == "web_search" and action == "parse_intent":
            # Это означает, что parse_search_intent нашел совпадение
            return self.web_search.parse_search_intent(params)
            
        elif category == "personal" and action == "response":
            # Это значит, что у нас уже есть готовый ответ от парсера личного ассистента
            return params
        
        # Для неизвестных команд используем ИИ
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