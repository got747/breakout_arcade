from arcade import Sprite, load_texture

class Block( Sprite):
    def __init__(self, tuple_texturs):
        super().__init__(filename=tuple_texturs[0], scale=0.2)
        self.hp = 2
        if len(tuple_texturs) > 1:
            self.append_texture(load_texture(tuple_texturs[1]))

    def hit(self):
        self.hp -= 1
        if len(self.textures) > 1:
            self.set_texture(1)

        if self.hp == 0:
            self.kill()


