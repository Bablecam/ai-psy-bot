from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import asyncio

from states import UserMode
from keyboards import get_main_keyboard

# ИМПОРТИРУЕМ НОВЫЕ ФУНКЦИИ ИЗ SERVICES
from services import get_ai_response, clear_user_context

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    clear_user_context(message.from_user.id) # ОЧИЩАЕМ ПАМЯТЬ
    
    welcome_text = (
        "Привет! 👋 Я твой ИИ-помощник.\n\n"
        "Выбери нужный режим работы в меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@router.message(F.text == "🧠 Психолог")
async def set_psychologist(message: types.Message, state: FSMContext):
    await state.set_state(UserMode.psychologist)
    clear_user_context(message.from_user.id) # ОЧИЩАЕМ ПАМЯТЬ ПРИ СМЕНЕ РОЛИ
    await message.answer("Режим 'Психолог' включен. 🛋\nПоделись со мной тем, что тебя беспокоит.")

@router.message(F.text == "✍️ Копирайтер")
async def set_content_maker(message: types.Message, state: FSMContext):
    await state.set_state(UserMode.content_maker)
    clear_user_context(message.from_user.id) # ОЧИЩАЕМ ПАМЯТЬ ПРИ СМЕНЕ РОЛИ
    await message.answer("Режим 'Копирайтер' включен. 📝\nНапиши тему, и я сгенерирую для тебя текст.")

# --- БЛОК ФУНКЦИЙ БЕЗ ИИ (КЛАССИЧЕСКИЕ АЛГОРИТМЫ) ---

@router.message(F.text == "🆘 Помощь")
async def sos_contacts(message: types.Message, state: FSMContext):
    await state.clear() # Выходим из режимов ИИ
    sos_text = (
        "🚨 **Экстренная психологическая помощь:**\n\n"
        "Если вы чувствуете, что не справляетесь, пожалуйста, обратитесь к специалистам. Это бесплатно и анонимно:\n\n"
        "📞 Единый телефон доверия: 8-800-333-44-34\n"
        "📞 Горячая линия психологической помощи: +7 (495) 051\n"
        "🌐 Сайт: https://psi.mchs.gov.ru/ (Психологическая служба МЧС)\n\n"
        "ИИ-бот не заменяет настоящего врача. Берегите себя! ❤️"
    )
    # Отправляем статичный текст (никакого Сбера тут нет)
    await message.answer(sos_text, parse_mode="Markdown")

@router.message(F.text == "🧘 Дыхание")
async def breathing_exercise(message: types.Message, state: FSMContext):
    await state.clear() # Выходим из режимов ИИ
    
    # Отправляем первое сообщение
    msg = await message.answer("Устройтесь поудобнее. Начинаем дыхательную гимнастику (техника 4-7-8) 🍃")
    await asyncio.sleep(2)
    
    # Цикл дыхания с использованием асинхронных пауз (Демонстрация навыков программирования)
    cycles = 2 # Сделаем 2 цикла, чтобы не затягивать
    for i in range(cycles):
        await msg.edit_text(f"Цикл {i+1}/{cycles}\n\n🟢 ДЕЛАЕМ ВДОХ... (4 сек)")
        await asyncio.sleep(4)
        
        await msg.edit_text(f"Цикл {i+1}/{cycles}\n\n🟡 ЗАДЕРЖИВАЕМ ДЫХАНИЕ... (7 сек)")
        await asyncio.sleep(7)
        
        await msg.edit_text(f"Цикл {i+1}/{cycles}\n\n🔵 МЕДЛЕННЫЙ ВЫДОХ... (8 сек)")
        await asyncio.sleep(8)
        
    await msg.edit_text("✨ Гимнастика завершена. Надеюсь, вам стало спокойнее.\nВыберите режим работы в меню.")

@router.message()
async def handle_text(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer("Пожалуйста, сначала выбери режим работы 👇", reply_markup=get_main_keyboard())
        return

    processing_msg = await message.answer("⏳ Думаю...")
    
    # Строгая настройка ролей (Guardrails)
    if current_state == UserMode.psychologist.state:
        system_prompt = (
            "Ты — эмпатичный психолог. Твоя цель — эмоциональная поддержка. "
            "ВАЖНОЕ ПРАВИЛО: Если пользователь просит написать код, решить математическую задачу, "
            "перевести текст или спрашивает факты (погоду, курс валют) — ВЕЖЛИВО ОТКАЖИСЬ. "
            "Скажи, что ты умеешь только поддерживать беседу о чувствах и переживаниях. "
            "Не пиши длинные тексты. Задавай открытые вопросы."
        )
    else:
        system_prompt = (
            "Ты — профессиональный копирайтер. Твоя цель — писать тексты. "
            "ВАЖНОЕ ПРАВИЛО: Если пользователь жалуется на жизнь или просит совет — ОТКАЖИСЬ. "
            "Скажи, что для этого есть режим Психолога. "
            "Если просят написать код — ОТКАЖИСЬ. "
            "Пиши только посты, статьи, письма и рекламные тексты."
        )

    # Вызываем ИИ, передавая ID пользователя
    ai_answer = get_ai_response(
        user_id=message.from_user.id,
        user_text=message.text,
        system_prompt=system_prompt
    )
    
    await processing_msg.edit_text(ai_answer)