# Add background image and music

import pygame
from pygame.locals import *
import time
import random


SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = (int(random.randint(1, 7) * 3) + 0) * SIZE
        self.y = (int(random.randint(1, 19) / 2)) * SIZE


class Peach:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/peach.jpg").convert()
        self.foodIsCreated = False

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = (int(random.randint(1, 7) * 3) + 1) * SIZE
        self.y = (int(random.randint(1, 19) / 2)) * SIZE
        self.foodIsCreated = True


class Poison:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/poison.jpg").convert()
        self.foodIsCreated = False

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = (int(random.randint(1, 7) * 3) + 2) * SIZE
        self.y = (int(random.randint(1, 19) / 2)) * SIZE
        self.foodIsCreated = True


class Score:
    totalScore = 0
    appleScore = 10
    peachScore = 150
    poisonScore = -22


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
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
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game_ Ahmet Emin SAGLIK/ Emirhan Dogandemir")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.peach = Peach(self.surface)
        self.poison = [Poison(self.surface)]
        self.score = Score()
        self.snakeConfused = False

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)
        # pygame.mixer.music.stop()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.peach = Peach(self.surface)
        self.poison = [Poison(self.surface)]
        self.snakeConfused=False
        self.score.totalScore = 0

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()

        if self.peach.foodIsCreated == True:
            self.peach.draw()

        if self.snake.length % 3 == 0:
            if self.peach.foodIsCreated == False:
                self.peach.move()
            self.peach.draw()

        for i in range(len(self.poison)):
            # print("For a girdik : ")
            if self.poison[i].foodIsCreated == True:
                self.poison[i].draw()
                # print("Olusturulan poison  [", i, "] x : ", self.poison[i].x, " y : ", self.poison[i].y)
                # time.sleep(len(self.poison) / 4)

        if self.snake.length % 2 == 0:
            poisonNumber = int(self.snake.length / 2)
            # print("Poison Number : ", poisonNumber)
            if len(self.poison) < poisonNumber:
                self.poison.append(Poison(self.surface))

        for i in range(len(self.poison)):
            # print("For a girdik : ")
            if self.poison[i].foodIsCreated == False:
                self.poison[i].move()
                self.poison[i].draw()
                # print("Olusturulan poison  [", i, "] x : ", self.poison[i].x, " y : ", self.poison[i].y)

                # time.sleep(len(self.poison) / 4)

        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        # for i in range(self.snake.length):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.score.totalScore += self.score.appleScore
            self.clearAllPoison()
            self.peach.move()
            self.peach.foodIsCreated = False


            self.apple.move()

        if self.peach.foodIsCreated == True and self.is_collision(self.snake.x[0], self.snake.y[0], self.peach.x,
                                                                  self.peach.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.score.totalScore += self.score.peachScore;
            # self.peach.move()
            self.snakeConfused=False
            self.peach.foodIsCreated = False

        for i in range(len(self.poison)):
            if self.poison[i].foodIsCreated == True and self.is_collision(self.snake.x[0], self.snake.y[0],
                                                                          self.poison[i].x,
                                                                          self.poison[i].y):
                self.play_sound("crash")
                self.score.totalScore += self.score.poisonScore
                self.snakeConfused = True

            if (self.score.totalScore < 0):
                raise "Lost Too much Score"

        # snake colliding with itself
        for i in range(3, self.snake.length):
            # print("x:  ", self.snake.x[i], " y:  ", self.snake.y[i])
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {(self.score.totalScore)}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.score.totalScore}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def clearAllPoison(self):
        print("temizlenecek posion sayisi ", len(self.poison))
        # time.sleep(1)
        for i in range(len(self.poison)):
            self.poison[i].foodIsCreated = False

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if self.snake.movedInThisDirection == True:

                            if event.key == K_LEFT:
                                if not self.snakeConfused:
                                    self.snake.move_left()

                                else:
                                    self.snake.move_right()

                                self.snake.movedInThisDirection = False

                            if event.key == K_RIGHT:
                                if not self.snakeConfused:
                                    self.snake.move_right()
                                else:
                                    self.snake.move_left()

                                self.snake.movedInThisDirection = False

                            if event.key == K_UP:
                                if not self.snakeConfused:
                                    self.snake.move_up()
                                else:
                                    self.snake.move_down()

                                self.snake.movedInThisDirection = False

                            if event.key == K_DOWN:
                                if not self.snakeConfused:
                                    self.snake.move_down()
                                else:
                                    self.snake.move_up()
                                self.snake.movedInThisDirection = False

                        # else:
                        # print("TIKANDIKKKK deger : ", self.movedInThisDirection)

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)


if __name__ == '__main__':
    game = Game()
    game.run()
