import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReactionTypeEmoji
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
EMOJI = "👍"

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


async def like(bot: Bot, msg: Message):
    try:
        await bot.set_message_reaction(
            chat_id=msg.chat.id,
            message_id=msg.message_id,
            reaction=[ReactionTypeEmoji(emoji=EMOJI)],
        )
    except Exception as e:
        logging.warning(f"Like failed: {e}")


# Channel posts
@dp.channel_post()
async def on_channel_post(msg: Message, bot: Bot):
    await like(bot, msg)


# Groups / supergroups
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def on_group_message(msg: Message, bot: Bot):
    await like(bot, msg)


# Private chat
@dp.message(F.chat.type == "private")
async def on_private(msg: Message, bot: Bot):
    await like(bot, msg)


async def main():
    bot = Bot(BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
