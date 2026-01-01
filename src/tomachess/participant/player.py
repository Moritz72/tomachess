from tomachess.enum import Sex, Title
from tomachess.models import Entity


class Player(Entity):
    name: str
    sex: Sex = Sex.UNKNOWN
    birthday: int | None = None
    country: str | None = None
    title: Title = Title.NONE
    rating: int | None = None
