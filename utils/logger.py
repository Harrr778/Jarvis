import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    """Настраивает логгер"""
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Создаем обработчик для вывода в файл с ротацией
    # Максимальный размер файла - 1 МБ, максимальное количество файлов - 3
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3, encoding='utf-8')
    
    # Создаем форматтер
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(handler)
    
    return logger