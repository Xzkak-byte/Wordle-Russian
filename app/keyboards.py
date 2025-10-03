from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup

base_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Играть 🕹",callback_data="start_play")],
    [InlineKeyboardButton(text="Настройки ⚙️",callback_data="settings"), InlineKeyboardButton(text="Правила 📙", callback_data="rules")]
])

settings_if_6 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да, поставить 6 жизней ✅",callback_data="turn_off_inf")],
    [InlineKeyboardButton(text="Нет, оставить бесконечность ❌",callback_data="nothing")]
])

settings_if_inf = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да, поставить бесконечность ✅",callback_data="turn_on_inf")],
    [InlineKeyboardButton(text="Нет, оставить 6 жизней ❌",callback_data="nothing")]
])

out_game = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Выйти из игры 🚪",callback_data="quit")]
])

yes_no_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да ✅", callback_data="settings_yes"),InlineKeyboardButton(text="Нет ❌",callback_data="nothing")]
]) 

play = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Играть 🕹",callback_data="start_play")]
])

otmena = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена ❌",callback_data="nothing")]
])

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить число бесконечных игр ♾️", callback_data="admin_change_inf_games")],
    [InlineKeyboardButton(text="Изменить число обычных игр 👾", callback_data="admin_change_simple_games")],
    [InlineKeyboardButton(text="Отправить сообщение 💬", callback_data="send_messages")]
])

ceo_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить число бесконечных игр ♾️", callback_data="admin_change_inf_games")],
    [InlineKeyboardButton(text="Изменить число обычных игр 👾", callback_data="admin_change_simple_games")],
    [InlineKeyboardButton(text="Назначить админа 👤",callback_data="set_admin"),InlineKeyboardButton(text="Уволить админа 👤",callback_data="remove_admin")],
    [InlineKeyboardButton(text="Отправить сообщение 💬", callback_data="send_messages")]
])

choice_message = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Всем пользователям 👥"),KeyboardButton(text="Конкретному человеку 🧍")],
    [KeyboardButton(text="Главной администрации 👨‍💻"),KeyboardButton(text="Всем администраторам 👤")]
],resize_keyboard=True,one_time_keyboard=True)