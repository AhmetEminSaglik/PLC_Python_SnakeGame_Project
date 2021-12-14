from typing import Final

from .Item import Item

AppleModValue: Final = 0


class Apple(Item):

    def __init__(self, parent_screen):
        super(Apple, self).__init__(parent_screen)
        self.move()

    def move(self):
        self.ItemSpecialModValue = AppleModValue
        super().move()

    def getImagePath(self):
        return "resources/apple.jpg"
