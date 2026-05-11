from mazegenerator.mazegenerator import MazeGenerator
import json
import pygame as pg
import pygame.freetype
import os
from player import Player, init_player
from pacgums import load_pacgums
from maze_visu import build_maze_visu
from ghost import Ghost, move_all_ghosts, init_ghosts
from game_end import time_out, game_over
from environment import draw_env
from buttons import init_buttons, draw_button
from scorers import load_scorers, fill_scorers
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


def get_leaderboard(screen, scorers, size):
    loc = (size[0] // 2, size[1] // 2)
    txt = "Highscores:"
    screen['font'].render_to(screen['screen'], (loc[0] - len(txt)*10, loc[1] + 72), f"{txt}", (255, 255, 255))
    cnt = 1
    for name, value in scorers.items():
        if cnt > 5:
            break
        screen['font'].render_to(screen['screen'], (loc[0] - len(txt) * 15, loc[1] + 72 + 30*cnt), f"{cnt}. {name}: {value}", (255, 255, 255))
        cnt += 1


def print_score(score, screen, size):
    loc1 = (size[0] * 32 * 2 + 20, 12)
    loc2 = (size[0] * 32 * 2 + 20, 36)
    screen['font'].render_to(screen['screen'], loc1, "SCORE:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2, f"{score}", (255, 255, 255))


def print_life(sprite, lives, screen, size):
    loc1 = (size[0] * 32 * 2 + 20, 96)
    loc2 = (size[0] * 32 * 2 + 20, 120)
    screen['font'].render_to(screen['screen'], loc1, "Lives:", (255, 255, 255))
    for i in range(0, lives):
        screen['screen'].blit(sprite, (loc2[0] + i * 24, loc2[1]))


def print_timer(time, screen, size):
    loc1 = (size[0] * 32 * 2 + 20, 180)
    loc2 = (size[0] * 32 * 2 + 20, 204)
    screen['font'].render_to(screen['screen'], loc1, "Time:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2, f"{time}", (255, 255, 255))


def print_all():
    pass


def print_countdown(screen, value, size) -> None:
    loc = ((size[0] - 300) // 2 - 10, size[1] // 2 - 72)
    screen['font'].render_to(screen['screen'], loc, f"{value}", (255, 255, 255))


def end_game_print(screen, score, size):
    loc1 = (size[0] // 2 - 116, size[1] // 2 - 48)
    loc2 = (size[0] // 2, size[1] // 2)
    screen['font'].render_to(screen['screen'], loc1, "Final Score:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2, f"{score}", (255, 255, 255))


def get_username(screen, username, size):
    loc1 = (size[0] // 2 - 116, size[1] // 2 + 48)
    loc2 = (size[0] // 2, size[1] // 2 + 80)
    screen['font'].render_to(screen['screen'], loc1, "Enter Name:", (255, 255, 255))
    screen['font'].render_to(screen['screen'], loc2, f"{username}", (255, 255, 255))


def respawn(player, ghosts, loc, conf, visu, maze_hexa):
    player.x, player.y = loc
    player.direction = []
    ghosts.clear()
    ghosts.update(init_ghosts(conf, visu, player, maze_hexa))


def main():
    os.system("clear")
    conf = load_config()
    size = (conf['width'], conf['height'])
    win_size = (size[0] * 32 * 2 + 300, size[1] * 32 * 2)
    screen_conf = load_pygame(size)
    screen = screen_conf["screen"]
    spawn_loc = ((size[0] + size[0] % 2 - 1) * 32 - 12, (size[1] + size[1] % 2 - 1) * 32 - 12)
    pacman = init_player(spawn_loc[0], spawn_loc[1], "sprite/Pacman.png", conf['lives'])
    running = True
    mazegen = MazeGenerator(size=size, seed=conf['seed'])
    mazegen.generate(mazegen._seed)
    visu = build_maze_visu(convert_maze(mazegen.maze))
    hex_maze = convert_maze(mazegen.maze)
    walls = load_walls()
    ghosts = init_ghosts(conf, visu, pacman, hex_maze)
    scorers = load_scorers(conf['highscore_filename'])
    pacgums = []
    if (load_pacgums(pacgums, conf['pacgums'],
                     hex_maze, visu, conf)) == 0:
        return
    buttons = init_buttons(win_size)
    timer = time.time()
    lvl_timer = conf['level_max_time']
    respawn_timer = None
    over = False
    state = "menu"
    win = False
    usr_name = ''
    end_usr = False
    pg.display.set_caption("PACMAN")
    while running:
        keys = pg.key.get_pressed()
        n_timer = time.time()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and state == "score":
                keys = pg.key.get_pressed()
                if keys[pg.K_RETURN] or len(usr_name) == 10:
                    end_usr = True
                else:
                    if event.unicode.isalpha() or event.unicode.isspace():
                        usr_name += event.unicode
        dt = screen_conf['clock'].tick(60) / 1000
        if state == "menu":
            screen.fill((0, 0, 0))
            draw_button(buttons['main'], screen_conf, size)
            if buttons["main"].clicked() is True:
                state = "game"
            get_leaderboard(screen_conf, scorers, win_size)
        elif state == "game":
            if over is False:
                screen.fill((0, 0, 0))
                nb_gums = len(pacgums)
                if pacman.alive and time.time() - timer >= 1:
                    timer = n_timer
                    lvl_timer -= 1
                draw_env(screen, mazegen.maze, walls, pacgums, ghosts, pacman)
                print_score(pacman.score, screen_conf, size)
                print_life(pacman.get_sprite((0, 3)),
                           pacman.lives, screen_conf, size)
                print_timer(lvl_timer, screen_conf, size)

                pacman.eat_pacgums(pacgums, ghosts)
                pacman.touch_ghost(ghosts)

                if pacman.alive is True:
                    pacman.move_player(dt * 2, visu)
                    move_all_ghosts(ghosts, dt * 2)
                if pacman.just_respawned is True:
                    if time.time() - respawn_timer >= 3:
                        pacman.just_respawned = False
                        pacman.alive = True
                    else:
                        print_countdown(screen_conf,
                                        (3 - int(time.time() - respawn_timer)),
                                        win_size)
                if pacman.alive is False:
                    respawn(pacman, ghosts, spawn_loc, conf, visu, hex_maze)
                    pacman.just_respawned = True
                    pacman.alive = None
                    respawn_timer = time.time()
                if time_out(lvl_timer) or pacman.lives <= 0:
                    game_over(screen_conf, win_size)
                    over = True
                if nb_gums == 0:
                    game_over(screen_conf, win_size)
                    over = True
                    win = True
            else:
                if keys[pg.K_SPACE]:
                    state = "score" if not win else "game"
                    win = False
                    mazegen.generate()
                    visu = build_maze_visu(convert_maze(mazegen.maze))
                    hex_maze = convert_maze(mazegen.maze)
                    lvl_timer = conf["level_max_time"]
                    pacman.lives = conf["lives"]
                    respawn(pacman, ghosts, spawn_loc, conf, visu, hex_maze)
                    pacgums = []
                    if (load_pacgums(pacgums, conf['pacgums'],
                                     hex_maze, visu, conf)) == 0:
                        break
                    over = False
        elif state == "score":
            screen.fill((0, 0, 0))
            end_game_print(screen_conf, pacman.score, win_size)
            get_username(screen_conf, usr_name, win_size)
            if end_usr is True:
                user = {usr_name: pacman.score}
                fill_scorers(scorers, user, conf['highscore_filename'])
                state = "menu"
                end_usr = False
                usr_name = ''
                pacman.score = 0

        pg.display.update()


if __name__ == "__main__":
    main()
