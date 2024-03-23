import pygame
from main.buttons import button

current_page_height = 0


def check_limit_y(limit, text_surface):
    """
    Checks if the current page height of the parsed text has reached the limit.

    Parameters
    ----------
    limit : int
    text_surface : pygame.Surface
        The surface to check the height of.

    Returns
    -------
    int
        1 if the current page height has reached the limit, 0 otherwise.
    """
    global current_page_height
    if current_page_height >= limit:
        current_page_height = text_surface.get_height()
        return 1
    current_page_height += text_surface.get_height()
    return 0


def parse_text(text_to_parse, surface_to_append, font, limit, active_width):
    """
    Parses the given text and appends it to the given surface.

    Parameters
    ----------
    text_to_parse : str
    surface_to_append : list
    font : pygame.font.Font
    limit : int
        The maximum allowed page height.
    active_width : int
        The maximum allowed line width.

    Returns
    -------
    None
    """
    global current_page_height
    current_page_height = 0
    page = 1
    text_list = []
    test_text = ""
    text_surface = font.render(test_text, True, (255, 255, 255))
    for i in range(len(text_to_parse)):
        if text_to_parse[i] == "\n":
            page += check_limit_y(limit, text_surface)
            if i > 0 and text_to_parse[i - 1] == "\n":
                text_surface = font.render(test_text, True, (255, 255, 255))
                surface_to_append.append((text_surface, page))
            else:
                surface_to_append.append((text_surface, page))
            text_list.append(test_text)
            test_text = ""
            continue
        test_text += text_to_parse[i]
        text_surface = font.render(test_text, True, (255, 255, 255))
        if text_surface.get_width() >= active_width - 60:
            if i + 1 < len(text_to_parse) and (text_to_parse[i + 1] != " " or text_to_parse[i + 1] != "\n"):
                j = len(test_text) - 1
                count = 0
                offset_text = ""
                while test_text[j] != " ":
                    count += 1
                    offset_text += test_text[-1]
                    test_text = test_text[:-1]
                    j = len(test_text) - 1
                i -= count
                text_surface = font.render(test_text, True, (255, 255, 255))
                test_text = offset_text[::-1]
            else:
                test_text = ""
            page += check_limit_y(limit, text_surface)
            surface_to_append.append((text_surface, page))
            text_list.append(test_text)

        if i == len(text_to_parse) - 1:
            page += check_limit_y(limit, text_surface)
            surface_to_append.append((text_surface, page))
            text_list.append(test_text)


class UserManual:
    """
    A class to represent a help manual to explain the game and its objectives.

    Attributes
    ----------
    x : int
    y : int
    active : bool
        Whether the manual is currently active.
    user_manual_text : str
        The text of the manual tab.
    level_text : str
        The text of the level tab.
    hint_text : str
        The text of the hint tab.
    text : str
        The current text to display.
    state : str
        The current state of the manual ("LEVEL", "HINT", or "MANUAL").
    active_width : int
        The width the text can occupy in the manual when it's active.
    inactive_rect : pygame.Rect
        The rectangle representing the manual when it's inactive.
    active_rect : pygame.Rect
        The rectangle representing the manual when it's active.
    rect : pygame.Rect
        The current rectangle representing the manual.
    text_font : pygame.font.Font
    limit : int
        The maximum allowed page height the text can occupy.
    manual_text_surface : list
        The list of surfaces representing the pages of the manual tab.
    level_text_surface : list
        The list of surfaces representing the pages of the level tab.
    hint_text_surface : list
        The list of surfaces representing the pages of the hint tab.
    page_button_font : pygame.font.Font
    text_surface : list
        The current list of surfaces representing the pages to display.
    page : int
        The current page number.
    next_page_button : Button
    previous_page_button : Button
    tabs : list
        The list of tabs ("MANUAL", "LEVEL", "HINT").
    tab_rects : list
        The list of rectangles representing the tabs.
    manual_tab_button : Button
    level_tab_button : Button
    hint_tab_button : Button
    """

    def __init__(self, x, y, user_manual_text):
        """
        Parameters
        ----------
        x : int
        y : int
        user_manual_text : str
            The text of the manual tab.
        """
        self.x = x
        self.y = y
        self.active = True
        self.user_manual_text = user_manual_text
        self.level_text = ""
        self.hint_text = ""
        self.text = self.user_manual_text
        self.state = "LEVEL"
        self.active_width = 400
        self.inactive_rect = pygame.Rect(self.x + 115, self.y + 15, 70, self.y + 70)
        self.active_rect = pygame.Rect(self.x - 250, 25, self.active_width, self.y + 600)
        self.rect = self.inactive_rect
        self.text_font = pygame.font.SysFont('arialblack', 16)
        self.limit = self.active_rect.bottom - 215
        self.manual_text_surface = []
        self.level_text_surface = []
        self.hint_text_surface = []
        self.page_button_font = pygame.font.Font('assets/joystix monospace.otf', 32)
        self.text_surface = self.manual_text_surface
        self.page = 1
        self.__init_components()

    def __init_components(self):
        """
        Parses the text into surfaces to be displayed in the UserManual by tabs, and creates relevant buttons.

        Returns
        -------
        None
        """
        parse_text(self.user_manual_text, self.manual_text_surface, self.text_font, self.limit, self.active_width)
        parse_text(self.level_text, self.level_text_surface, self.text_font, self.limit, self.active_width)
        parse_text(self.hint_text, self.hint_text_surface, self.text_font, self.limit, self.active_width)
        next_button_surface = self.page_button_font.render("→", True, (255, 255, 255))
        self.next_page_button = button.Button(self.active_rect.right - 45, self.active_rect.bottom - 45,
                                              next_button_surface, 1, "lightgreen", "blue")
        previous_button_surface = self.page_button_font.render("←", True, (255, 255, 255))
        self.previous_page_button = button.Button(self.active_rect.left + 15, self.active_rect.bottom - 45,
                                                  previous_button_surface, 1, "lightgreen", "blue")

        self.tabs = ["MANUAL", "LEVEL", "HINT"]
        self.tab_rects = [pygame.Rect(self.active_rect.left, self.active_rect.top, 135, self.active_rect.top + 25),
                          pygame.Rect(self.active_rect.left + 137, self.active_rect.top, 110,
                                      self.active_rect.top + 25),
                          pygame.Rect(self.active_rect.left + 247, self.active_rect.top, 110,
                                      self.active_rect.top + 25)]

        self.manual_tab_button = self.__make_tab_button(0, 1.5)
        self.level_tab_button = self.__make_tab_button(1, 1.4)
        self.hint_tab_button = self.__make_tab_button(2, 1.6)

    def __make_tab_button(self, index, scale) -> button.Button:
        """
        Creates a tab button.

        Parameters
        ----------
        index : int
            The index of the tab in the tab list.
        scale : float
            The scale of the button.

        Returns
        -------
        Button
            The created tab button.
        """
        button_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render(self.tabs[index], True,
                                                                                     (255, 255, 255))
        tab_button = button.Button(self.tab_rects[index].x,
                                   self.tab_rects[index].y + button_surface.get_height() / 2,
                                   button_surface, scale, "white", "white")
        return tab_button

    def __handle_state(self):
        """
        Sets the current text surface to be displayed based on the current state.
        """
        if self.state == "MANUAL":
            self.text_surface = self.manual_text_surface
        elif self.state == "LEVEL":
            self.text_surface = self.level_text_surface
        elif self.state == "HINT":
            self.text_surface = self.hint_text_surface

    def __draw_inactive_mode(self, screen):
        """
        Draws the UserManual in its inactive mode, a gold circle with a question mark in its center.

        Parameters
        ----------
        screen : pygame.Surface
        """
        self.rect = self.inactive_rect
        pygame.draw.circle(screen, "gold", (self.x + 150, self.y + 50), 35)
        text_surface = pygame.font.Font('assets/joystix monospace.otf', 32).render("?", True, (255, 255, 255))
        screen.blit(text_surface, (self.x + 136, self.y + 30))
        text_surface = pygame.font.Font('assets/joystix monospace.otf', 24).render("Help", True, (0, 0, 128))
        screen.blit(text_surface, (self.x + 116, self.y + 85))

    def __draw_tab_buttons(self, screen):
        """
        Draws the tab buttons on the screen. If a tab button is clicked, it changes the state of the UserManual.

        Parameters
        ----------
        screen : pygame.Surface
        """
        if self.manual_tab_button.draw(screen):
            self.change_state("MANUAL")
        if self.level_tab_button.draw(screen):
            self.change_state("LEVEL")
        if self.hint_tab_button.draw(screen):
            self.change_state('HINT')

    def __draw_paging_buttons(self, screen):
        """
        Draws the paging buttons on the screen. If a paging button is clicked, it changes the current page.

        Parameters
        ----------
        screen : pygame.Surface
        """
        if self.previous_page_button.draw(screen):
            if self.page == 1:
                self.page = self.text_surface[-1][1]
            else:
                self.page -= 1
        if self.next_page_button.draw(screen):
            if self.page == self.text_surface[-1][1]:
                self.page = 1
            else:
                self.page += 1

        page_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render(f"Page: {self.page}",
                                                                                   True, "white")

        screen.blit(page_surface, (self.active_rect.left + self.active_width / 2 - page_surface.get_width() / 2,
                                   self.active_rect.bottom - 25))

    def __draw_text(self, screen):
        """
        Draws the text of the current tab and page on the screen. It also draws a red "X" and a blue rectangle, core visual components of the active state of the UserManual.

        Parameters
        ----------
        screen : pygame.Surface
        """
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
                screen.blit(text_surface, (self.active_rect.left + self.active_width / 2 - text_surface.get_width() / 2,
                                           start_y + 25 * (i + 1) + 20))

    def __draw_tab_bar(self, screen):
        """
        Draws the tab bar on the screen. It highlights the tab that corresponds to the current state.

        Parameters
        ----------
        screen : pygame.Surface
        """
        for i in range(len(self.tabs)):

            tab_surface = pygame.font.Font('assets/joystix monospace.otf', 18).render(self.tabs[i], True, "white")
            if self.tabs[i] == self.state:
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

    def draw(self):
        """
        Draws the UserManual on the screen. It is the main function called by the main loop of the pygame's application.
        """
        screen = pygame.display.get_surface()
        self.__handle_state()

        if not self.active:
            self.__draw_inactive_mode(screen)
        else:
            self.__draw_tab_buttons(screen)

            self.__draw_text(screen)

            self.__draw_paging_buttons(screen)

            self.__draw_tab_bar(screen)

    def change_state(self, value):
        """
        Changes the state of the UserManual and resets the page number to 1.

        Parameters
        ----------
        value : str
        """
        self.state = value
        self.page = 1

    def flip_active(self):
        self.active = not self.active

    def set_active(self, value):
        """
        Parameters
        ----------
        value : bool
        """
        self.active = value

    def set_level_text(self, text):
        """
        Parameters
        ----------
        text : str
        """
        self.level_text = text
        self.level_text_surface = []
        parse_text(self.level_text, self.level_text_surface, self.text_font, self.limit, self.active_width)

    def reset_page(self):
        self.page = 1

    def set_hint_text(self, text):
        """
        Parameters
        ----------
        text : str
        """
        self.hint_text = text
        self.hint_text_surface = []
        parse_text(self.hint_text, self.hint_text_surface, self.text_font, self.limit, self.active_width)

    def change_page(self, value):
        """
        Parameters
        ----------
        value : str
            The direction to change the page number ("RIGHT" or "LEFT").
        """
        if value == "RIGHT":
            if self.page == self.text_surface[-1][1]:
                self.page = 1
            else:
                self.page += 1
        elif value == "LEFT":
            if self.page == 1:
                self.page = self.text_surface[-1][1]
            else:
                self.page -= 1

    def mouse_colliding(self, pos) -> bool:
        return self.rect.collidepoint(pos)

    def get_active(self) -> bool:
        return self.active
