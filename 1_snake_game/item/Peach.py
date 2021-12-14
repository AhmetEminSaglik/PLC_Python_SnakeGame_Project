from typing import Final
from .Item import Item

PeachModValue: Final = 1


class Peach(Item):

    def __init__(self, parent_screen):
        super(Peach, self).__init__(parent_screen)

    def move(self):
        self.ItemSpecialModValue = PeachModValue
        super().move()

    def getImagePath(self):
        return "resources/peach.jpg"
