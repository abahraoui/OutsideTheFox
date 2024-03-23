import ast
import sys
import pygame
from main import fox_class, user_execution_visitor


class Runner:
    """
    The Runner class parse, sanitize, then execute the code written in the TextEditor.

    Attributes
    ----------
    text_list : list
    player : Player
    queue : list
        Queue of actions to be performed.
    listeners : list
        A part of the 'Observer' pattern, a list of objects listening to it, contains the TextEditor instance.
    visitor : UserExecutionVisitor
        Visitor object to sanitize user's code.
    finished : bool
        Flag indicating whether the execution of actions is finished.
    last_action_timer : int
        Timer since the last action performed.
    fox : Fox
        The front object used to be called by the execution, to add a layer of abstraction and improve security.
    error_feedback : list
        Array of error feedback messages to be displayed by the TextEditor class.
    screen : pygame.Surface
    font : pygame.Font
    fox_feedback_queue : list
        Queue of feedback messages to be displayed by the Player class.
    mode : str
        Mode of the game ("Player" or "Problem").
    problem : Problem
        The current problem to be solved.
    problem_completed : bool
        Flag indicating whether the current problem is completed.
    problem_try : Try
        The current attempt at solving the problem.
    busy : bool
        Flag indicating whether an action is executed.
    """

    def __init__(self, player):
        """
        Parameters
        ----------
        player : Player
        """
        self.text_list = []
        self.player = player
        self.queue = []
        self.listeners = []
        self.visitor = user_execution_visitor.UserExecutionVisitor()
        self.finished = True
        self.last_action_timer = 0
        self.fox = fox_class.Fox(self)
        self.error_feedback = []
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/joystix monospace.otf', 16)
        self.fox_feedback_queue = []
        self.mode = "Player"
        self.problem = None
        self.problem_completed = False
        self.problem_try = None
        self.busy = False

    def validate(self, text_to_validate):
        """
        Parses, sanitzes the user's code, then executes it.

        Parameters
        ----------
        text_to_validate : list
            Array of strings representing the user's code.

        Returns
        -------
        None
        """
        self.text_list = text_to_validate
        self.error_feedback = []

        def __restrict_vars() -> dict:
            """
            Restrict the variables available during execution based on the game mode and problem. 

            Returns
            -------
            dict
                A dictionary containing the variables available during execution.
            """
            execution_variables = {"fox": self.fox}
            if self.mode == "Problem":
                match self.problem.get_id():
                    case "bridge":
                        execution_variables["bridge"] = []
                    case "ladder":
                        execution_variables["ladder"] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]
                    case "spike":
                        execution_variables["spike"] = [True, True, True]
                    case _:
                        raise NotImplementedError("This problem is not yet implemented in here.")
            return execution_variables

        def __write_text_to_file():
            """
            Write the user's code to the execution file named 'user_execution.py'. 
            If the game mode is "Problem", it also writes a validation line at the end of the file for the front's validate function to be automatically called and verify the attempt.
            """
            with open('main/user_execution.py', 'w') as file:
                for text in self.text_list:
                    file.write(text + "\n")
                if self.mode == "Problem":
                    file.write(f"fox.validate_problem_attempt({self.problem.get_id()})")
                file.close()

        def __parse_code() -> ast.Module:
            """
            Parse the code written in 'user_execution.py' using the ast module. 
            It sanitizes the code using the 'Visitor' pattern by removing 'Import' and dangerous built-in functions like 'eval' and 'exec'.

            Returns
            -------
            ast.Module
                The abstract syntax tree of the parsed code.
            """
            with open('main/user_execution.py', 'r') as file:
                read_content = file.read()
                tree = ast.parse(str(read_content))
                for elem in tree.body:
                    self.visitor.visit(elem)
                    if isinstance(elem, ast.Expr) and elem.value and isinstance(elem.value, ast.Pass):
                        tree.body.remove(elem)
                    # removes import statements
                    elif isinstance(elem, ast.Import):
                        tree.body.remove(elem)
                return tree

        def __process_error(exception):
            """
            In the event of a syntax error or an exception during execution, this function stores the error's message and line to be returned to the TextEditor class.

            Parameters
            ----------
            exception : Exception
            """
            exc_type, exc_value, exc_traceback = sys.exc_info()

            if not issubclass(exception.__class__, SyntaxError):
                while exc_traceback.tb_next:
                    exc_traceback = exc_traceback.tb_next

                line_number = exc_traceback.tb_lineno
            else:
                line_number = exc_value.end_lineno

            self.error_feedback.append(f"Error occurred at line {line_number}")
            self.error_feedback.append(str(exc_value))
            self.error_feedback.append(line_number)
            self.queue = []

        self.finished = False
        if not self.text_list:
            return
        try:
            __write_text_to_file()
            code = __parse_code()
            obj = compile(code, filename="<ast>", mode="exec")
            # restricts the allowed variables to 'fox' or problem relevant variables.
            allowed_vars = __restrict_vars()
            exec(obj, allowed_vars)
        except Exception as e:
            __process_error(e)

    def process_queue(self) -> tuple:
        """
        Process the actions in the queue. It checks the first action in the queue and performs the corresponding action 

        Returns
        -------
        tuple
            A tuple containing the wanted scroll direction and a boolean indicating whether scrolling shall start.

        Raises
        ------
        NotImplementedError
            If the action is not yet implemented in the queue.
        """

        def __invalid_action(text) -> tuple:
            """
            Handles an invalid action. Makes the player display text feedback.

            Parameters
            ----------
            text : str
                The text to be displayed by the player.
            Returns
            -------
            tuple
                The return will always be (0, False) as the scroll won't happen.
            """
            self.say(text)
            self.queue.pop(0)
            return 0, False

        def __valid_action(goal_scroll, scrolling, ):
            """
            Handles a valid action.

            Parameters
            ----------
            goal_scroll : int or float
            scrolling : bool

            Returns
            -------
            tuple
                The scroll might or not be employed, depending on the action to be performed.
            """
            self.queue.pop(0)
            return goal_scroll, scrolling

        def __process_move(movement_kind, scroll_direction, text):
            blocked = self.player.get_blocked_left() if movement_kind == 1 else self.player.get_blocked_right()
            move = self.player.moveLeft if movement_kind == 1 else self.player.moveRight
            if not blocked and self.player.get_valid_lerping():
                move()
                return __valid_action(scroll_direction, True)
            if blocked and self.player.get_invalid_lerping():
                return __invalid_action(text)

        if self.busy:
            return 0, False
        match self.queue[0]:
            case 0:
                return __process_move(0, 1, "Ouch I cannot move right, I am blocked!")
            case 1:
                return __process_move(1, -1, "Unfortunately I cannot move left, I am blocked!")
            case 2:
                if not self.player.get_blocked_above() and not self.player.get_falling() and self.player.get_valid_lerping():
                    self.player.jump()
                    return __valid_action(0, False)
                if self.player.get_blocked_above() and self.player.get_invalid_lerping():
                    return __invalid_action("Oops I cannot jump above, I am blocked!")
            case 3:
                if self.player.get_not_jumping_or_falling():
                    self.player.crouch()
                    return __valid_action(0, False)
            case 4:
                if self.player.get_not_jumping_or_falling() and self.player.get_can_climb():
                    self.player.climbUp()
                    return __valid_action(0, False)
                if not self.player.get_can_climb():
                    return __invalid_action("Sadly I cannot climb up, there is no valid ladder!")
            case 5:
                if not self.player.get_lerping() and not self.player.get_jumping() and not self.player.get_blocked_below() and self.player.get_can_climb():
                    self.player.climbDown()
                    return __valid_action(0, False)
                if self.player.get_blocked_below() or not self.player.get_can_climb():
                    return __invalid_action("Darn I cannot climb down, "
                                            "there is no ladder or a floor tile is blocking me!")
            case 6:
                if not self.player.get_show_feedback():
                    self.player.say(self.fox_feedback_queue[0], self.font, self.mode)
                    self.fox_feedback_queue.pop(0)
                    return __valid_action(0, False)
            case _:
                raise NotImplementedError("This action is not yet implemented in the queue.")

    def finish_exec(self):
        """
        Marks the execution as finished, and notifies the listening TextEditor of it.
    
        """
        self.finished = True
        message = self.error_feedback if self.has_error() else "Done"
        self.notify(message)
        self.last_action_timer = pygame.time.get_ticks()

    def is_done(self) -> bool:
        """
        Checks if the execution is done.

        Returns
        -------
        bool
            Whether the execution is done.
        """
        if self.finished and pygame.time.get_ticks() > self.last_action_timer + 800:
            return True
        self.notify("Running")
        return False

    def set_problem_completed(self, value):
        """
        Parameters
        ----------
        value : bool
        """
        self.problem_completed = value

    def set_problem(self, problem):
        """
        Parameters
        ----------
        problem : Problem
        """
        self.problem = problem

    def set_problem_try(self, value):
        """
        Parameters
        ----------
        value : object
        """
        self.problem_try = value

    def set_fox_feedback(self, text):
        """
        Parameters
        ----------
        text : str
        """
        self.fox_feedback_queue.append(text)

    def set_mode(self, value):
        """
        Parameters
        ----------
        value : str
        """
        self.mode = value

    def set_busy(self, value):
        """
        Parameters
        ----------
        value : bool
        """
        self.busy = value

    def subscribe(self, listener):
        """
        Parameters
        ----------
        listener : ListenerInterface
        """
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        """
        Parameters
        ----------
        listener : ListenerInterface
        """
        self.listeners.remove(listener)

    def notify(self, message):
        """
        Notifies all the listeners with the given message.

        Parameters
        ----------
        message : object
        """
        for listener in self.listeners:
            listener.update(message)

    def has_error(self) -> list:
        return self.error_feedback

    def get_mode(self) -> str:
        return self.mode

    def get_error_feedback(self) -> list:
        return self.error_feedback

    def get_queue(self) -> list:
        if not self.queue and not self.finished:
            self.finish_exec()
        return self.queue

    def get_problem(self) -> object:
        return self.problem

    def get_problem_completed(self) -> bool:
        return self.problem_completed

    def get_problem_try(self) -> object:
        return self.problem_try

    '''Callback functions used by the fox_class.'''
    def moveRight(self):
        self.queue.append(0)

    def moveLeft(self):
        self.queue.append(1)

    def jump(self):
        self.queue.append(2)

    def crouch(self):
        self.queue.append(3)

    def climbUp(self):
        self.queue.append(4)

    def climbDown(self):
        self.queue.append(5)

    def canClimb(self) -> bool:
        return self.player.get_can_climb()

    def canMoveRight(self) -> bool:
        return not self.player.get_blocked_right()

    def canMoveLeft(self) -> bool:
        return not self.player.get_blocked_left()

    def canJump(self) -> bool:
        return not self.player.get_blocked_above()

    def say(self, text):
        """
        Parameters
        ----------
        text : str
            The text for the fox to say.
        """
        self.queue.append(6)
        self.set_fox_feedback(text)
