import pygame

import button

current_page_height = 0


def check_limit_y(limit, text_surface):
    global current_page_height
    if current_page_height >= limit:
        current_page_height = text_surface.get_height()
        return 1
    else:
        current_page_height += text_surface.get_height()
        return 0


def parse_text(text_to_parse, surface_to_append, font, limit, active_W):
    global current_page_height
    current_page_height = 0
    page = 1
    text_list = []
    test_text = ""
    text_surface = font.render(test_text, True, (255, 255, 255))
    for i in range(len(text_to_parse)):
        if text_to_parse[i] == "\n":
            page += check_limit_y(limit, text_surface)
            surface_to_append.append((text_surface, page))
            text_list.append(test_text)
            test_text = ""
            continue
        test_text += text_to_parse[i]
        text_surface = font.render(test_text, True, (255, 255, 255))
        if text_surface.get_width() >= active_W - 60:
            page += check_limit_y(limit, text_surface)
            surface_to_append.append((text_surface, page))
            text_list.append(test_text)
            test_text = ""
        if i == len(text_to_parse) - 1:
            page += check_limit_y(limit, text_surface)
            surface_to_append.append((text_surface, page))
            text_list.append(test_text)


class UserManual:

    def __init__(self, x, y, user_manual_text, level_text, hint_text):

        self.x = x
        self.y = y
        self.active = False
        self.user_manual_text = user_manual_text
        self.level_text = level_text
        self.hint_text = hint_text
        self.text = self.user_manual_text
        self.state = 'M'
        self.active_W = 400
        self.inactive_rect = pygame.Rect(self.x + 115, self.y + 15, 70, self.y + 70)
        self.active_rect = pygame.Rect(self.x - 250, 25, self.active_W, self.y + 600)
        self.rect = self.inactive_rect
        self.text_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        print(self.active_rect.y)
        limit = self.active_rect.bottom - 215
        self.manual_text_surface = []
        parse_text(self.user_manual_text, self.manual_text_surface, self.text_font, limit, self.active_W)
        self.level_text_surface = []
        parse_text(self.level_text, self.level_text_surface, self.text_font, limit, self.active_W)
        self.hint_text_surface = []
        parse_text(self.hint_text, self.hint_text_surface, self.text_font, limit, self.active_W)

        self.text_surface = self.manual_text_surface
        self.page = 1
        next_button_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("→", True, (255, 255, 255))
        self.nextPageButton = button.Button(self.active_rect.right - 45, self.active_rect.bottom - 45,
                                            next_button_surface, 1, "lightgreen", "blue")
        previous_button_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("←", True,
                                                                                              (255, 255, 255))
        self.previousPageButton = button.Button(self.active_rect.left + 15, self.active_rect.bottom - 45,
                                                previous_button_surface, 1, "lightgreen", "blue")

        self.tabs = ["Manual", "Level", "Hint"]
        self.tab_rects = [pygame.Rect(self.active_rect.left, self.active_rect.top, 135, self.active_rect.top + 25),
                          pygame.Rect(self.active_rect.left + 137, self.active_rect.top, 110,
                                      self.active_rect.top + 25),
                          pygame.Rect(self.active_rect.left + 247, self.active_rect.top, 110,
                                      self.active_rect.top + 25)]
        manual_button_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render("Manual", True,
                                                                                            (255, 255, 255))
        self.manualTabButton = button.Button(self.tab_rects[0].x,
                                             self.tab_rects[0].y + manual_button_surface.get_height() / 2,
                                             manual_button_surface, 1.5, "white", "white")

        level_button_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render("Level", True,
                                                                                           (255, 255, 255))
        self.levelTabButton = button.Button(self.tab_rects[1].x,
                                            self.tab_rects[1].y + level_button_surface.get_height() / 2,
                                            level_button_surface, 1.4, "white", "white")

        hint_button_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render("Hint", True,
                                                                                          (255, 255, 255))
        self.hintTabButton = button.Button(self.tab_rects[2].x,
                                           self.tab_rects[2].y + hint_button_surface.get_height() / 2,
                                           hint_button_surface, 1.6, "white", "white")

    def draw(self):
        screen = pygame.display.get_surface()

        if self.state == 'M':
            self.text_surface = self.manual_text_surface
        elif self.state == 'L':
            self.text_surface = self.level_text_surface
        elif self.state == 'H':
            self.text_surface = self.hint_text_surface

        if not self.active:
            self.rect = self.inactive_rect
            pygame.draw.circle(screen, "gold", (self.x + 150, self.y + 50), 35)
            text_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("?", True, (255, 255, 255))
            screen.blit(text_surface, (self.x + 136, self.y + 30))
            text_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Help", True, (0, 0, 128))
            screen.blit(text_surface, (self.x + 116, self.y + 85))
        else:
            if self.manualTabButton.draw(screen):
                self.change_state('M')
            if self.levelTabButton.draw(screen):
                self.change_state('L')
            if self.hintTabButton.draw(screen):
                self.change_state('H')

            text_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("X", True, "red")
            pygame.draw.rect(screen, "blue", self.active_rect, 0, 3)
            screen.blit(text_surface, (self.x + 118, self.y + 30))
            start_y = self.y + 80

            text_surfaces = [x for x in self.text_surface if x[1] == self.page]
            for i in range(len(text_surfaces)):
                current_surface = text_surfaces[i]
                screen.blit(current_surface[0], (self.active_rect.left + 30, start_y + 25 * (i + 1)))
                if current_surface == self.text_surface[-1]:
                    text_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render("End of file", True,
                                                                                               "crimson")
                    screen.blit(text_surface, (self.active_rect.left + self.active_W / 2 - text_surface.get_width() / 2,
                                               start_y + 25 * (i + 1) + 20
                                               ))

            if self.previousPageButton.draw(screen) and self.page > 1:
                self.page -= 1
            if self.nextPageButton.draw(screen) and len([x for x in self.text_surface if x[1] == self.page + 1]) > 0:
                self.page += 1

            page_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render(f"Page: {self.page}", True,
                                                                                       "white")

            screen.blit(page_surface, (
            self.active_rect.left + self.active_W / 2 - page_surface.get_width() / 2, self.active_rect.bottom - 25))

            for i in range(len(self.tabs)):

                tab_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render(self.tabs[i], True, "white")
                if self.tabs[i][0] == self.state:
                    pygame.draw.rect(screen, "magenta", self.tab_rects[i])
                screen.blit(tab_surface, (self.active_rect.left + 25 + 125 * i, self.active_rect.top + 15))
                pygame.draw.line(screen, "white",
                                 (self.active_rect.left + 45 + 125 * i + tab_surface.get_width(), self.active_rect.top),
                                 (self.active_rect.left + 45 + 125 * i + tab_surface.get_width(),
                                  self.active_rect.top + 50), 2)
            last = len(self.tabs) - 1
            tab_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render(self.tabs[last], True, "white")
            pygame.draw.line(screen, "white", (self.active_rect.left, self.active_rect.top + 50),
                             (self.active_rect.left + 45 + 125 *
                              last + tab_surface.get_width(), self.active_rect.top + 50), 5)

    def change_state(self, value):
        self.state = value
        self.page = 1

    def flip_active(self):
        self.active = not self.active

    def get_active(self):
        return self.active

    def mouse_colliding(self, pos):
        return self.rect.collidepoint(pos)
