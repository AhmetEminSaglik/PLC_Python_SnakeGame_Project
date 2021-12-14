from typing import Final

from .Item import Item


AppleModValue: Final = 0


class Apple(Item):

    def __init__(self, parent_screen):
        super(Apple, self).__init__(parent_screen)
        self.move()

    def draw(self):
        super().draw()

    def move(self):
        super(Apple, self).move()
        self.x += AppleModValue * self.getSize()
        # super().refactorItemLocation()
        self.foodIsCreated = True

    def getImagePath(self):
        return "resources/apple.jpg"
