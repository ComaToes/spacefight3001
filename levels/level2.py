import planet, pygame, enemy, random, base, result

class Level2(base.BaseLevel):

    def __init__(self,screen):
        
        base.BaseLevel.__init__(self, screen)
       
        ball = pygame.image.load("resource/sprites/600blue.png").convert_alpha()
        ball2 = pygame.image.load("resource/sprites/600yellow.png").convert_alpha()
        ball3 = pygame.image.load("resource/sprites/bunny.png").convert_alpha()
        
        self.addPlanet( planet.Planet(ball, 300, 300, 300, 100) )
        self.addPlanet( planet.Planet(ball2, 800, 800, 200, 40) )
        self.addPlanet( planet.Planet(ball3, 800, 400, 100, 10) )
        self.addPlanet( planet.Planet(ball, 1200, 200, 250, 80) )
        self.addPlanet( planet.Planet(ball2, 750, -100, 50, 10) )
        
        self.player.forceMove(750, -150)

        for i in range(1,10):
            self.addEnemy( enemy.Enemy( random.randint(100,800), random.randint(100,800)) )

    def loop(self, dt):
        base.BaseLevel.loop(self, dt)
        if len( self.enemies ) == 0:
            self.stop( result.Result(True, 0, 0) )