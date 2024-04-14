import string
import random
from typing import Sequence


def generate_id(
    size: int = 8,
    chars: Sequence[str] = string.ascii_letters + string.digits,
) -> str:
    return "".join(random.choices(chars, k=size))
