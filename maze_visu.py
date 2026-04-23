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
            if maze[j][i] == '5':
                visu[j * 2 + 1][i * 2 + 1]
    return visu
