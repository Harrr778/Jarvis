import subprocess
import os
import webbrowser
import logging

logger = logging.getLogger("jarvis.apps")

class ApplicationManager:
    def __init__(self):
        """Инициализация менеджера приложений"""
        # Словарь приложений и их команд запуска
        self.app_commands = {
            "chrome": "chrome",
            "гугл": "chrome",
            "браузер": "chrome",
            "блокнот": "notepad",
            "калькулятор": "calc",
            "проводник": "explorer",
            "word": "winword",
            "excel": "excel",
            "музыка": "wmplayer",
            "медиаплеер": "wmplayer",
            "paint": "mspaint",
            "настройки": "ms-settings:",
            "диспетчер задач": "taskmgr"
        }
        
        # Список URL для быстрого доступа
        self.urls = {
            "youtube": "https://www.youtube.com",
            "ютуб": "https://www.youtube.com",
            "google": "https://www.google.com",
            "гугл": "https://www.google.com",
            "почта": "https://mail.google.com",
            "gmail": "https://mail.google.com",
            "новости": "https://news.google.com",
            "погода": "https://www.gismeteo.ru",
            "карты": "https://maps.google.com"
        }
        
        logger.info("Менеджер приложений инициализирован")
    
    def open_application(self, app_name):
        """Открывает приложение по имени"""
        app_name = app_name.lower()
        
        logger.info(f"Попытка открыть приложение: {app_name}")
        
        # Проверяем, есть ли приложение в словаре
        if app_name in self.app_commands:
            try:
                subprocess.Popen(self.app_commands[app_name])
                return f"Открываю {app_name}"
            except Exception as e:
                logger.error(f"Ошибка при открытии {app_name}: {e}")
                return f"Не удалось открыть {app_name}: {e}"
        
        # Проверяем, есть ли это веб-сайт
        elif app_name in self.urls:
            try:
                webbrowser.open(self.urls[app_name])
                return f"Открываю {app_name}"
            except Exception as e:
                logger.error(f"Ошибка при открытии {app_name}: {e}")
                return f"Не удалось открыть {app_name}: {e}"
        
        # Проверяем, может это путь к файлу
        elif os.path.exists(app_name):
            try:
                os.startfile(app_name)
                return f"Открываю {app_name}"
            except Exception as e:
                logger.error(f"Ошибка при открытии {app_name}: {e}")
                return f"Не удалось открыть {app_name}: {e}"
        
        # Если ничего не подошло
        return f"Не знаю, как открыть {app_name}"
    
    def close_application(self, app_name):
        """Закрывает приложение по имени"""
        app_name = app_name.lower()
        
        # Словарь соответствия имен и процессов
        app_processes = {
            "chrome": "chrome.exe",
            "браузер": "chrome.exe",
            "блокнот": "notepad.exe",
            "калькулятор": "calc.exe",
            "word": "winword.exe",
            "excel": "excel.exe"
        }
        
        if app_name in app_processes:
            try:
                subprocess.run(["taskkill", "/f", "/im", app_processes[app_name]])
                return f"Закрываю {app_name}"
            except Exception as e:
                logger.error(f"Ошибка при закрытии {app_name}: {e}")
                return f"Не удалось закрыть {app_name}: {e}"
        
        return f"Не знаю, как закрыть {app_name}"