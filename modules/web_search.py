import webbrowser
import urllib.parse
import logging
import requests
from bs4 import BeautifulSoup
import re

logger = logging.getLogger("jarvis.web_search")

class WebSearch:
    def __init__(self):
        """Инициализация модуля поиска"""
        self.search_engines = {
            "google": "https://www.google.com/search?q={}",
            "yandex": "https://yandex.ru/search/?text={}",
            "bing": "https://www.bing.com/search?q={}"
        }
        
        self.specialized_searches = {
            "рецепт": "https://www.google.com/search?q={}+рецепт",
            "видео": "https://www.youtube.com/results?search_query={}",
            "карта": "https://www.google.com/maps/search/{}",
            "новости": "https://news.google.com/search?q={}"
        }
        
        logger.info("Модуль веб-поиска инициализирован")
    
    def search(self, query, engine="google"):
        """Выполняет поиск запроса в указанном поисковике"""
        logger.info(f"Поиск запроса: '{query}' в {engine}")
        
        if engine in self.search_engines:
            url = self.search_engines[engine].format(urllib.parse.quote(query))
            webbrowser.open(url)
            return f"Ищу '{query}' в {engine}"
        else:
            return f"Поисковый движок {engine} не поддерживается"
    
    def specialized_search(self, query, search_type):
        """Выполняет специализированный поиск"""
        logger.info(f"Специализированный поиск: '{query}', тип: {search_type}")
        
        if search_type in self.specialized_searches:
            url = self.specialized_searches[search_type].format(urllib.parse.quote(query))
            webbrowser.open(url)
            return f"Ищу {search_type} по запросу '{query}'"
        else:
            return f"Тип поиска {search_type} не поддерживается"
    
    def search_recipe(self, dish_name):
        """Ищет рецепт блюда"""
        return self.specialized_search(dish_name, "рецепт")
    
    def search_video(self, query):
        """Ищет видео по запросу"""
        return self.specialized_search(query, "видео")
    
    def parse_search_intent(self, query):
        """Анализирует запрос и определяет тип поиска"""
        query = query.lower()
        
        # Проверяем различные шаблоны запросов
        if re.search(r'найти рецепт|как приготовить|рецепт', query):
            # Извлекаем название блюда
            match = re.search(r'рецепт\s+([а-яё\s]+)', query) or \
                    re.search(r'приготовить\s+([а-яё\s]+)', query) or \
                    re.search(r'найти\s+рецепт\s+([а-яё\s]+)', query)
            
            if match:
                dish_name = match.group(1).strip()
                return self.search_recipe(dish_name)
            else:
                # Если не удалось извлечь название блюда
                dish_name = query.replace("найти рецепт", "").replace("рецепт", "").replace("как приготовить", "").strip()
                return self.search_recipe(dish_name)
        
        elif re.search(r'найти видео|посмотреть видео', query):
            # Извлекаем тему видео
            match = re.search(r'видео\s+([а-яё\s]+)', query)
            if match:
                video_topic = match.group(1).strip()
                return self.search_video(video_topic)
            else:
                # Если не удалось извлечь тему видео
                video_topic = query.replace("найти видео", "").replace("посмотреть видео", "").strip()
                return self.search_video(video_topic)
        
        elif re.search(r'найти|поиск|искать|загугли|найди', query):
            # Общий поиск
            search_query = re.sub(r'найти|поиск|искать|загугли|найди', '', query).strip()
            return self.search(search_query)
        
        # Если не подходит ни один из шаблонов, возвращаем None
        return None