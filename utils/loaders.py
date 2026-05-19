import pygame as pg
import pygame.freetype
from typing import Tuple, Dict, Any


def load_pygame(size: Tuple[int, int]) -> Dict[str, Any]:
    screen_conf: Dict[str, Any] = {}
    pg.init()
    pg.display.init()
    pg.mixer.init()
    screen_conf['screen'] = pg.display.set_mode((size[0],
                                                 size[1]))
    screen_conf['clock'] = pg.time.Clock()
    screen_conf['font'] = pygame.freetype.Font("./font/PacmanFont.ttf", 24)
    return screen_conf


def load_sounds() -> Dict[str, Any]:
    snd = {
        "main": pg.mixer.Sound("./sounds/main_menu.mp3"),
        "waka": pg.mixer.Sound("./sounds/wakawaka.mp3"),
        "scared": pg.mixer.Sound("./sounds/scared.mp3")
    }
    return snd


def load_walls(scale: Tuple[int, int]) -> Dict[str, Any]:
    wall_sprite = pg.transform.scale_by(
        pg.image.load("sprite/Wall.png").convert_alpha(),
        scale
        )
    corner_wall_sprite = pg.transform.scale_by(
        pg.image.load("sprite/Corner_wall.png").convert_alpha(),
        scale
        )
    incline_wall_sprite = pg.transform.scale_by(
        pg.image.load("sprite/Incline_wall.png").convert_alpha(),
        scale
        )
    four_wall_sprite = pg.transform.scale_by(
        pg.image.load("sprite/Four_wall.png").convert_alpha(),
        scale
        )
    Triple_wall_sprite = pg.transform.scale_by(
        pg.image.load("sprite/Triple_wall.png").convert_alpha(),
        scale
        )
    walls = {
        "wall": wall_sprite,
        "corner_wall": corner_wall_sprite,
        "incline_wall": incline_wall_sprite,
        "four_wall": four_wall_sprite,
        "triple_wall": Triple_wall_sprite
    }
    return walls
