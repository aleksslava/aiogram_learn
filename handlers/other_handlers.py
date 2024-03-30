from aiogram import Router, Bot
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command

router = Router()


@router.message(Command(commands='del_menu'))
async def del_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')


@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])