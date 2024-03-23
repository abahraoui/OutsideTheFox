# pylint: disable=line-too-long
import math
import pygame

from main import usermanual


class Player(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Attributes
    ----------
    x : int
    y : int
        The coordinates of the player.
    w : int
        The width of the player.
    h : int
        The height of the player.
    velocity : int
        The velocity of the player.
    max_jump_range : int
        The maximum jump range of the player, defines how high it will jump before falling.
    animation_list : list
        The list of animations for the player.
    direction : str
        The direction the player is facing ('R' for right, 'L' for left).
    current_anim : int
        The index of the current animation in the animation list.
    animation_cooldown : int
        The cooldown time between change animation.
    last_update : int
        Store the previous time when a frame was changed.
    action : int
        The current animation action of the player.
    moving : bool
        Whether the player is currently moving.
    blocked_right : bool
        Whether the player is blocked on the right.
    blocked_left : bool
        Whether the player is blocked on the left.
    blocked_above : bool
        Whether the player is blocked above.
    blocked_below : bool
        Whether the player is blocked below.
    image : pygame.Surface
        The image of the player.
    normal_rect : pygame.Rect
        The normal rectangle of the player, used for every action but crouching.
    crouching_rect : pygame.Rect
        The crouching rectangle of the player, used when the player is crouched.
    rect : pygame.Rect
        The current rectangle of the player.
    colliding : bool
        Whether the player is currently colliding with something.
    running_sound : pygame.mixer.Sound
        The sound played when the player is running.
    climbing_sound_channel : pygame.mixer.Channel
        The sound channel used to play the climbing sound.
    climbing_sound_cooldown : int
        The cooldown time used to play the climbing sound.
    collider : dict
        The collider structure storing each tiles colliding with the player.
    tile_size : int
        The size of a tile in the game.
    goal_x : int
        The goal x-coordinate of the player, used when lerping to move left or right.
    goal_y : int
        The goal y-coordinate of the player, used when lerping to jump.
    lerping : bool
        Whether the player is currently lerping.
    finished : bool
        Whether the player has finished the level.
    crouching : bool
        Whether the player is currently crouching.
    finished_crouching : bool
        Whether the player has finished transitionning into crouch mode.
    crouching_cooldown : int
        The cooldown time for crouching.
    can_climb : bool
        Whether the player can currently climb.
    climbing : bool
        Whether the player is currently climbing.
    climbing_direction : str
        The direction the player is climbing ('U' for up, 'D' for down).
    ladders : list
        The list of ladder tiles colliding with the player.
    x_velocity : int
        The x-velocity of the player. Not used for lerping.
    jumping : bool
        Whether the player is currently jumping.
    jump_counter : int
        The jump counter of the player, to compare with the max jump range when jumping.
    falling : bool
        Whether the player is currently falling.
    free_jump : bool
        Whether the player is currently free jumping.
    fox_feedback : str
        The feedback the player should display.
    fox_feedback_kind : str
        The kind of feedback, if it's due to an invalid action or if it's to be said.
    fox_feedback_surfaces : list
        The surfaces to display the feedback.
    fox_feedback_rect : pygame.Rect
        The drawn rectangle to display the feedback on.
    show_feedback : bool
        Whether to show the feedback.
    show_feedback_timer : int
        The timer for showing the feedback.
    """

    def __init__(self, velocity, max_jump_range, animation_list, screen_size, tile_size):
        """
        Parameters
        ----------
        velocity : int
        max_jump_range : int
        animation_list : list
        screen_size : tuple
            The size of the game screen (width, height).
        tile_size : int
        """
        pygame.sprite.Sprite.__init__(self)
        self.y = 0
        self.x = 0
        self.w = screen_size[0]
        self.h = screen_size[1]
        self.velocity = velocity
        self.max_jump_range = max_jump_range
        self.animation_list = animation_list
        self.direction = 'R'
        self.current_anim = 0
        self.animation_cooldown = 100
        self.last_update = pygame.time.get_ticks()
        self.action = 0
        self.moving = False
        self.blocked_right = False
        self.blocked_left = False
        self.blocked_above = False
        self.blocked_below = False
        self.image = pygame.Surface((tile_size + 3, 64))
        self.normal_rect = self.image.get_rect()
        self.crouching_rect = pygame.Rect(0, 0, self.normal_rect.width, tile_size + 2)
        self.rect = self.normal_rect
        self.colliding = False
        self.running_sound = pygame.mixer.Sound(
            "assets/audio/sounds/419181__14gpanskahonc_petr__14-man-fast-walking-dirt.wav")
        self.climbing_sound_channel = None
        self.climbing_sound_cooldown = pygame.time.get_ticks()
        self.collider = {}
        self.tile_size = tile_size
        self.goal_x = 0
        self.goal_y = 0
        self.lerping = False
        self.finished = False
        self.crouching = False
        self.finished_crouching = True
        self.crouching_cooldown = None
        self.can_climb = False
        self.climbing = False
        self.climbing_direction = 'U'
        self.ladders = []
        self.x_velocity = 0
        self.jumping = False
        self.jump_counter = 0
        self.falling = True
        self.free_jump = False
        self.fox_feedback = ""
        self.fox_feedback_kind = "Player"
        self.fox_feedback_surfaces = []
        self.fox_feedback_rect = None
        self.show_feedback = False
        self.show_feedback_timer = pygame.time.get_ticks()

    def set_location(self, x, y):
        """
        Parameters
        ----------
        x : int
        y : int
        """
        self.x = x
        self.y = y

    @staticmethod
    def __jump_sound():
        """
        Plays the jump sound.
        """
        jump_sound = pygame.mixer.Sound("assets/audio/sounds/350905__cabled_mess__jump_c_05.wav")
        jump_sound.set_volume(1)
        jump_sound.play()
        # pygame.mixer.music.stop()

    def __climb_sound(self):
        """
        Plays the climbing sound.
        """
        if self.climbing_sound_channel is None or (
                not self.climbing_sound_channel.get_busy()
                and pygame.time.get_ticks() > self.climbing_sound_cooldown + 500):
            self.climbing_sound_cooldown = pygame.time.get_ticks()
            climbing_sound = pygame.mixer.Sound("assets/audio/sounds/478054__deleted_user_10023915__ladderclimb2.wav")
            climbing_sound.set_volume(0.5)
            self.climbing_sound_channel = climbing_sound.play()

    def __play_run_sound(self):
        if self.running_sound.get_num_channels() == 0 and not self.falling:
            self.running_sound.play()
            self.running_sound.set_volume(1)

    def __stop_run_sound(self):
        self.running_sound.stop()

    def __flip_anim(self, direction):
        """
        Flips the player's animation if the direction is different from the current one.

        Parameters
        ----------
        direction : str
            The direction to flip the animation to ('R' for right, 'L' for left).
        """
        if self.direction != direction:
            self.direction = direction

    def __not_moving(self):
        self.moving = False

    def __move(self):
        if 149 < self.x + self.x_velocity:
            self.x += self.x_velocity
        # check x boundaries

        if self.jumping and self.free_jump:
            self.y -= self.velocity * 2
            self.jump_counter += 1
            if self.jump_counter == self.max_jump_range:
                self.jumping = False
                self.falling = True
                self.free_jump = False
        elif self.jumping and not self.free_jump:
            if not self.lerping:
                self.jumping = False
                self.falling = True
        elif self.falling:
            self.y += self.velocity / 5

        self.rect.center = (self.x, self.y)

    def __change_action(self, action, cooldown):
        """
        Changes the player's action and sets the animation cooldown.

        Parameters
        ----------
        action : int
            The new action for the player.
        cooldown : int
            The cooldown time for the animation's frames to be displayed.
        """
        self.action = action
        self.animation_cooldown = cooldown
        self.current_anim = 0

    def __check_can_idle(self) -> bool:
        """
        Checks if the player's animation can change to the idling action.

        Returns
        -------
        bool
        """
        return not (self.lerping or self.moving) and not self.climbing and not self.crouching and not self.jumping \
            and not self.falling

    def __check_can_run(self) -> bool:
        """
        Checks if the player's animation can change to the running action.

        Returns
        -------
        bool
        """
        return (self.lerping or self.moving) and not self.climbing and not self.crouching and not self.jumping \
            and not self.falling

    def __check_can_crouch(self) -> bool:
        """
        Checks if the player's animation can change to the crouching action.

        Returns
        -------
        bool
        """
        return self.crouching and not self.climbing and not self.jumping and not self.falling

    def __choose_action(self):
        """
        Chooses the player's action based on their current state.
        """
        if self.__check_can_run() and self.action != 1:
            self.__change_action(1, 100)
        elif self.__check_can_idle() and self.action != 0:
            self.__change_action(0, 250)
        elif self.__check_can_crouch() and self.action != 4:
            self.__change_action(4, 250)
        elif self.climbing and not self.jumping and self.action != 5:
            self.__change_action(5, 250)
        elif self.jumping and not self.climbing and self.action != 2:
            self.__change_action(2, 250)
        elif self.falling and not self.climbing and self.action != 2:
            self.__change_action(2, 250)

    def __choose_rect(self):
        """
        Chooses the player's rectangle based on whether they are crouching.
        """
        if self.crouching:
            self.rect = self.crouching_rect
        else:
            self.rect = self.normal_rect

    def __choose_anim(self) -> pygame.Surface:
        """
        Handles how the animation frame should be displayed.

        Returns
        -------
        pygame.Surface
            The chosen animation.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.current_anim += 1
            self.last_update = current_time
            if self.current_anim >= len(self.animation_list[self.action]):
                self.current_anim = 0
        if self.direction == 'R':
            animation = self.animation_list[self.action][self.current_anim]
        else:
            animation = pygame.transform.flip(self.animation_list[self.action][self.current_anim], True, False)
            animation.set_colorkey((0, 0, 0))
        return animation

    def __draw(self):
        """
        Draws the player on the display surface. This is the main method called to display the player in the game loop.
        """
        self.__choose_rect()
        display = pygame.display.get_surface()
        animation = self.__choose_anim()
        if self.crouching:
            display.blit(animation, (self.x - 48, self.y - 52))
        else:
            display.blit(animation, (self.x - 48, self.y - 48))
        '''pygame.draw.rect(pygame.display.get_surface(), 'red', self.rect, 3)  
        # Uncomment to debug Player's hit box.'''
        self.__choose_action()
        if self.show_feedback:
            self.__draw_fox_feedback(display)

    def __check_collider_direction(self) -> tuple:
        """
        Checks the direction of the collider. And returns the colliding directions

        Returns
        -------
        tuple
        """
        right = False
        left = False
        above = False
        below = False
        below_coll_y = 0
        y = self.rect.y
        x = self.rect.x
        width = self.rect.width
        height = self.rect.height
        for coll in self.collider:
            coll_x = self.collider[coll][0]
            coll_y = self.collider[coll][1]
            # pygame.draw.rect(pygame.display.get_surface(), "lightblue",
            #                   pygame.Rect(coll_x, coll_y, self.tile_size, self.tile_size), 3) # Debug collider

            if coll_y > y and (coll_x <= x + width / 2 <= coll_x + self.tile_size):
                below = True
                if not self.moving and not self.lerping and not self.climbing:
                    below_coll_y = coll_y
            if coll_y < y and (coll_x <= x + width / 2 <= coll_x + self.tile_size):
                above = True
            if coll_x > x and (y < coll_y < y + height - 1 or y + 1 < coll_y + self.tile_size - 3 < y + height):
                right = True
                self.x_velocity = 0
            if coll_x < x and (y < coll_y < y + height - 1 or y + 1 < coll_y + self.tile_size - 3 < y + height):
                left = True
                self.x_velocity = 0
        return right, left, above, below, below_coll_y

    def __process_collider(self):
        """
        Processes the collider based on the colliding directions.
        """
        right, left, above, below, below_coll_y = self.__check_collider_direction()

        if below:
            self.falling = False
            self.blocked_below = True
            if not self.moving and not self.lerping and not self.climbing:
                offset = math.ceil(self.rect.height / 2) - 1
                self.y = math.ceil(below_coll_y - offset)
        elif not self.climbing:
            self.falling = True
            self.blocked_below = False
        else:
            self.blocked_below = False
        if above and self.jumping:
            self.lerping = False
            self.y = math.floor(self.y)
        elif above:
            self.blocked_above = True
        else:
            self.blocked_above = False

        if right:
            self.blocked_right = True
        else:
            self.blocked_right = False
        if left:
            self.blocked_left = True
        else:
            self.blocked_left = False

    def __handle_climbing(self):
        """
        Handles the player's climbing action and movement. Depending on the direction, the player will climb up or down the ladder.
        """
        if len(self.ladders) > 0:
            self.can_climb = True
        else:
            self.can_climb = False

        if self.climbing:
            if self.climbing_direction == 'U':
                self.y -= self.velocity / 2
            elif self.climbing_direction == 'D':
                self.y += self.velocity / 3
            self.__climb_sound()

        if self.climbing and not self.can_climb and self.climbing_direction == 'U':
            self.climbing = False
            self.lerping = False
        elif self.climbing and (not self.can_climb or self.blocked_below) and self.climbing_direction == 'D':
            self.climbing = False
            self.lerping = False
            self.y -= 10

    def __handle_lerping(self):
        """
        Handles the player's lerping action and movement. Lerping horizontally when moving left or right, and vertically when jumping.
        """
        if self.lerping:
            if self.jumping:
                self.y = pygame.math.lerp(self.y, self.goal_y, 0.05)
                if math.floor(self.y) == math.floor(self.goal_y):
                    self.y = self.goal_y
                    self.lerping = False

            if self.moving:
                self.x = pygame.math.lerp(self.x, self.goal_x, 0.05)
                if math.ceil(self.x) == math.ceil(self.goal_x) or math.floor(self.x) == math.floor(self.goal_x):
                    self.x = self.goal_x
                    self.lerping = False
                    self.__not_moving()

    def __handle_crouching(self):
        """
        Handles the player's crouching state.
        """
        if self.crouching and not self.falling and pygame.time.get_ticks() > self.crouching_cooldown + 300:
            self.finished_crouching = True

    def __check_left_x(self) -> bool:
        """
        Checks if the player's x-coordinate is greater than a boundary.
        Not used anymore, but left for future reference.

        Returns
        -------
        bool
        """
        check_boundary = self.x - self.tile_size
        if check_boundary > 149:
            return True
        return False

    def __check_current_text(self) -> str:
        """
        Checks the current text of the feedback and formats it when meeting certain cases.

        Returns
        -------
        str
            The formatted text.
        """
        current_text = self.fox_feedback
        match current_text:
            case "canClimb":
                text = str(self.get_can_climb()) + (", I can climb." if self.get_can_climb() else ", I cannot climb.")
            case "canMoveRight":
                text = str(self.get_blocked_right()) + (
                    ", I can move right." if self.get_blocked_right() else ", I cannot move right.")
            case "canMoveLeft":
                text = str(self.get_blocked_left()) + (
                    ", I can move left." if self.get_blocked_left() else ", I cannot move left.")
            case "canJump":
                text = str(self.get_blocked_above()) + (
                    ", I can jump." if self.get_blocked_above() else ", I cannot jump.")
            case _:
                text = current_text
        if not isinstance(text, str):
            text = "This is not a valid string."
        return text

    def __process_fox_feedback(self, font):
        """
        Processes the feedback to turn it into displayable surfaces.

        Parameters
        ----------
        font : pygame.font.Font
        """
        self.fox_feedback_surfaces = []
        self.fox_feedback_rect = pygame.Rect(self.x - 100, self.y - 300, 500, 200)
        text = self.__check_current_text()
        limit = self.fox_feedback_rect.height - 50
        usermanual.parse_text(text, self.fox_feedback_surfaces, font, limit, self.fox_feedback_rect.width)
        self.fox_feedback = ""
        self.show_feedback = True
        self.show_feedback_timer = pygame.time.get_ticks()

    def __draw_fox_feedback(self, screen):
        """
        Draws the feedback on the screen, in the drawn polygon.

        Parameters
        ----------
        screen : pygame.Surface
        """
        page = 1
        start_y = self.fox_feedback_rect.top + 5
        pygame.draw.polygon(screen, (0, 0, 128),
                            [(self.x + 35, self.y - 40), (self.x + 100, self.y - 100), (self.x + 400, self.y - 100),
                             (self.x + 400, self.y - 300), (self.x - 100, self.y - 300), (self.x - 100, self.y - 100),
                             (self.x + 35, self.y - 100)])
        self.fox_feedback_rect = pygame.Rect(self.x - 100, self.y - 300, 500, 200)

        pygame.draw.rect(screen, 'green', self.fox_feedback_rect, 3, 3)
        pygame.draw.line(screen, 'green', (self.x + 35, self.y - 40), (self.x + 100, self.y - 100), 3)
        pygame.draw.line(screen, 'green', (self.x + 35, self.y - 40), (self.x + 35, self.y - 100), 3)
        text_surfaces = [x for x in self.fox_feedback_surfaces if x[1] == page]
        for i in range(len(text_surfaces)):
            current_surface = text_surfaces[i]
            screen.blit(current_surface[0], (self.fox_feedback_rect.topleft[0] + 5, start_y + 25 * i))
        if self.fox_feedback_kind != 'Player':
            cooldown = 3000
        else:
            cooldown = 1500
        if pygame.time.get_ticks() > self.show_feedback_timer + cooldown:
            self.show_feedback = False

    def say(self, fox_feedback, font, feedback_kind):
        """
        Sets the feedback and processes it.

        Parameters
        ----------
        fox_feedback : str
            The feedback to set.
        font : pygame.font.Font
        feedback_kind : str
            The kind of feedback, whether it's feedback resulted by trying an invalid action or using 'fox.say()'.
        """
        self.set_fox_feedback(fox_feedback)
        self.fox_feedback_kind = feedback_kind
        self.__process_fox_feedback(font)

    def moveRight(self):
        """
        Moves the player to the right if they are not lerping and not blocked on the right.
        """
        if not self.lerping and not self.get_blocked_right():
            self.moving = True
            self.__flip_anim('R')
            self.goal_x = self.x + self.tile_size / 2  # 22.5
            self.lerping = True
            self.__play_run_sound()

    def moveLeft(self):
        """
        Moves the player to the left if they are not lerping, and not blocked on the left.
        """
        if not self.lerping and not self.get_blocked_left():
            self.moving = True
            self.__flip_anim('L')
            self.goal_x = self.x - self.tile_size / 2  # 22.5
            self.lerping = True
            self.__play_run_sound()

    def jump(self):
        """
        Makes the player jump.
        """
        self.jumping = True
        if self.crouching:
            self.crouching = False
        self.goal_y = self.y - 1.5 * self.tile_size
        self.lerping = True
        self.__jump_sound()

    def crouch(self):
        """
        Makes the player crouch.
        """
        if not self.crouching:
            self.crouching_cooldown = pygame.time.get_ticks()
            self.crouching = True
            self.finished_crouching = False
            self.falling = True

    def climbUp(self):
        """
        Makes the player climb up.
        """
        if self.can_climb and self.blocked_below:
            self.climbing = True
            self.lerping = True
            self.climbing_direction = 'U'

    def climbDown(self):
        """
        Makes the player climb down.
        """
        if self.can_climb and not self.blocked_below:
            self.climbing = True
            self.lerping = True
            self.climbing_direction = 'D'

    def do(self) -> bool:
        """
        Performs the player's actions, handles collisions, and more. Voids the player if they have finished a level or have fallen off the screen.
        This is the main method called in the game loop to display the player.

        Returns
        -------
        bool
            True if the player has finished or fallen off the screen, False otherwise.
        """
        self.__move()
        self.__process_collider()
        self.__draw()
        if not self.moving:
            self.__stop_run_sound()
        if self.y > self.h or self.finished:
            self.__stop_run_sound()
            return True
        self.__handle_climbing()
        self.__handle_crouching()
        self.__handle_lerping()
        return False

    def is_colliding(self, collider, tile):
        """
        Adds or updates a collider tile identifier in the player's collider structure.

        Parameters
        ----------
        collider : tuple
        tile : tuple
        """
        if tile not in self.collider:
            self.collider[tile] = collider
            self.__process_collider()
        elif tile in self.collider:
            self.collider[tile] = collider
            self.__process_collider()

    def not_colliding(self, tile):
        """
        Removes a tile identifier from the player's collider structure.

        Parameters
        ----------
        tile : tuple
            The tile to remove.
        """       
        if tile in self.collider:
            self.collider.pop(tile)
            self.__process_collider()

    def set_finished(self):
        self.finished = True

    def set_fox_feedback(self, text):
        """
        Sets the feedback.

        Parameters
        ----------
        text : str
        """
        self.fox_feedback = text

    def add_ladder(self, value):
        """
        Adds a ladder to the player's list of ladders.

        Parameters
        ----------
        value : tuple
            The ladder identifier to add.
        """
        if value not in self.ladders:
            self.ladders.append(value)

    def remove_ladder(self, value):
        """
        Removes a ladder from the player's list of ladders.

        Parameters
        ----------
        value : tuple
            The ladder identifier to remove.
        """
        if value in self.ladders:
            self.ladders.remove(value)

    def get_direction(self) -> str:
        return self.direction

    def get_moving(self) -> bool:
        return self.moving

    def get_jumping(self) -> bool:
        return self.jumping

    def get_falling(self) -> bool:
        return self.falling

    def get_valid_lerping(self) -> bool:
        """
        Used in Runner to check if the player can lerp.
        """
        return not self.get_lerping() and not self.get_jumping() and self.get_finished_crouching()

    def get_invalid_lerping(self) -> bool:
        """
        Used in Runner to check if the player cannot lerp.
        """
        return self.get_finished_crouching() and not self.get_lerping()

    def get_not_jumping_or_falling(self) -> bool:
        return not self.get_lerping() and not self.get_jumping() and not self.get_falling()

    def get_can_climb(self) -> bool:
        return self.can_climb

    def get_finished_crouching(self) -> bool:
        return self.finished_crouching

    def get_lerping(self) -> bool: 
        return self.lerping

    def get_location(self) -> tuple:
        return self.x, self.y

    def get_show_feedback(self) -> bool:
        return self.show_feedback

    def get_blocked_right(self) -> bool:
        return self.blocked_right

    def get_blocked_left(self) -> bool:
        return self.blocked_left

    def get_blocked_above(self) -> bool:
        return self.blocked_above

    def get_blocked_below(self) -> bool:
        return self.blocked_below
