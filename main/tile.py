import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, screenSize, img, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.id = id
        self.rect = self.image.get_rect()
        if self.id == 13:
            self.rect.center = (x + 22, y + 10)
        else:
            self.rect.center = (x + 22, y + 22)
        self.x = x
        self.y = y
        self.H = screenSize[1]

    def draw(self):
        if self.id == 14:
            pygame.display.get_surface().blit(self.image, (self.x, self.y - 32))
        else:
            pygame.display.get_surface().blit(self.image, (self.x, self.y))

        # pygame.draw.rect(pygame.display.get_surface(), 'magenta', self.rect, 3)

    def get_rect(self):
        return self.rect

    def colliderect(self, collided):
        if pygame.sprite.collide_rect(self, collided):
            return True
        return False
