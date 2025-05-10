import os
import json
import logging
from datetime import datetime

logger = logging.getLogger("jarvis.memory")

class MemorySystem:
    def __init__(self, memory_dir):
        """Инициализация системы памяти"""
        self.memory_dir = memory_dir
        self.conversation_file = os.path.join(memory_dir, "conversation.json")
        self.user_data_file = os.path.join(memory_dir, "user_data.json")
        
        # Создаем директорию, если она не существует
        os.makedirs(memory_dir, exist_ok=True)
        
        # Загружаем или создаем файлы памяти
        self.load_memory()
        
        logger.info("Система памяти инициализирована")
    
    def load_memory(self):
        """Загружает данные памяти из файлов"""
        # Загружаем историю разговоров
        try:
            with open(self.conversation_file, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.conversation_history = []
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f)
        
        # Загружаем данные пользователя
        try:
            with open(self.user_data_file, 'r', encoding='utf-8') as f:
                self.user_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.user_data = {
                "preferences": {},
                "facts": {},
                "last_interaction": None
            }
            with open(self.user_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f)
    
    def save_conversation(self):
        """Сохраняет историю разговоров"""
        with open(self.conversation_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
    
    def save_user_data(self):
        """Сохраняет данные пользователя"""
        with open(self.user_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_data, f, ensure_ascii=False, indent=2)
    
    def add_to_conversation(self, user_input, assistant_response):
        """Добавляет диалог в историю"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response
        })
        
        # Обновляем время последнего взаимодействия
        self.user_data["last_interaction"] = datetime.now().isoformat()
        
        # Сохраняем изменения
        self.save_conversation()
        self.save_user_data()
    
    def get_conversation_history(self):
        """Возвращает историю разговоров"""
        return self.conversation_history
    
    def add_user_preference(self, key, value):
        """Добавляет предпочтение пользователя"""
        self.user_data["preferences"][key] = value
        self.save_user_data()
    
    def get_user_preference(self, key, default=None):
        """Возвращает предпочтение пользователя"""
        return self.user_data["preferences"].get(key, default)
    
    def add_user_fact(self, key, value):
        """Добавляет факт о пользователе"""
        self.user_data["facts"][key] = value
        self.save_user_data()
    
    def get_user_fact(self, key, default=None):
        """Возвращает факт о пользователе"""
        return self.user_data["facts"].get(key, default)