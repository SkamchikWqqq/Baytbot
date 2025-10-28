from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.utils.exceptions import TelegramForbiddenError, TelegramAPIError
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
    try:
        await message.answer("👋 Привет! Подпишись на каналы ниже:", reply_markup=keyboard)
    except TelegramForbiddenError:
        print(f"[!] Пользователь {message.from_user.id} заблокировал бота.")
    except TelegramAPIError as e:
        print(f"[Ошибка Telegram API]: {e}")


@dp.callback_query(lambda c: c.data == "check_subs")
async def check_subs(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    subscribed_all = True

    for channel in CHANNELS:
        try:
            chat = await bot.get_chat(channel)
            member = await bot.get_chat_member(chat.id, user_id)
            if member.status == "left":
                subscribed_all = False
        except TelegramForbiddenError:
            print(f"[!] Пользователь {user_id} заблокировал бота.")
            return
        except Exception as e:
            print(f"[Ошибка при проверке подписки]: {e}")
            subscribed_all = False

    try:
        if subscribed_all:
            await callback.message.answer("✅ Отлично! Ты подписан на все каналы.")
        else:
            await callback.message.answer("❌ Подпишись на все каналы и попробуй снова.")
    except TelegramForbiddenError:
        print(f"[!] Пользователь {user_id} заблокировал бота.")
    except TelegramAPIError as e:
        print(f"[Ошибка Telegram API]: {e}")


# 🔹 Глобальный обработчик ошибок, чтобы бот не вылетал
@dp.errors_handler()
async def global_error_handler(update, exception):
    print(f"[GLOBAL ERROR] {exception}")
    return True  # предотвращает остановку бота


async def main():
    print("✅ Бот запущен и работает...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
