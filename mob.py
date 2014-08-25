import pygame, math, constants

class Mob(pygame.sprite.Sprite):
    def __init__(self, image, x, y, mass):
        pygame.sprite.Sprite.__init__(self)
        self.rotation = 0
        self.image0 = image
        self.image = pygame.transform.rotate(self.image0, 0)
        self.rect0 = self.image0.get_rect()
        self.rect = image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.movable = True
        self.movingLeft = False
        self.movingRight = False
        
    def forceMove(self,x,y):
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y
        
    def rotate(self,angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
    def move(self,dt):
        
        if self.movable:
            self.vx += self.ax * dt
            self.vy += self.ay * dt
            self.x += self.vx * dt
            self.y += self.vy * dt

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def clearAcceleration(self):
        self.ax = 0
        self.ay = 0

    def applyGravity(self, mob):

        if not self.movable:
            return
        
        dx = self.x-mob.x
        dy = self.y-mob.y
        dist2 = dx*dx + dy*dy
        
        if dist2 == 0:
            return
        
        f = (-constants.GRAVITY) * ( self.mass * mob.mass ) / dist2
        acc = f/self.mass
        
        if dy == 0:
            dy = 0.0000001
        
        theta = math.atan( dx/dy )
        
        if dx > 0:
            if dy < 0:
                theta += math.pi
        elif dy < 0:
            theta += math.pi
        
        ax = math.sin( theta ) * acc
        ay = math.cos( theta ) * acc
        self.ax += ax
        self.ay += ay