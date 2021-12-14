from abc import ABC, abstractmethod
import pygame
import random
from snake.Snake import Snake
from fundamental.GameFundamental import SIZE


class Item(Snake):

    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = ""
        self.foodIsCreated = False
        self.setImage(self.getImagePath())
        self.snake =Snake

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = int(random.randint(1, 7) * 3) * SIZE  # (int(random.randint(1, 7) * 3) + 2) * SIZE
        self.y = (int(random.randint(1, 19) / 2)) * SIZE


    def setImage(self, imagePath):
        self.image = pygame.image.load(imagePath).convert()

    @abstractmethod
    def getImagePath(self):
        pass

    # def refactorItemLocation(self):
    #     self.snake= Snake
    #     snakeLength=Snake.Length
    #     print("Yilanin uzunlugu : ", snakeLength)
    #     for i in range(snakeLength):
    #         print("Snake x : ", self.snake.x[i], "y ", self.snake.y[i], " ", self.__class__, " x :", self.x,
    #               " y : ", self.y)
    #         if self.snake.x[i] == self.x and self.snake.y[i] != self.y:
    #             print("REFACTOR EDILIYOR  --> Ust uste bindi :", self.x, " ", self.y)
    #             self.y += 1
    #             self.refactorItemLocation()
    #             print("Fonk Bitecek")
    #             return

    def getSize(self):
        return SIZE
