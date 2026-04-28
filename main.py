from mazegenerator.mazegenerator import MazeGenerator
import json
import pygame as pg
import os
from player import Player
from pacgums import load_pacgums, draw_pacgums
from maze_visu import draw_maze, build_maze_visu
from ghost import Ghost


TILE_SIZE = 32


def load_config():
    conf = {}
    try:
        with open("config.json") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise Exception("There is a problem with the config.json file.")
    try:
        for elem in config:
            for key, value in elem.items():
                conf[key] = value
    except Exception:
        raise Exception("An error occured during the config parsing.")
    return conf


def convert_maze(maze: list[int]) -> list[int]:
    n_maze = []
    hexa = "0123456789ABCDEF"
    for lst in maze:
        lst_to_add = []
        for elem in lst:
            lst_to_add.append(hexa[elem])
        n_maze.append(lst_to_add)
    return n_maze


def load_pygame(size):
    screen_conf = {}
    pg.init()
    pg.display.init()
    screen_conf['screen'] = pg.display.set_mode((size[0] * TILE_SIZE * 2,
                                                 size[1] * TILE_SIZE * 2))
    screen_conf['clock'] = pg.time.Clock()
    return screen_conf


def debug_print_visu(player, visu):
    os.system("clear")
    for i in range(len(visu)):
        for j in range(len(visu[0])):
            if (i == int((player.y + 23) / 32) and
               j == int((player.x + 23) / 32)):
                print("P", end="")
            else:
                print(visu[i][j], end="")
        print()


def main():
    os.system("clear")
    conf = load_config()
    size = (conf['width'], conf['height'])
    screen_conf = load_pygame(size)
    screen = screen_conf["screen"]
    pacman = Player(size[0] * 32 - 12, size[1] * 32 - 12, "sprite/Pacman.png")
    running = True
    mazegen = MazeGenerator(size=size, seed=conf['seed'])
    mazegen.generate()
    visu = build_maze_visu(convert_maze(mazegen.maze))

    wall_sprite = pg.transform.scale2x(
        pg.image.load("sprite/Wall.png").convert_alpha()
        )
    corner_wall_sprite = pg.transform.scale2x(
        pg.image.load("sprite/Corner_wall.png").convert_alpha()
        )
    incline_wall_sprite = pg.transform.scale2x(
        pg.image.load("sprite/Incline_wall.png").convert_alpha()
        )
    four_wall_sprite = pg.transform.scale2x(
        pg.image.load("sprite/Four_wall.png").convert_alpha()
        )
    Triple_wall_sprite = pg.transform.scale2x(
        pg.image.load("sprite/Triple_wall.png").convert_alpha()
        )
    walls = {
        "wall": wall_sprite,
        "corner_wall": corner_wall_sprite,
        "incline_wall": incline_wall_sprite,
        "four_wall": four_wall_sprite,
        "triple_wall": Triple_wall_sprite
    }
    ghosts = {
        "blinky": Ghost("blinky")
    }
    pacgums = []
    if (load_pacgums(pacgums, conf['pacgums'],
                     convert_maze(mazegen.maze), visu)) == 0:
        return
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        dt = screen_conf['clock'].tick(60) / 1000
        screen_conf['screen'].fill((0, 0, 0))
        draw_maze(screen, mazegen.maze, walls)
        draw_pacgums(pacgums, screen)
        pacman.eat_pacgums(pacgums)
        pg.display.set_caption(f"Score: {pacman.score}. " +
                               f"Coords: {int((pacman.x + pacman._scaled[0]/2) // 32)}/{int((pacman.y + pacman._scaled[1]/2) // 32)}")
        screen_conf['screen'].blit(pacman.sprite, (pacman.x, pacman.y))
        pacman.move_player(dt * 2, visu)
        pg.display.update()


if __name__ == "__main__":
    main()
