from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from config import GIGACHAT_TOKEN

# История диалогов
users_context = {}

def clear_user_context(user_id: int):
    if user_id in users_context:
        del users_context[user_id]

def get_ai_response(user_id: int, user_text: str, system_prompt: str) -> str:
    # Инициализация истории, если её нет
    if user_id not in users_context:
        users_context[user_id] = [
            Messages(role=MessagesRole.SYSTEM, content=system_prompt)
        ]
    
    # Добавляем сообщение пользователя
    users_context[user_id].append(Messages(role=MessagesRole.USER, content=user_text))
    
    # Оставляем только системный промпт + 10 последних сообщений (чтобы не перегружать память)
    if len(users_context[user_id]) > 11:
        users_context[user_id] = [users_context[user_id][0]] + users_context[user_id][-10:]

    try:
        # ВОТ ЗДЕСЬ ВАЖНЫЙ МОМЕНТ:
        # verify_ssl_certs=False — отключает проверку сертификатов (лечит ошибки SSL)
        # scope="GIGACHAT_API_PERS" — говорит Сберу, что мы физлицо (лечит ошибку 401)
        with GigaChat(
            credentials=GIGACHAT_TOKEN, 
            verify_ssl_certs=False, 
            scope="GIGACHAT_API_PERS",
            model="GigaChat" # Явно укажем модель, иногда это помогает
        ) as giga:
            
            chat_payload = Chat(messages=users_context[user_id])
            response = giga.chat(chat_payload)
            
            ai_answer = response.choices[0].message.content
            
            # Сохраняем ответ бота
            users_context[user_id].append(Messages(role=MessagesRole.ASSISTANT, content=ai_answer))
            
            return ai_answer
            
    except Exception as e:
        # Эта строка напечатает точную ошибку в терминал, чтобы мы её увидели
        print(f"🔴 КРИТИЧЕСКАЯ ОШИБКА GIGACHAT: {e}")
        
        # Если ошибка, откатываем историю назад (удаляем последнее сообщение юзера)
        if user_id in users_context and len(users_context[user_id]) > 1:
            users_context[user_id].pop()
            
        return "❌ Ошибка соединения с нейросетью. Проверьте консоль сервера."