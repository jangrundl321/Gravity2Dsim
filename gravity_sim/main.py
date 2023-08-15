import itertools
import math
import random
import pygame
from sys import exit

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

BACKGROUND = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
BACKGROUND.fill("Black")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(500, 500))

G = 0.5


class Body(pygame.sprite.Sprite):

    def __init__(self, mass, radius, start_pos, color, xv, yv):
        super().__init__()

        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill("Black")
        self.rect = self.image.get_rect(center=start_pos)
        pygame.draw.circle(self.image, color, (radius, radius), radius, 0)

        self.color = color

        self.mass = mass
        self.radius = radius
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.xv = xv
        self.yv = yv
        self.xa = 0
        self.ya = 0

    def animate(self):
        self.xv += self.xa
        self.yv += self.ya

        self.x += self.xv
        self.y += self.yv

        self.rect.center = (round(self.x), round(self.y))

    def gravitate(self, otherbody):
        dx = abs(self.x - otherbody.x)
        dy = abs(self.y - otherbody.y)

        r = math.sqrt(dx ** 2 + dy ** 2)
        a = G * otherbody.mass / r ** 2
        theta = math.asin(dy / r)

        if dx < self.radius * 2 and dy < self.radius * 2:
            pass
        else:
            try:
                if self.y > otherbody.y:
                    self.ya = -math.sin(theta) * a
                else:
                    self.ya = math.sin(theta) * a

                if self.x > otherbody.x:
                    self.xa = -math.sin(theta) * a
                else:
                    self.xa = math.sin(theta) * a
            except ZeroDivisionError:
                print("Zero Division Error")


body_group = pygame.sprite.Group()
BODY_COUNT = 20
for i in range(BODY_COUNT):
    body_group.add((Body(1, 3, (random.randrange(200, 800), random.randrange(200, 800)), "White",
                         random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2))))

body_group.add((Body(30, 4, (500, 500), "Yellow", 0, 0)))

body_group_list = list(body_group)
body_pairs = list(itertools.combinations(body_group_list, 2))

while True:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()
            exit()

    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)

    body_group.draw(SCREEN)

    for body, otherbody in body_pairs:
        body.gravitate(otherbody)
        otherbody.gravitate(body)
        body.animate()
        otherbody.animate()

    pygame.display.update()
    CLOCK.tick(60)

    # BACKGROUND.fill("Black")
