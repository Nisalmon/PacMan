from typing import Dict, Any, Tuple


def time_out(timer: int) -> bool:
    """
    To stop the running game if the timer ran out

    :params:
        - timer : actual time

    :returns:
        bool : the result
    """
    return timer <= 0


def game_over(screen: Dict[str, Any], size: Tuple[int, int]) -> None:
    """
    To draw the game over screen

    :params:
        - screen : pygame screen

        - size : the scaling of the maze
    """
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 108, size[1] // 2),
                             "GAME OVER", (255, 255, 255))
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 132, size[1] // 2 + 48),
                             "PRESS SPACE", (255, 255, 255))


def win_screen(screen: Dict[str, Any], size: Tuple[int, int]) -> None:
    """
    To draw the win screen

    :params:
        - screen : pygame screen

        - size : the scaling of the maze
    """
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 156, size[1] // 2),
                             "LEVEL COMPLETED", (255, 255, 255))
    screen['font'].render_to(screen['screen'],
                             ((size[0] - 300) // 2 - 132, size[1] // 2 + 48),
                             "PRESS SPACE", (255, 255, 255))
