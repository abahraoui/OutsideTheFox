from abc import abstractmethod
from main.listener_interface import ListenerInterface


class UserInputInterface(ListenerInterface):
    """

    This class is meant to be inherited when implementing a user input game, like the implemented TextEditor class, or a potential DragAndDropEditor.

    Methods
    -------
    draw_feedback(screen):
    draw_error_feedback(screen):
    draw():
    set_user_answer(value):
    get_user_answer():
    """

    ...

    @abstractmethod
    def draw_feedback(self, screen):
        """
        To be implemented in a concrete class that inherits from this interface.

        This method is meant to draw feedback in the case of a valid use.

        Parameters
        ----------
        screen : pygame.Surface

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def draw_error_feedback(self, screen):
        """
        To be implemented in a concrete class that inherits from this interface.

        This method is meant to draw feedback in the case of an error made by the user.

        Parameters
        ----------
        screen : pygame.Surface

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def draw(self):
        """
        To be implemented in a concrete class that inherits from this interface.

        This method is meant to draw the whole class component on the game's screen.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def set_user_answer(self, value):
        """
        To be implemented in a concrete class that inherits from this interface.

        This method is meant to set the user's input. Use it with on your own relevant class attribute.

        Parameters
        ----------
        value : object

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

    @abstractmethod
    def get_user_answer(self) -> object:
        """
        To be implemented in a concrete class that inherits from this interface.

        This method is meant to get the user's answer to process it in another class.
        Use it with your own relevant class attribute.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")
