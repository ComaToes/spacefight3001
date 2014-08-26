import gamemode, planet, pygame, player, bullet, camera, enemy, result, resource

class BaseLevel(gamemode.GameMode):
    
    def __init__(self,screen,levelnum):
        self.screen = screen
        self.levelnum = levelnum
        
        self.mapWidth = 2048
        self.mapHeight = 2048
        
        resource.planets
        
        self.background = resource.background
        
        self.bulletSprite = resource.sprite("tempRound")
        self.boostSprite = resource.sprite("splode2")
        self.heartSprite = resource.sprite("heart")
        self.arrowSpriteTop = resource.sprite("arrow")
        self.arrowSpriteLeft = pygame.transform.rotate( self.arrowSpriteTop, 90 )
        self.arrowSpriteRight = pygame.transform.rotate( self.arrowSpriteTop, -90 )
        self.arrowSpriteBottom = pygame.transform.rotate( self.arrowSpriteTop, 180 )
        
        self.mobs = pygame.sprite.Group()
        self.planets = pygame.sprite.Group()
        self.people = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = player.Player(self.mapWidth/2,self.mapHeight/2)
        self.mobs.add( self.player )
        self.people.add(self.player)
        
        self.camera = camera.Camera(camera.simple_camera, self.mapWidth, self.mapHeight)
        
        self.shootSound = resource.sounds["bazooka_fire"]
        self.shootSound.set_volume(0.75)
        self.explosionSound = resource.sounds["explosion"]
        self.painSound = resource.sounds["human_pain"]
        self.boostSound = resource.sounds["sound_psh"]
        self.boostSound.set_volume(0.3)

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
        self.boostSound.stop()
        
    def start(self):
        pygame.mixer.music.load( resource.music["theme"] )
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
                if e.button == 3 and self.player.movable:
                    mx, my = pygame.mouse.get_pos()
                    self.player.boost(mx-self.camera.state.x,my-self.camera.state.y)
                    self.boostSound.play()
                    
            if e.type == pygame.MOUSEBUTTONUP:
                
                if e.button == 3:
                    self.player.stopBoost()
                    self.boostSound.stop()
        
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
                    self.stop( result.Result(False,self.levelnum, 0, 0) )
                    
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
            pos = self.camera.apply(mob)
            vp = self.camera.viewport()
            if vp.contains(pos):
                self.screen.blit(mob.image, pos)
            else:
                c = intersect( 0.0, 0.0, 0.0, vp.h, vp.w/2, vp.h/2, pos.x, pos.y )
                if c:
                    x,y = c
                    self.screen.blit(self.arrowSpriteLeft, c)
                    x += self.arrowSpriteLeft.get_width() + 5
                    y -= (mob.image0.get_height() - self.arrowSpriteLeft.get_height()) / 2
                    self.screen.blit(mob.image0, (x,y))

                c = intersect( 0.0, 0.0, vp.w, 0.0, vp.w/2, vp.h/2, pos.x, pos.y )
                if c:
                    x,y = c
                    self.screen.blit(self.arrowSpriteTop, c)
                    x -= (mob.image0.get_width() - self.arrowSpriteTop.get_width()) / 2
                    y += self.arrowSpriteLeft.get_height() + 5
                    self.screen.blit(mob.image0, (x,y))

                c = intersect( vp.w, 0.0, vp.w, vp.h, vp.w/2, vp.h/2, pos.x, pos.y )
                if c:
                    x,y = c
                    x -= self.arrowSpriteBottom.get_width()
                    self.screen.blit(self.arrowSpriteRight, (x,y))
                    x -= mob.image0.get_width() + 5
                    y -= (mob.image0.get_height() - self.arrowSpriteRight.get_height()) / 2
                    self.screen.blit(mob.image0, (x,y))
                
                c = intersect( 0.0, vp.h, vp.w, vp.h, vp.w/2, vp.h/2, pos.x, pos.y )
                if c:
                    x,y = c
                    y -= self.arrowSpriteBottom.get_height()
                    self.screen.blit(self.arrowSpriteBottom, (x,y))
                    x -= (mob.image0.get_width() - self.arrowSpriteTop.get_width()) / 2
                    y -= mob.image0.get_height() + 5
                    self.screen.blit(mob.image0, (x,y))

        if self.player.boostx != 0 or self.player.boosty != 0:
            # draw boost
            pos = self.camera.apply(self.player)
            self.screen.blit(self.boostSprite, (pos.x-self.player.boostx/4000, pos.y-self.player.boosty/4000))
            
        for mob in self.bullets:
            self.screen.blit(mob.image, self.camera.apply(mob))
        
        hx = 10
        for i in range(0,self.player.health):
            self.screen.blit( self.heartSprite, (hx, 10) )
            hx += self.heartSprite.get_width() + 10
        
        if self.player.x < -self.mapWidth or self.player.x > self.mapWidth*2 or self.player.y < -self.mapHeight or self.player.y > self.mapHeight*2:
            self.stop( result.Result(False,self.levelnum,0,0) )
        
        pygame.display.flip()

def intersect(p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
    
    s10_x = p1_x - p0_x
    s10_y = p1_y - p0_y
    s32_x = p3_x - p2_x
    s32_y = p3_y - p2_y

    denom = s10_x * s32_y - s32_x * s10_y
    if denom == 0:
        return False
    denomPositive = denom > 0;

    s02_x = p0_x - p2_x
    s02_y = p0_y - p2_y
    s_numer = s10_x * s02_y - s10_y * s02_x
    if (s_numer < 0) == denomPositive:
        return False

    t_numer = s32_x * s02_y - s32_y * s02_x
    if ((t_numer < 0) == denomPositive):
        return False

    if (((s_numer > denom) == denomPositive) or ((t_numer > denom) == denomPositive)):
        return False
    
    # Collision detected
    t = t_numer / denom
    
    i_x = p0_x + (t * s10_x)
    i_y = p0_y + (t * s10_y)
    
    return (i_x, i_y)

def intersect2(p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
    
    s1_x = p1_x - p0_x;     s1_y = p1_y - p0_y;
    s2_x = p3_x - p2_x;     s2_y = p3_y - p2_y;

    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y);
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y);

    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        i_x = p0_x + (t * s1_x);
        i_y = p0_y + (t * s1_y);
        return (i_x,i_y);

    return False