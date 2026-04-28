import pygame as pg


class Ghost:
    def __init__(self, name):
        self.__name = name
        self._sprite_size = (32, 32)
        self._scaled = (24, 24)
        self._sheet = self.load_sprite_sheet()
        self.sprite = self.get_sprite((0, 0))
        self.path = []

    def load_sprite_sheet(self):
        if self.__name == "blinky":
            return pg.image.load("./sprite/blinky.png").convert_alpha()

    def get_sprite(self, loc, colorkey=(255, 255, 255)):
        x = loc[1] * self._sprite_size[0]
        y = loc[0] * self._sprite_size[1]

        rect = pg.Rect(x, y, *self._sprite_size)
        img = pg.Surface(self._sprite_size, pg.SRCALPHA).convert_alpha()
        img.blit(self._sheet, (0, 0), rect)
        if colorkey:
            if colorkey == -1:
                colorkey = img.get_at((0, 0))
            img.set_colorkey(colorkey, pg.RLEACCEL)
        return pg.transform.scale(img, (self._scaled[0],
                                        self._scaled[1]))

    def set_algo(self):
        if self.__name == "blinky":
            self.algo_blinky()

    def algo_blinky(self):
        pass
