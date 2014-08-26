import gamemode, pygame, camera, titles
import result

class LevelSummary(gamemode.GameMode):
    
    def __init__(self, screen, result):
        gamemode.GameMode.__init__(self)
        
        self.screen = screen
        self.result = result
        
        self.background = pygame.image.load("resource/images/starfield.png").convert()
        
    def start(self):
        pygame.mixer.music.load("resource/music/title_music.ogg")
        pygame.mixer.music.play(-1,3)
        
        self.mapWidth = camera.WIN_WIDTH
        self.mapHeight = camera.WIN_HEIGHT
        for y in range(0,self.mapHeight,self.background.get_rect().height):
            for x in range(0,self.mapWidth,self.background.get_rect().width):
                self.screen.blit(self.background, (x,y))
                
        ball = pygame.image.load("resource/sprites/600blue.png").convert_alpha()
        ball = pygame.transform.scale(ball,(1200,1200))
        self.screen.blit(ball,pygame.Rect(-1050,-200,0,0))
        
        ball = pygame.image.load("resource/sprites/bunny.png").convert_alpha()
        ball = pygame.transform.scale(ball,(1200,1200))
        self.screen.blit(ball,pygame.Rect(1450,-200,0,0))

        titleFont = pygame.font.SysFont("monospace", 100, True)
        itemFont = pygame.font.SysFont("monospace", 32, True)
        
        cx = self.screen.get_width()/2
        cy = 200
        
        if self.result.success:
            titleText = "Level " + str(self.result.levelnum) + " Complete"
        else:
            titleText = "You Died"
        
        text = titleFont.render( titleText , 1 , (255,0,0) )
        rect = text.get_rect( centerx=cx, centery=cy )
        self.screen.blit(text, rect)
        cy += rect.height
        
        cy += 50
       
        self.items = []

        if self.result.success:
            menuText = "Next Level"
            self.items.append( titles.MenuItem(itemFont, menuText, cx, cy) )
            cy += 50

        menuText = "Quit to Menu"
        self.items.append( titles.MenuItem(itemFont, menuText, cx, cy) )
        cy += 50
        
        # sounds
        self.shootSound = pygame.mixer.Sound("resource/sounds/bazooka_fire.ogg")
        self.shootSound.set_volume(0.5)
        self.explosionSound = pygame.mixer.Sound("resource/sounds/explosion.ogg")
        
        gamemode.GameMode.start(self)
        
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
                        # hacky continue condition
                        self.stop( result.Result(item.text == "Next Level", 0, 0, 0) )
                                 
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
        