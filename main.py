from mazegenerator.mazegenerator import MazeGenerator
import json
import pygame as pg
import os
from player import Player
from maze_visu import generate_maze_visu


WIDTH = 1080
HEIGHT = 720
RES = (WIDTH, HEIGHT)


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


def load_pygame():
    screen_conf = {}
    pg.init()
    pg.display.init()
    screen_conf['screen'] = pg.display.set_mode(RES)
    screen_conf['clock'] = pg.time.Clock()
    return screen_conf


def load_walls(maze):
    wall = pg.image.load("wall.png")


def main():
    os.system("clear")
    conf = load_config()
    screen_conf = load_pygame()
    pacman = Player("Pacman.png")
    running = True
    size = (conf['width'], conf['height'])
    mazegen = MazeGenerator(size=size, seed=conf['seed'])
    mazegen.generate()
    generate_maze_visu(convert_maze(mazegen.maze))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        dt = screen_conf['clock'].tick(60) / 1000
        screen_conf['screen'].fill((0, 0, 0))
        screen_conf['screen'].blit(pacman.sprite, (pacman.x, pacman.y))
        pacman.move_player(dt * 2)
        pg.display.update()

    maze_output = convert_maze(mazegen.maze)
    # print(maze_output)


if __name__ == "__main__":
    main()
