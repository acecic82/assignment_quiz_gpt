from enum import Enum


class Level(Enum):
    EASY = "EASY"
    HARD = "HARD"

    def valueOf(value: str):
        for item in Level:
            if item.name == value:
                return item
        return None
