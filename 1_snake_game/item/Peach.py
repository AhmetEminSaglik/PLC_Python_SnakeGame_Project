from typing import Final
from .Item import Item

PeachModValue: Final = 1

class Peach(Item):

    def __init__(self, parent_screen):
        super(Peach, self).__init__(parent_screen)
        # self.move()

    def draw(self):
        super().draw()

    def move(self):
        super(Peach, self).move()
        self.x += PeachModValue * self.getSize()
        self.foodIsCreated = True

    def getImagePath(self):
        return "resources/peach.jpg"
