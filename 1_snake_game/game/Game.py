import pygame
import time
from fundamental import GameFundamental
from pygame.locals import *

from item.Apple import Apple
from item.Peach import Peach
from item.Poison import Poison
from snake.Snake import \
    Snake  # TypeError: 'module' object is not callable  hatasini bu sekilde cozebildik internetten aratinca --> Module erisim sagliyor

BACKGROUND_COLOR = (110, 110, 5)

SIZE = GameFundamental.SIZE


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
        self.snakeConfused = False
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
            self.snakeConfused = False
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
                print(self.snake.x[0]," ",self.snake.y[0]," " ,self.snake.x[i]," ", self.snake.y[i])
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
        # print("temizlenecek posion sayisi ", len(self.poison))
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
                        #
                        # ("TIKANDIKKKK deger : ", self.movedInThisDirection)

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


class Score:
    totalScore = 0
    appleScore = 10
    peachScore = 150
    poisonScore = -100
