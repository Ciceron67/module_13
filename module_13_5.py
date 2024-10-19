import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher()
router = Router()

button = KeyboardButton(text='Информация')
button1 = KeyboardButton(text='Рассчитать')
kb = ReplyKeyboardMarkup(keyboard=[[button, button1]], resize_keyboard=True)




@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.'
                         'Я могу рассчитать твою суточную норму потребления калорий. '
                         'Для расчета калорий нажмите "Рассчитать"', reply_markup=kb)

@dp.message(F.text=='Информация')
async def bot_information(message: Message):
    await message.answer('Бот, считающий, количество калорий. ')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()



@dp.message(F.text=='Рассчитать')
async def set_age(message: Message, state: FSMContext):
    await message.reply('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    try:
        await state.update_data(age=int(message.text))
        await message.answer('Введите свой рост:')
        await state.set_state(UserState.growth)
    except ValueError:
        await message.answer('Введены не корректные данные, рост должен быть числом')


@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(growth=int(message.text))
        await message.answer('Введите свой вес:')
        await state.set_state(UserState.weight)
    except ValueError:
        await message.answer('Введены не корректные данные, вес должен быть числом')


@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data.get('age')
    growth = data.get('growth')
    weight = data.get('weight')
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Суточная норма {calories} ккал')
    await state.finish()


@dp.message()
async def all_massages(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
