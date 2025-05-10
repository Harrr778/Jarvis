import openai
import logging

logger = logging.getLogger("jarvis.ai")

class AI:
    def __init__(self, config, memory):
        """Инициализация ИИ-мозга"""
        openai.api_key = config.get("api_key", "")
        self.model = config.get("model", "gpt-4")
        self.memory = memory
        
        logger.info(f"ИИ инициализирован, модель: {self.model}")
    
    def process(self, user_input):
        """Обрабатывает ввод пользователя и генерирует ответ"""
        if not openai.api_key:
            return "API ключ не настроен. Пожалуйста, добавьте ключ API в настройках."
        
        # Получаем историю диалога
        history = self.memory.get_conversation_history()
        
        # Формируем сообщения для API
        messages = [
            {"role": "system", "content": "Вы - Джарвис, персональный ИИ-ассистент. Вы работаете на Windows компьютере пользователя. Отвечайте кратко и по делу."}
        ]
        
        # Добавляем историю диалога (последние 5 сообщений)
        for item in history[-5:]:
            messages.append({"role": "user", "content": item["user"]})
            messages.append({"role": "assistant", "content": item["assistant"]})
        
        # Добавляем текущий ввод пользователя
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Запрос к API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=150
            )
            
            # Получаем ответ
            ai_response = response.choices[0].message["content"]
            
            # Сохраняем диалог в памяти
            self.memory.add_to_conversation(user_input, ai_response)
            
            return ai_response
        except Exception as e:
            logger.error(f"Ошибка при запросе к API: {e}")
            return "Извините, у меня возникла проблема при обработке вашего запроса."