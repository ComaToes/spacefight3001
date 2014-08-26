import planet, enemy, random, base, result, resource

class Level1(base.BaseLevel):

    def __init__(self,screen):
        
        base.BaseLevel.__init__(self, screen, 1)
       
        self.addPlanet( planet.Planet(resource.planets["600blue"], -100, 200, 150, 0) )
        self.addPlanet( planet.Planet(resource.planets["spacehattanday"], 600, 350, 200, 0) )
        self.addPlanet( planet.Planet(resource.planets["bunny"], 200, 600, 100, 0) )
        self.addPlanet( planet.Planet(resource.planets["600yellow"], 1800, 400, 600, 0) )
        
        self.player.forceMove(500, 350)

        for i in range(1,3):
            self.addEnemy( enemy.Enemy( random.randint(-250,300), random.randint(50,350)) )

    def loop(self, dt):
        base.BaseLevel.loop(self, dt)
        if len( self.enemies ) == 0:
            self.stop( result.Result(True,self.levelnum, 0, 0) )