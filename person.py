import math, mob

class Person(mob.Mob):
    def __init__(self, image, x, y):
        mob.Mob.__init__(self, image, x, y, 10.0)
        self.planet = None
        self.boostx = 0
        self.boosty = 0
        self.walkSpeed = 300
        self.staticLeftImage = image
        self.staticRightImage = image
        self.walkLeftAnim = None
        self.walkRightAnim = None
        
    def move(self,dt):
        
        if self.planet:
            
            if self.movingLeft and self.walkLeftAnim:
                self.walkLeftAnim.update(dt)
                self.image0 = self.walkLeftAnim.image
            elif self.movingRight and self.walkRightAnim:
                self.walkRightAnim.update(dt)
                self.image0 = self.walkRightAnim.image
            
            circ = 2 * math.pi * self.planet.radius
            
            dr = self.vx / circ * 2 * math.pi
            
            self.rotation = (self.rotation + dr * dt) % (2*math.pi)
           
            r = self.planet.radius + self.rect0.height/2
            
            theta = self.rotation
            
            px = r * math.sin(theta)
            py = r * math.cos(theta)
            
            self.x = self.planet.x + px
            self.y = self.planet.y + py
            
            theta += math.pi
            
            self.rotate( theta/(math.pi*2)*360 )
            
        mob.Mob.move(self, dt)
    
    # On-planet movement
    
    def moveLeft(self, dt):
        if not self.movingLeft:
            if self.planet:
                self.vx += self.walkSpeed
            self.movingLeft = True
    
    def moveRight(self, dt):
        if not self.movingRight:
            if self.planet:
                self.vx -= self.walkSpeed
            self.movingRight = True
        
    def stopLeft(self):
        if self.movingLeft:
            if self.planet and (self.vx > 0 or self.movingRight):
                self.vx -= self.walkSpeed
            self.movingLeft = False
            if self.walkLeftAnim:
                self.image0 = self.walkLeftAnim.images[0]

    def stopRight(self):
        if self.movingRight:
            if self.planet and (self.vx < 0 or self.movingLeft):
                self.vx += self.walkSpeed
            self.movingRight = False
            if self.walkRightAnim:
                self.image0 = self.walkRightAnim.images[0]
   
    def jump(self):
        
        if self.planet:

            self.ax = 0
            self.ay = 0

            # convert rotational vx to space vx/vy            
            rv = self.vx
            self.vx = rv * math.sin( self.rotation+math.pi/2 )
            self.vy = rv * math.cos( self.rotation+math.pi/2 )

            # add jump velocity
            v = 300
            self.vx += v * math.sin( self.rotation )
            self.vy += v * math.cos( self.rotation )

            # reset animations so we don't jump mid-anim
            if self.walkLeftAnim:
                self.walkLeftAnim.reset()
                self.image0 = self.staticLeftImage
            if self.walkRightAnim:
                self.walkRightAnim.reset()
                self.image0 = self.staticRightImage
            
            # forces image rotation & change
            self.move(0)
            
            self.planet = None
            self.movable = True
            

    def attachToPlanet(self, planet):
        
        if self.planet != None:
            return
        
        self.planet = planet
        self.movable = False
        self.vx = 0
        self.vy = 0
        
        # determine impact point
        dx = self.x-planet.x
        dy = self.y-planet.y
        
        theta = math.atan( dx/dy )
        
        if dx > 0:
            if dy < 0:
                theta += math.pi
        elif dy < 0:
            theta += math.pi
            
        self.rotation = theta
        
        if self.movingLeft:
            self.vx += self.walkSpeed
        if self.movingRight:
            self.vx -= self.walkSpeed
        
        self.move(0)

    def shoot(self,mx,my):
        
        dx = mx-self.x
        dy = my-self.y
        
        theta = math.atan( dx/dy )
        
        if dx > 0:
            if dy < 0:
                theta += math.pi
        elif dy < 0:
            theta += math.pi
            
        v = 500
        
        bvx = v * math.sin( theta )
        bvy = v * math.cos( theta )
        
        return self.x, self.y, bvx, bvy
    
    def boost(self,mx,my):
        
        if not self.movable:
            return
        
        dx = mx-self.x
        dy = my-self.y
        
        theta = math.atan( dx/dy )
        
        if dx > 0:
            if dy < 0:
                theta += math.pi
        elif dy < 0:
            theta += math.pi
            
        acc = 50000
        
        self.boostx = acc * math.sin( theta )
        self.boosty = acc * math.cos( theta )
        
    def applyBoost(self,dt):
        self.ax += self.boostx * dt
        self.ay += self.boosty * dt
        
    def stopBoost(self):
        self.boostx = 0
        self.boosty = 0