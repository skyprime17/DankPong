import pygame
import tkinter as tk
from tkinter import messagebox
import random
from time import sleep

WIDTH = 600
HEIGHT = 800
BORDER = 15
VELOCITY = 5
FPS = 120
LIVES = 3
FG_COLOUR = pygame.Color('white')
BG_COLOUR = pygame.Color('black')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DankPong")


def draw_screen(player):
        """Draws all the needed rectangles and a scoreboard."""
    screen.fill(BG_COLOUR)
    pygame.draw.rect(screen, FG_COLOUR, pygame.Rect((0, 0), (WIDTH, BORDER)))
    pygame.draw.rect(screen, FG_COLOUR, pygame.Rect(0, 0, BORDER, HEIGHT))
    pygame.draw.rect(screen, FG_COLOUR, pygame.Rect(WIDTH - BORDER, 0, BORDER, HEIGHT))
    font = pygame.font.SysFont("monospace", 32)
    scoretext = font.render("Score:{} Lives:{}".format(player.score, player.lives), 1, (128, 128, 128))
    screen.blit(scoretext, (WIDTH // 2 - 150, 20))


def loss_screen(subject, object):
        """Message box for the loss screen."""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.askyesno(subject, object)


class Player:
    def __init__(self, lives=3, score=0):
        self.lives = lives
        self.score = score

    def reset(self):
        self.lives, self.score = 3, 0


class Ball(Player):
    RADIUS = 15

    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        

    def show(self, colour=(128, 128, 128)):
        global screen
        pygame.draw.circle(screen, colour, (self.x, self.y), self.RADIUS)

    def update(self):
        global FG_COLOUR
        newx = self.x + self.vx
        newy = self.y + self.vy

        if newy < BORDER + self.RADIUS:
            self.vy = -self.vy
        elif newx < BORDER + self.RADIUS or newx > WIDTH - self.RADIUS:
            self.vx = -self.vx
        elif newy + Ball.RADIUS > HEIGHT - Paddle.HEIGHT and abs(newx - paddle.x) < Paddle.WIDTH // 2:
            self.vy = -self.vy
            if self.vy < HEIGHT:
                player.score += 1
        else:
            self.show(BG_COLOUR)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(FG_COLOUR)

    def check_pos(self):
        if self.y > HEIGHT + self.RADIUS or self.x > WIDTH:
            self.x, self.y = random.randint(self.RADIUS, WIDTH), random.randint(self.RADIUS, HEIGHT)
            player.lives -= 1
            self.update()


class Paddle:
    WIDTH = 150
    HEIGHT = 20

    def __init__(self, x):
        self.x = x

    def show(self, colour):
        global screen
        pygame.draw.rect(screen, colour,
                         pygame.Rect((self.x - self.WIDTH // 2, HEIGHT - self.HEIGHT), (self.WIDTH, self.HEIGHT)))

    def update(self):
        self.show(pygame.Color("black"))
        self.x = pygame.mouse.get_pos()[0]
        self.show(pygame.Color("white"))


def main():
    global paddle, ball, player
    pygame.init()
    clock = pygame.time.Clock()
    screen.fill(BG_COLOUR)

    player = Player()
    ball = Ball(random.randint(BORDER + Ball.RADIUS, WIDTH - BORDER - Ball.RADIUS),
                random.randint(BORDER + Ball.RADIUS, HEIGHT - Ball.RADIUS), -VELOCITY, VELOCITY)

    draw_screen(player)
    paddle = Paddle(HEIGHT // 2)
    paddle.show(FG_COLOUR)
    pygame.mouse.set_visible(False)
    running = True

    while running:
        draw_screen(player)
        if pygame.event.poll().type == pygame.QUIT:
            break

        paddle.update()
        ball.update()
        ball.check_pos()

        if player.lives == 0:
            loss_screen("You lost!", "Score:" + str(player.score) + "\n" "Play again?")
            if messagebox.askyesno():
                player.reset()
            else:
                running = False

        clock.tick(FPS)
        pygame.display.flip()


main()
