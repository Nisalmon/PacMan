import sys
from mazegenerator import MazeGenerator
import pygame as pg
import os
from utils.config import load_config, check_conf
from utils.player import init_player, Player
from utils.pacgums import load_pacgums, Pacgums
from utils.maze_visu import build_maze_visu
from utils.ghost import move_all_ghosts, init_ghosts, Ghost, scared_ghost
from utils.game_end import time_out, game_over, win_screen
from utils import (draw_env, print_all, print_countdown, print_paused,
                   end_game_print, get_leaderboard, get_username, load_walls,
                   load_pygame, load_sounds, enter_input, enable_cheats,
                   init_cheats, get_cheats, activate_cheats, game_over_print,
                   congrats_print, print_guide)
from utils.buttons import init_buttons, draw_button, cheat_button
from utils.scorers import load_scorers, fill_scorers
import time
from typing import Tuple, List, Dict


TILE_SIZE = 32


def get_scale(maze_len: Tuple[int, int],
              maze_size: Tuple[int, int]) -> Tuple[int, int]:
    x = maze_size[0]/maze_len[0]/TILE_SIZE
    y = maze_size[1]/maze_len[1]/TILE_SIZE
    x = int(x)
    y = int(y)
    return (x, y)


def convert_maze(maze: List[List[int]]) -> List[List[str]]:
    n_maze = []
    hexa = "0123456789ABCDEF"
    for lst in maze:
        lst_to_add = []
        for elem in lst:
            lst_to_add.append(hexa[elem])
        n_maze.append(lst_to_add)
    return n_maze


def respawn(player: Player, ghosts: Dict[str, Ghost],
            loc: Tuple[int, int], conf: Dict[str, int | str],
            visu: List[List[str]], maze_hexa: List[List[str]],
            scale: Tuple[int, int]) -> None:
    player.x, player.y = loc
    player.direction = []
    ghosts.clear()
    ghosts.update(init_ghosts(conf, visu, player, maze_hexa, scale[0]))


def main(argv: List[str]) -> None:
    try:
        os.system("clear")
        if len(argv) != 2:
            print("Invalid number of arguments.")
            print("To use this program you must do:")
            print("python3 main.py 'path/to/config.json'")
            return
        conf = load_config(argv[1])
        check_conf(conf)
        size = (int(conf['width']), int(conf['height']))
        win_size = (15 * TILE_SIZE * 2 + 300, 15 * TILE_SIZE * 2)
        maze_size = (15 * TILE_SIZE * 2, 15 * TILE_SIZE * 2)
        paused = pg.Surface(win_size)
        scale = get_scale(size, maze_size)
        screen_conf = load_pygame(win_size)
        sounds = load_sounds()
        sounds['main'].set_volume(0.4)
        screen = screen_conf["screen"]
        pacman = init_player(0, 0, "sprite/Pacman.png",
                             int(conf['lives']), scale[0])
        spawn_loc = (
            int((size[0] + size[0] % 2 - 1) * TILE_SIZE * scale[0] / 2
                - pacman._scaled[0]/2),
            int((size[1] + size[1] % 2 - 1) * TILE_SIZE * scale[1] / 2
                - pacman._scaled[1]/2)
            )
        pacman.x, pacman.y = spawn_loc
        running = True
        mazegen = MazeGenerator(size=size, seed=int(conf['seed']))
        mazegen.generate(mazegen._seed)
        visu = build_maze_visu(convert_maze(mazegen.maze))
        hex_maze = convert_maze(mazegen.maze)
        walls = load_walls(scale)
        ghosts = init_ghosts(conf, visu, pacman, hex_maze, scale[0])
        scorers = load_scorers(str(conf['highscore_filename']))
        if len(scorers) > 10:
            raise Exception("There is an error with the highscore file.")
        pacgums: List[Pacgums] = []
        if (load_pacgums(pacgums, int(conf['pacgums']),
                         hex_maze, visu, conf)) == 0:
            return
        scr_snd = False
        buttons = init_buttons(win_size)
        timer = time.time()
        lvl_timer = int(conf['level_max_time'])
        respawn_timer = None
        over = False
        pause = False
        state = "menu"
        win = False
        usr_name = ''
        end_usr = False
        inputs: List[str] = []
        cheat = False
        cheats = init_cheats()
        icon = pg.image.load("./sprite/Icon.png")
        title = pg.transform.scale(pg.image.load("./sprite/Title.png"),
                                   (600, 200))
        pg.display.set_caption("PACMAN")
        pg.display.set_icon(icon)
    except Exception as e:
        raise Exception(e)
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
                    if event.unicode.isalnum() or event.unicode.isspace():
                        usr_name += event.unicode
                    if keys[pg.K_BACKSPACE]:
                        usr_name = usr_name[:-1]
        dt = screen_conf['clock'].tick(60) / 1000
        if state == "menu":
            level = 0
            screen.fill((0, 0, 60))
            screen.blit(title, (win_size[0] / 4, win_size[1] / 4))
            sounds['main'].play(-1)
            running = enter_input(inputs, running)
            if not cheat and enable_cheats(inputs):
                cheat = True
                cheat_button(buttons, win_size)
                screen.fill((0, 255, 0))
            draw_button(buttons, screen_conf)
            if buttons["main"].clicked() is True:
                state = "game"
                sounds['main'].stop()
                lvl_timer = int(conf["level_max_time"])
                pacman.lives = int(conf['lives'])
                pacman.score = 0
            if buttons["score"].clicked() is True:
                state = "lead"
            if buttons["guide"].clicked() is True:
                state = "guide"
            if buttons["exit"].clicked() is True:
                running = False
            if cheat and buttons["cheat"].clicked() is True:
                state = "cheat_menu"
        elif state == "game":
            pause = False
            if over is False:
                screen.fill((0, 0, 60))
                draw_env(screen, mazegen.maze, walls, pacgums, ghosts,
                         pacman, scale)
                if cheats['Skip level (press S)'] and keys[pg.K_s]:
                    win_screen(screen_conf, win_size)
                    over = True
                    win = True
                if keys[pg.K_ESCAPE]:
                    state = "paused"
                nb_gums = len(pacgums)
                if pacman.alive and time.time() - timer >= 1:
                    timer = n_timer
                    lvl_timer -= 1
                print_all(screen_conf, maze_size, pacman.score,
                          pacman.get_sprite((0, 3),), pacman.lives,
                          lvl_timer, level + 1, int(conf["level"]))
                pacman.eat_pacgums(pacgums, ghosts, sounds['waka']
                                   )
                if not cheats['Invincibility']:
                    pacman.touch_ghost(ghosts)

                if pacman.alive is True:
                    pacman.move_player(dt * 2, visu)
                    if not cheats['Ghost Freeze']:
                        move_all_ghosts(ghosts, dt * 2)
                if pacman.just_respawned is True:
                    if respawn_timer and time.time() - respawn_timer >= 3:
                        pacman.just_respawned = False
                        pacman.alive = True
                    else:
                        if respawn_timer:
                            cnt_down: int = (3 - int(time.time()
                                                     - respawn_timer))
                        else:
                            cnt_down = 0
                        print_countdown(screen_conf,
                                        (cnt_down),
                                        win_size)
                if scared_ghost(ghosts) and not scr_snd:
                    sounds['scared'].play(-1)
                    scr_snd = True
                elif not scared_ghost(ghosts) and scr_snd:
                    sounds['scared'].stop()
                    scr_snd = False
                if pacman.alive is False:
                    respawn(pacman, ghosts, spawn_loc, conf, visu,
                            hex_maze, scale)
                    pacman.just_respawned = True
                    pacman.alive = None
                    respawn_timer = time.time()
                if time_out(lvl_timer) or pacman.lives <= 0:
                    game_over(screen_conf, win_size)
                    over = True
                if nb_gums == 0:
                    win_screen(screen_conf, win_size)
                    over = True
                    win = True
            else:
                if keys[pg.K_SPACE]:
                    state = "score" if not win else "game"
                    level += 1
                    if level == conf['level']:
                        state = "score"
                    win = False
                    mazegen.generate()
                    visu = build_maze_visu(convert_maze(mazegen.maze))
                    hex_maze = convert_maze(mazegen.maze)
                    lvl_timer = int(conf["level_max_time"])
                    respawn(pacman, ghosts, spawn_loc, conf,
                            visu, hex_maze, scale)
                    pacgums = []
                    if (load_pacgums(pacgums, int(conf['pacgums']),
                                     hex_maze, visu, conf)) == 0:
                        break
                    over = False
        elif state == "paused":
            if not pause:
                paused.fill((0, 0, 0))
                paused.set_alpha(160)
                screen.blit(paused, (0, 0))
                pause = True
                sounds['scared'].stop()
                scr_snd = False
            print_paused(screen_conf, win_size)
            if keys[pg.K_TAB]:
                state = "menu"
                mazegen.generate()
                visu = build_maze_visu(convert_maze(mazegen.maze))
                hex_maze = convert_maze(mazegen.maze)
                respawn(pacman, ghosts, spawn_loc, conf,
                        visu, hex_maze, scale)
                pacman.just_respawned = False
                pacman.alive = True
                pacgums = []
                if (load_pacgums(pacgums, int(conf['pacgums']),
                                 hex_maze, visu, conf)) == 0:
                    break
            if keys[pg.K_SPACE]:
                state = "game"
        elif state == "score":
            screen.fill((0, 0, 60))
            if level == conf['level']:
                congrats_print(screen_conf, win_size)
            else:
                game_over_print(screen_conf, win_size)
            end_game_print(screen_conf, pacman.score, win_size)
            get_username(screen_conf, usr_name, win_size)
            if end_usr is True:
                user = {usr_name: pacman.score}
                scorers = fill_scorers(scorers, user,
                                       str(conf['highscore_filename']))
                state = "menu"
                end_usr = False
                usr_name = ''
        elif state == "lead":
            screen.fill((0, 0, 60))
            get_leaderboard(screen_conf, scorers, win_size)
            if keys[pg.K_BACKSPACE]:
                state = "menu"
        elif state == "guide":
            screen.fill((0, 0, 60))
            print_guide(screen_conf)
            if keys[pg.K_BACKSPACE]:
                state = "menu"
        elif state == "cheat_menu":
            screen.fill((0, 0, 60))
            get_cheats(screen_conf, cheats)
            if keys[pg.K_BACKSPACE]:
                state = "menu"
            activate_cheats(cheats)

        pg.display.update()


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print(e)
