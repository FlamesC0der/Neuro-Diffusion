import random
import os

import app.database.functions as fn
from app.exceptions import *

ROOT_DIR = os.path.dirname(__file__)


async def get_random_start_image():
    return random.choice(os.listdir(os.path.join(ROOT_DIR, "assets/start_images")))


async def activate_promo_code(tg_id: int, promo_code: str) -> int:
    PROMOCODES = await fn.get_all_promo_codes()
    activated_promo_codes = await fn.get_activated_promo_codes(tg_id)
    if activated_promo_codes:
        activated_promo_codes = list(map(int, activated_promo_codes.split(";")))
    else:
        activated_promo_codes = []

    promocode = await fn.get_promocode(promo_code, "id")
    active = await fn.get_promocode(promo_code, "active")

    if not (promocode in PROMOCODES) or not active:
        raise PromocodeInvalidException()
    elif promocode in activated_promo_codes:
        raise PromocodeAlreadyActivatedException()
    else:
        reward = await fn.get_promocode(promo_code, "value")
        await fn.activate_promocode(tg_id, promo_code)
        return reward
