def generate_maze_visu(maze):
    visu = [["█" for _ in range(len(maze[0]) * 2 + 1)]
            for _ in range(len(maze) * 2 + 1)]

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            visu[j * 2 + 1][i * 2 + 1] = " "
    for elem in visu:
        for ch in elem:
            print(ch, end="")
        print()
