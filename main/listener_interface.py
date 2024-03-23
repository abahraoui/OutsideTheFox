
class ListenerInterface:
    """
    A class used as an interface for listeners in an application.

    This class is meant to be inherited by other classes to use the 'Observer' pattern by implementing the `update` method.

    ...

    Methods
    -------
    update(message):
    """
    def update(self, message):
        """
        To be implemented in a concrete class that inherits from this interface.

        This method is meant to update the state of the listener based on the received message.

        Parameters
        ----------
        message : object

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Implement this in a concrete class.")

