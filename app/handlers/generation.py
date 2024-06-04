import uuid

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from app.exceptions import *
import app.keyboards as kb
import app.database.functions as fn
# from app.ai.main import diffusion_manager

generation_router = Router()


@generation_router.message(F.text)
async def generate_image_message(message: Message):
    try:
        prompt = message.text
        prompt_id = str(uuid.uuid4())

        await fn.create_prompt(prompt_id, prompt, message.from_user.id)

        prompt_id_text = prompt_id.replace("-", "\-")

        await message.answer(
            f'`{prompt_id_text}`\n\n🎨Запрос: `{prompt}`\n🗂Модель: Cetus',
            reply_markup=await kb.create_image_button(prompt_id)
        )
    except Exception as e:
        print(f"Произошла ошибка: \n{e}")
        await message.edit_text(f'Произошла ошибка')


@generation_router.callback_query(F.data.startswith("create_image"))
async def create_image(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        prompt_id = callback.data.split('_')[2]
        prompt_id_text = prompt_id.replace("-", "\-")

        prompt = await fn.get_prompt(prompt_id)
        tokens = await fn.get_tokens(user_id)

        if tokens < 5:
            raise NotEnoughTokensException()

        await callback.answer('')
        await callback.message.edit_text(
            f'`{prompt_id_text}`\n\n🎨Генерация изображения по запросу: `{prompt}`\n\nЭто займёт примерно 40 секунд\-1\.5 минуты\.',
        )
        image = await diffusion_manager.generate_image(model_name="CetusMix", prompt=prompt)

        await fn.update_images_generated(user_id, 1)
        await fn.update_tokens(user_id, -10)

        await callback.message.delete()
        document = BufferedInputFile(image.getvalue(), filename=f"{prompt_id}.png")
        await callback.message.answer_document(document, caption=f"`{prompt_id_text}`\n\n🎨Запрос: `{prompt}`\.")

    except GenerationErrorException:
        await callback.message.edit_text('🎨Ошибка генерации изображения💔\.')
    except NotEnoughTokensException:
        await callback.message.edit_text('🎨Недостаточно токенов для генерации изображения💔\.')
    except Exception as e:
        print(f"Произошла ошибка: \n{e}")
        await callback.message.edit_text(f'Произошла ошибка')
