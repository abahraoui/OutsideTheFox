import pygame
from main import usermanual
from main.buttons import button
from main.user_input import UserInputInterface


class TextEditor(UserInputInterface):
    """
    A class used to represent a text editor in a pygame application. It implements the UserInputInterface and follows
    the 'Observer' pattern. It is used to allow the user to input text to write code and interact with the game.

    Attributes
    ----------
    user_text : str
        The text entered by the user, used to store the answer.
    active_char : str
        The beeping character indicating the currently edited character in the text.
    font : pygame.font.Font
    numbering_font : pygame.font.Font
    width : int
    height : int
    input_rect : pygame.Rect
        The rectangle representing the input area.
    color_active : pygame.Color
    color_passive : pygame.Color
    color : pygame.Color
    problem_color : pygame.Color
        The color used in 'Problem' mode.
    active : bool
        Whether the editor is currently active.
    mouse_over : bool
        Whether the mouse is currently over the editor.
    last_cooldown : int
        The last recorded cooldown time used to alternately display and hide the active_char.
    text_saved : list
        The user text split and saved in a list.
    newline : bool
        Whether a new line needs to be added.
    last_line_filled : bool
        Whether the last line of the editor has been filled.
    line_count : int
        The current line count in the editor.
    old_line_count : int
        The old line count, used to compare to detect a new line.
    feedback_rect : pygame.Rect
        The rectangle representing the area where feedback can be drawn.
    error_line : int
        The line where an error occurred.
    error_processed : bool
        Whether the error has been processed.
    copy_rect : pygame.Rect
        The rectangle representing the copied area.
    copy_rect_edited : bool
        Whether the copied rectangle has been edited.
    copy_text : str
        The copied text.
    drawing_feedback : bool
        Whether feedback is currently being drawn.
    drawing_feedback_timer : int
        The timer for displaying feedback.
    feedback_text : str
        The feedback text to be displayed.
    error_feedback : list
        The erroneous feedback to be displayed.
    char_offset : int
        The character offset in the currently edited line.
    active_char_offset : int
        The offset required by the active char to be drawn between the text.
    line_offset : int
        The line offset used to navigate up and down lines (not currently used by the game but implemented).
    mode : str
        The mode of the editor, default 'Player', can be 'Problem', mainly visual.
    run_button : Button
        The 'Run' button. When clicked, it executes the code currently written in the editor.
    clear_button : Button
        The 'Clear' button. When clicked, it clears the code currently written in the editor.
    """

    def __init__(self, title, title_font_size, editable_y_top, editable_y_down, line_limit):
        """
        Parameters
        ----------
        title : str
        title_font_size : int
        editable_y_top : float
            The top y-coordinate of the user's editable area.
        editable_y_down : float
            The bottom y-coordinate of the user's editable area.
        line_limit : int
            The maximum number of lines allowed to be written in the editor.
        """
        super().__init__()
        self.user_text = " "
        self.active_char = ""
        self.title = title
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.numbering_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        self.width = 400
        self.height = 720
        self.editable_y_top = editable_y_top
        self.editable_y_down = editable_y_down
        self.input_rect = pygame.Rect(1180, 0, self.width, self.height)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        self.color = self.color_passive
        self.problem_color = pygame.Color('purple')
        self.active = False
        self.mouse_over = False
        self.last_cooldown = pygame.time.get_ticks()
        self.text_saved = []
        self.newline = False
        self.last_line_filled = False
        self.title_font_size = title_font_size
        self.line_limit = line_limit
        self.line_count = 0
        self.old_line_count = self.line_count
        self.feedback_rect = pygame.Rect(self.input_rect.x, editable_y_down - 100, self.width, 100)
        self.error_line = None
        self.error_processed = True
        self.copy_rect = pygame.Rect(0, 0, 0, 0)
        self.copy_rect_edited = False
        self.copy_text = ""
        self.drawing_feedback = False
        self.drawing_feedback_timer = pygame.time.get_ticks()
        self.feedback_text = ""
        self.error_feedback = []
        self.char_offset = 0
        self.active_char_offset = 0
        self.line_offset = 0
        self.mode = "Player"
        self.__init_buttons()

    def __init_buttons(self):
        """
        This method creates a 'Run' button and a 'Clear' button, and positions them at the bottom of the editor.
        """
        run_button_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Run", True, (255, 255, 255))
        self.run_button = button.Button(self.input_rect.x + (self.width - run_button_surface.get_width()) / 3.5,
                                        self.editable_y_down, run_button_surface, 1, "lightgreen", "blue")
        clear_button_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Clear", True,
                                                                                           (255, 255, 255))
        self.clear_button = button.Button(self.input_rect.x + (self.width + clear_button_surface.get_width()) / 2.5,
                                          self.editable_y_down, clear_button_surface, 1, "lightgreen", "blue")

    def __init_draw(self):
        """
        This method sets the color of the editor based on its current state and mode, and initializes the user text if it's empty. It's called at the beginning of the draw method.

        Returns
        -------
        pygame.Surface
            The surface of the current display.
        """
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive if self.mode == "Player" else self.problem_color
        if self.mouse_over and not self.active:
            self.color = "blue"
        else:
            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_passive if self.mode == "Player" else self.problem_color

        if not self.user_text:
            self.user_text = " "
        screen = pygame.display.get_surface()
        self.title = self.mode + " Editor"
        return screen

    def __calculate_offset(self):
        """
        This method calculates the offset based on the spaces at the end of the last line and the lengths of the lines above the last line. Not currently used by the game but implemented.
        """
        count = 0
        text = self.text_saved[-1 - self.line_offset]
        for i in range(len(text) - 1, 0, -1):
            if text[i] == " ":
                count += 1
            else:
                break
        lengths = [len(x) for x in self.text_saved if
                   self.text_saved.index(x) > len(self.text_saved) - 1 - self.line_offset]
        offset_previous_lines = sum(lengths)
        self.active_char_offset = -(len(text) - count)
        self.char_offset = abs(count + offset_previous_lines + self.line_offset)

    def __draw_title_section(self, screen):
        """
        Draw the title section of the code editor.

        Parameters
        ----------
        screen : pygame.Surface
            The surface of the current display.
        """
        title_color = (255, 255, 255) if self.mode == "Player" else (255, 253, 208)
        pygame.draw.rect(screen, self.color, self.input_rect)
        passive_color = self.color_passive if self.mode == "Player" else self.problem_color
        pygame.draw.rect(screen, passive_color, pygame.Rect(1180, 0, self.width, 36))
        title_surface = pygame.font.Font('assets/joystix monospace.otf', self.title_font_size).render(self.title, True,
                                                                                                      title_color)
        screen.blit(title_surface,
                    (self.input_rect.x + (self.width - title_surface.get_width()) / 2, self.input_rect.y))
        pygame.draw.rect(screen, 'white', (1180, 36, self.width,
                                           16))

    def __process_text(self, text_surfaces, text_list, color):
        """
        Process the user text to fit within the editor's width and line limit.

        Parameters
        ----------
        text_surfaces : list
            Array of rendered text surfaces.
        text_list : list
            Array of parsed lines of text.
        color : tuple, str
        """
        test_text = ""
        for i in range(len(self.user_text)):
            if len(text_surfaces) >= self.line_limit:
                continue
            char = self.user_text[i]
            if char not in ('\r', '\n'):
                test_text += char
            text_surface = self.font.render(test_text, True, color)
            if i == len(self.user_text) - 1:
                if char == '\r' and self.newline is False and self.line_count < self.line_limit:
                    self.newline = True
                    while text_surface.get_width() <= self.width - 24:
                        test_text += " "
                        self.user_text += " "
                        text_surface = self.font.render(test_text, True, color)
                    text_surfaces.append(text_surface)
                    text_list.append(test_text)
                    new_text_surface = self.font.render("", True, color)
                    text_surfaces.append(new_text_surface)
                else:
                    text_surfaces.append(text_surface)
                    text_list.append(test_text)
            elif text_surface.get_width() >= self.width - 30:
                text_surfaces.append(text_surface)
                if self.newline:
                    self.newline = False
                text_list.append(test_text)
                test_text = ""
                if len(text_surfaces) == self.line_limit:
                    self.last_line_filled = True

        # removes unintended space.
        for i in range(0, len(text_list)):
            if text_list[i][0] == " ":
                text_list[i] = text_list[i][1:]

        self.text_saved = text_list.copy()  # Saves the text to a class field.
        old = self.line_count
        self.line_count = len(text_surfaces)
        if self.line_count > old:
            self.old_line_count = self.line_count

    def __draw_text(self, screen) -> tuple:
        """
        Draw the processed text onto the screen. Called in the draw method.

        Parameters
        ----------
        screen : pygame.Surface
            The surface of the current display.
        """
        text_surfaces = []
        text_list = []
        white = (255, 255, 255)
        color = white
        self.__process_text(text_surfaces, text_list, color)
        indent_list = []
        rect_list = []

        for i in range(len(text_surfaces)):
            test_text = ""
            if i < len(text_list) and len(text_list[i]) > 0 and text_list[i][0] == " ":
                j = 0
                while j < len(text_list[i]) and text_list[i][j] == " ":
                    test_text += '_'
                    j += 1
                unique = list(set(text_list[i]))
                if unique == [" "] and i != len(text_list) - 1:
                    test_text = ""
            if self.error_line is not None and i + 1 == self.error_line:
                numbering_surface = self.numbering_font.render(f"{i + 1}", True, 'crimson')
                current_surface = self.font.render(text_list[i], True, 'crimson')
            else:
                numbering_surface = self.numbering_font.render(f"{i + 1}", True, 'grey')
                current_surface = text_surfaces[i]

            indentation_surface = self.font.render(test_text, True, 'grey')
            screen.blit(indentation_surface,
                        (self.input_rect.x + 12, self.input_rect.y + self.editable_y_top * (i + 1)))

            screen.blit(numbering_surface, (self.input_rect.x, self.input_rect.y + self.editable_y_top * (i + 1) + 8))
            indent_offset = indentation_surface.get_width() / 2 - 12 if indentation_surface.get_width() > 0 else 0
            indent_list.append(indent_offset)

            screen.blit(current_surface,
                        (self.input_rect.x + 15 + indent_offset, self.input_rect.y + self.editable_y_top * (i + 1)))
            rect = pygame.Rect(self.input_rect.x, self.input_rect.y + self.editable_y_top * (i + 1), self.width,
                               current_surface.get_height())
            rect_list.append(rect)
        return text_surfaces, text_list, rect_list, indent_list

    def __draw_active_char(self, screen, text_surfaces, text_list, indent_list):
        """
        Draw the active character (cursor) onto the screen.

        Parameters
        ----------
        screen : pygame.Surface
        text_surfaces : list
        text_list : list
        indent_list : list
            Array of indentation offsets for each line.
        """
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
        indent_offset = indent_list[index_of_last - self.line_offset]
        text_offset = text_surfaces[len(text_surfaces) - 1 - self.line_offset].get_width() if len(
            text_surfaces) > 0 else 0
        offset = 0

        if self.char_offset > 0:
            offset_string = text_list[-1 - self.line_offset][-self.active_char_offset:]
            offset = self.font.render(offset_string, True, (255, 255, 255)).get_width()

        screen.blit(active_char_surface,
                    (self.input_rect.x + text_offset + 12 + indent_offset - offset,
                     self.input_rect.y + self.editable_y_top * (index_of_last + 1 - self.line_offset)))

    def __draw_copy_rect(self, screen, rect_list, text_list):
        """
        Draw the rectangle for the copied text, select text to copy, and store the copied text.
        Used in the draw method.

        Parameters
        ----------
        screen : pygame.Surface
        rect_list : list
            Array of line rectangles colliding with the copy rectangle.
        text_list : list
            Array of lines of text.
        """
        if self.copy_rect.height > 5 and self.copy_rect.width > 5:
            pygame.draw.rect(screen, (0, 0, 128, 180), self.copy_rect, 3, 3)
        self.copy_text = ""
        for i in range(len(rect_list)):
            rect = rect_list[i]
            if rect.colliderect(self.copy_rect):
                self.copy_text += text_list[i] + " "

    def __draw_buttons_section(self, screen) -> bool:
        """
        Draw the editor's buttons and the display the lines left.

        Parameters
        ----------
        screen : pygame.Surface
        """
        lines_surface = self.numbering_font.render(f"Lines left: {self.line_limit - self.line_count}", True,
                                                   'darkblue')
        screen.blit(lines_surface, (self.input_rect.x + (self.width - lines_surface.get_width()) / 2,
                                    self.editable_y_down + 32))
        if self.clear_button.draw(screen):
            self.clear_text()
        return self.run_button.draw(screen)

    def start_feedback(self, text):
        """
        Start displaying feedback.

        Parameters
        ----------
        text : str
            The feedback text to display.
        """
        self.drawing_feedback = True
        self.drawing_feedback_timer = pygame.time.get_ticks()
        self.feedback_text = text

    def draw_feedback(self, screen):
        """
        Draw the feedback on the feedback area of the editor.

        Parameters
        ----------
        screen : pygame.Surface
        """
        text_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render(self.feedback_text, True, "white")
        screen.blit(text_surface, (self.feedback_rect.left + text_surface.get_width(), self.feedback_rect.top))

    def draw_error_feedback(self, screen):
        """
        Draw the error feedback on the feedback area of the editor.

        Parameters
        ----------
        screen : pygame.Surface
        """
        start_y = self.feedback_rect.top
        text_surface = self.font.render(self.error_feedback[0], True, (255, 255, 255))
        screen.blit(text_surface, (self.feedback_rect.left + self.feedback_rect.width / 5, start_y))
        text_surfaces = []
        limit = self.feedback_rect.bottom - 10
        usermanual.parse_text(self.error_feedback[1], text_surfaces, self.font, limit,
                              self.feedback_rect.width)

        for i in range(len(text_surfaces)):
            current_surface = text_surfaces[i]
            screen.blit(current_surface[0],
                        (self.feedback_rect.left + current_surface[0].get_width() / 5, start_y + 25 * (i + 1)))

    def draw(self):
        """
        Draw the code editor onto the screen. Is the main method called in the main loop of the pygame's application.
        """
        screen = self.__init_draw()
        self.__draw_title_section(screen)

        text_surfaces, text_list, rect_list, indent_list = self.__draw_text(screen)

        if self.drawing_feedback:
            self.draw_feedback(screen)
            if pygame.time.get_ticks() > self.drawing_feedback_timer + 1000:
                self.drawing_feedback = False
            # pygame.draw.rect(screen, "red", self.feedback_rect, 3) # Uncomment to Debug feedback rect

        if not self.error_processed:
            self.draw_error_feedback(screen)
        if self.active:
            self.__draw_active_char(screen, text_surfaces, text_list, indent_list)
            if self.is_copy_rect():
                self.__draw_copy_rect(screen, rect_list, text_list)
            return self.__draw_buttons_section(screen)
        return False

    def set_active(self, value):
        """
        Parameters
        ----------
        value : bool
        """
        self.active = value

    def set_mode(self, value):
        """
        Parameters
        ----------
        value : str
        """
        self.mode = value

    def set_user_answer(self, value):
        """
        Parameters
        ----------
        value : str
        """
        self.user_text = value

    def clear_text(self):
        self.user_text = ""
        self.char_offset = 0
        self.active_char_offset = 0
        self.line_offset = 0
        self.set_error_processed()
        self.last_line_filled = False

    def set_mouse_over(self, value):
        """    
        Parameters
        ----------
        value : bool
            The new mouse over state.
        """
        self.mouse_over = value

    def set_error_line(self, value):
        """
        Parameters
        ----------
        value : int
        """
        self.error_line = value

    def set_error_processed(self):
        """
        Set the error as processed and clear the error line.
        """
        self.error_processed = True
        self.error_line = None

    def set_copy_rect_start_pos(self, pos):
        """
        Set the start position of the copy rectangle at the initial mouse's click postion.

        Parameters
        ----------
        pos : tuple
        """
        if pos[0] < self.width / 2:
            self.copy_rect.left = pos[0]
        elif pos[0] > self.width / 2:
            self.copy_rect.right = pos[0]

        if pos[1] < self.height / 2:
            self.copy_rect.top = pos[1]
        elif pos[1] > self.height / 2:
            self.copy_rect.bottom = pos[1]

        self.copy_rect_edited = True

    def set_copy_rect_end_pos(self, pos):
        """
        Set the end position of the copy rectangle at the position of the mouse's motion.

        Parameters
        ----------
        pos : tuple
        """
        x = pos[0]
        y = pos[1]
        if self.copy_rect.left:
            if x > self.copy_rect.left:
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

    def increment_offset(self):
        self.char_offset += 1
        self.active_char_offset += 1

    def decrement_offset(self):
        if self.char_offset > 0:
            self.char_offset -= 1
            self.active_char_offset -= 1

    def increment_offset_up(self):
        if self.line_count > self.line_offset + 1:
            self.line_offset += 1
            self.__calculate_offset()

    def decrement_offset_down(self):
        if self.line_offset > 0:
            self.line_offset -= 1
            self.__calculate_offset()

    def void_copy_rect_pos(self):
        """
        Void the copy rectangle position and set the copy rectangle as not edited.
        """
        self.copy_rect = pygame.Rect(0, 0, 0, 0)
        self.copy_rect_edited = False

    def paste_clipboard(self, content):
        """
        Paste the content from the clipboard into the user text.

        Parameters
        ----------
        content : str
        """
        if self.line_count <= self.line_limit and not self.last_line_filled:
            self.user_text += content

    def update(self, message):
        """
        Update the code editor based on the received message. Used in the 'Observer' pattern and implemented from the Listener interface.

        Parameters
        ----------
        message : str or list
        """
        if message == "Done":
            self.set_active(True)
            return
        if message == "Running":
            self.set_mouse_over(False)
            self.set_active(False)
            return
        if isinstance(message, list):
            self.set_error_line(message[2])
            self.error_feedback = [message[0], message[1]]
            self.error_processed = False
            return

    def remove_text(self):
        """
        Modify the user text by removing the character at current offset position, from the user text.
        """
        if self.error_line is not None:
            self.set_error_processed()
        if self.char_offset == 0:
            self.user_text = self.user_text[:-1]
        else:
            index = len(self.user_text) - 1 - self.char_offset
            if index >= 0:
                self.user_text = self.user_text[:index] + self.user_text[index + 1:]
                if self.line_offset != 0:
                    self.active_char_offset += 1

        if self.last_line_filled:
            self.last_line_filled = False
        text_surfaces = []
        text_list = []
        self.__process_text(text_surfaces, text_list, "white")
        removed_line = False
        if self.old_line_count != self.line_count:
            self.old_line_count = self.line_count
            self.user_text = self.user_text[:-1]
            removed_line = True
            self.char_offset = 0

        if len(self.user_text) > 0 and self.user_text[-1] == " " and removed_line:
            while len(self.user_text) > 0 and self.user_text[- 1] == " ":
                self.user_text = self.user_text[:-1]
                if len(self.user_text) > 0 and self.user_text[- 1] == "\r":
                    self.user_text = self.user_text[:-1]

    def add_text(self, text):
        """
        Add text to the user text at the current offset position.

        Parameters
        ----------
        text : str
        """
        if self.error_line is not None:
            self.set_error_processed()
        text_surfaces = []
        text_list = []
        self.__process_text(text_surfaces, text_list, "white")
        if self.line_count > self.line_limit and self.last_line_filled and len(text_surfaces) > self.line_limit:
            return
        if self.char_offset == 0:
            self.user_text += text
        else:
            index = len(self.user_text) - 1 - self.char_offset
            self.user_text = self.user_text[:index + 1] + text + self.user_text[index + 1:]
            if self.line_offset != 0 and text != '':
                self.active_char_offset -= 1

    def is_copy_rect(self) -> bool:
        return self.copy_rect_edited

    def get_copy_text(self) -> bytes:
        return self.copy_text.encode()

    def get_active(self) -> bool:
        return self.active

    def get_mode(self) -> str:
        return self.mode

    def get_error_processed(self) -> bool:
        return self.error_processed

    def get_user_answer(self) -> list:
        self.error_line = None
        return self.text_saved

    def mouse_colliding(self, pos) -> bool:
        return self.input_rect.collidepoint(pos)
