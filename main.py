import logging
import asyncio
import config
import user_data
from aiogram import Bot, Router, Dispatcher, F
from aiogram.filters import Command, BaseFilter
from aiogram.types import Message, CallbackQuery
from keyboard import SettingsKeyboard, FilterProfanityKeyboard, FilterRepostAndLinksKb, AntispamKeyboard
from utils import get_value, transform_value, add_to_filter
from user_data import profanity_state_ru, profanity_state_eng, repost_state, antispam_state


bot = Bot(config.TOKEN)  # Bot instance
router = Router()


class Restrict(BaseFilter):
    def __init__(self, privileges: bool):
        self.userPrivileges = privileges

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

        if user.status in 'creator':
            return True
        elif isinstance(self.userPrivileges, str):
            return user.can_restrict_members == self.userPrivileges
        else:
            return str(user.can_restrict_members) in str(self.userPrivileges)


class RemoveProfanity(BaseFilter):
    def __init__(self, enabled: bool):
        self.remove_profanity = enabled

    async def __call__(self, message: Message) -> bool:
        chat_id = message.chat.id
        msq_text = message.text.lower().split()

        if get_value(profanity_state_ru, chat_id):
            for profanity_word in user_data.profanity_ru:
                if profanity_word in msq_text:
                    return True

        if get_value(profanity_state_eng, chat_id):
            for profanity_word in user_data.profanity_eng:
                if profanity_word in msq_text:
                    return True

        return False


#  /start command handler if chat is private
@router.message(Command(commands=['start']), F.chat.type == "private")
async def start_private(m: Message):
    q = "Hello. I am a simplified group moderation bot. Add me to your group so I can suggest settings changes."
    await m.answer(q)


#  /start command handler if chat is group or super group
@router.message(Command(commands=['start']), F.chat.type == ("group" or "supergroup"), Restrict(True))
async def start_group(m: Message):
    q = "Hello. Thank you for adding me to the group."
    await m.answer(q)


#  /settings command handler. open settings options
@router.message(Command(commands=['settings']), Restrict(True))
async def settings(m: Message):
    text = "Welcome to settings"
    chat_id = m.chat.id
    await bot.send_message(chat_id, text, reply_markup=SettingsKeyboard.keyboard.as_markup())


# redaction command handler if press "back" button in sub menu
@router.callback_query(F.data == "settings")
async def back_settings(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    text = "Welcome to settings"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=SettingsKeyboard.keyboard.as_markup())
    await cq.answer()


# open submenu function "Filter profanity"
@router.callback_query(F.data == "profanity")
async def profanity(cq: CallbackQuery):
    text = "Select language"
    chat_id = cq.message.chat.id
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterProfanityKeyboard.keyboard.as_markup())
    await cq.answer()


# toggles filter settings display for ru language
@router.callback_query(F.data == "filter_ru")
async def filter_ru(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    profanity_enabled = transform_value(get_value(profanity_state_ru, chat_id))
    text = "Filter Profanity: " + profanity_enabled
    markup = FilterProfanityKeyboard.keyboard_on if not get_value(profanity_state_ru, chat_id) \
        else FilterProfanityKeyboard.keyboard_off
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=markup.as_markup())
    await cq.answer()


#  enables profanity filtering function for ru language
@router.callback_query(F.data == "filter_ru_on")
async def filter_ru_on(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(profanity_state_ru, chat_id, True)
    text = "Filter Profanity: Enabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterProfanityKeyboard.keyboard_off.as_markup())
    await cq.answer()


#  disables profanity filtering function for ru language
@router.callback_query(F.data == "filter_ru_off")
async def filter_ru_off(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(profanity_state_ru, chat_id, False)
    text = "Filter Profanity: Disabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterProfanityKeyboard.keyboard_on.as_markup())
    await cq.answer()


# toggles filter settings display for english language
@router.callback_query(F.data == "filter_eng")
async def filter_eng(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    profanity_enabled = transform_value(get_value(profanity_state_eng, chat_id))
    text = "Filter Profanity: " + profanity_enabled
    markup = FilterProfanityKeyboard.keyboard_on if not get_value(profanity_state_eng, chat_id) \
        else FilterProfanityKeyboard.keyboard_off
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=markup.as_markup())
    await cq.answer()


#  enables profanity filtering function for english language
@router.callback_query(F.data == "filter_eng_on")
async def filter_eng_on(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(profanity_state_eng, chat_id, True)
    text = "Filter Profanity: Enabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterProfanityKeyboard.keyboard_off_eng.as_markup())
    await cq.answer()


#  disables profanity filtering function for english language
@router.callback_query(F.data == "filter_eng_off")
async def filter_eng_off(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(profanity_state_eng, chat_id, False)
    text = "Filter Profanity: Disabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterProfanityKeyboard.keyboard_on_eng.as_markup())
    await cq.answer()


# toggles filter settings display for remove repost function
@router.callback_query(F.data == "repost")
async def remove_repost(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    repost_enabled = transform_value(get_value(repost_state, chat_id))
    text = "Remove Repost and links: " + repost_enabled
    markup = FilterRepostAndLinksKb.keyboard_on if not get_value(repost_state, chat_id) \
        else FilterRepostAndLinksKb.keyboard_off
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=markup.as_markup())
    await cq.answer()


@router.callback_query(F.data == "repost_on")
async def repost_on(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(repost_state, chat_id, True)
    text = "Remove Repost: Enabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterRepostAndLinksKb.keyboard_off.as_markup())
    await cq.answer()


@router.callback_query(F.data == "repost_off")
async def repost_off(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(repost_state, chat_id, False)
    text = "Remove Repost: Disabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=FilterRepostAndLinksKb.keyboard_on.as_markup())
    await cq.answer()


# toggles filter settings display for antispam function
@router.callback_query(F.data == "antispam")
async def antispam(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    repost_enabled = transform_value(get_value(antispam_state, chat_id))
    text = "Remove Repost and links: " + repost_enabled
    markup = AntispamKeyboard.keyboard_on if not get_value(repost_state, chat_id) \
        else AntispamKeyboard.keyboard_off
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=markup.as_markup())
    await cq.answer()


@router.callback_query(F.data == "antispam_on")
async def antispam_on(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(antispam_state, chat_id, True)
    text = "Antispam: Enabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=AntispamKeyboard.keyboard_off.as_markup())
    await cq.answer()


@router.callback_query(F.data == "antispam_off")
async def antispam_off(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    add_to_filter(antispam_state, chat_id, False)
    text = "Antispam: Disabled"
    await bot.edit_message_text(chat_id=chat_id, message_id=cq.message.message_id, text=text,
                                reply_markup=AntispamKeyboard.keyboard_on.as_markup())
    await cq.answer()


@router.message(RemoveProfanity(True))
async def remove_profanity_handler(m: Message):
    await bot.delete_message(m.chat.id, m.message_id)


async def main() -> None:
    slave = Dispatcher()
    slave.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    # await filters.bot2.delete_webhook(drop_pending_updates=True)
    await slave.start_polling(bot)
    # await slave.start_polling(filters.bot2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
