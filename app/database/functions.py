from app.database.models import async_session
from app.database.models import User, Promocode, Prompt
from sqlalchemy import select, update, delete


async def register_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_tokens(tg_id: int) -> int:
    async with async_session() as session:
        return await session.scalar(select(User.tokens).where(User.tg_id == tg_id))


async def set_tokens(tg_id: int, value: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.tokens = value
            await session.commit()


async def update_tokens(tg_id: int, value: int) -> None:
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(tokens=User.tokens + value))
        await session.commit()


async def create_prompt(id: str, prompt: str, user_id: int) -> None:
    async with async_session() as session:
        _prompt = await session.scalar(select(Prompt).where(Prompt.id == id))
        if not _prompt:
            session.add(Prompt(id=id, prompt=prompt, user_id=user_id))
            await session.commit()


async def get_prompt(id: str) -> str:
    async with async_session() as session:
        return await session.scalar(select(Prompt.prompt).where(Prompt.id == id))


async def create_promocode(name: str, active: bool, value: int) -> None:
    async with async_session() as session:
        promocode = await session.scalar(select(Promocode).where(Promocode.name == name))

        if not promocode:
            session.add(Promocode(name=name, active=active, value=value))
            await session.commit()


async def get_promocode(name: str, param: str) -> bool | int | str:
    async with async_session() as session:
        if param == "active":
            return await session.scalar(select(Promocode.active).where(Promocode.name == name))
        elif param == "value":
            return await session.scalar(select(Promocode.value).where(Promocode.name == name))
        elif param == "id":
            return await session.scalar(select(Promocode.id).where(Promocode.name == name))


async def get_all_promo_codes() -> list[int]:
    async with async_session() as session:
        return list(await session.scalars(select(Promocode.id)))


async def get_activated_promo_codes(tg_id: int) -> str | None:
    async with async_session() as session:
        return await session.scalar(select(User.activated_promo_codes).where(User.tg_id == tg_id))


async def activate_promocode(tg_id: int, promo_code: str) -> None:
    async with async_session() as session:
        promo_code_id = await session.scalar(select(Promocode.id).where(Promocode.name == promo_code))
        user_promocodes = await session.scalar(select(User.activated_promo_codes).where(User.tg_id == tg_id))

        if user_promocodes:
            await session.execute(update(User).where(User.tg_id == tg_id).values(
                activated_promo_codes=user_promocodes + ";" + promo_code_id
            ))
        else:
            await session.execute(update(User).where(User.tg_id == tg_id).values(
                activated_promo_codes=str(promo_code_id)
            ))
        await session.commit()


async def get_images_generated(tg_id: int) -> int:
    async with async_session() as session:
        return await session.scalar(select(User.images_generated).where(User.tg_id == tg_id))


async def update_images_generated(tg_id: int, value: int) -> None:
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(images_generated=User.images_generated + value))
        await session.commit()
