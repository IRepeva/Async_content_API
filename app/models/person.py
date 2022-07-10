import uuid
from typing import List

from models.mixin import MixinModel


class Person(MixinModel):
    full_name: str
    role: str | None = ''
    film_ids: List[uuid.UUID | str] | None = []
