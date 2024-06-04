from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📖Гайд (soon)", url="https://telegra.ph/Neuro-Diffusion-Guide-06-02"),
            InlineKeyboardButton(text="❤️Поддержать автора", url="https://boosty.to/flamescoder/donate")
        ],
    ]
)


async def create_image_button(promt_id: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="✨Создать", callback_data=f"create_image_{promt_id}"))
    return keyboard.as_markup()
