import os
from dotenv import load_dotenv

# Читаем файл .env
load_dotenv(override=True)

# Просто копируем названия из .env. 
# В кавычках тут НЕ токен, а ИМЯ переменной!
BOT_TOKEN = os.getenv("BOT_TOKEN") 
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")