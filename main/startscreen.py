import math
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

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

class StartScreen:

    def __init__(self, lastUpdate, playerRunCycle, text_surface, textRect, screenSize, help_text, end_text):
        self.W = screenSize[0]
        self.H = screenSize[1]
        self.lastUpdate = lastUpdate
        self.playerRunCycle = playerRunCycle
        self.playerAnim = next(self.playerRunCycle)
        self.player_anim_offset = 110
        self.text_surface = text_surface
        self.textRect = textRect
        self.title = "Outside The"
        self.title_font = pygame.font.Font('assets/joystix monospace.otf', 56)
        self.title_surface = self.title_font.render(self.title, True, "navy")
        self.title_surface.set_alpha(210)
        self.sub_title = "A programming game!"
        self.sub_title_font = pygame.font.Font('assets/joystix monospace.otf', 32)
        self.sub_title_surface = self.sub_title_font.render(self.sub_title, True, "navy")
        self.sub_title_surface = pygame.transform.rotate(self.sub_title_surface, 270)
        self.flip_anim = False
        self.flip_anim_timer = pygame.time.get_ticks() - 1000

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
        self.levels_button = make_button("Pick", self.W, self.H, -50)
        self.quit_button = make_button("Quit", self.W, self.H, 250)
        self.back_button = make_button("Back", self.W, self.H, 290)
        self.continue_button = make_button("Continue", self.W, self.H, 290)

        self.can_play = False
        self.can_help = False
        self.can_level = False
        self.can_quit = False
        self.can_back = False
        self.can_continue = False
        self.page = 1
        self.anim_angle = 0
        self.level_wanted = 0
        self.level_page = 1
        self.max_level = 0
        self.started = False

        next_button_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("→", True, (255, 255, 255))
        self.nextPageButton = button.Button(self.menu_rect.right - 45, self.menu_rect.bottom - 45,
                                            next_button_surface, 1, "lightgreen", "blue")
        previous_button_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("←", True,
                                                                                              (255, 255, 255))
        self.previousPageButton = button.Button(self.menu_rect.left + 15, self.menu_rect.bottom - 45,
                                                previous_button_surface, 1, "lightgreen", "blue")

    def animation(self, current_time):
        if current_time > self.lastUpdate + 100:
            self.playerAnim = next(self.playerRunCycle)
            self.lastUpdate = current_time
            if self.lastUpdate > self.flip_anim_timer + 3000:
                self.flip_anim = True
            if self.flip_anim:
                self.anim_angle += 10
                if self.anim_angle % 360 < 180:
                    self.player_anim_offset -= 2.5
                else:
                    self.player_anim_offset += 2.5
                if self.anim_angle % 360 == 0:
                    self.flip_anim = False
                    self.title_surface.set_alpha(self.title_surface.get_alpha() + 10)
                    self.flip_anim_timer = pygame.time.get_ticks()

            self.playerAnim = pygame.transform.rotate(self.playerAnim, self.anim_angle)
            self.playerAnim = pygame.transform.flip(self.playerAnim, True, False)
            self.playerAnim.set_colorkey("black")
        if pygame.time.get_ticks() % 100 == 0:
            self.sub_title_surface = pygame.transform.flip(self.sub_title_surface, True, True)

    def start_screen_on(self, current_time):
        if self.state == 'M':
            self.animation(current_time)
            # opposite_title_surface = pygame.transform.flip(self.title_surface, True, False)
            opposite_sub_title_surface = pygame.transform.flip(self.sub_title_surface, True, True)
            self.screen.blit(self.playerAnim, (
                self.W / 2 - self.playerAnim.get_width() / 2,
                self.H / 2 - self.playerAnim.get_height() / 2 - 400 + self.player_anim_offset))
            # self.screen.blit(opposite_title_surface, (self.W / 2 + opposite_title_surface.get_width() - 470, self.H / 2 - self.title_surface.get_height() - 270))
            self.screen.blit(self.title_surface, (
                self.W / 2 - self.title_surface.get_width() - 45, self.H / 2 - self.title_surface.get_height() - 270))
            self.screen.blit(opposite_sub_title_surface, (self.W / 2 - opposite_sub_title_surface.get_width() / 2 - 180,
                                                          self.H / 2 - self.sub_title_surface.get_height() + 270))
            self.screen.blit(self.sub_title_surface, (self.W / 2 - self.sub_title_surface.get_width() / 2 + 180,
                                                      self.H / 2 - self.sub_title_surface.get_height() + 270))

            # pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)
            if self.play_button.draw(self.screen):
                self.can_play = True
            if self.can_play and self.play_button.is_finished():
                self.can_play = False
                self.started = True
                self.paused = False

            if self.help_button.draw(self.screen):
                self.can_help = True
            if self.can_help and self.help_button.is_finished():
                self.state = 'H'
                self.can_help = False

            if self.levels_button.draw(self.screen):
                self.can_level = True
            if self.can_level and self.levels_button.is_finished():
                self.set_max_level_unlocked(10)
                self.state = 'L'
                self.can_level = False

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
        if self.state == 'L':
            text_surface = self.sub_title_font.render("Select a level", True, "navy")
            self.screen.blit(text_surface, (
            self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2, self.menu_rect.top - 100))
            if not self.started:
                text_surface = self.sub_title_font.render("To try out levels,", True, "navy")
                self.screen.blit(text_surface, (
                    self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2,
                    self.menu_rect.top - 75))
                text_surface = self.sub_title_font.render("without following the main progression", True, "navy")
                self.screen.blit(text_surface, (
                    self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2,
                    self.menu_rect.top - 50))
            else:
                text_surface = self.sub_title_font.render("To go back to a level, you've already beaten", True, "navy")
                self.screen.blit(text_surface, (
                    self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2,
                    self.menu_rect.top - 50))
            pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)
            if self.back_button.draw(self.screen):
                self.can_back = True
            if self.can_back and self.back_button.is_finished():
                self.can_back = False
                if self.started:
                    self.paused = False
                else:
                    self.state = 'M'

            thumbnails = []
            text_surfaces = []
            buttons = []
            for i in range(self.max_level + 1):
                level_thumbnail = pygame.image.load("main/level_data/level_thumbnail/img.png").convert_alpha()
                level_thumbnail = pygame.transform.scale(level_thumbnail, (int(1280 / 6), int(720 / 6)))
                text_surface = self.text_font.render(f"Level: {i} | Title: | Best score: ", True, "white")
                rect = pygame.Rect(self.menu_rect.left + 5, self.menu_rect.top + 5 + 145 * i, self.menu_rect.width - 10,
                                   123)
                level_button = button.Button(self.menu_rect.left + 5, self.menu_rect.top + 5 + 145 * i, None, 1,
                                             "lightgreen", "empty", rect)
                thumbnails.append(level_thumbnail)
                text_surfaces.append(text_surface)
                buttons.append(level_button)

            level_text_surfaces = [x for x in text_surfaces if
                             self.level_page * 3 - 4 < text_surfaces.index(x) < self.level_page * 3]
            for i in range(len(level_text_surfaces)):
                rect = pygame.Rect(self.menu_rect.left + 5, self.menu_rect.top + 5 + 145 * i, self.menu_rect.width - 10,
                                   120)
                if buttons[i].draw(self.screen):
                    self.set_level_wanted(text_surfaces.index(level_text_surfaces[i]))
                    self.paused = False
                    if not self.started:
                        self.started = True
                pygame.draw.rect(self.screen, "crimson", rect)
                self.screen.blit(thumbnails[0], rect)
                self.screen.blit(level_text_surfaces[i], (rect.left + 250, rect.top + rect.height / 2))
            if self.nextPageButton.draw(self.screen):
                if text_surfaces.index(level_text_surfaces[-1]) < self.max_level:
                    self.level_page += 1
            if self.previousPageButton.draw(self.screen):
                if self.level_page > 1:
                    self.level_page -= 1

    def get_paused(self):
        return self.paused

    def get_level_wanted(self):
        return self.level_wanted

    def set_paused(self):
        self.paused = True

    def set_level_wanted(self, value):
        self.level_wanted = value

    def set_state(self, state):
        self.state = state

    def set_max_level_unlocked(self, value):
        self.level_page = 1
        self.max_level = value
