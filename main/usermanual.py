
import pygame


class UserManual:

    def __init__(self, x, y, user_manual_text, level_text):
        self.x = x
        self.y = y
        self.active = False
        self.user_manual_text = user_manual_text
        self.level_text = level_text
        self.text = self.user_manual_text
        self.state = 'M'
        self.active_W = 200
        self.inactive_rect = pygame.Rect(self.x + 215, self.y + 15, 70, self.y + 70)
        self.active_rect = pygame.Rect(self.x + 50, 25, self.active_W, self.y + 600)
        self.rect = self.inactive_rect
        self.font = pygame.font.Font('assets/joystix monospace.otf', 16)

        text_list = []
        test_text = ""
        self.text_surfaces = []
        text_surface = self.font.render(test_text, True, (255, 255, 255))
        for i in range(len(self.user_manual_text)):
            if self.user_manual_text[i] == "\n":
                self.text_surfaces.append(text_surface)
                text_list.append(test_text)
                test_text = ""
                continue
            test_text += self.user_manual_text[i]
            text_surface = self.font.render(test_text, True, (255, 255, 255))
            if text_surface.get_width() >= self.active_W - 24:
                self.text_surfaces.append(text_surface)
                text_list.append(test_text)
                test_text = ""
            if i == len(self.user_manual_text) - 1:
                self.text_surfaces.append(text_surface)
                text_list.append(test_text)

    def draw(self):
        screen = pygame.display.get_surface()

        if not self.active:
            self.rect = self.inactive_rect
            pygame.draw.circle(screen, "gold", (self.x + 250, self.y + 50), 35)
            text_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("?", True, (255, 255, 255))
            screen.blit(text_surface, (self.x + 236, self.y + 30))
        else:
            # self.rect = self.inactive_rect
            text_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("X", True, "red")
            pygame.draw.rect(screen, "blue", self.active_rect)
            screen.blit(text_surface, (self.x + 218, self.y + 30))
            start_y = self.y + 80
            for i in range(len(self.text_surfaces)):
                screen.blit(self.text_surfaces[i], (self.x + 60, start_y + 15 * (i + 1)))








    def flip_active(self):
        self.active = not self.active

    def get_active(self):
        return self.active

    def mouse_colliding(self, pos):
        return self.rect.collidepoint(pos)
