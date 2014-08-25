import pygame

class GameMode():
    
    def __init__(self):
        self.running = False
        self.result = None
    
    def start(self):
        
        time = pygame.time.get_ticks()

        clock = pygame.time.Clock()
        
        self.running = True
        
        while(self.running):
            
            clock.tick(60)
        
            now = pygame.time.get_ticks()    
            dt = (now - time) / 1000.0
            time = now
            
            self.loop(dt)
            
    def stop(self,result):
        self.running = False
        self.result = result
        
    def loop(self,dt):
        None