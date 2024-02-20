import sys

import pygame.display
import button
import usermanual


def make_button(text, W, H, offset):
    button_surface = pygame.font.Font('assets/joystix monospace.otf', 48).render(text, True,
                                                                                 "green")
    rect = button_surface.get_rect()
    rect.width *= 2
    rect.height *= 2

    return button.Button(W / 2 - button_surface.get_width(),
                         H / 2 - button_surface.get_height() + offset, button_surface, 1,
                         "lightgreen", "empty", rect)


class StartScreen:

    def __init__(self, lastUpdate, playerRunCycle, text_surface, textRect, screenSize, help_text, end_text):
        self.W = screenSize[0]
        self.H = screenSize[1]
        self.lastUpdate = lastUpdate
        self.playerRunCycle = playerRunCycle
        self.playerAnim = next(self.playerRunCycle)
        self.text_surface = text_surface
        self.textRect = textRect
        self.screen = pygame.display.get_surface()
        self.menu_rect = pygame.Rect(300, self.H / 2 - self.text_surface.get_height() / 2 - 148, self.W - 600,
                                     self.H - 200)
        self.state = 'M'
        self.paused = True
        self.text_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        self.help_surface = []
        self.end_level_text = []

        limit = self.menu_rect.bottom - 200
        usermanual.parse_text(help_text, self.help_surface, self.text_font, limit, self.menu_rect.width)
        usermanual.parse_text(end_text, self.end_level_text, self.text_font, limit, self.menu_rect.width)

        self.play_button = make_button("Play", self.W, self.H, -200)
        self.help_button = make_button("Help", self.W, self.H, 100)
        self.new_button = make_button("New ", self.W, self.H, -50)
        self.quit_button = make_button("Quit", self.W, self.H, 250)
        self.back_button = make_button("Back", self.W, self.H, 290)
        self.continue_button = make_button("Continue", self.W, self.H, 290)

        self.can_play = False
        self.can_help = False
        self.can_new = False
        self.can_quit = False
        self.can_back = False
        self.can_continue = False
        self.page = 1

    def start_screen_on(self, current_time):
        if self.state == 'M':
            if current_time > self.lastUpdate + 100:
                self.playerAnim = next(self.playerRunCycle)
                self.lastUpdate = current_time
            self.screen.blit(self.playerAnim, (
                self.W / 2 - self.playerAnim.get_width() / 2,
                self.H / 2 - self.playerAnim.get_height() / 2 - 400 + 110))
            # self.screen.blit(self.text_surface, (
            #     self.W / 2 - self.text_surface.get_width() / 2, self.H / 2 - self.text_surface.get_height() / 2 - 300))

            # pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)
            if self.play_button.draw(self.screen):
                self.can_play = True
            if self.can_play and self.play_button.is_finished():
                self.can_play = False
                self.paused = False

            if self.help_button.draw(self.screen):
                self.can_help = True
            if self.can_help and self.help_button.is_finished():
                self.state = 'H'
                self.can_help = False

            if self.new_button.draw(self.screen):
                self.can_new = True
            if self.can_new and self.new_button.is_finished():
                self.can_new = False

            if self.quit_button.draw(self.screen):
                self.can_quit = True
            if self.can_quit and self.quit_button.is_finished():
                self.can_quit = False
                pygame.quit()
                sys.exit()

        if self.state == 'H':
            pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)
            if self.back_button.draw(self.screen):
                self.can_back = True
            if self.can_back and self.back_button.is_finished():
                self.can_back = False
                self.state = 'M'

            start_y = self.menu_rect.top + 10

            text_surfaces = [x for x in self.help_surface if x[1] == self.page]
            for i in range(len(text_surfaces)):
                current_surface = text_surfaces[i]
                self.screen.blit(current_surface[0], (self.menu_rect.left + 30, start_y + 25 * (i + 1)))
                if current_surface == self.help_surface[-1]:
                    text_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render("End of file", True,
                                                                                               "crimson")
                    self.screen.blit(text_surface,
                                     (self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                      start_y + 25 * (i + 1) + 20
                                      ))

        if self.state == 'E':
            pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)
            if self.continue_button.draw(self.screen):
                self.can_continue = True
            if self.can_continue and self.continue_button.is_finished():
                self.can_continue = False
                self.paused = False

            start_y = self.menu_rect.top + 10

            text_surfaces = [x for x in self.end_level_text if x[1] == self.page]
            for i in range(len(text_surfaces)):
                current_surface = text_surfaces[i]
                self.screen.blit(current_surface[0], (self.menu_rect.left + 30, start_y + 25 * (i + 1)))
                if current_surface == self.end_level_text[-1]:
                    text_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render("End of file", True,
                                                                                               "crimson")
                    self.screen.blit(text_surface,
                                     (self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                      start_y + 25 * (i + 1) + 20
                                      ))


    def get_paused(self):
        return self.paused

    def set_paused(self):
        self.paused = True

    def set_state(self, state):
        self.state = state
