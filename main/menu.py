import math
import os
import pygame.display
from main.buttons import button
from main import usermanual


def roundup(x) -> int:
    """
    Rounds up the given number to the nearest hundred.

    Parameters
    ----------
    x : int or float

    Returns
    -------
    int
    """
    return int(math.ceil(x / 100.0)) * 100


def make_paging_buttons(x, y, text, font, font_color, color_active, color_passive):
    """
    Creates a paging button.

    Parameters
    ----------
    x : int
    y : int
    text : str
        The text on the button.
    font : pygame.font.Font
    font_color : tuple, str
    color_active : tuple, str
    color_passive : tuple, str

    Returns
    -------
    Button
    """
    button_surface = font.render(text, True, font_color)
    paging_button = button.Button(x, y, button_surface, 1, color_active, color_passive)
    return paging_button


class Menu:
    """
    A class to represent a Menu.

    Attributes
    ----------
    width : int
        The width of the screen.
    height : int
        The height of the screen.
    final_level : int
        The final level of the game.
    last_update : int
        The timer handling the animation.
    player_run_cycle : cycle
        The cycle used to display the player's running animation.
    player_anim : pygame.Surface
        The current frame of the player's running animation to display.
    player_anim_offset : int
        The offset for the player's running animation.
    text_surface : pygame.Surface
    text_rect : pygame.Rect
    title : str
        The title of the menu.
    title_font : pygame.font.Font
    title_surface : pygame.Surface
    sub_title : str
        The subtitle of the menu.
    sub_title_font : pygame.font.Font
    sub_title_surface : pygame.Surface
    flip_anim : bool
        Whether to flip the animation.
    flip_anim_timer : int
        The timer to flip the animation.
    screen : pygame.Surface
    menu_rect : pygame.Rect
        The rectangle area used to display text.
    state : str
        The current state of the menu.
    paused : bool
        Whether the game is paused.
    text_font : pygame.font.Font
    help_surface : list
        The list of surfaces for the help text.
    end_level_surface : list
        The list of surfaces for the end level text.
    level_titles : list
        The list of titles for the levels selection screen.
    limit : int
        The limit height to display text in the help screen.
    can_play : bool
    can_help : bool
    can_level : bool
    can_quit : bool
    can_back : bool
    can_continue : bool
    The above 'can' variables are used to animate the buttons.
    page : int
        The current page number.
    anim_angle : int
        The angle for the animation.
    level_wanted : int
        The level selected by the player.
    level_page : int
        The current page number for the levels selection screen.
    max_level : int
        The maximum level that the player can play based on progression.
    started : bool
        Whether the game has started.
    quitting : bool
        Whether the player is quitting the game to trigger the save and quit from the game file.
    """

    def __init__(self, last_update, player_run_cycle, text_surface, text_rect, screen_size, help_text, final_level):
        """
        Parameters
        ----------
        last_update : int
        player_run_cycle : cycle
        text_surface : pygame.Surface
        text_rect : pygame.Rect
        screen_size : tuple
        help_text : str
        final_level : int
        """
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.final_level = final_level
        self.last_update = last_update
        self.player_run_cycle = player_run_cycle
        self.player_anim = next(self.player_run_cycle)
        self.player_anim_offset = 110
        self.text_surface = text_surface
        self.text_rect = text_rect
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
        self.menu_rect = pygame.Rect(300, self.height / 2 - self.text_surface.get_height() / 2 - 148, self.width - 600,
                                     self.height - 200)
        self.state = 'MENU'
        self.paused = True
        self.text_font = pygame.font.Font('assets/joystix monospace.otf', 16)
        self.help_surface = []
        self.end_level_surface = []
        self.level_titles = ["Function Calls", "Function Chaining and Comments", "Conditionals",
                             "Function Parameters and Debugging", "Loops", "Datatypes and Arrays",
                             "Array Accessing and Modifying", "2D-Arrays", "Final Assessment"]

        self.limit = self.menu_rect.bottom - 400
        self.__init_menu(help_text)
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
        self.quitting = False

    def __init_menu(self, help_text):
        """
        Parses the help text and creates the menu buttons.

        Parameters
        ----------
        help_text : str
        """
        usermanual.parse_text(help_text, self.help_surface, pygame.font.SysFont("arialblack", 16), self.limit,
                              self.menu_rect.width)
        usermanual.parse_text("", self.end_level_surface, self.text_font, self.limit, self.menu_rect.width)
        self.menu_button_font = pygame.font.Font('assets/joystix monospace.otf', 48)
        self.play_button = self.__make_menu_button("Play", self.width, self.height, -200)
        self.help_button = self.__make_menu_button("Help", self.width, self.height, 100)
        self.levels_button = self.__make_menu_button("Pick", self.width, self.height, -50)
        self.quit_button = self.__make_menu_button("Quit", self.width, self.height, 250)
        self.back_button = self.__make_menu_button("Back", self.width, self.height, 290)
        self.continue_button = self.__make_menu_button("Continue", self.width, self.height, 290)
        self.next_page_button = make_paging_buttons(self.menu_rect.right - 45, self.menu_rect.bottom - 45, "→",
                                                    self.sub_title_font, "white", "lightgreen", "blue")
        self.previous_page_button = make_paging_buttons(self.menu_rect.left + 15, self.menu_rect.bottom - 45, "←",
                                                        self.sub_title_font, "white", "lightgreen", "blue")

    def __make_menu_button(self, text, width, height, offset) -> button.Button:
        """
        Creates a menu button.

        Parameters
        ----------
        text : str
            The text on the button.
        width : int
        height : int
        offset : int
            The offset for the button's position.

        Returns
        -------
        Button
        """
        button_surface = self.menu_button_font.render(text, True, "green")
        rect = button_surface.get_rect()
        rect.width *= 2
        rect.height *= 2
        x = width / 2 - button_surface.get_width()
        y = height / 2 - button_surface.get_height() + offset
        return button.Button(x, y, button_surface, 1, "lightgreen", (0, 0, 128), rect,
                             (x + button_surface.get_width() / 2, y + button_surface.get_height() / 2))

    def __handle_menu_button(self, button_to_display, var_to_check, attr_to_modify) -> bool:
        """
        Handles the interaction and animation of a menu button.

        Parameters
        ----------
        button_to_display : Button
        var_to_check : bool
            The variable to check to determine whether to modify the attribute.
        attr_to_modify : str
            The name of the attribute to modify.

        Returns
        -------
        bool
            True if the button is finished and the attribute was modified, False otherwise.
        """
        if button_to_display.draw(self.screen):
            setattr(self, attr_to_modify, True)
        if var_to_check and button_to_display.is_finished():
            setattr(self, attr_to_modify, False)
            return True
        return False

    def __display_text_surfaces(self, surface_to_display):
        """
        Displays the text on the screen.

        Parameters
        ----------
        surface_to_display : list
        """
        start_y = self.menu_rect.top + 10
        text_surfaces = [x for x in surface_to_display if x[1] == self.page]
        for i, current_surface in enumerate(text_surfaces):
            self.screen.blit(current_surface[0], (self.menu_rect.left + 30, start_y + 25 * (i + 1)))
            if current_surface == surface_to_display[-1]:
                text_surface = pygame.font.Font('assets/joystix monospace.otf', 16).render("End of file", True,
                                                                                           "crimson")
                self.screen.blit(text_surface,
                                 (self.menu_rect.left + self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                  start_y + 25 * (i + 1) + 20
                                  ))

    def __display_menu_state(self, current_time):
        """
        Displays the menu state.

        Parameters
        ----------
        current_time : int
        """

        def __handle_menu_animation(current_time):
            """
            Handles the menu animation.

            Parameters
            ----------
            current_time : int
            """
            if current_time > self.last_update + 100:
                self.player_anim = next(self.player_run_cycle)
                self.last_update = current_time
                if self.last_update > self.flip_anim_timer + 3000:
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

                self.player_anim = pygame.transform.rotate(self.player_anim, self.anim_angle)
                self.player_anim = pygame.transform.flip(self.player_anim, True, False)
                self.player_anim.set_colorkey("black")
            if pygame.time.get_ticks() % 100 == 0:
                self.sub_title_surface = pygame.transform.flip(self.sub_title_surface, True, True)
            opposite_sub_title_surface = pygame.transform.flip(self.sub_title_surface, True, True)
            self.screen.blit(self.player_anim, (
                self.width / 2 - self.player_anim.get_width() / 2,
                self.height / 2 - self.player_anim.get_height() / 2 - 400 + self.player_anim_offset))
            self.screen.blit(self.title_surface, (
                self.width / 2 - self.title_surface.get_width() - 45,
                self.height / 2 - self.title_surface.get_height() - 270))
            self.screen.blit(opposite_sub_title_surface,
                             (self.width / 2 - opposite_sub_title_surface.get_width() / 2 - 180,
                              self.height / 2 - self.sub_title_surface.get_height() + 270))
            self.screen.blit(self.sub_title_surface, (self.width / 2 - self.sub_title_surface.get_width() / 2 + 180,
                                                      self.height / 2 - self.sub_title_surface.get_height() + 270))

        if self.started:
            self.started = False
        __handle_menu_animation(current_time)

        if self.__handle_menu_button(self.play_button, self.can_play, "can_play"):
            if not self.started:
                self.started = True
            self.paused = False

        if self.__handle_menu_button(self.help_button, self.can_help, "can_help"):
            self.state = 'HELP'

        if self.__handle_menu_button(self.levels_button, self.can_level, "can_level"):
            self.set_max_level_unlocked(self.final_level)
            self.state = 'LEVEL_SELECTION'

        if self.__handle_menu_button(self.quit_button, self.can_quit, "can_quit"):
            self.can_quit = False
            self.quitting = True

    def __display_help_state(self):
        """
        Displays the help state of the menu.
        """
        pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)

        if self.__handle_menu_button(self.back_button, self.can_back, "can_back"):
            self.can_back = False
            self.state = 'MENU'

        if self.previous_page_button.draw(self.screen):
            if self.page == 1:
                self.page = self.help_surface[-1][1]
            else:
                self.page -= 1
        if self.next_page_button.draw(self.screen):
            if self.page == self.help_surface[-1][1]:
                self.page = 1
            else:
                self.page += 1

        self.__display_text_surfaces(self.help_surface)

    def __display_end_level_state(self):
        """
        Displays the end screen after finishing levels.
        """
        pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)

        if self.continue_button.draw(self.screen):
            self.can_continue = True
        if self.can_continue and self.continue_button.is_finished():
            self.can_continue = False
            self.paused = False

        self.__display_text_surfaces(self.end_level_surface)

    def __display_level_selection_state(self):
        """
        Displays the level selection screen of the menu.
        """

        def __draw_background():
            """
            Draws the background for the level selection screen.

            It renders the title and instructions for the level selection screen,
            draws a rectangle for the menu, and handles the interaction with the back button.
            If the back button is clicked, it either unpauses the game or changes the state to 'MENU'.
            """
            text_surface = self.sub_title_font.render("Select a level", True, "navy")

            self.screen.blit(text_surface, (self.menu_rect.left +
                                            self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                            self.menu_rect.top - 100))
            if not self.started:
                text_surface = self.sub_title_font.render("To try out levels,", True, "navy")
                self.screen.blit(text_surface, (self.menu_rect.left +
                                                self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                                self.menu_rect.top - 75))
                text_surface = self.sub_title_font.render("without following the main progression", True, "navy")
                self.screen.blit(text_surface, (self.menu_rect.left +
                                                self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                                self.menu_rect.top - 50))
            else:
                text_surface = self.sub_title_font.render("To go back to a level, you've already beaten", True, "navy")
                self.screen.blit(text_surface, (self.menu_rect.left +
                                                self.menu_rect.width / 2 - text_surface.get_width() / 2,
                                                self.menu_rect.top - 50))
            pygame.draw.rect(self.screen, (0, 0, 128), self.menu_rect)
            if self.__handle_menu_button(self.back_button, self.can_back, "can_back"):
                self.can_back = False
                if self.started:
                    self.paused = False
                else:
                    self.state = 'MENU'

        def __draw_level_info():
            """
            Draws the level information for the level selection screen.
            It also handles the navigation between level pages and the selection of levels.
            """
            thumbnails = []
            text_surfaces = []
            score_surfaces = []
            buttons = []
            for i in range(self.max_level + 1):
                if i > self.max_level:
                    return
                path = f"main/level_data/level_thumbnail/{i}.PNG"
                if os.path.exists(path):
                    level_thumbnail = pygame.image.load(path).convert_alpha()
                    level_thumbnail = pygame.transform.scale(level_thumbnail, (int(1280 / 6), int(720 / 6)))
                    text_surface = self.text_font.render(f"Level: {i} | Title: {self.level_titles[i]}", True,
                                                         "white")
                    with open(f'main/level_data/level_score/level{i}_score.txt', 'r') as file:
                        best_score = int(str(file.readline()))
                    score_surface = self.text_font.render(f"Best score: {best_score}", True, "white")

                    rect = pygame.Rect(self.menu_rect.left + 5, self.menu_rect.top + 5 + 145 * i,
                                       self.menu_rect.width - 10, 123)
                    level_button = button.Button(self.menu_rect.left + 5, self.menu_rect.top + 5 + 145 * i,
                                                 pygame.Surface((1, 1)), 1,
                                                 "lightgreen", (0, 0, 128), rect)
                    thumbnails.append(level_thumbnail)
                    text_surfaces.append(text_surface)
                    score_surfaces.append(score_surface)
                    buttons.append(level_button)

            level_text_surfaces = [x for x in text_surfaces if
                                   self.level_page * 3 - 4 < text_surfaces.index(x) < self.level_page * 3]
            best_score_surfaces = [x for x in score_surfaces if
                                   self.level_page * 3 - 4 < score_surfaces.index(x) < self.level_page * 3]
            for i in range(len(level_text_surfaces)):
                rect = pygame.Rect(self.menu_rect.left + 5, self.menu_rect.top + 5 + 145 * i, self.menu_rect.width - 10,
                                   120)
                if buttons[i].draw(self.screen):
                    self.set_level_wanted(text_surfaces.index(level_text_surfaces[i]))
                    self.paused = False
                    if not self.started:
                        self.started = True
                pygame.draw.rect(self.screen, "crimson", rect)
                self.screen.blit(thumbnails[text_surfaces.index(level_text_surfaces[i])], rect)
                self.screen.blit(level_text_surfaces[i], (rect.left + 250, rect.top + rect.height / 2 - 50))
                self.screen.blit(best_score_surfaces[i], (rect.left + 250, rect.top + rect.height / 2))

            if self.next_page_button.draw(self.screen):
                if text_surfaces.index(level_text_surfaces[-1]) < self.max_level:
                    self.level_page += 1
            if self.previous_page_button.draw(self.screen):
                if self.level_page > 1:
                    self.level_page -= 1

        __draw_background()
        __draw_level_info()

    def draw(self, current_time):
        """
        Draws the menu based on the current state.
        It is the main function called by the main game loop to display the menu.

        Parameters
        ----------
        current_time : int
        """
        if self.state == 'MENU':
            self.__display_menu_state(current_time)

        if self.state == 'HELP':
            self.__display_help_state()

        if self.state == 'END_SCREEN':
            self.__display_end_level_state()

        if self.state == 'LEVEL_SELECTION':
            self.__display_level_selection_state()

    def set_paused(self):
        self.paused = True

    def set_end_text(self, text):
        """
        Parameters
        ----------
        text : str
        """
        self.end_level_surface = []
        usermanual.parse_text(text, self.end_level_surface, self.text_font, self.limit, self.menu_rect.width)

    def set_level_wanted(self, value):
        """
        Parameters
        ----------
        value : int
        """
        self.level_wanted = value

    def set_state(self, state):
        """
        Parameters
        ----------
        state : str
        """
        self.state = state

    def set_max_level_unlocked(self, value):
        """
        Parameters
        ----------
        value : int
        """
        self.level_page = 1
        self.max_level = value

    def change_page(self, value):
        """
        Changes the page in the help or level selection screen.

        Parameters
        ----------
        value : str
            The direction to change the page ('LEFT' or 'RIGHT').
        """
        if self.state == "HELP":
            if value == "LEFT":
                if self.page == 1:
                    self.page = self.help_surface[-1][1]
                else:
                    self.page -= 1
            elif value == "RIGHT":
                if self.page == self.help_surface[-1][1]:
                    self.page = 1
                else:
                    self.page += 1
        if self.state == "LEVEL_SELECTION":
            if value == "RIGHT":
                if self.level_page * 3 < self.max_level:
                    self.level_page += 1
            elif value == "LEFT":
                if self.level_page > 1:
                    self.level_page -= 1

    def get_paused(self) -> bool:
        return self.paused

    def get_level_wanted(self) -> int:
        return self.level_wanted

    def get_state(self) -> str:
        return self.state

    def get_started(self) -> bool:
        return self.started

    def get_quitting(self) -> bool:
        return self.quitting
