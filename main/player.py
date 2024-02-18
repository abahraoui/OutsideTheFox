import math

import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):

    def __init__(self, velocity, maxJumpRange, animationList, screenSize, tileSize):
        pygame.sprite.Sprite.__init__(self)

        self.W = screenSize[0]
        self.H = screenSize[1]
        self.velocity = velocity
        self.maxJumpRange = maxJumpRange
        self.animationList = animationList
        self.direction = 'R'
        self.currentAnim = 0
        self.animationCooldown = 100
        self.lastUpdate = pygame.time.get_ticks()
        self.action = 0
        self.moving = False
        self.blockedRight = False
        self.blockedLeft = False
        f = pygame.font.Font('freesansbold.ttf', 24)
        txt = f.render('Player', True, 'navy')
        self.text = txt
        self.image = pygame.Surface((tileSize + 3, 64))
        self.normal_rect = self.image.get_rect()
        self.crouching_rect = pygame.Rect(0, 0, self.normal_rect.width, 32)
        self.rect = self.normal_rect
        self.colliding = False
        self.runningSound = pygame.mixer.Sound(
            "assets/audio/sounds/419181__14gpanskahonc_petr__14-man-fast-walking-dirt.wav")
        self.collider = {}
        self.tileSize = tileSize
        self.goalX = 0
        self.goalY = 0
        self.lerping = False
        self.reachedRightBoundary = False
        self.hurt = True
        self.hurtLastCooldown = pygame.time.get_ticks()
        self.finished = False
        self.crouching = False
        self.finishedCrouching = True

    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.xVelocity = 0
        self.jumping = False
        self.jumpCounter = 0
        self.falling = True
        self.freeJump = False
        txtRect = self.text.get_rect()
        txtRect.center = (self.x, self.y - 70)
        self.textRect = txtRect

    def jumpSound(self):
        jump_sound = pygame.mixer.Sound("assets/audio/sounds/350905__cabled_mess__jump_c_05.wav")
        jump_sound.play()
        jump_sound.set_volume(1)
        # pygame.mixer.music.stop()

    def playRunSound(self):
        if self.runningSound.get_num_channels() == 0 and not self.falling:
            self.runningSound.play()
            self.runningSound.set_volume(1)

    def stopRunSound(self):
        self.runningSound.stop()

    def flipAnim(self, direction):
        if self.direction != direction:
            self.direction = direction

    def notMoving(self):
        self.moving = False

    def keys(self):
        keys = pygame.key.get_pressed()

        if keys[K_q]:
            if not self.blockedLeft:
                self.xVelocity = -self.velocity
            self.moving = True
            self.flipAnim('L')
            if self.action == 1:
                self.playRunSound()
        elif keys[K_d]:
            if not self.blockedRight:
                self.xVelocity = self.velocity
            self.moving = True
            self.flipAnim('R')
            if self.action == 1:
                self.playRunSound()
        else:
            self.xVelocity = 0
            # self.notMoving()
            # self.stopRunSound()
        if keys[K_SPACE] and not self.jumping and not self.falling:
            self.jumpSound()
            self.jumping = True
            self.freeJump = True
            self.jumpCounter = 0

    def move(self):
        if 149 < self.x + self.xVelocity:
            self.x += self.xVelocity
        # check x boundaries

        if self.jumping and self.freeJump:
            self.y -= self.velocity * 2
            self.jumpCounter += 1
            if self.jumpCounter == self.maxJumpRange:
                self.jumping = False
                self.falling = True
                self.freeJump = False
        elif self.jumping and not self.freeJump:
            if not self.lerping:
                self.jumping = False
                self.falling = True
        elif self.falling:
            self.y += self.velocity / 5

        self.textRect.center = (self.x, self.y - 70)
        self.rect.center = (self.x, self.y)

    def draw(self):

        if self.crouching:
            self.rect = self.crouching_rect
        else:
            self.rect = self.normal_rect
        display = pygame.display.get_surface()
        # pygame.display.get_surface().blit(self.text, self.textRect)
        current_time = pygame.time.get_ticks()
        if current_time - self.lastUpdate >= self.animationCooldown:
            self.currentAnim += 1
            self.lastUpdate = current_time
            if self.currentAnim >= len(self.animationList[self.action]):
                self.currentAnim = 0
        if self.direction == 'R':
            animation = self.animationList[self.action][self.currentAnim]
        else:
            animation = pygame.transform.flip(self.animationList[self.action][self.currentAnim], True, False)
            animation.set_colorkey((0, 0, 0))
        if self.crouching:
            display.blit(animation, (self.x - 48, self.y - 56))
        else:
            display.blit(animation, (self.x - 48, self.y - 48))
        pygame.draw.rect(pygame.display.get_surface(), 'red', self.rect, 3)  # Debug Player's hit box.
        pygame.draw.rect(pygame.display.get_surface(), 'purple',
                         pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 3)
        if (
                self.lerping or self.moving) and not self.crouching and not self.jumping and not self.falling and self.action != 1:
            self.action = 1
            self.animationCooldown = 100
            self.currentAnim = 0
        elif not (
                self.lerping or self.moving) and not self.crouching and not self.jumping and not self.falling and self.action != 0 and not self.hurt:
            self.action = 0
            self.animationCooldown = 250
            self.currentAnim = 0
        elif self.crouching and not self.jumping and not self.falling and self.action != 4:
            self.action = 4
            self.animationCooldown = 250
            self.currentAnim = 0
        elif self.jumping and self.action != 2:
            self.action = 2
            self.animationCooldown = 250
            self.currentAnim = 0
        elif self.falling and self.action != 2:
            self.action = 2
            self.animationCooldown = 250
            self.currentAnim = 0
        # elif self.hurt and self.action != 3:
        #     self.action = 3
        #     self.currentAnim = 0
        #     self.animationCooldown = 250

        if self.hurt and pygame.time.get_ticks() > self.hurtLastCooldown + 500:
            self.hurt = False
        # print(self.action.__str__() + ' : ' + self.currentAnim.__str__()) #Debug anim

    def is_colliding(self, collider, tile):
        if tile not in self.collider:
            self.collider[tile] = collider
            self.process_collider()

    def not_colliding(self, tile):
        if tile in self.collider:
            self.collider.pop(tile)

    def process_collider(self):
        right = False
        left = False
        above = False
        below = False
        y = self.rect.y
        x = self.rect.x
        width = self.rect.width
        height = self.rect.height
        for coll in self.collider:
            coll_x = self.collider[coll][0]
            coll_y = self.collider[coll][1]
            pygame.draw.rect(pygame.display.get_surface(), "lightblue",
                             pygame.Rect(coll_x, coll_y, self.tileSize, self.tileSize), 3)

            if coll_y > y and (coll_x <= x + width / 2 <= coll_x + self.tileSize):
                below = True
            if coll_y < y and (coll_x <= x + width / 2 <= coll_x + self.tileSize):
                above = True
            if coll_x > x and (y < coll_y < y + height - 1 or y < coll_y + self.tileSize < y + height):
                # print(y, coll_y - self.tileSize, y + height - 1)
                # print(y < coll_y - self.tileSize < y + height)
                right = True
                self.xVelocity = 0
            if coll_x < x and (y < coll_y < y + height - 1 or y < coll_y + self.tileSize < y + height):
                left = True
                self.xVelocity = 0
        if below:
            self.falling = False
        else:
            self.falling = True
        if above and self.jumping:
            self.lerping = False
            self.y = math.floor(self.y)
        if right:
            self.blockedRight = True
        else:
            self.blockedRight = False
        if left:
            self.blockedLeft = True
        else:
            self.blockedLeft = False

        return right

    def checkRightX(self):
        check_boundary = self.x + self.tileSize
        if check_boundary < self.W - 149:
            return True
        else:
            return False

    def checkLeftX(self):
        check_boundary = self.x - self.tileSize
        if check_boundary > 149:
            return True
        else:
            return False

    def moveRight(self):
        if self.x + self.tileSize > (self.W - 150):
            self.reachedRightBoundary = True
        if not self.lerping and not self.get_blocked_right():
            self.moving = True
            self.flipAnim('R')
            self.goalX = self.x + self.tileSize / 2  # 22.5
            if self.reachedRightBoundary:
                self.goalX -= 850
            self.lerping = True
            self.playRunSound()
        elif self.get_blocked_right():
            self.hurt = True
            self.hurtLastCooldown = pygame.time.get_ticks()

    def moveLeft(self, scroll):
        if scroll == 0:
            distance = self.tileSize
        else:
            distance = self.tileSize / 2

        if not self.lerping and self.checkLeftX() and not self.get_blocked_left():
            self.moving = True
            self.flipAnim('L')
            self.goalX = self.x - distance  # 22.5
            self.lerping = True
            self.playRunSound()
        elif self.get_blocked_left():
            self.hurt = True
            self.hurtLastCooldown = pygame.time.get_ticks()

    def jump(self):
        # TODO restrict jump when crouching if under something.
        # if not self.lerping and not self.jumping:
        self.jumping = True
        if self.crouching:
            self.crouching = False
        self.goalY = self.y - 1.5 * self.tileSize
        self.lerping = True
        self.jumpSound()

    def crouch(self):
        if not self.crouching:
            self.crouching = True
            self.finishedCrouching = False
            self.falling = True

    def reset_right_boundary(self):
        if self.reachedRightBoundary:
            self.reachedRightBoundary = False

    def do(self):

        self.keys()
        self.move()
        self.process_collider()
        self.draw()
        if self.y > self.H or self.finished:
            return True

        if self.crouching and not self.falling:
            self.finishedCrouching = True

        if self.lerping and not self.reachedRightBoundary:
            if self.jumping:
                self.y = pygame.math.lerp(self.y, self.goalY, 0.05)
                if math.floor(self.y) == math.floor(self.goalY):
                    self.y = self.goalY
                    self.lerping = False

            if self.moving:
                self.x = pygame.math.lerp(self.x, self.goalX, 0.05)
                if math.ceil(self.x) == math.ceil(self.goalX) or math.floor(self.x) == math.floor(self.goalX):
                    self.x = self.goalX
                    self.lerping = False
                    self.notMoving()
                    # self.stopRunSound()

        return False

    def set_finished(self):
        self.finished = True

    def get_reach_right_boundary(self):
        return self.reachedRightBoundary

    def get_direction(self):
        return self.direction

    def get_moving(self):
        return self.moving

    def get_lerping(self):
        return self.lerping

    def get_location(self):
        return self.x, self.y

    def get_rect(self):
        return self.rect

    def get_blocked_right(self):
        return self.blockedRight

    def get_blocked_left(self):
        return self.blockedLeft

    def stop_scroll(self):
        if self.blockedLeft:
            return "L"
        if self.blockedRight:
            return "R"
        else:
            return "O"

    def last_collider(self):
        if self.collider:
            return sorted(self.collider.keys())[-1], len(self.collider)

    def blocked_left_right(self):
        return self.blockedLeft, self.blockedRight
