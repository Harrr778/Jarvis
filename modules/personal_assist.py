import datetime
import requests
import logging
import re
import json
import os

logger = logging.getLogger("jarvis.personal")

class PersonalAssistant:
    def __init__(self, config_path=None):
        """Инициализация модуля персонального ассистента"""
        self.config_path = config_path
        self.weather_api_key = ""  # Ключ OpenWeatherMap API (требует регистрации)
        
        # Если указан путь к конфигу, пытаемся загрузить ключ API
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if "weather_api_key" in config:
                        self.weather_api_key = config["weather_api_key"]
            except Exception as e:
                logger.error(f"Ошибка загрузки конфигурации: {e}")
        
        logger.info("Модуль персонального ассистента инициализирован")
    
    def get_date(self):
        """Возвращает текущую дату"""
        now = datetime.datetime.now()
        # Возвращаем дату в формате "понедельник, 1 января 2023 года"
        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
                 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        
        return f"Сегодня {weekdays[now.weekday()]}, {now.day} {months[now.month-1]} {now.year} года"
    
    def get_time(self):
        """Возвращает текущее время"""
        now = datetime.datetime.now()
        # Функция для правильного склонения слова "час"
        def format_hours(h):
            if h % 10 == 1 and h != 11:
                return f"{h} час"
            elif 2 <= h % 10 <= 4 and (h < 10 or h > 20):
                return f"{h} часа"
            else:
                return f"{h} часов"
        
        # Функция для правильного склонения слова "минута"
        def format_minutes(m):
            if m % 10 == 1 and m != 11:
                return f"{m} минута"
            elif 2 <= m % 10 <= 4 and (m < 10 or m > 20):
                return f"{m} минуты"
            else:
                return f"{m} минут"
        
        return f"Сейчас {format_hours(now.hour)} {format_minutes(now.minute)}"
    
    def get_weather(self, city="Москва"):
        """Получает информацию о погоде через API"""
        if not self.weather_api_key:
            return "Для получения информации о погоде необходимо настроить API ключ OpenWeatherMap"
        
        try:
            # Запрос к API
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric&lang=ru"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # Обрабатываем данные
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                description = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                
                return (f"Погода в городе {city}: {description}, "
                       f"температура {temp:.1f}°C, ощущается как {feels_like:.1f}°C, "
                       f"влажность {humidity}%")
            else:
                return f"Не удалось получить информацию о погоде: {data.get('message', 'неизвестная ошибка')}"
        
        except Exception as e:
            logger.error(f"Ошибка получения погоды: {e}")
            return f"Произошла ошибка при получении данных о погоде: {e}"
    
    def parse_intent(self, query):
        """Анализирует запрос пользователя и определяет, что он хочет узнать"""
        query = query.lower()
        
        # Запросы о дате
        if re.search(r'какое сегодня число|какая сегодня дата|дата сегодня|число сегодня', query):
            return self.get_date()
        
        # Запросы о времени
        elif re.search(r'который час|сколько времени|время сейчас|текущее время', query):
            return self.get_time()
        
        # Запросы о погоде
        elif re.search(r'погода|прогноз погоды', query):
            # Пробуем найти город в запросе
            city_match = re.search(r'погода в (\w+)', query) or re.search(r'погода (\w+)', query)
            if city_match:
                city = city_match.group(1)
                return self.get_weather(city)
            else:
                return self.get_weather()  # Погода по умолчанию
        
        # Если не нашли совпадений
        return None