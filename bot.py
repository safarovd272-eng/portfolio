import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
import os

from config import BOT_TOKEN
from generator import generate_portfolio

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8587190645:AAE0q_5DSnRpHcyg8WE248l29gSKZ1CuDe8")
dp = Dispatcher(storage=MemoryStorage())


# ============ STATES ============
class PortfolioForm(StatesGroup):
    full_name = State()
    profession = State()
    bio = State()
    skills = State()
    experience = State()
    projects = State()
    github = State()
    linkedin = State()
    email = State()
    phone = State()
    template = State()


# ============ KEYBOARDS ============
def template_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌙 Dark Modern", callback_data="template_dark"),
            InlineKeyboardButton(text="☀️ Light Clean", callback_data="template_light"),
        ],
        [
            InlineKeyboardButton(text="🎨 Creative Bold", callback_data="template_creative"),
        ]
    ])


def skip_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data="skip")]
    ])


# ============ HANDLERS ============
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 <b>Portfolio Generator Botga xush kelibsiz!</b>\n\n"
        "Men sizga professional portfolio yaratib beraman.\n"
        "Bir necha savollarga javob bering va tayyor portfolio oling! 🚀\n\n"
        "Boshlaylik! Ismingiz va familiyangizni kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(PortfolioForm.full_name)


@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi. /start bilan qayta boshlang.")


@dp.message(PortfolioForm.full_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("✅ Ajoyib!\n\n💼 Kasbingiz/Lavozimingiz nima? (masalan: Python Developer, UI/UX Designer)")
    await state.set_state(PortfolioForm.profession)


@dp.message(PortfolioForm.profession)
async def get_profession(message: Message, state: FSMContext):
    await state.update_data(profession=message.text.strip())
    await message.answer(
        "📝 O'zingiz haqingizda qisqacha bio yozing:\n"
        "(2-4 jumlada o'zingizni tanishtiring)"
    )
    await state.set_state(PortfolioForm.bio)


@dp.message(PortfolioForm.bio)
async def get_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text.strip())
    await message.answer(
        "🛠 Ko'nikmalaringizni (skills) kiriting:\n"
        "Vergul bilan ajrating: <code>Python, Django, PostgreSQL, Docker</code>",
        parse_mode="HTML"
    )
    await state.set_state(PortfolioForm.skills)


@dp.message(PortfolioForm.skills)
async def get_skills(message: Message, state: FSMContext):
    skills = [s.strip() for s in message.text.split(",") if s.strip()]
    await state.update_data(skills=skills)
    await message.answer(
        "🏢 Ish tajribangizni kiriting:\n"
        "Har bir ish joyini yangi qatordan yozing:\n\n"
        "<code>2022-2024 | Senior Dev | ABC Company\n"
        "2020-2022 | Junior Dev | XYZ Startup</code>\n\n"
        "Tajriba yo'q bo'lsa ⏭ O'tkazib yuborish tugmasini bosing.",
        parse_mode="HTML",
        reply_markup=skip_keyboard()
    )
    await state.set_state(PortfolioForm.experience)


@dp.callback_query(F.data == "skip")
async def skip_field(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    await callback.answer()

    if current_state == PortfolioForm.experience.state:
        await state.update_data(experience=[])
        await callback.message.answer(
            "📁 Loyihalaringizni kiriting:\n"
            "Har bir loyihani yangi qatordan:\n\n"
            "<code>Portfolio Bot | Telegram bot | github.com/user/bot\n"
            "E-commerce | Online do'kon | github.com/user/shop</code>\n\n"
            "Yo'q bo'lsa o'tkazib yuboring.",
            parse_mode="HTML",
            reply_markup=skip_keyboard()
        )
        await state.set_state(PortfolioForm.projects)

    elif current_state == PortfolioForm.projects.state:
        await state.update_data(projects=[])
        await callback.message.answer("🐙 GitHub profilingiz URL-i? (masalan: github.com/username)", reply_markup=skip_keyboard())
        await state.set_state(PortfolioForm.github)

    elif current_state == PortfolioForm.github.state:
        await state.update_data(github="")
        await callback.message.answer("💼 LinkedIn profilingiz URL-i?", reply_markup=skip_keyboard())
        await state.set_state(PortfolioForm.linkedin)

    elif current_state == PortfolioForm.linkedin.state:
        await state.update_data(linkedin="")
        await callback.message.answer("📧 Email manzilingiz?")
        await state.set_state(PortfolioForm.email)

    elif current_state == PortfolioForm.phone.state:
        await state.update_data(phone="")
        await ask_template(callback.message, state)


async def ask_template(message: Message, state: FSMContext):
    await message.answer(
        "🎨 Portfolio dizayni tanlang:",
        reply_markup=template_keyboard()
    )
    await state.set_state(PortfolioForm.template)


@dp.message(PortfolioForm.experience)
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
    await message.answer(
        "📁 Loyihalaringizni kiriting:\n"
        "Har bir loyihani yangi qatordan:\n\n"
        "<code>Portfolio Bot | Telegram bot | github.com/user/bot</code>",
        parse_mode="HTML",
        reply_markup=skip_keyboard()
    )
    await state.set_state(PortfolioForm.projects)


@dp.message(PortfolioForm.projects)
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
    await message.answer("🐙 GitHub profilingiz URL-i?", reply_markup=skip_keyboard())
    await state.set_state(PortfolioForm.github)


@dp.message(PortfolioForm.github)
async def get_github(message: Message, state: FSMContext):
    await state.update_data(github=message.text.strip())
    await message.answer("💼 LinkedIn profilingiz URL-i?", reply_markup=skip_keyboard())
    await state.set_state(PortfolioForm.linkedin)


@dp.message(PortfolioForm.linkedin)
async def get_linkedin(message: Message, state: FSMContext):
    await state.update_data(linkedin=message.text.strip())
    await message.answer("📧 Email manzilingiz?")
    await state.set_state(PortfolioForm.email)


@dp.message(PortfolioForm.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    await message.answer("📱 Telefon raqamingiz? (ixtiyoriy)", reply_markup=skip_keyboard())
    await state.set_state(PortfolioForm.phone)


@dp.message(PortfolioForm.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await ask_template(message, state)


@dp.callback_query(F.data.startswith("template_"))
async def choose_template(callback: CallbackQuery, state: FSMContext):
    try:
        template = callback.data.replace("template_", "")
        await state.update_data(template=template)
        await callback.answer()

        data = await state.get_data()

        # Default qiymatlar — None bo'lsa xato chiqmasin
        data.setdefault("full_name", "Ism Familiya")
        data.setdefault("profession", "Mutaxassis")
        data.setdefault("bio", "")
        data.setdefault("skills", [])
        data.setdefault("experience", [])
        data.setdefault("projects", [])
        data.setdefault("github", "")
        data.setdefault("linkedin", "")
        data.setdefault("email", "")
        data.setdefault("phone", "")

        await callback.message.answer("⏳ Portfolio yaratilmoqda...")

        # Generate HTML
        user_id = callback.from_user.id
        filepath = f"/tmp/portfolio_{user_id}.html"

        generate_portfolio(data, filepath)

        # Send file
        doc = FSInputFile(filepath, filename="portfolio.html")
        await callback.message.answer_document(
            doc,
            caption=(
                "✅ <b>Portfolio tayyor!</b>\n\n"
                "📌 <b>Netlify (eng oson — 1 daqiqa):</b>\n"
                "1. netlify.com ga kiring\n"
                "2. Faylni drag & drop qiling\n"
                "3. Bepul link olasiz ✨\n\n"
                "📌 <b>GitHub Pages:</b>\n"
                "1. Yangi repo yarating\n"
                "2. Faylni <code>index.html</code> deb yuklang\n"
                "3. Settings → Pages → Deploy\n"
                "4. <code>username.github.io/repo-name</code>\n\n"
                "Yangi portfolio uchun /start"
            ),
            parse_mode="HTML"
        )
        os.remove(filepath)
        await state.clear()

    except Exception as e:
        await callback.message.answer(
            f"❌ Xato yuz berdi:\n<code>{str(e)}</code>\n\n"
            "Qaytadan urinish uchun /start",
            parse_mode="HTML"
        )
        await state.clear()


async def main():
    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
