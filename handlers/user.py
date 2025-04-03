from aiogram import types, Dispatcher
from keyboards import main_menu, generate_day_reply_keyboard
from database.db import get_material

# Har bir foydalanuvchining sahifasini saqlash uchun
user_pages = {}

# /start komandasi
async def start_command(message: types.Message):
    await message.answer(
        "🧠 *Marathon bo'tiga hush kelibsiz!*\n\n"
        "Ushbu botdagi materiallar katta ustozlar tomonidan tayyorlangan va bir joyga yig'ilgan. "
        "Ularning mehnatini qadrlang va ular haqqiga duo qilib qo'ying 🙏",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )

# Bo‘lim tanlanganda sahifani 1 dan boshlaymiz
async def section_selected(message: types.Message):
    section_map = {
        "📘 Reading Marathon": "reading",
        "🎧 Listening Marathon": "listening",
        "🗣️ Shadowing. Speak like a native": "shadowing",
        "✍️ Writing Marathon": "writing"
    }
    section = section_map.get(message.text)
    if section:
        user_pages[message.from_user.id] = {"section": section, "page": 1}
        markup = generate_day_reply_keyboard(section, page=1)
        await message.answer(f"{section.title()} bo‘limi tanlandi. Quyidagi kunlardan birini tanlang:", reply_markup=markup)

# Matn asosida tugmalarni boshqarish
async def handle_day_text(message: types.Message):
    text = message.text.strip().lower()
    user_id = message.from_user.id

    # Orqaga
    if text == "⬅️ orqaga":
        await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=main_menu)
        return

    # Sahifalash
    if user_id in user_pages:
        current = user_pages[user_id]
        section = current["section"]
        page = current["page"]

        if text == "➡️ next":
            page += 1
            user_pages[user_id]["page"] = page
            await message.answer(f"{section.title()} — {page}-sahifa", reply_markup=generate_day_reply_keyboard(section, page))
            return

        if text == "⬅️ previous":
            page = max(1, page - 1)
            user_pages[user_id]["page"] = page
            await message.answer(f"{section.title()} — {page}-sahifa", reply_markup=generate_day_reply_keyboard(section, page))
            return

    # Day materiallar
    for sec in ["reading", "listening", "shadowing", "writing"]:
        if text.startswith(sec):
            parts = text.split()
            if len(parts) >= 3 and parts[1] == "day" and parts[2].isdigit():
                day = int(parts[2])
                mtype = "answer" if "answer" in text else "main"

                material = get_material(sec, day, mtype)
                if material:
                    await message.answer(material)
                else:
                    await message.answer("❗Bu kun uchun material hali yuklanmagan.")
                return

# Ro‘yxatdan o‘tkazamiz
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(section_selected, lambda msg: msg.text in [
        "📘 Reading Marathon", "🎧 Listening Marathon",
        "🗣️ Shadowing. Speak like a native", "✍️ Writing Marathon"
    ])
    dp.register_message_handler(handle_day_text)
