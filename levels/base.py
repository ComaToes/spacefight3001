import gamemode, planet, pygame, player, bullet, camera, enemy, result

class BaseLevel(gamemode.GameMode):
    
    def __init__(self,screen):
        self.screen = screen
        
        self.mapWidth = 2048
        self.mapHeight = 2048
        
        self.background = pygame.image.load("resource/images/starfield.png").convert()
        
        self.bulletSprite = pygame.image.load("resource/sprites/tempRound.png").convert_alpha()
        
        self.heartSprite = pygame.image.load("resource/sprites/heart.png").convert_alpha()
        
        self.mobs = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = player.Player(self.mapWidth/2,self.mapHeight/2)
        self.mobs.add( self.player )
        self.people.add(self.player)
        
        self.camera = camera.Camera(camera.simple_camera, self.mapWidth, self.mapHeight)
        
        self.shootSound = pygame.mixer.Sound("resource/sounds/bazooka_fire.ogg")
        self.shootSound.set_volume(0.75)
        self.explosionSound = pygame.mixer.Sound("resource/sounds/explosion.ogg")
        self.painSound = pygame.mixer.Sound("resource/sounds/human_pain.ogg")

    def addPlanet(self, planet):
        self.mobs.add(planet)
        self.planets.add(planet)
        
    def addEnemy(self, enemy):
        self.enemies.add(enemy)
        self.people.add(enemy)
        self.mobs.add(enemy)
        
    def removeEnemy(self, enemy):
        self.enemies.remove(enemy)
        self.people.remove(enemy)
        self.mobs.remove(enemy)

    def stop(self, result):
        gamemode.GameMode.stop(self, result)
        pygame.mixer.music.stop()
        
    def start(self):
        pygame.mixer.music.load("resource/music/theme.ogg")
        pygame.mixer.music.play(-1)
        gamemode.GameMode.start(self)

    def loop(self,dt):
    
        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:
                raise SystemExit, "QUIT"
            
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    self.player.stopLeft()
                if e.key == pygame.K_d:
                    self.player.stopRight()
                    
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.player.moveLeft(dt)
                if e.key == pygame.K_d:
                    self.player.moveRight(dt)
                if e.key == pygame.K_SPACE:
                    self.player.jump()
                    
            if e.type == pygame.MOUSEBUTTONDOWN:
                # shoot
                if e.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    bx, by, bvx, bvy = self.player.shoot(mx-self.camera.state.x,my-self.camera.state.y)
                    b = bullet.Bullet(self.bulletSprite, bx, by)
                    b.vx = bvx
                    b.vy = bvy
                    self.mobs.add(b)
                    self.bullets.add(b)
                    self.shootSound.play()
                
                # boost
                if e.button == 3:
                    mx, my = pygame.mouse.get_pos()
                    self.player.boost(mx-self.camera.state.x,my-self.camera.state.y)
                    
            if e.type == pygame.MOUSEBUTTONUP:
                
                if e.button == 3:
                    self.player.stopBoost()
        
        for y in range(0,self.mapHeight,self.background.get_rect().height):
            for x in range(0,self.mapWidth,self.background.get_rect().width):
                self.screen.blit(self.background, (x,y))

        for enemy in self.enemies:
            enemy.logic(self.player, dt)
            
        for mob in self.mobs:
            mob.clearAcceleration()
            if mob.movable:
                for other in self.mobs:
                    if other != mob:
                        mob.applyGravity(other)
            if mob == self.player:
                self.player.applyBoost(dt)
            mob.move(dt)
            
        for person in self.people:
            if person.movable:
                
                for planet in pygame.sprite.spritecollide(person, self.planets, False):
                    if pygame.sprite.collide_mask(planet, person):
                        person.attachToPlanet(planet)
                        
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            if pygame.sprite.collide_mask(enemy, self.player):
                self.enemies.remove(enemy)
                self.people.remove(enemy)
                self.mobs.remove(enemy)
                self.painSound.play()
                if not self.player.damage():
                    self.stop( result.Result(False, 0, 0) )
                    
        for b in self.bullets:
            if b.movable:
                for enemy in pygame.sprite.spritecollide(b, self.enemies, False):
                    if pygame.sprite.collide_mask(enemy, b):
                        self.bullets.remove(b)
                        self.mobs.remove(b)
                        self.enemies.remove(enemy)
                        self.people.remove(enemy)
                        self.mobs.remove(enemy)
                        self.painSound.play()
                
                for planet in pygame.sprite.spritecollide(b, self.planets, False):
                    if pygame.sprite.collide_mask(planet, b):
                        b.vx = 0
                        b.vy = 0
                        b.movable = False
                        self.bullets.remove(b)
                        self.mobs.remove(b)
        
        self.camera.update(self.player)
        
        for mob in self.planets:
            self.screen.blit(mob.image, self.camera.apply(mob))
        
        for mob in self.people:
            self.screen.blit(mob.image, self.camera.apply(mob))
        
        for mob in self.bullets:
            self.screen.blit(mob.image, self.camera.apply(mob))
        
        hx = 10
        for i in range(0,self.player.health):
            self.screen.blit( self.heartSprite, (hx, 10) )
            hx += self.heartSprite.get_width() + 10
        
        pygame.display.flip()
