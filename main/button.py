import pygame


# button class
class Button():
    def __init__(self, x, y, image, scale, color_active, color_passive, rect=None):
        if image is not None:
            W = image.get_width()
            H = image.get_height()
            self.img = pygame.transform.scale(image, (int(W * scale), int(H * scale)))
        else:
            self.img = None
        if rect is None:
            self.rect = self.img.get_rect()
        else:
            self.rect = rect
        self.rect.topleft = (x, y)
        self.clicked = False
        self.color_active = color_active  # "lightgreen"
        self.color_passive = color_passive  # "blue"
        self.color = self.color_passive
        self.time_at_pressed = pygame.time.get_ticks()
        self.colliding = False

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            # pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            self.colliding = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True
        if not self.rect.collidepoint(pos) and self.colliding:
            self.colliding = False
            # pygame.mouse.set_cursor(*pygame.cursors.arrow)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if action:
            self.color = self.color_active
            self.time_at_pressed = pygame.time.get_ticks()
        if self.time_at_pressed + 300 <= pygame.time.get_ticks():
            self.color = self.color_passive
        if self.color_passive == "empty" and self.color == self.color_passive:
            pygame.draw.rect(screen, (0, 0, 128), self.rect, 0, 3)
            if self.img is not None:
                screen.blit(self.img, (self.rect.x + self.img.get_width() / 2, self.rect.y + self.img.get_height() / 2))
        elif self.color_passive == "empty" and not self.color == self.color_passive:
            pygame.draw.rect(screen, self.color, self.rect, 3, 3)
            if self.img is not None:
                screen.blit(self.img, (self.rect.x + self.img.get_width() / 2, self.rect.y + self.img.get_height() / 2))
        else:
            pygame.draw.rect(screen, self.color, self.rect, 0, 3)
            if self.img is not None:
                screen.blit(self.img, (self.rect.x, self.rect.y))

        return action

    def is_finished(self):
        return self.color == self.color_passive
