from mazegenerator.mazegenerator import MazeGenerator
import json
import pygame as pg
import pygame.freetype
import os
from player import Player
from pacgums import load_pacgums, draw_pacgums
from maze_visu import draw_maze, build_maze_visu
from ghost import Ghost, draw_ghosts, move_all_ghosts, init_ghosts
import time


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
    screen_conf['screen'] = pg.display.set_mode((size[0] * TILE_SIZE * 2 + 300,
                                                 size[1] * TILE_SIZE * 2))
    screen_conf['clock'] = pg.time.Clock()
    screen_conf['font'] = pygame.freetype.Font("./font/PacmanFont.ttf", 24)
    return screen_conf


def load_walls():
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
    return walls


def print_score(score, screen, size):
    loc1 = (size[0] * 32 * 2 + 20, 0)
    loc2 = (size[0] * 32 * 2 + 20, 24)
    screen['font'].render_to(screen['screen'], loc1, "SCORE:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2, f"{score}", (255, 255, 255))


def print_life(sprite, lives, screen, size):
    loc1 = (size[0] * 32 * 2 + 20, 96)
    loc2 = (size[0] * 32 * 2 + 20, 120)
    screen['font'].render_to(screen['screen'], loc1, "Lives:", (255, 255, 255))
    for i in range(0, lives):
        screen['screen'].blit(sprite, (loc2[0] + i * 24, loc2[1]))


def print_all():
    pass


def respawn(player, ghosts, loc, conf, visu, maze_hexa):
    player.x, player.y = loc
    player.direction = []
    ghosts.clear()
    ghosts.update(init_ghosts(conf, visu, player, maze_hexa))


def main():
    os.system("clear")
    conf = load_config()
    size = (conf['width'], conf['height'])
    screen_conf = load_pygame(size)
    screen = screen_conf["screen"]
    spawn_loc = ((size[0]) * 32 - 12, (size[1]) * 32 - 12)
    pacman = Player((size[0]) * 32 - 12, (size[1]) * 32 - 12, "sprite/Pacman.png")
    running = True
    mazegen = MazeGenerator(size=size, seed=conf['seed'])
    mazegen.generate()
    visu = build_maze_visu(convert_maze(mazegen.maze))
    walls = load_walls()
    ghosts = init_ghosts(conf, visu, pacman, convert_maze(mazegen.maze))
    pacgums = []
    if (load_pacgums(pacgums, conf['pacgums'],
                     convert_maze(mazegen.maze), visu)) == 0:
        return
    while running:
        if pacman.just_respawned is True:
            st = time.time()
            while time.time() - st < 3:
                continue
            pacman.just_respawned = False
            pacman.alive = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        dt = screen_conf['clock'].tick(60) / 1000
        screen_conf['screen'].fill((0, 0, 0))

        print_score(pacman.score, screen_conf, size)
        print_life(pacman.get_sprite((0, 3)), pacman.lives, screen_conf, size)

        draw_maze(screen, mazegen.maze, walls)
        draw_pacgums(pacgums, screen)
        pacman.eat_pacgums(pacgums)
        pacman.touch_ghost(ghosts)
        pg.display.set_caption(f"Score: {pacman.score}. " +
                               f"Coords: {int((pacman.x + pacman._scaled[0]/2) // 32)}/{int((pacman.y + pacman._scaled[1]/2) // 32)}")
        screen_conf['screen'].blit(pacman.sprite, (pacman.x, pacman.y))

        # Supposed player collisions
        # pg.draw.rect(screen, (0, 255, 0), (pacman.x - 2, pacman.y - 2, 28, 28), 1)
        if pacman.alive is True:
            pacman.move_player(dt * 2, visu)
            move_all_ghosts(ghosts, dt * 2)
        draw_ghosts(screen, ghosts)
        if pacman.alive is False:
            respawn(pacman, ghosts, spawn_loc, conf, visu, convert_maze(mazegen.maze))
            pacman.just_respawned = True

        # Corridors suposed collisions
        # for i in range(size[1] * 2 + 1):
        #     for j in range(size[0] * 2 + 1):
        #         if visu[i][j] == " ":
        #             pg.draw.rect(screen, (0, 255, 0), (j*32 - 16, i*32 - 16, 32, 32), 1)

        pg.display.update()


if __name__ == "__main__":
    main()
