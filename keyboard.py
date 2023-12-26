from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


class SettingsKeyboard:
    delete_profanity = InlineKeyboardButton(text="Filter Profanity", callback_data="profanity")
    delete_repost = InlineKeyboardButton(text="Remove Reposts", callback_data="repost")
    # delete_political = InlineKeyboardButton(text="Remove Political Mentions", callback_data="political") ~~ soon.
    delete_spam = InlineKeyboardButton(text="Antispam", callback_data="spam")
    keyboard = InlineKeyboardBuilder()
    keyboard.add(delete_profanity, delete_repost, delete_spam)
    keyboard.adjust(1)


class FilterProfanityKeyboard:
    ru = InlineKeyboardButton(text="Ru", callback_data="filter_ru")
    eng = InlineKeyboardButton(text="Eng", callback_data="filter_eng")
    keyboard = InlineKeyboardBuilder()
    keyboard.add(ru, eng)
