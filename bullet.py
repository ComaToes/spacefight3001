import mob

class Bullet(mob.Mob):
    def __init__(self, image, x, y):
        mob.Mob.__init__(self, image, x, y, 1.0)