import asyncio
import logging
import aiogram

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery, FSInputFile

from pip import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

buttons = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'),
                                         KeyboardButton(text='Информация')],
                                        [KeyboardButton(text='Купить')]],resize_keyboard=True)
in_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas'),
                                                   InlineKeyboardButton(text='Рассчитать норму калорий',
                                                                        callback_data='calories')]],resize_keyboard=True)
in_button2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Product1',callback_data='product_buying1'),
                                                    InlineKeyboardButton(text='Product2',callback_data='product_buying2'),
                                                    InlineKeyboardButton(text='Product3',callback_data='product_buying3'),
                                                    InlineKeyboardButton(text='Product4',callback_data='product_buying4')]])

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=buttons)
    print('Привет! Я бот помогающий твоему здоровью.')



async def start():
    await dp.start_polling(bot)

class UserState(StatesGroup):
    #(возраст, рост, вес)
    age = State()
    growth = State()
    weight = State()

@dp.message(F.text == 'Рассчитать')
async def main_menu(message:Message):
    await message.answer('Выберите опцию:',reply_markup=in_button)

@dp.callback_query(F.data == 'formulas')
async def get_formulas(callback:CallbackQuery):
    await callback.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")

@dp.message(F.text == 'Купить')
async def get_buying_list(message:Message):
    for number in range(1, 5):
        await message.answer(f'Название: Product {number} | Описание: описание {number} | Цена: {number * 100}')
        badt = FSInputFile(f'C:/Users/Diana/PycharmProjects/PythonProject2/baden {number}.jpg')
        await message.answer_photo(photo=badt)
    await message.answer('Выберите продукт для покупки:',reply_markup=in_button2)


@dp.callback_query(F.data == 'product_buying1')
async  def set_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Вы успешно приобрели продукт!")
    await state.set_state(UserState.age)

@dp.callback_query(F.data == 'product_buying2')
async  def set_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Вы успешно приобрели продукт!")
    await state.set_state(UserState.age)

@dp.callback_query(F.data == 'product_buying3')
async  def set_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Вы успешно приобрели продукт!")
    await state.set_state(UserState.age)

@dp.callback_query(F.data == 'product_buying4')
async  def set_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Вы успешно приобрели продукт!")
    await state.set_state(UserState.age)


@dp.callback_query(F.data == 'calories')
async  def set_age(callback:CallbackQuery, state:FSMContext):
    await callback.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    norma = int(data['weight'])*10 + int(data['growth'])* 6.25 - int(data['age'])*5-161
    await message.answer(f'Ваша норма калорий в сутки: {norma}')
    await state.clear()

@dp.message()
async def cmd_not_start(message: Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('exit')

# module_14_3.py