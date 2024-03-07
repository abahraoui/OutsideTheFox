
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

    def validate(self, problem):
        if self.higher_entity.get_mode() == 'Bridge':
            self.higher_entity.set_problem_try(problem)
            if isinstance(problem, list) and len(problem) == self.higher_entity.get_problem_size() and len(set(problem)) == 1 and problem[0] == "wood":
                self.higher_entity.set_problem_completed(True)
            else:
                text = "\n"
                if not isinstance(problem, list):
                    text += f"Your 'bridge' object is not an array\n"
                if len(problem) != self.higher_entity.get_problem_size():
                    text += f"Your 'bridge' array is too big or too small. Remember it should be of size {self.higher_entity.get_problem_size()}\n"
                if len(set(problem)) != 1:
                    text += "You didn't represent a bridge's tile with the same kind of object.\n"
                if problem[0] != "wood":
                    text += "Your bridge is not filled with 'wood'.\n"
                self.higher_entity.say(text)
        elif self.higher_entity.get_mode() == 'Ladder':
            if isinstance(problem, list):
                num_rows = len(problem)

                if num_rows > 0 and isinstance(problem[0], list):
                    num_columns = len(problem[0])
                else:
                    num_columns = 0
                count = 0
                is_valid = False
                index_of_one = []
                for i in range(len(problem)):
                    if isinstance(problem[i], list):
                        count += problem[i].count(1)
                        if 1 in problem[i]:
                            index_of_one.append(problem[i].index(1))
                if len(set(index_of_one)) == 1:
                    is_valid = True

                if num_rows == self.higher_entity.get_problem_size()[0] and num_columns == self.higher_entity.get_problem_size()[1]:
                    self.higher_entity.set_problem_try(problem)
                    if count == self.higher_entity.get_problem_size()[2] and is_valid:
                        self.higher_entity.set_problem_completed(True)
                    else:
                        text = "\n"
                        if count != self.higher_entity.get_problem_size()[2]:
                            text += f"You are using too few or too many ladders, remember you have {self.higher_entity.get_problem_size()[2]} ladders available.\n"
                        if not is_valid:
                            text += "Your ladder is not in a vertical and aligned valid position, try changing it.\n"
                        self.higher_entity.say(text)
                else:
                    text = "\n"
                    if num_rows != self.higher_entity.get_problem_size()[0]:
                        text += "Your 'ladder' array has too many or too few rows.\n"
                    if num_columns != self.higher_entity.get_problem_size()[1]:
                        text += "Your 'ladder' array has too many or too few columns.\n"
                    self.higher_entity.say(text)
            else:
                self.higher_entity.say("Your 'ladder' object, is not an array.\n")
        elif self.higher_entity.get_mode() == 'Spike':
            self.higher_entity.set_problem_try(problem)
            if isinstance(problem, list) and len(problem) == self.higher_entity.get_problem_size() and len(set(problem)) == 1 and bool(problem[0]) is False:
                self.higher_entity.set_problem_completed(True)
            else:
                text = "\n"
                if not isinstance(problem, list):
                    text += f"Your 'spike' object is not an array\n"
                if len(problem) != self.higher_entity.get_problem_size():
                    text += f"Your 'spike' array is too big or too small. Remember it should be of size {self.higher_entity.get_problem_size()}\n"
                if len(set(problem)) != 1:
                    text += "You didn't represent a spike's tile with the same kind of object.\n"
                if bool(problem[0]) is not False:
                    text += "Your spike's tiles are not a 'False' object.\n"
                self.higher_entity.say(text)

