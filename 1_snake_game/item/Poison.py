from typing import Final

from .Item import Item

PoisonModValue: Final = 2


class Poison(Item):
    def __init__(self, parent_screen):
        super(Poison, self).__init__(parent_screen)
        self.move()

    def move(self):
        self.ItemSpecialModValue = PoisonModValue
        super().move()

    def getImagePath(self):
        return "resources/poison.jpg"
