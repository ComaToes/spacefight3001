import person, random, math, anim

class Enemy(person.Person):
    def __init__(self, x, y):
        walkRightAnim = anim.Anim("alien_right_", 4, 0.05)
        person.Person.__init__(self, walkRightAnim.images[0], x, y)
        self.walkSpeed = 200
        self.walkLeftAnim = anim.Anim("alien_left_", 4, 0.05)
        self.walkRightAnim = walkRightAnim
        self.staticLeftImage = self.walkLeftAnim.images[0]
        self.staticRightImage = self.walkRightAnim.images[0]
        
        
    def logic(self,player,dt):
        
        if self.planet: 
            if self.planet == player.planet:
                if (self.rotation - player.rotation) % (2*math.pi) > math.pi:
                    self.stopRight()
                    self.moveLeft(dt)
                else:
                    self.stopLeft()
                    self.moveRight(dt)
            else:
                r = random.randint(0,30);
                if r <= 2:
                    self.stopRight()
                    self.moveLeft(dt)
                elif r <= 4:
                    self.stopLeft()
                    self.moveRight(dt)
                elif r <= 6:
                    self.jump()
                #else:
                 #   self.stopLeft()
                  #  self.stopRight()