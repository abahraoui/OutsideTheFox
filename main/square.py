import pygame


class Square(pygame.sprite.Sprite):
    def __init__(self, col, x, y, screenSize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 20))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.H = screenSize[1]

    def update(self):
        self.rect.move_ip(0, 3)
        if self.rect.top > self.H:
            self.kill()

    def colliderect(self, collided):
        if pygame.sprite.collide_rect(self, collided):
            # self.kill()
            return True
        return False
