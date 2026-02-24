import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN
from generator import generate_portfolio

logging.basicConfig(level=logging.INFO)
bot = Bot(token="8587190645:AAE0q_5DSnRpHcyg8WE248l29gSKZ1CuDe8")
dp = Dispatcher(storage=MemoryStorage())


# ─── STATES ───────────────────────────────────────────────
class Form(StatesGroup):
    full_name  = State()
    profession = State()
    bio        = State()
    skills     = State()
    experience = State()
    projects   = State()
    github     = State()
    linkedin   = State()
    email      = State()
    phone      = State()


# ─── KEYBOARD ─────────────────────────────────────────────
def skip_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data="skip")]
    ])


# ─── HELPERS ──────────────────────────────────────────────
async def ask_experience(target: Message, state: FSMContext):
    await target.answer(
        "🏢 Ish tajribangizni kiriting (har biri yangi qatorda):\n\n"
        "<code>2022-2024 | Senior Dev | ABC Company\n"
        "2020-2022 | Junior Dev | XYZ Startup</code>\n\n"
        "Yo'q bo'lsa ⏭ tugmasini bosing.",
        parse_mode="HTML", reply_markup=skip_kb()
    )
    await state.set_state(Form.experience)

async def ask_projects(target: Message, state: FSMContext):
    await target.answer(
        "📁 Loyihalaringizni kiriting (har biri yangi qatorda):\n\n"
        "<code>Portfolio Bot | Telegram bot | github.com/user/bot</code>\n\n"
        "Yo'q bo'lsa ⏭ tugmasini bosing.",
        parse_mode="HTML", reply_markup=skip_kb()
    )
    await state.set_state(Form.projects)

async def ask_github(target: Message, state: FSMContext):
    await target.answer(
        "🐙 GitHub profilingiz? (masalan: github.com/username)\n"
        "Yo'q bo'lsa ⏭ tugmasini bosing.",
        reply_markup=skip_kb()
    )
    await state.set_state(Form.github)

async def ask_linkedin(target: Message, state: FSMContext):
    await target.answer(
        "💼 LinkedIn profilingiz?\n"
        "Yo'q bo'lsa ⏭ tugmasini bosing.",
        reply_markup=skip_kb()
    )
    await state.set_state(Form.linkedin)

async def ask_phone(target: Message, state: FSMContext):
    await target.answer(
        "📱 Telefon raqamingiz?\n"
        "Yo'q bo'lsa ⏭ tugmasini bosing.",
        reply_markup=skip_kb()
    )
    await state.set_state(Form.phone)


async def generate_and_send(target: Message, state: FSMContext):
    """Ma'lumotlarni yig'ib, tasodifiy template bilan portfolio yaratadi."""
    data = await state.get_data()
    data.setdefault("full_name",  "Ism Familiya")
    data.setdefault("profession", "Mutaxassis")
    data.setdefault("bio",        "")
    data.setdefault("skills",     [])
    data.setdefault("experience", [])
    data.setdefault("projects",   [])
    data.setdefault("github",     "")
    data.setdefault("linkedin",   "")
    data.setdefault("email",      "")
    data.setdefault("phone",      "")

    # Tasodifiy template tanlanadi
    template = random.choice(["dark", "light", "creative"])
    data["template"] = template

    template_names = {
        "dark":     "🌙 Dark Modern",
        "light":    "☀️ Light Clean",
        "creative": "🎨 Creative Bold",
    }

    await target.answer(f"⏳ Portfolio yaratilmoqda... ({template_names[template]})")

    try:
        filepath = f"/tmp/portfolio_{target.chat.id}.html"
        generate_portfolio(data, filepath)

        doc = FSInputFile(filepath, filename="portfolio.html")
        await target.answer_document(
            doc,
            caption=(
                f"✅ <b>Portfolio tayyor!</b> ({template_names[template]})\n\n"
                "📌 <b>Netlify orqali joylash (1 daqiqa):</b>\n"
                "1. netlify.com ga kiring\n"
                "2. Faylni sahifaga tashlang (drag & drop)\n"
                "3. Bepul link olasiz ✨\n\n"
                "📌 <b>GitHub Pages:</b>\n"
                "1. Yangi repo → faylni <code>index.html</code> deb yuklang\n"
                "2. Settings → Pages → Deploy\n"
                "3. <code>username.github.io/repo-name</code>\n\n"
                "🔄 Yangi portfolio uchun /start"
            ),
            parse_mode="HTML"
        )
        os.remove(filepath)

    except Exception as e:
        await target.answer(
            f"❌ Xato yuz berdi:\n<code>{e}</code>\n\n"
            "/start bilan qayta urinib ko'ring.",
            parse_mode="HTML"
        )

    await state.clear()


# ─── START ────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 <b>Portfolio Generator Botga xush kelibsiz!</b>\n\n"
        "Bir necha savol — tayyor portfolio! 🚀\n\n"
        "Ismingiz va familiyangizni kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(Form.full_name)


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bekor qilindi. /start bilan qayta boshlang.")


# ─── FORM STEPS ───────────────────────────────────────────
@dp.message(Form.full_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("✅ Yaxshi!\n\n💼 Kasbingiz/Lavozimingiz? (masalan: Python Developer)")
    await state.set_state(Form.profession)


@dp.message(Form.profession)
async def get_profession(message: Message, state: FSMContext):
    await state.update_data(profession=message.text.strip())
    await message.answer("📝 O'zingiz haqingizda qisqacha bio yozing (2-4 jumla):")
    await state.set_state(Form.bio)


@dp.message(Form.bio)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text.strip())
    await message.answer(
        "🛠 Ko'nikmalaringizni kiriting (vergul bilan):\n\n"
        "<code>Python, Django, PostgreSQL, Docker</code>",
        parse_mode="HTML"
    )
    await state.set_state(Form.skills)


@dp.message(Form.skills)
async def get_skills(message: Message, state: FSMContext):
    skills = [s.strip() for s in message.text.split(",") if s.strip()]
    await state.update_data(skills=skills)
    await ask_experience(message, state)


@dp.message(Form.experience)
async def get_experience(message: Message, state: FSMContext):
    lines = [l.strip() for l in message.text.split("\n") if l.strip()]
    experience = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            experience.append({"period": parts[0], "role": parts[1], "company": parts[2]})
        elif len(parts) == 2:
            experience.append({"period": parts[0], "role": parts[1], "company": ""})
        else:
            experience.append({"period": "", "role": line, "company": ""})
    await state.update_data(experience=experience)
    await ask_projects(message, state)


@dp.message(Form.projects)
async def get_projects(message: Message, state: FSMContext):
    lines = [l.strip() for l in message.text.split("\n") if l.strip()]
    projects = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            projects.append({"name": parts[0], "desc": parts[1], "link": parts[2]})
        elif len(parts) == 2:
            projects.append({"name": parts[0], "desc": parts[1], "link": ""})
        else:
            projects.append({"name": line, "desc": "", "link": ""})
    await state.update_data(projects=projects)
    await ask_github(message, state)


@dp.message(Form.github)
async def get_github(message: Message, state: FSMContext):
    await state.update_data(github=message.text.strip())
    await ask_linkedin(message, state)


@dp.message(Form.linkedin)
async def get_linkedin(message: Message, state: FSMContext):
    await state.update_data(linkedin=message.text.strip())
    await message.answer("📧 Email manzilingiz?")
    await state.set_state(Form.email)


@dp.message(Form.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await ask_phone(message, state)


@dp.message(Form.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await generate_and_send(message, state)


# ─── SKIP HANDLER ─────────────────────────────────────────
@dp.callback_query(F.data == "skip")
async def handle_skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    current = await state.get_state()

    if current == Form.experience.state:
        await state.update_data(experience=[])
        await ask_projects(callback.message, state)

    elif current == Form.projects.state:
        await state.update_data(projects=[])
        await ask_github(callback.message, state)

    elif current == Form.github.state:
        await state.update_data(github="")
        await ask_linkedin(callback.message, state)

    elif current == Form.linkedin.state:
        await state.update_data(linkedin="")
        await callback.message.answer("📧 Email manzilingiz?")
        await state.set_state(Form.email)

    elif current == Form.phone.state:
        await state.update_data(phone="")
        await generate_and_send(callback.message, state)

    else:
        await callback.message.answer("Noaniq holat. /start bilan qayta boshlang.")
        await state.clear()


# ─── RUN ──────────────────────────────────────────────────
async def main():
    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
