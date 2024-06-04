import os

from aiogram import F, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile

from app.handlers.generation import generation_router
from app.misc import get_random_start_image, activate_promo_code
from app.exceptions import *
import app.keyboards as kb
import app.database.functions as fn

router = Router()
router.include_router(generation_router)


@router.message(CommandStart(deep_link=True, magic=None))
async def promo_code(message: Message, command: CommandObject):
    try:
        user_id = message.from_user.id
        promo_code = command.args

        reward = await activate_promo_code(user_id, promo_code)

        await fn.update_tokens(user_id, reward)
        balance = await fn.get_tokens(user_id)
        await message.answer(f"Промокод активирован\!\nТеперь ваш балланс — {balance} tokens\(\+{reward}\)")
    except PromocodeInvalidException:
        await message.answer("Промокод недействителен, или у него истёк срок действия💔")
    except PromocodeAlreadyActivatedException:
        await message.answer("Промокод уже активирован\!")
    except Exception as e:
        print(f"Произошла ошибка: \n{e}")
        await message.answer(f"Произошла ошибка")


@router.message(CommandStart(deep_link=False, magic=None))
async def cmd_start(message: Message):
    try:
        await fn.register_user(message.from_user.id)
        photo = FSInputFile(os.path.join('assets/start_images', await get_random_start_image()))
        await message.answer_photo(
            photo,
            caption=f"✋Привет {message.from_user.full_name}\!\n\nЭтот бот умеет генерировать картинки в аниме стилистике по запросу\. Для генерации используется ИИ, несколько моделей, такие как: Cetus\.\n\nДля того чтобы начать создавать, напиши мне запрос, на английском, например: `anime girl in white clothes with a red bow`\.",
            reply_markup=kb.start
        )
    except Exception as e:
        print(f"Произошла ошибка: \n{e}")
        await message.answer(f"Произошла ошибка")


@router.message(Command("balance"))
async def balance(message: Message):
    try:
        user_id = message.from_user.id
        balance = await fn.get_tokens(user_id)
        await message.answer(f"💸Баланс: {balance} токенов")
    except Exception as e:
        print(f"Произошла ошибка: \n{e}")
        await message.answer(f"Произошла ошибка")
