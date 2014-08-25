import pygame

WIN_WIDTH = 800
WIN_HEIGHT = 600
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

class Camera():
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def applyRect(self, rect):
        return rect.move(self.state.topleft)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
    def viewport(self):
        return pygame.Rect(0,0,WIN_WIDTH,WIN_HEIGHT)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)