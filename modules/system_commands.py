import os
import subprocess
import pyautogui
import time
import logging

logger = logging.getLogger("jarvis.system")

class SystemCommands:
    def __init__(self):
        """Инициализация модуля системных команд"""
        logger.info("Модуль системных команд инициализирован")
    
    def shutdown(self):
        """Выключает компьютер"""
        logger.info("Выполняется команда выключения")
        try:
            subprocess.run(["shutdown", "/s", "/t", "60", "/c", "Выключение компьютера по команде пользователя"])
            return "Компьютер будет выключен через 60 секунд. Скажите 'отмени выключение', чтобы отменить."
        except Exception as e:
            logger.error(f"Ошибка при выключении: {e}")
            return f"Не удалось выключить компьютер: {e}"
    
    def cancel_shutdown(self):
        """Отменяет выключение компьютера"""
        logger.info("Отмена выключения")
        try:
            subprocess.run(["shutdown", "/a"])
            return "Выключение отменено"
        except Exception as e:
            logger.error(f"Ошибка при отмене выключения: {e}")
            return f"Не удалось отменить выключение: {e}"
    
    def restart(self):
        """Перезагружает компьютер"""
        logger.info("Выполняется команда перезагрузки")
        try:
            subprocess.run(["shutdown", "/r", "/t", "60", "/c", "Перезагрузка компьютера по команде пользователя"])
            return "Компьютер будет перезагружен через 60 секунд. Скажите 'отмени перезагрузку', чтобы отменить."
        except Exception as e:
            logger.error(f"Ошибка при перезагрузке: {e}")
            return f"Не удалось перезагрузить компьютер: {e}"
    
    def take_screenshot(self, save_dir):
        """Делает скриншот экрана"""
        logger.info("Делаю скриншот")
        try:
            # Создаем директорию, если она не существует
            os.makedirs(save_dir, exist_ok=True)
            
            # Формируем имя файла с временной меткой
            filename = f"screenshot_{int(time.time())}.png"
            filepath = os.path.join(save_dir, filename)
            
            # Делаем скриншот
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            return f"Скриншот сохранен: {filepath}"
        except Exception as e:
            logger.error(f"Ошибка при создании скриншота: {e}")
            return f"Не удалось сделать скриншот: {e}"
    
    def lock_computer(self):
        """Блокирует компьютер"""
        logger.info("Блокировка компьютера")
        try:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            return "Компьютер заблокирован"
        except Exception as e:
            logger.error(f"Ошибка при блокировке: {e}")
            return f"Не удалось заблокировать компьютер: {e}"