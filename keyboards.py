from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    # Первый ряд: Режимы ИИ
    row1 =[KeyboardButton(text="🧠 Психолог"), KeyboardButton(text="✍️ Копирайтер")]
    # Второй ряд: Не-ИИ функции (Классические алгоритмы)
    row2 = [KeyboardButton(text="🧘 Дыхание"), KeyboardButton(text="🆘 Помощь")]
    
    kb = [row1, row2]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)