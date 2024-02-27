import pygame
import button


class UserInputField:

    def __init__(self, title, title_font_size, editable_y_top, editable_y_down, line_limit):
        self.active_char = ""
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.user_text = ' '
        self.W = 400
        self.H = 720
        self.editable_y_top = editable_y_top
        self.editable_y_down = editable_y_down
        self.title = title
        self.input_rect = pygame.Rect(1180, 0, self.W, self.H)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.active = False
        self.mouseOver = False
        self.last_cooldown = pygame.time.get_ticks()
        self.text_saved = []
        self.newline = False
        self.lastLineFilled = False
        self.titleFontSize = title_font_size
        run_button_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Run", True, (255, 255, 255))
        self.runButton = button.Button(self.input_rect.x + (self.W - run_button_surface.get_width()) / 5,
                                       self.editable_y_down, run_button_surface, 1, "lightgreen", "blue")
        clear_button_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Clear", True,
                                                                                           (255, 255, 255))
        self.clearButton = button.Button(self.input_rect.x + (self.W + clear_button_surface.get_width()) / 3,
                                         self.editable_y_down, clear_button_surface, 1, "lightgreen", "blue")
        self.lineLimit = line_limit
        self.lineCount = 0
        self.oldLineCount = self.lineCount
        self.feedback_rect = pygame.Rect(self.input_rect.x, editable_y_down - 100, self.W, 100)
        self.errorLine = None
        self.errorProcessed = False
        self.copy_rect = pygame.Rect(0, 0, 0, 0)
        self.copy_rect_edited = False
        self.copy_text = ""
        self.drawing_feedback = False
        self.drawing_feedback_timer = pygame.time.get_ticks()
        self.feedback_text = ""
        self.char_offset = 0
        self.mode = "Player"

    def process_text(self, text_surfaces, text_list, color):
        test_text = ""
        for i in range(len(self.user_text)):
            if len(text_surfaces) < self.lineLimit:
                char = self.user_text[i]
                if char != '\r' and char != '\n':
                    test_text += char

                text_surface = self.font.render(test_text, True, color)
                if i == len(self.user_text) - 1:
                    if char == '\r' and self.newline is False and self.lineCount < self.lineLimit:
                        self.newline = True
                        while text_surface.get_width() <= self.W - 24:
                            test_text += " "
                            self.user_text += " "
                            text_surface = self.font.render(test_text, True, color)
                        # test_text = test_text[:-1]
                        # self.user_text = self.user_text[:-1]
                        text_surfaces.append(text_surface)
                        text_list.append(test_text)
                        new_text_surface = self.font.render("", True, color)
                        text_surfaces.append(new_text_surface)
                    else:
                        text_surfaces.append(text_surface)
                        text_list.append(test_text)
                elif text_surface.get_width() >= self.W - 30:
                    text_surfaces.append(text_surface)
                    if self.newline:
                        self.newline = False
                    text_list.append(test_text)
                    test_text = ""
                    if len(text_surfaces) == self.lineLimit:
                        self.lastLineFilled = True

        # removes unintended space.
        for i in range(0, len(text_list)):
            if text_list[i][0] == " ":
                text_list[i] = text_list[i][1:]

        self.text_saved = text_list.copy()  # Saves the text to a class field.
        old = self.lineCount
        self.lineCount = len(text_surfaces)
        if self.lineCount > old:
            self.oldLineCount = self.lineCount

    def start_feedback(self, text):
        self.drawing_feedback = True
        self.drawing_feedback_timer = pygame.time.get_ticks()
        self.feedback_text = text

    def draw_feedback(self, screen):
        text_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render(self.feedback_text, True, "white")
        screen.blit(text_surface, (self.feedback_rect.left + text_surface.get_width(), self.feedback_rect.top))

    def draw(self):
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
        if self.mouseOver and not self.active:
            self.color = "red"
        else:
            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_passive

        if not self.user_text:
            self.user_text = ' '
        screen = pygame.display.get_surface()
        self.title = self.mode + " Editor"
        if self.mode == "Player":
            title_color = (255, 255, 255)
            pygame.draw.rect(screen, self.color, self.input_rect)
            pygame.draw.rect(screen, self.color_passive, (1180, 0, self.W, 36))

        else:
            title_color = (255, 253, 208)
            bg_color = "purple" if not self.active else self.color
            pygame.draw.rect(screen, bg_color, self.input_rect)
            pygame.draw.rect(screen, "purple", (1180, 0, self.W, 36))

        title_surface = pygame.font.Font('assets/joystix monospace.otf', self.titleFontSize).render(self.title, True,
                                                                                                    title_color)
        numbering_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        screen.blit(title_surface, (self.input_rect.x + (self.W - title_surface.get_width()) / 2, self.input_rect.y))
        pygame.draw.rect(screen, 'white', (1180, 36, self.W,
                                           16))
        # ,(self.input_rect.x, self.input_rect.y + self.editable_y),
        # (self.input_rect.x + self.W, self.input_rect.y + self.editable_y))
        text_surfaces = []
        text_list = []
        white = (255, 255, 255)
        color = white
        self.process_text(text_surfaces, text_list, color)
        indent_list = []
        rect_list = []
        for i in range(len(text_surfaces)):
            test_text = ""
            if i < len(text_list) and len(text_list[i]) > 0 and text_list[i][0] == " ":
                j = 0
                # print("s",text_list[i][j], "e")
                while j < len(text_list[i]) and text_list[i][j] == " ":
                    test_text += '_'
                    # print(test_text)
                    j += 1
                unique = list(set(text_list[i]))
                if unique == [" "] and i != len(text_list) - 1:
                    test_text = ""
            if self.errorLine is not None and i + 1 == self.errorLine:
                numbering_surface = numbering_font.render(f"{i + 1}", True, 'crimson')
                current_surface = self.font.render(text_list[i], True, 'crimson')
            else:
                numbering_surface = numbering_font.render(f"{i + 1}", True, 'grey')
                current_surface = text_surfaces[i]
            indentation_surface = self.font.render(test_text, True, 'grey')
            screen.blit(indentation_surface,
                        (self.input_rect.x + 12, self.input_rect.y + self.editable_y_top * (i + 1)))
            screen.blit(numbering_surface, (self.input_rect.x, self.input_rect.y + self.editable_y_top * (i + 1) + 8))
            indent_offset = indentation_surface.get_width() / 2 - 12 if indentation_surface.get_width() > 0 else 0
            indent_list.append(indent_offset)

            screen.blit(current_surface,
                        (self.input_rect.x + 15 + indent_offset, self.input_rect.y + self.editable_y_top * (i + 1)))
            rect = pygame.Rect(self.input_rect.x, self.input_rect.y + self.editable_y_top * (i + 1), self.W,
                               current_surface.get_height())
            # pygame.draw.rect(screen, "white", rect, 3, 3)
            rect_list.append(rect)
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
            indent_offset = indent_list[index_of_last]
            text_offset = text_surfaces[len(text_surfaces) - 1].get_width() if len(text_surfaces) > 0 else 0
            offset = 0
            if self.char_offset > 0:
                offset_string = text_list[-1][-self.char_offset:]
                offset = self.font.render(offset_string, True, (255, 255, 255)).get_width()

            screen.blit(active_char_surface,
                        (self.input_rect.x + text_offset + 12 + indent_offset - offset,
                         self.input_rect.y + self.editable_y_top * (index_of_last + 1)))
            if self.is_copy_rect():
                if self.copy_rect.height > 5 and self.copy_rect.width > 5:
                    pygame.draw.rect(screen, (0, 0, 128, 180), self.copy_rect, 3, 3)
                self.copy_text = ""
                for i in range(len(rect_list)):
                    rect = rect_list[i]
                    if rect.colliderect(self.copy_rect):
                        # pygame.draw.rect(screen, "crimson", rect, 3, 3)
                        self.copy_text += text_list[i] + " "
        if self.drawing_feedback:
            self.draw_feedback(screen)
            if pygame.time.get_ticks() > self.drawing_feedback_timer + 1000:
                self.drawing_feedback = False

        lines_surface = numbering_font.render(f"Lines left: {self.lineLimit - self.lineCount}", True, 'darkblue')
        # pygame.draw.rect(screen, "red", self.feedback_rect, 3) # Uncomment to Debug feedback rect
        if self.active:
            screen.blit(lines_surface, (self.input_rect.x + (self.W - lines_surface.get_width()) / 2,
                                        self.editable_y_down + 32))
            if self.clearButton.draw(screen):
                self.clear_text()
            if self.runButton.draw(screen):
                return True
            else:
                return False

    def set_active(self, value):
        self.active = value

    def set_mode(self, value):
        self.mode = value

    def set_user_text(self, value):
        self.user_text = value

    def clear_text(self):
        self.user_text = ""
        self.char_offset = 0
        self.lastLineFilled = False

    def set_mouse_over(self, value):
        self.mouseOver = value

    def set_error_line(self, value):
        self.errorLine = value

    def set_error_processed(self):
        self.errorProcessed = True

    def increment_line_limit(self):
        self.lineLimit += 1

    def set_copy_rect_start_pos(self, pos):
        if pos[0] < self.W / 2:
            self.copy_rect.left = pos[0]
        elif pos[0] > self.W / 2:
            self.copy_rect.right = pos[0]

        if pos[1] < self.H / 2:
            self.copy_rect.top = pos[1]
        elif pos[1] > self.H / 2:
            self.copy_rect.bottom = pos[1]

        self.copy_rect_edited = True

    def set_copy_rect_end_pos(self, pos):
        x = pos[0]
        y = pos[1]
        if self.copy_rect.left and x > self.copy_rect.left:
            self.copy_rect.width = x - self.copy_rect.left
            self.copy_rect.right = x
        elif self.copy_rect.right and x < self.copy_rect.right:
            self.copy_rect.width = self.copy_rect.right - x
            self.copy_rect.left = x

        if self.copy_rect.top and y > self.copy_rect.top:
            self.copy_rect.height = y - self.copy_rect.top
            self.copy_rect.bottom = y
        elif self.copy_rect.bottom and y < self.copy_rect.bottom:
            self.copy_rect.height = self.copy_rect.bottom - y
            self.copy_rect.top = y

        # print(self.copy_rect.left)

    def increment_offset(self):
        self.char_offset += 1

    def decrement_offset(self):
        if self.char_offset > 0:
            self.char_offset -= 1

    def void_copy_rect_pos(self):
        self.copy_rect = pygame.Rect(0, 0, 0, 0)
        self.copy_rect_edited = False

    def is_copy_rect(self):
        return self.copy_rect_edited

    def get_copy_text(self):
        print("Copy content length:", self.copy_text.__len__())
        return self.copy_text.encode()

    def get_active(self):
        return self.active  # return active in a not fashion, to no make it confusing in game (active is False
        # means user input is running).

    def get_mode(self):
        return self.mode

    def get_error_processed(self):
        return self.errorProcessed

    def get_feedback_rect(self):
        return self.feedback_rect

    def remove_text(self):
        if self.errorLine is not None:
            self.errorProcessed = True
            self.errorLine = None
        if self.char_offset == 0:
            self.user_text = self.user_text[:-1]
        else:
            index = len(self.user_text) - 1 - self.char_offset
            if index >= 0:
                self.user_text = self.user_text[:index] + self.user_text[index + 1:]

        if self.lastLineFilled:
            self.lastLineFilled = False
        text_surfaces = []
        text_list = []
        self.process_text(text_surfaces, text_list, "white")
        removed_line = False
        if self.oldLineCount != self.lineCount:
            self.oldLineCount = self.lineCount
            self.user_text = self.user_text[:-1]
            removed_line = True
            self.char_offset = 0

        if len(self.user_text) > 0 and self.user_text[-1] == " " and removed_line:
            while len(self.user_text) > 0 and self.user_text[- 1] == " ":
                self.user_text = self.user_text[:-1]
                if len(self.user_text) > 0 and self.user_text[- 1] == "\r":
                    self.user_text = self.user_text[:-1]

    def add_text(self, text):
        if self.errorLine is not None:
            self.errorProcessed = True
            self.errorLine = None
        text_surfaces = []
        text_list = []
        self.process_text(text_surfaces, text_list, "white")
        if self.lineCount <= self.lineLimit and not self.lastLineFilled and len(text_surfaces) <= self.lineLimit:
            if self.char_offset == 0:
                self.user_text += text
            else:
                index = len(self.user_text) - 1 - self.char_offset
                self.user_text = self.user_text[:index + 1] + text + self.user_text[index + 1:]

    def get_text_saved(self):
        self.errorProcessed = False
        self.errorLine = None
        return self.text_saved

    def paste_clipboard(self, content):
        if self.lineCount <= self.lineLimit and not self.lastLineFilled:
            self.user_text += content

    def mouse_colliding(self, pos):
        return self.input_rect.collidepoint(pos)
