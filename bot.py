import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from get_num import get_binance_avr_rates

API_TOKEN = '6130803945:AAE26K43qBVYjVyoMHnm1-yKYSHYAfGZcJ0'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

button1 = KeyboardButton('Курс')

button2 = KeyboardButton('Условия')

keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard.add(button1).add(button2)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(
        "💲Привет, этот бот может показать тебе курс перевода средств из Казахстана в Россию и обратном направлении.💲",
        reply_markup=keyboard)


@dp.message_handler(Text("Курс"))
async def process_hi1_command(message: types.Message):
    usdt_rub_buy = float(get_binance_avr_rates())
    usdt_rub_sell = float(get_binance_avr_rates(type="SELL"))
    usdt_kgs_buy = float(get_binance_avr_rates(fiat='KZT', pay='KaspiBank'))
    usdt_kgs_sell = float(get_binance_avr_rates(fiat='KZT', type="SELL", pay='KaspiBank'))
    comission = 3.5
    comission_r = comission / 100
    my_rate_kg = usdt_kgs_sell / usdt_rub_buy
    my_rate_ru = usdt_kgs_buy / usdt_rub_sell
    client_rate_kg = (my_rate_kg) - (my_rate_kg * comission_r)
    client_rate_ru = (my_rate_ru) + (my_rate_ru * comission_r)
    await message.reply(
        f"Курс для переводов в KZ: {round(client_rate_kg, 4)}\nКурс для переводов в РФ: {round(client_rate_ru, 3)}\n📞Для перевода денег пишите сюда: @M_T_B_vendur")


@dp.message_handler(Text("Условия"))
async def with_puree(message: types.Message):
    await message.reply(
        "🪪Ф.И.О Отправителя, Ф.И.О получателя,  номер карты и банк получателя. 💳\n💵сумма перевода💵\n💎Как осуществляется перевод?💎\nПеред переводом денег мы отправим вам номер карты на которую нужно зачислить средства и в течении 15 минут они будут переведены ( курс перевода нужно проверять непосредственно перед переводом)\n🪙Переводы совершаются от 1000 рублей или 5000 тенге🪙",
        reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
