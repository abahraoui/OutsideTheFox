import decimal
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, screenSize, img, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.id = id
        self.rect = self.image.get_rect()
        self.rect.center = (x + 22, y + 22)
        self.x = x
        self.y = y
        self.H = screenSize[1]

    def draw(self):
        if self.id == 14:
            pygame.display.get_surface().blit(self.image, (self.x, self.y - 32))
            pygame.draw.rect(pygame.display.get_surface(), 'BLUE', self.rect, 3)
        else:
            pygame.display.get_surface().blit(self.image, (self.x, self.y))

        # pygame.draw.rect(pygame.display.get_surface(), 'magenta', self.rect, 3)

    def get_rect(self):
        return self.rect

    def collide_rect(self, collided):
        x, y = collided.get_location()

        if pygame.sprite.collide_rect(self, collided) and self.id != 9:
            return True

        elif (decimal.Decimal(str(x)).as_tuple().exponent == - 1 or isinstance(x, int)) and self.id == 9 and \
                20 < x - self.x <= 22.5 and (self.y < y or y >= self.y - 45):
            print(y, self.y - 45)
            return True
        else:
            return False
