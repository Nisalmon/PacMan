import pygame as pg
# from typing import Union, Tuple


class Player:
    def __init__(self, sprite_loc):
        self.x = 100
        self.y = 100
        self._sheet = pg.image.load(sprite_loc).convert_alpha()
        self._sprite_size = (32, 32)
        self.sprite = self.get_sprite((0, 0))
        self.sprite_index = 0
        self.sprite_increment = 1
        self.speed = 32
        self.anim_timer = 0
        self.__anim_speed = 0.08

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
        return img

    def move_player(self, dt):
        keys = pg.key.get_pressed()
        moving = False
        if keys[pg.K_LEFT]:
            self.x -= self.speed * dt
            moving = True
        elif keys[pg.K_RIGHT]:
            self.x += self.speed * dt
            moving = True
        elif keys[pg.K_UP]:
            self.y -= self.speed * dt
            moving = True
        elif keys[pg.K_DOWN]:
            self.y += self.speed * dt
            moving = True

        if moving:
            self.anim_timer += dt
            if self.anim_timer >= self.__anim_speed:
                self.anim_timer -= self.__anim_speed
                self.sprite_index += self.sprite_increment
                if self.sprite_index == 3 or self.sprite_index == 0:
                    self.sprite_increment *= -1
            base_sprite = self.get_sprite((0, self.sprite_index))
            if keys[pg.K_LEFT]:
                self.sprite = pg.transform.rotate(base_sprite, 180)
            elif keys[pg.K_RIGHT]:
                self.sprite = pg.transform.rotate(base_sprite, 0)
            elif keys[pg.K_UP]:
                self.sprite = pg.transform.rotate(base_sprite, 90)
            elif keys[pg.K_DOWN]:
                self.sprite = pg.transform.rotate(base_sprite, 270)
