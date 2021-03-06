import gamemode, pygame, camera, resource

class MenuItem():
    
    def __init__(self, font, text, cx, cy):
        self.font = font
        self.text = text
        self.cx = cx
        self.cy = cy
        self.normalSurface = font.render( text , 1 , (255,0,0) )
        self.highlightSurface = font.render( text , 1 , (255,255,0) )
        self.surface = self.normalSurface
        self.rect = self.normalSurface.get_rect( centerx=cx, centery=cy )
        self.highlight = False
        
    def setHighlight(self,h):
        if h:
            self.surface = self.highlightSurface
        else:
            self.surface = self.normalSurface
        self.highlight = h

class Titles(gamemode.GameMode):
    
    def __init__(self, screen):
        gamemode.GameMode.__init__(self)
        
        self.screen = screen
        
        self.background = resource.background
        
        self.mapWidth = camera.WIN_WIDTH
        self.mapHeight = camera.WIN_HEIGHT
        for y in range(0,self.mapHeight,self.background.get_rect().height):
            for x in range(0,self.mapWidth,self.background.get_rect().width):
                self.screen.blit(self.background, (x,y))
        
        # planets
        ball = pygame.transform.scale( resource.planets["600blue"], (300,300) )
        screen.blit(ball,pygame.Rect(50,50,100,100))

        ball = pygame.transform.scale( resource.planets["spacehattanday"], (400,400) )
        screen.blit(ball,pygame.Rect(800,150,100,100))

        ball = pygame.transform.scale( resource.planets["bunny"], (200,200) )
        screen.blit(ball,pygame.Rect(300,500,100,100))

        ball = pygame.transform.scale( resource.planets["600yellow"], (1200,1200) )
        screen.blit(ball,pygame.Rect(1450,-200,0,0))
        
        # text
        titleFont = pygame.font.SysFont("verdana", 80, True)
        itemFont = pygame.font.SysFont("monospace", 40, True)
        helpFont = pygame.font.SysFont("monospace", 32, True)
        creditFont = pygame.font.SysFont("monospace", 20, True)
        
        cx = screen.get_width()/2
        cy = 100
        
        text = titleFont.render( "Space" , 1 , (255,0,0) )
        rect = text.get_rect( centerx=cx - 100, centery=cy )
        self.screen.blit(text, rect)
        cy += rect.height
        text = titleFont.render( "Fight" , 1 , (0,0,255) )
        rect = text.get_rect( centerx=cx, centery=cy )
        self.screen.blit(text, rect)
        cy += rect.height
        text = titleFont.render( "3000" , 1 , (255,255,0) )
        rect = text.get_rect( centerx=cx + 100, centery=cy )
        self.screen.blit(text, rect)
        cy += rect.height

        text = titleFont.render( "(II)" , 1 , (255,255,0) )
        rect = text.get_rect( centerx=cx + 200, centery=cy )
        self.screen.blit(text, rect)
        cy += rect.height
        
        self.items = []
        
        cy += 100
        
        hy = cy
        iy = cy
        
        self.items.append( MenuItem(itemFont, "Play", cx, cy) )
        cy += 70
        
        self.items.append( MenuItem(itemFont, "Exit", cx, cy) )
        
        hx = screen.get_width()/6 * 4

        text = helpFont.render( " Walk: WASD" , 1 , (255,255,255) )
        rect = text.get_rect( x=hx, centery=hy )
        self.screen.blit(text, rect)
        hy += rect.height

        text = helpFont.render( " Jump: Space" , 1 , (255,255,255) )
        rect = text.get_rect( x=hx, centery=hy )
        self.screen.blit(text, rect)
        hy += rect.height

        text = helpFont.render( "Shoot: Left Mouse" , 1 , (255,255,255) )
        rect = text.get_rect( x=hx, centery=hy )
        self.screen.blit(text, rect)
        hy += rect.height

        text = helpFont.render( "Boost: Right Mouse" , 1 , (255,255,255) )
        rect = text.get_rect( x=hx, centery=hy )
        self.screen.blit(text, rect)
        hy += rect.height
        
        cy = self.mapHeight - 10
        text = creditFont.render( "Assets: teamawesome" , 1 , (255,255,255) )
        rect = text.get_rect()
        rect.x = 10
        rect.y = cy - rect.height
        cy -= rect.height
        self.screen.blit(text, rect)
        
        text = creditFont.render( "  Game: ComaToes" , 1 , (255,255,255) )
        rect = text.get_rect()
        rect.x = 10
        rect.y = cy - rect.height
        self.screen.blit(text, rect)
        
        # music & sounds
        self.shootSound = resource.sounds["bazooka_fire"]
        self.shootSound.set_volume(0.5)
        self.explosionSound = resource.sounds["explosion"]

    def start(self):
        pygame.mixer.music.load( resource.music["title_music"] ) 
        pygame.mixer.music.play(-1)
        gamemode.GameMode.start(self)
    
    def stop(self, result):
        gamemode.GameMode.stop(self, result)
        pygame.mixer.music.stop()
    
    def loop(self, dt):
        
        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:
                raise SystemExit, "QUIT"
            
            if e.type == pygame.KEYUP:
                None
                    
            if e.type == pygame.KEYDOWN:
                None
                    
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for item in self.items:
                    if item.rect.collidepoint(mx,my):
                        self.explosionSound.play()
                        self.stop(item.text)
                                 
            if e.type == pygame.MOUSEBUTTONUP:
                None
            
            if e.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                for item in self.items:
                    if item.rect.collidepoint(mx,my):
                        if not item.highlight:
                            self.shootSound.play()
                        item.setHighlight(True)
                    elif item.highlight:
                        item.setHighlight(False)
                    
        for item in self.items:
            self.screen.blit(item.surface, item.rect)
        
        pygame.display.flip()
