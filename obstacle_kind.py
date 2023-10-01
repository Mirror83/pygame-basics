from enum import Enum, auto


class ObstacleKind(Enum):
    SNAIL = auto()
    FLY = auto()

    def get_bottom_y(self) -> int:
        if self is ObstacleKind.FLY:
            return 210
        else:
            return 300
