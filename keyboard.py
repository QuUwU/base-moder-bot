from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder


class SettingsKeyboard:
    delete_profanity = InlineKeyboardButton(text="Filter Profanity", callback_data="profanity")
    delete_repost = InlineKeyboardButton(text="Remove Reposts", callback_data="repost")
    # delete_political = InlineKeyboardButton(text="Remove Political Mentions", callback_data="political") ~~ soon.
    delete_spam = InlineKeyboardButton(text="Antispam", callback_data="antispam")
    keyboard = InlineKeyboardBuilder()
    keyboard.add(delete_profanity, delete_repost, delete_spam)
    keyboard.adjust(1)


class FilterProfanityKeyboard:
    ru = InlineKeyboardButton(text="Ru", callback_data="filter_ru")
    eng = InlineKeyboardButton(text="Eng", callback_data="filter_eng")
    back_settings = InlineKeyboardButton(text="Back", callback_data="settings")
    keyboard = InlineKeyboardBuilder()
    keyboard.add(ru, eng, back_settings)
    keyboard.adjust(2)

    ru_on = InlineKeyboardButton(text="On", callback_data="filter_ru_on")
    ru_off = InlineKeyboardButton(text="Off", callback_data="filter_ru_off")
    back = InlineKeyboardButton(text="Back", callback_data="profanity")

    keyboard_on = InlineKeyboardBuilder()
    keyboard_off = InlineKeyboardBuilder()
    keyboard_on.add(ru_on, back)
    keyboard_off.add(ru_off, back)

    eng_on = InlineKeyboardButton(text="On", callback_data="filter_eng_on")
    eng_off = InlineKeyboardButton(text="Off", callback_data="filter_eng_off")

    keyboard_on_eng = InlineKeyboardBuilder()
    keyboard_off_eng = InlineKeyboardBuilder()
    keyboard_on_eng.add(eng_on, back)
    keyboard_off_eng.add(eng_off, back)


class FilterRepostAndLinksKb:
    back = InlineKeyboardButton(text="Back", callback_data="settings")
    on = InlineKeyboardButton(text="On", callback_data="repost_on")
    off = InlineKeyboardButton(text="Off", callback_data="repost_off")

    keyboard_on = InlineKeyboardBuilder()
    keyboard_off = InlineKeyboardBuilder()

    keyboard_on.add(on, back)
    keyboard_off.add(off, back)


class AntispamKeyboard:
    back = InlineKeyboardButton(text="Back", callback_data="settings")
    on = InlineKeyboardButton(text="On", callback_data="antispam_on")
    off = InlineKeyboardButton(text="Off", callback_data="antispam_off")

    keyboard_on = InlineKeyboardBuilder()
    keyboard_off = InlineKeyboardBuilder()

    keyboard_on.add(on, back)
    keyboard_off.add(off, back)
