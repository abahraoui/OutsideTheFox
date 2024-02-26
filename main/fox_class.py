
class Fox:

    def __init__(self, higher):
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

    def canClimb(self):
        return self.higher_entity.canClimb()

    def canMoveRight(self):
        return self.higher_entity.canMoveRight()

    def canMoveLeft(self):
        return self.higher_entity.canMoveLeft()
    def canJump(self):
        return self.higher_entity.canJump()

    def say(self, text):
        self.higher_entity.say(text)

    def validate(self, problem, wood=False):
        if self.higher_entity.get_mode() == 'Bridge':
            if problem == wood:
                self.higher_entity.set_problem_completed(True)
        elif self.higher_entity.get_mode() == 'Ladder':
            num_rows = len(problem)
            if num_rows > 0:
                num_columns = len(problem[0])
            else:
                num_columns = 0
            if num_rows == 3 and num_columns == 4:
                self.higher_entity.set_problem_try(problem)
                if problem == [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]:
                    self.higher_entity.set_problem_completed(True)
        elif self.higher_entity.get_mode() == 'Spike':
            if problem == [False, False, False]:
                self.higher_entity.set_problem_completed(True)
