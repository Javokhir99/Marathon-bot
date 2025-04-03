from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("📘 Reading Marathon"),
    KeyboardButton("🎧 Listening Marathon")
)
main_menu.add(
    KeyboardButton("🗣️ Shadowing. Speak like a native"),
    KeyboardButton("✍️ Writing Marathon")
)

# Sahifalanuvchi Day tugmalari
def generate_day_reply_keyboard(section, page=1):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    start_day = (page - 1) * 5 + 1
    end_day = min(start_day + 4, 30)

    for day in range(start_day, end_day + 1):
        btn1 = KeyboardButton(f"{section.title()} Day {day}")
        if section != "shadowing":
            btn2 = KeyboardButton(f"{section.title()} Day {day} Answers")
            markup.row(btn1, btn2)
        else:
            markup.add(btn1)

    nav_buttons = []
    if page > 1:
        nav_buttons.append(KeyboardButton("⬅️ Previous"))
    if end_day < 30:
        nav_buttons.append(KeyboardButton("➡️ Next"))

    if nav_buttons:
        markup.row(*nav_buttons)

    markup.add(KeyboardButton("⬅️ Orqaga"))
    return markup
