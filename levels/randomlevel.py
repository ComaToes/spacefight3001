import planet, pygame, enemy, random, base, result, resource

class RandomLevel(base.BaseLevel):

    def __init__(self,screen,levelnum):
        
        base.BaseLevel.__init__(self, screen, levelnum)
        
        for i in range( 0, random.randint(4,10) ):
            overlap = True
            while overlap:
                x = random.randint( 0, self.mapWidth )
                y = random.randint( 0, self.mapHeight )
                r = random.randint( 50, 300 )
                img = resource.planets.values()[ random.randint(0,len(resource.planets)-1) ]
                p = planet.Planet(img, x, y, r, 0)
                overlap = pygame.sprite.spritecollideany(p, self.planets)

            self.addPlanet( p )

        x = random.randint( 0, self.mapWidth )
        y = random.randint( 0, self.mapHeight )
        self.player.forceMove(x,y)

        for i in range(1, random.randint(7,20) ):
            x = random.randint( 200, self.mapWidth-200 )
            y = random.randint( 200, self.mapHeight-200 )
            self.addEnemy( enemy.Enemy( x, y ) )
    
    def loop(self, dt):
        base.BaseLevel.loop(self, dt)
        if len( self.enemies ) == 0:
            self.stop( result.Result(True, self.levelnum, 0, 0) )