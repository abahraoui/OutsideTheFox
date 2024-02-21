
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
