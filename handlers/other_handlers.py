from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command
from keyboards.keyboards import clbk_keyboard

router = Router()


@router.message(Command(commands='del_menu'))
async def del_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')


@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])

@router.callback_query(F.data == 'clbk_1')
async def reply_clbk_1(callback: CallbackQuery):
    if callback.message.text != 'Нажата кнопка 1':
        await callback.message.edit_text(text='Нажата кнопка 1', reply_markup=clbk_keyboard)
    else:
        await callback.answer(text='нажата кнопка 1')

@router.callback_query(F.data == 'clbk_2')
async def reply_clbk_2(callback: CallbackQuery):
    if callback.message.text != 'Нажата кнопка 2':
        await callback.message.edit_text(text='Нажата кнопка 2', reply_markup=clbk_keyboard)
    else:
        await callback.answer(text="Нажата кнопка 2")



