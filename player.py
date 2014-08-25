import person
import anim

class Player(person.Person):
    def __init__(self, x, y):
        walkRightAnim = anim.Anim("redtrooper_right_", 4, 0.05)
        person.Person.__init__(self, walkRightAnim.images[0], x, y)
        self.walkLeftAnim = anim.Anim("redtrooper_left_", 4, 0.05)
        self.walkRightAnim = walkRightAnim
        self.staticLeftImage = self.walkLeftAnim.images[0]
        self.staticRightImage = self.walkRightAnim.images[0]
