import pygame


# button class
class Button():
    def __init__(self, x, y, image, scale):
        W = image.get_width()
        H = image.get_height()
        self.img = pygame.transform.scale(image, (int(W * scale), int(H * scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.color_active = "lightgreen"
        self.color_passive = "blue"
        self.color = self.color_passive
        self.time_at_pressed = pygame.time.get_ticks()

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if action:
            self.color = self.color_active
            self.time_at_pressed = pygame.time.get_ticks()
        if self.time_at_pressed + 300 <= pygame.time.get_ticks():
            self.color = self.color_passive
        # draw button
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.img, (self.rect.x, self.rect.y))

        return action
