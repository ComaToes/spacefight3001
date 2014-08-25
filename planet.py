import mob, pygame, math

class Planet(mob.Mob):
    def __init__(self, image, x, y, radius, massMultiplier):
        image = pygame.transform.scale(image, (radius*2,radius*2))
        density = 350
        mass = math.pi * radius * radius * density
        mob.Mob.__init__(self, image, x, y, mass)
        self.radius = radius
        self.movable = False