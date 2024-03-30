from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU


button_yes = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no = KeyboardButton(text=LEXICON_RU['no_button'])

yes_no_kb_builder = ReplyKeyboardBuilder()

yes_no_kb_builder.row(button_yes, button_no, width=2)

yes_no_kb: ReplyKeyboardMarkup = yes_no_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True
)


button_1 = KeyboardButton(text=LEXICON_RU['rock'])
button_2 = KeyboardButton(text=LEXICON_RU['scissors'])
button_3 = KeyboardButton(text=LEXICON_RU['paper'])

game_kb = ReplyKeyboardMarkup(
    keyboard=[
        [button_1],
        [button_2],
        [button_3]],
    resize_keyboard=True

)

url_button = InlineKeyboardButton(text='Ссылка на что-то', url='Https://www.google.com')

url_keyboard = InlineKeyboardMarkup(inline_keyboard=[[url_button]])

clbk_button_1 = InlineKeyboardButton(text='Коллбэк_1',
                                     callback_data='clbk_1')

clbk_button_2 = InlineKeyboardButton(text='Коллбэк_2',
                                     callback_data='clbk_2')

clbk_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [clbk_button_1],
    [clbk_button_2]
])

