import pygame as pg

TILE_SIZE = 32


def build_maze_visu(maze):
    visu = [["█" for _ in range(len(maze[0]) * 2 + 1)]
            for _ in range(len(maze) * 2 + 1)]
    for i in range(len(maze[0])):
        for j in range(len(maze)):
            visu[j * 2 + 1][i * 2 + 1] = " "
    return break_walls(visu, maze)


def generate_maze_visu(maze):
    visu = [["█" for _ in range(len(maze[0]) * 2 + 1)]
            for _ in range(len(maze) * 2 + 1)]

    for i in range(len(maze[0])):
        for j in range(len(maze)):
            visu[j * 2 + 1][i * 2 + 1] = " "

    for elem in maze:
        for ch in elem:
            print(ch, end="")
        print()
    print()
    visu = break_walls(visu, maze)
    for elem in visu:
        for ch in elem:
            print(ch, end="")
        print()


def break_walls(visu, maze):
    for i in range(len(maze[0])):
        for j in range(len(maze)):
            if maze[j][i] == '1':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "
                visu[j * 2 + 1][i * 2 + 2] = " "

            if maze[j][i] == '2':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "
                visu[j * 2][i * 2 + 1] = " "

            if maze[j][i] == '3':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 2][i * 2 + 1] = " "

            if maze[j][i] == '4':
                visu[j * 2 + 1][i * 2] = " "
                visu[j * 2 + 1][i * 2 + 2] = " "
                visu[j * 2][i * 2 + 1] = " "

            # if maze[j][i] == '5':
            #     visu[j * 2 + 1][i * 2 + 1]

    return visu


def draw_maze(screen, visu, wall_sprite):
    rotated_wall = pg.transform.rotate(wall_sprite, 90)
    for r_id, row in enumerate(visu):
        for c_id, col in enumerate(row):
            x = c_id * TILE_SIZE * 2
            y = r_id * TILE_SIZE * 2
            if col == 1:
                screen.blit(wall_sprite, (x, y - 2))
            if col == 2:
                screen.blit(rotated_wall, (x + 2, y))
            if col == 3:
                screen.blit(wall_sprite, (x, y - 2))
                screen.blit(rotated_wall, (x + 2, y))
            if col == 4:
                screen.blit(wall_sprite, (x, y + 2))
