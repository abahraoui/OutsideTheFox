
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

    def canMove(self, direction):
        return self.higher_entity.canMove(direction)

    def canJump(self):
        return self.higher_entity.canJump()
