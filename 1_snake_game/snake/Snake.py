import pygame
from fundamental import GameFundamental

SIZE = GameFundamental.SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.imageHead = pygame.image.load("resources/snakeHead.png").convert()
        self.imageBody = pygame.image.load("resources/snakeBody.png").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]
        self.movedInThisDirection = True

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def movedInDirection(self):
        self.movedInThisDirection = True

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            # print("Yurumeye geldik : i  ",i,"x[i]",self.x[i],"y[i]",self.y[i])
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.movedInDirection()
        self.draw()

    def draw(self):
        for i in range(self.length):
            if i == 0:
                self.parent_screen.blit(self.imageHead, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.imageBody, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(+1)
        self.y.append(+1)

    def getLenght(self):
        return self.length
