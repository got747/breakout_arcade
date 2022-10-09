from arcade import Sprite

from config import WiDTH, HEIGHT


class Ball(Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right >= WiDTH or self.left <= 0:
            self.change_x = -self.change_x
        if self.top >= HEIGHT or self.bottom <= 0:
            self.change_y = -self.change_y
