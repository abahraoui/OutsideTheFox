class Fox:
    """
        A class used to represent the 'fox' object as an allowed variable in a compiling unit.
        This class is used as a wrapper for the higher entity that the Fox object is associated with.
    """

    def __init__(self, higher):
        """
        Parameters
        ----------
        higher : main.code_runner.Runner
            The higher entity that the Fox object is associated with.
        """
        self.higher_entity = higher

    def moveRight(self):
        self.higher_entity.moveRight()

    def moveLeft(self):
        self.higher_entity.moveLeft()

    def jump(self):
        self.higher_entity.jump()

    def crouch(self):
        self.higher_entity.crouch()

    def climbUp(self):
        self.higher_entity.climbUp()

    def climbDown(self):
        self.higher_entity.climbDown()

    def canClimb(self) -> bool:
        return self.higher_entity.canClimb()

    def canMoveRight(self) -> bool:
        return self.higher_entity.canMoveRight()

    def canMoveLeft(self) -> bool:
        return self.higher_entity.canMoveLeft()

    def canJump(self) -> bool:
        return self.higher_entity.canJump()

    def say(self, text):
        self.higher_entity.say(text)

    def validate_problem_attempt(self, attempt):
        """
        Validates an attempt at a problem using the problem's 'validate_problem' function.

        Parameters
        ----------
        attempt : object
            The attempted solution.
        """
        valid, text = self.higher_entity.get_problem().validate_problem(attempt)
        if not valid:
            self.higher_entity.say(text)
        else:
            self.higher_entity.set_problem_completed(True)
