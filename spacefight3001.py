import pygame
import camera

import levels.level1
import levels.level2
import titles

camera.WIN_WIDTH = 1600
camera.WIN_HEIGHT = 800
camera.HALF_WIDTH = int(camera.WIN_WIDTH / 2)
camera.HALF_HEIGHT = int(camera.WIN_HEIGHT / 2)
        
pygame.init()

size = width, height = camera.WIN_WIDTH, camera.WIN_HEIGHT

screen = pygame.display.set_mode(size)

tit = titles.Titles(screen)
tit.start()

if tit.result == "Exit":
    raise SystemExit

lvls = []

lvls.append( levels.level1.Level1(screen) )
lvls.append( levels.level2.Level2(screen) )

for level in lvls:
    
    level.start()
    
    if level.result == "Fail":
        raise SystemExit

