import planet, pygame, enemy, random, base, result

class Level1(base.BaseLevel):

    def __init__(self,screen):
        
        base.BaseLevel.__init__(self, screen, 1)
       
        ball = pygame.image.load("resource/sprites/600blue.png").convert_alpha()
        ball2 = pygame.image.load("resource/sprites/600yellow.png").convert_alpha()
        ball3 = pygame.image.load("resource/sprites/bunny.png").convert_alpha()
        ball4 = pygame.image.load("resource/sprites/spacehattanday.png").convert_alpha()
        
        self.addPlanet( planet.Planet(ball, -100, 200, 150, 0) )
        self.addPlanet( planet.Planet(ball4, 600, 350, 200, 0) )
        self.addPlanet( planet.Planet(ball3, 200, 600, 100, 0) )
        self.addPlanet( planet.Planet(ball2, 1800, 400, 600, 0) )
        
        self.player.forceMove(500, 350)

        for i in range(1,3):
            self.addEnemy( enemy.Enemy( random.randint(-250,300), random.randint(50,350)) )

    def loop(self, dt):
        base.BaseLevel.loop(self, dt)
        if len( self.enemies ) == 0:
            self.stop( result.Result(True,self.levelnum, 0, 0) )