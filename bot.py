from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboard import SettingsKeyboard

TOKEN = ''  # Token obtained after creating a bot on @BotFather
bot = Bot(TOKEN)  # Bot instance
router = Router()


#  /start command handler if chat is private
@router.message(Command(commands=['start']), F.chat.type == "private")
async def start(m: Message):
    q = "Hello. I am a simplified group moderation bot. Add me to your group so I can suggest settings changes."
    await m.answer(q)


#  /start command handler if chat is group or super group
@router.message(Command(commands=['start']), F.chat.type == ("group" or "supergroup"))
async def start(m: Message):
    q = "Hello. Thank you for adding me to the group."
    await m.answer(q)


@router.message(Command(commands=['settings']))
async def settings(m: Message):
    text = "Welcome to settings"
    chat_id = m.chat.id
    await bot.send_message(chat_id, text, reply_markup=SettingsKeyboard.keyboard.as_markup())
 
    
@router.callback_query(F.data == "profanity")
async def profanity(cq: CallbackQuery):
    text = f"Filter Profanity: {None}"

    await cq.answer()


async def main() -> None:
    slave = Dispatcher()
    slave.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await slave.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
