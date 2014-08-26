import planet, pygame, enemy, random, base, result, resource

class Level2(base.BaseLevel):

    def __init__(self,screen):
        
        base.BaseLevel.__init__(self, screen, 2)
       
        self.addPlanet( planet.Planet(resource.planets["600blue"], 300, 300, 300, 100) )
        self.addPlanet( planet.Planet(resource.planets["600yellow"], 800, 800, 200, 40) )
        self.addPlanet( planet.Planet(resource.planets["bunny"], 800, 400, 100, 10) )
        self.addPlanet( planet.Planet(resource.planets["600blue"], 1200, 200, 250, 80) )
        self.addPlanet( planet.Planet(resource.planets["600yellow"], 750, -100, 50, 10) )
        
        self.player.forceMove(750, -150)

        for i in range(1,10):
            self.addEnemy( enemy.Enemy( random.randint(100,800), random.randint(100,800)) )

    def loop(self, dt):
        base.BaseLevel.loop(self, dt)
        if len( self.enemies ) == 0:
            self.stop( result.Result(True,self.levelnum, 0, 0) )