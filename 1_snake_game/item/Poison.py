from typing import Final

from .Item import Item


PoisonModValue: Final = 2


class Poison(Item):
    def __init__(self, parent_screen):
        super(Poison, self).__init__(parent_screen)
        self.move()

    def draw(self):
        super().draw()

    def move(self):
        super(Poison, self).move()
        self.x += PoisonModValue * self.getSize()
        # super().refactorItemLocation()
        self.foodIsCreated = True

    def getImagePath(self):
        return "resources/poison.jpg"