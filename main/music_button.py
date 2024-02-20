import pygame
import button


class MusicButton:

    def __init__(self, x, y, img_active, img_passive, scale, color_active, color_passive):
        self.clicked = None
        self.x = x
        self.y = y
        self.img_active = pygame.transform.scale(img_active, (int(img_active.get_width() * scale), int(img_active.get_height() * scale)))
        self.img_active.set_colorkey((255,255,255))
        self.img_passive = pygame.transform.scale(img_passive, (int(img_passive.get_width() * scale), int(img_passive.get_height() * scale)))
        self.img_passive.set_colorkey((255,255,255))
        self.scale = scale
        self.color_active = color_active
        self.color_passive = color_passive
        self.active = True
        self.rect = self.img_passive.get_rect()
        self.rect.topleft = (x,y)

    def draw(self, screen):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.active = not self.active
                if self.active:
                    pygame.mixer.music.set_volume(0.03)
                else:
                    pygame.mixer.music.set_volume(0)
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.active:
            # pygame.draw.rect(screen, "red", self.rect, 3)
            screen.blit(self.img_active, (self.x, self.y))
        elif not self.active:
            # pygame.draw.rect(screen, "red", self.rect, 3)
            screen.blit(self.img_passive, (self.x, self.y))


