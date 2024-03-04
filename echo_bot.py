from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
from settings import token
from random import randint
from filters import IsAdmin, admin_ids, NumberInMessage

ATTEMPTS = 5

user = {}


def get_random() -> int:
    return randint(1,100)


bot = Bot(token)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    print(message.from_user.id)
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')

    if message.from_user.id not in user:
        user[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': 0,
            'total_games': 0,
            'wins': 0
        }

@dp.message(F.text.lower().startswith('найди числа'),
            NumberInMessage())
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(
        text=f'Нашёл: {", ".join(str(num) for num in numbers)}'
    )


@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(
            text='Не нашел что-то :(')


@dp.message(IsAdmin(admin_ids))
async def process_admin_panel(message: Message):
    await message.answer(text='Добро пожаловать господин админ')

@dp.message(Command(commands='help'))
async def process_command_help(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


@dp.message(Command(commands='stat'))
async def process_command_stat(message:Message):
    await message.answer(
        f'Всего игр сыграно: {user[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {user[message.from_user.id]["wins"]}'
    )


@dp.message(Command(commands='cancel'))
async def proceed_command_cancel(message: Message):
    if user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы итак с вами не играем. '
            'Может, сыграем разок?'
        )


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = True
        user[message.from_user.id]['secret_number'] = get_random()
        user[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def proceed_numbers_answer(message: Message):
    if user[message.from_user.id]['in_game']:
        if int(message.text) == user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['total_games'] += 1
            user[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['attempts'] -= 1
            await message.answer(
                'Мое число меньше'
            )
        elif int(message.text) < user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['attempts'] -= 1
            await message.answer(
                'Мое число больше'
            )
        if user[message.from_user.id]['attempts'] == 0:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {user[message.from_user.id]["secret_number"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer(
            'Мы еще не играем. Хотите сыграть?'
        )

@dp.message()
async def process_other_answers(message: Message):
    if user[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

if __name__ == '__main__':
    dp.run_polling(bot)

