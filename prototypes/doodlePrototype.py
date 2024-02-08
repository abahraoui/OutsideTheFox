import random
import sys

import pygame
from pygame.locals import *


# def pause():
#     while True:
#         events()
#         k = pygame.key.get_pressed()
#         if k[K_F1]: break


# Event handler
def events():
    global paused
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        # Start game handler
        elif event.type == KEYDOWN and event.key == K_F1:
            paused = False


def spawnHandler():
    global squares
    global spawnCounter
    spawnCounter += 1
    if spawnCounter % 100 == 0:
        squares.add(Square(random.choice(colors), random.randint(0, W), 0))


# display surface
W, H = 1280, 1024
HW, HH = W / 2, H / 2
AREA = W * 2

# pygame setup
pygame.init()
screen = pygame.display.set_mode((W, H))
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Serious Game")
FPS = 120

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)


class Player(pygame.sprite.Sprite):

    def __init__(self, velocity, maxJumpRange):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.maxJumpRange = maxJumpRange
        f = pygame.font.Font('freesansbold.ttf', 24)
        txt = f.render('Player', True, 'navy')
        self.text = txt
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()



    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.xVelocity = 0
        self.jumping = False
        self.jumpCounter = 0
        self.falling = True
        self.onPlatform = False
        txtRect = self.text.get_rect()
        txtRect.center = (self.x, self.y - 70)
        self.textRect = txtRect
        self.collider = None

    def keys(self):
        keys = pygame.key.get_pressed()

        if keys[K_q]:
            self.xVelocity = -self.velocity
        elif keys[K_d]:
            self.xVelocity = self.velocity
        else:
            self.xVelocity = 0

        if keys[K_SPACE] and not self.jumping and not self.falling:
            self.jumping = True
            self.jumpCounter = 0

    def move(self):
        #print(self.y)

        if 0 < self.x + self.xVelocity < W:
            self.x += self.xVelocity
        # check x boundaries

        if self.jumping:
            if self.onPlatform:
                self.onPlatform = False
            self.y -= self.velocity * 2
            self.jumpCounter += 1
            if self.jumpCounter == self.maxJumpRange:
                self.jumping = False
                self.falling = True
        elif self.falling:
            if self.y <= H - 10 and self.y + self.velocity >= H - 10:
                self.y = H - 10
                self.falling = False
            else:
                self.y += self.velocity * 2
        elif self.onPlatform:
            if pygame.sprite.collide_rect(self, self.collider):
                if self.y <= H - 10 and self.y + self.velocity >= H - 10:
                    self.onPlatform = False
                    self.falling = False
                else:
                 self.y += 3
            else:
                self.onPlatform = False
                self.falling = True
        self.textRect.center = (self.x, self.y - 70)
        self.rect.center = (self.x, self.y)

    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.circle(display, WHITE, (self.x, self.y - 25), 25, 0)
        pygame.display.get_surface().blit(self.text, self.textRect)

    def resetJump(self, collider):
        self.jumping = False
        self.falling = False
        self.onPlatform = True
        self.collider = collider

    def do(self):
        self.keys()
        self.move()
        self.draw()


class Square(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 20))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.move_ip(0, 3)
        if self.rect.top > H:
            self.kill()

    def colliderect(self, collided):
        if pygame.sprite.collide_rect(self, collided):
            #self.kill()
            return True
        return False


colors = ["crimson", "cyan", "navy", "violet"]
square = Square("crimson", 500, 300)
squares = pygame.sprite.Group()
squares.add(square)
P = Player(3, 50)
P.setLocation(HW, H - 100)

green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Press F1 to Start', True, green, blue)
textRect = text.get_rect()
textRect.center = (HW, HH)
paused = True
spawnCounter = 0
# Will pause the game until F1 is pressed


while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events()
    if not paused:
        P.do()
        squares.update()
        squares.draw(screen)
        #print(len(squares))
        spawnHandler()
        for square in squares:
            if square.colliderect(P):
                P.resetJump(square)
    else:
        screen.blit(text, textRect)

    pygame.display.update()
    clock.tick(FPS)
    screen.fill('purple')

