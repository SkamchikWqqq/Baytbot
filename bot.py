from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
import asyncio

# 🔹 Твой токен
TOKEN = "7917190360:AAFxfFYsEsx9kQiPbh7MtZ6N7HLZcSPQRNs"

# 🔹 Ссылки на каналы
CHANNELS = [
    "https://t.me/+yO5vZ2dUyRE3MzM0",
    "https://t.me/faicers"
]

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал 1", url=CHANNELS[0])],
            [InlineKeyboardButton(text="📢 Подписаться на канал 2", url=CHANNELS[1])],
            [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subs")]
        ]
    )
    await message.answer("👋 Привет! Подпишись на каналы ниже:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "check_subs")
async def check_subs(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    subscribed_all = True

    # Проверяем подписку (даже если уже подписан — просто игнорируем)
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        try:
            member = await bot.get_chat_member(chat.id, user_id)
            if member.status == "left":
                subscribed_all = False
        except Exception:
            subscribed_all = False

    if subscribed_all:
        await callback.message.answer("✅ Отлично! Ты подписан на все каналы.")
    else:
        await callback.message.answer("❌ Подпишись на все каналы и попробуй снова.")


async def main():
    print("✅ Бот запущен и работает...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
