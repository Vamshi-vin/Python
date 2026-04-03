import curses
import random
import time


BOARD_WIDTH = 40
BOARD_HEIGHT = 20
MIN_BOARD_WIDTH = 20
MIN_BOARD_HEIGHT = 10
START_SPEED = 0.14
MIN_SPEED = 0.06
SPEED_STEP = 0.008


def get_board_size(window):
    max_y, max_x = window.getmaxyx()
    board_height = min(BOARD_HEIGHT, max_y - 1)
    board_width = min(BOARD_WIDTH, max_x)
    return board_height, board_width


def make_food(snake, board_height, board_width):
    while True:
        food = [
            random.randint(1, board_height - 2),
            random.randint(1, board_width - 2),
        ]
        if food not in snake:
            return food


def safe_addstr(window, y, x, text):
    max_y, max_x = window.getmaxyx()
    if 0 <= y < max_y and 0 <= x < max_x:
        window.addstr(y, x, text[: max_x - x - 1])


def draw_border(window, board_height, board_width):
    window.border()
    safe_addstr(window, 0, 2, " Snake Game ")
    for y in range(1, board_height):
        window.addch(y, board_width - 1, "|")
    for x in range(1, board_width - 1):
        window.addch(board_height - 1, x, "-")
    window.addch(board_height - 1, board_width - 1, "+")


def draw_status(window, score, best_score, board_height, board_width):
    status = f" Score: {score}  Best: {best_score}  Q: quit "
    safe_addstr(window, board_height, 1, " " * max(0, board_width - 2))
    safe_addstr(window, board_height, 2, status[: max(0, board_width - 4)])


def show_center(window, lines, board_height, board_width):
    for index, line in enumerate(lines):
        y = board_height // 2 - len(lines) // 2 + index
        x = max(1, (board_width - len(line)) // 2)
        safe_addstr(window, y, x, line[: board_width - 2])


def game_loop(window):
    curses.curs_set(0)
    window.nodelay(True)
    window.keypad(True)

    best_score = 0

    while True:
        board_height, board_width = get_board_size(window)
        while board_height < MIN_BOARD_HEIGHT or board_width < MIN_BOARD_WIDTH:
            window.clear()
            safe_addstr(window, 1, 1, "Terminal too small for Snake.")
            safe_addstr(window, 2, 1, "Make the terminal bigger, then press any key.")
            safe_addstr(window, 3, 1, f"Need at least {MIN_BOARD_WIDTH}x{MIN_BOARD_HEIGHT + 1}.")
            window.refresh()
            window.nodelay(False)
            window.getch()
            window.nodelay(True)
            board_height, board_width = get_board_size(window)

        center_row = board_height // 2
        center_col = board_width // 2
        snake = [[center_row, center_col + offset] for offset in range(3)]
        direction = curses.KEY_LEFT
        food = make_food(snake, board_height, board_width)
        score = 0
        speed = START_SPEED

        while True:
            board_height, board_width = get_board_size(window)
            window.clear()
            draw_border(window, board_height, board_width)
            draw_status(window, score, best_score, board_height, board_width)

            if food[0] >= board_height - 1 or food[1] >= board_width - 1:
                food = make_food(snake, board_height, board_width)

            window.addch(food[0], food[1], "*")
            head = snake[0]
            window.addch(head[0], head[1], "@")
            for segment in snake[1:]:
                window.addch(segment[0], segment[1], "o")

            window.refresh()

            next_key = window.getch()
            if next_key == ord("q"):
                return

            if next_key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
                if (direction, next_key) not in {
                    (curses.KEY_UP, curses.KEY_DOWN),
                    (curses.KEY_DOWN, curses.KEY_UP),
                    (curses.KEY_LEFT, curses.KEY_RIGHT),
                    (curses.KEY_RIGHT, curses.KEY_LEFT),
                }:
                    direction = next_key

            new_head = head[:]
            if direction == curses.KEY_UP:
                new_head[0] -= 1
            elif direction == curses.KEY_DOWN:
                new_head[0] += 1
            elif direction == curses.KEY_LEFT:
                new_head[1] -= 1
            elif direction == curses.KEY_RIGHT:
                new_head[1] += 1

            if (
                new_head[0] in (0, board_height - 1)
                or new_head[1] in (0, board_width - 1)
                or new_head in snake
            ):
                best_score = max(best_score, score)
                window.nodelay(False)
                window.clear()
                draw_border(window, board_height, board_width)
                draw_status(window, score, best_score, board_height, board_width)
                show_center(
                    window,
                    [
                        "Game Over!",
                        f"You ate {score} snacks",
                        "Press R to restart or Q to quit",
                    ],
                    board_height,
                    board_width,
                )
                window.refresh()

                while True:
                    choice = window.getch()
                    if choice in (ord("q"), ord("Q")):
                        return
                    if choice in (ord("r"), ord("R")):
                        window.nodelay(True)
                        break
                break

            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                best_score = max(best_score, score)
                food = make_food(snake, board_height, board_width)
                speed = max(MIN_SPEED, speed - SPEED_STEP)
            else:
                snake.pop()

            time.sleep(speed)


def main():
    curses.wrapper(game_loop)


if __name__ == "__main__":
    main()
