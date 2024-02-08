import pygame
import button


class UserInputField:

    def __init__(self, title, title_font_size, editable_y_top, editable_y_down, line_limit):

        self.active_char = ""
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.user_text = ''
        self.W = 300
        self.editable_y_top = editable_y_top
        self.editable_y_down = editable_y_down
        self.title = title
        self.input_rect = pygame.Rect(1280, 0, self.W, 720)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False
        self.last_cooldown = pygame.time.get_ticks()
        self.text_saved = []
        self.newline = False
        self.lastLineFilled = False
        self.titleFontSize = title_font_size
        run_button_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Run", True, (255, 255, 255))
        self.run_button = button.Button(self.input_rect.x + (self.W - run_button_surface.get_width()) / 2,
                                        self.editable_y_down, run_button_surface, 1)
        self.lineLimit = line_limit
        self.lineCount = 0

    def draw(self):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
        screen = pygame.display.get_surface()

        pygame.draw.rect(screen, self.color, self.input_rect)
        pygame.draw.rect(screen, self.color_passive, (1280, 0, self.W, 36))

        title_surface = pygame.font.Font('assets/joystix monospace.otf', self.titleFontSize).render(self.title
                                                                                                    , True,
                                                                                                    (255, 255, 255))

        numbering_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        screen.blit(title_surface, (self.input_rect.x + (self.W - title_surface.get_width()) / 2, self.input_rect.y))
        pygame.draw.rect(screen, 'white', (1280, 36, self.W,
                                           16))  # ,(self.input_rect.x, self.input_rect.y + self.editable_y), (self.input_rect.x + self.W, self.input_rect.y + self.editable_y))
        text_surfaces = []
        test_text = ""
        text_list = []
        for i in range(len(self.user_text)):
            if len(text_surfaces) < self.lineLimit:
                test_text += self.user_text[i]
                text_surface = self.font.render(test_text, True, (255, 255, 255))
                if i == len(self.user_text) - 1:
                    if self.newline:
                        self.newline = False
                        while text_surface.get_width() <= self.W - 24:
                            test_text += " "
                            self.user_text += " "
                            text_surface = self.font.render(test_text, True, (255, 255, 255))
                        text_surfaces.append(text_surface)
                        text_list.append(test_text)
                        new_text_surface = self.font.render("", True, (255, 255, 255))
                        text_surfaces.append(new_text_surface)
                    else:
                        text_surfaces.append(text_surface)
                        text_list.append(test_text)

                elif text_surface.get_width() >= self.W - 30:
                    text_surfaces.append(text_surface)
                    text_list.append(test_text)
                    test_text = ""
                    if len(text_surfaces) == self.lineLimit:
                        self.lastLineFilled = True

        self.text_saved = text_list.copy()  # Saves the text to a class field.
        self.lineCount = len(text_surfaces)
        for i in range(len(text_surfaces)):
            numbering_surface = numbering_font.render(f"{i + 1}", True, 'grey')
            screen.blit(numbering_surface, (self.input_rect.x, self.input_rect.y + self.editable_y_top * (i + 1) + 8))
            screen.blit(text_surfaces[i], (self.input_rect.x + 12, self.input_rect.y + self.editable_y_top * (i + 1)))

        if self.active:
            active_char_surface = self.font.render(self.active_char, True, (255, 255, 255))
            cooldown = 500
            if pygame.time.get_ticks() > self.last_cooldown + cooldown:
                self.last_cooldown = pygame.time.get_ticks()
                if self.active_char == "":
                    self.active_char = "|"
                else:
                    self.active_char = ""

                active_char_surface = self.font.render(self.active_char, True, (255, 255, 255))
            last_text_surface = text_surfaces[len(text_surfaces) - 1] if len(text_surfaces) > 0 else 0
            index_of_last = text_surfaces.index(last_text_surface) if last_text_surface != 0 else 0
            text_offset = text_surfaces[len(text_surfaces) - 1].get_width() if len(text_surfaces) > 0 else 0
            screen.blit(active_char_surface,
                        (self.input_rect.x + text_offset + 12,
                         self.input_rect.y + self.editable_y_top * (index_of_last + 1)))

        error_surface = numbering_font.render(f"Lines left: {self.lineLimit - self.lineCount}", True, 'darkblue')
        screen.blit(error_surface, (self.input_rect.x + (self.W - error_surface.get_width()) / 2,
                                    self.editable_y_down + 32))
        if self.run_button.draw(screen):
            return True
        else:
            return False

    def set_active(self, value):
        self.active = value

    def remove_text(self):
        self.user_text = self.user_text[:-1]
        if self.lastLineFilled:
            self.lastLineFilled = False
        if len(self.user_text) > 0 and self.user_text[len(self.user_text) - 1] == " ":
            while self.user_text[len(self.user_text) - 1] == " ":
                self.user_text = self.user_text[:-1]

    def add_text(self, text):
        if self.lineCount <= self.lineLimit and not self.lastLineFilled:
            self.user_text += text

    def set_newline(self):
        if self.lineCount < self.lineLimit:
            self.newline = True

    def get_active(self):
        return self.active

    def get_text_saved(self):
        return self.text_saved

    def mouse_colliding(self, pos):
        return self.input_rect.collidepoint(pos)
