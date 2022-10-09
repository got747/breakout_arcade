from arcade import Sprite

from config import WiDTH


class Bat(Sprite):
    def update(self):
        self.center_x += self.change_x
        if self.right >= WiDTH or self.left <= 0:
            self.change_x = 0
