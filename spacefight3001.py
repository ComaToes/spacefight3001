import pygame
import camera

import resource
import levels.level1
import levels.level2
import levels.randomlevel
import titles
import summary

camera.WIN_WIDTH = 1600
camera.WIN_HEIGHT = 800
camera.HALF_WIDTH = int(camera.WIN_WIDTH / 2)
camera.HALF_HEIGHT = int(camera.WIN_HEIGHT / 2)
        
pygame.init()

size = width, height = camera.WIN_WIDTH, camera.WIN_HEIGHT

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Space Fight 3000 (II)")

resource.init()

while True:

    tit = titles.Titles(screen)
    tit.start()
    
    if tit.result == "Exit":
        raise SystemExit

    lvls = []
    
    lvls.append( levels.level1.Level1(screen) )
    lvls.append( levels.level2.Level2(screen) )

    for level in lvls:
        
        level.start()
        
        s = summary.LevelSummary(screen, level.result)
        s.start()
    
        if not s.result.success:
            break

    levelnum = len(lvls)+1

    while s.result.success:

        level = levels.randomlevel.RandomLevel(screen,levelnum)
        level.start()
        
        s = summary.LevelSummary(screen, level.result)
        s.start()
        
        levelnum += 1
