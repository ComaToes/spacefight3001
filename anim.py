import math, resource

class Anim():
    def __init__(self, name, frameCount, frameDuration):
        self.images = []
        for i in range(0,frameCount):
            image = resource.sprite( name + str(i) )
            self.images.append( image )
        self.image = self.images[0]
        self.frameDuration = frameDuration
        self.progress = 0
        self.totalDuration = self.frameDuration * frameCount
        
    def update(self,dt):
        self.progress = (self.progress + dt) %  self.totalDuration
        self.image = self.images[ int( math.floor( self.progress / self.frameDuration ) ) ]

    def reset(self):
        self.progress = 0
        self.image = self.images[0]
        
