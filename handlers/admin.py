from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import ADMINS
from database.db import add_material, delete_material

class AdminStates(StatesGroup):
    WaitingForSection = State()
    WaitingForDay = State()
    WaitingForType = State()
    WaitingForContent = State()

async def admin_start(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Sizda admin huquqlari yo‘q.")
        return
    await message.answer("Bo‘lim nomini kiriting (reading/listening/shadowing/writing):")
    await AdminStates.WaitingForSection.set()

async def section_chosen(message: types.Message, state: FSMContext):
    section = message.text.strip().lower()
    if section not in ["reading", "listening", "shadowing", "writing"]:
        await message.answer("Noto‘g‘ri bo‘lim nomi.")
        return
    await state.update_data(section=section)
    await message.answer("Kun raqamini kiriting (1-30):")
    await AdminStates.WaitingForDay.set()

async def day_chosen(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or not (1 <= int(message.text) <= 30):
        await message.answer("Faqat 1–30 oralig‘idagi raqamni yozing.")
        return
    await state.update_data(day=int(message.text))
    await message.answer("Material turi: main yoki answer?")
    await AdminStates.WaitingForType.set()

async def type_chosen(message: types.Message, state: FSMContext):
    mtype = message.text.strip().lower()
    if mtype not in ["main", "answer"]:
        await message.answer("Faqat main yoki answer deb yozing.")
        return
    await state.update_data(type=mtype)
    await message.answer("Endi material matnini yuboring:")
    await AdminStates.WaitingForContent.set()

async def content_received(message: types.Message, state: FSMContext):
    data = await state.get_data()
    section = data["section"]
    day = data["day"]
    mtype = data["type"]
    content = message.text

    delete_material(section, day, mtype)
    add_material(section, day, mtype, content)

    await message.answer(f"{section.title()} {day}-kun uchun {mtype} material saqlandi ✅")
    await state.finish()

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['admin'])
    dp.register_message_handler(section_chosen, state=AdminStates.WaitingForSection)
    dp.register_message_handler(day_chosen, state=AdminStates.WaitingForDay)
    dp.register_message_handler(type_chosen, state=AdminStates.WaitingForType)
    dp.register_message_handler(content_received, state=AdminStates.WaitingForContent)
