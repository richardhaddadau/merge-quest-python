import os
import sys
import random

random.seed()

# windows
if os.name == 'nt':
    import msvcrt
# unix
else:
    import tty
    import termios


def clear_screen():
    if os.name == 'nt':  # windows
        os.system('cls')
    else:  # linux
        os.system('clear')


def introduce_game():
    clear_screen()
    print("")
    print("Welcome to Merge Quest!")
    print("How to play: use W/A/S/D to shift the blocks.")
    print("Blocks at the same level will merge and upgrade.")


def generate_grid(width, height):
    grid = [[0 for col in range(width)] for row in range(height)]
    return grid


def display_grid(grid):
    print("+---+---+---+---+")
    for row in grid:
        print("| " + " | ".join(map(str, row)) + " |")
    print("+---+---+---+---+")


def reverse_array(arr):
    return list(reversed(arr))


def process_row(row, original_length):
    processed_row = []
    skip = False
    for col in range(len(row)):
        if skip:
            skip = False
            continue
        if col + 1 < len(row) and row[col] == row[col + 1]:
            processed_row.append(row[col] + 1)
            skip = True
        else:
            processed_row.append(row[col])
    while len(processed_row) < original_length:
        processed_row.append(0)
    return processed_row


def move_up(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for col in range(cols):
        # Remove Zeros
        remove_zeros = [grid[row][col] for row in range(rows) if grid[row][col] != 0]
        new_col = process_row(remove_zeros, len(grid))
        for row in range(rows):
            grid[row][col] = new_col[row]


def move_down(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for col in range(cols):
        # Remove Zeros
        remove_zeros = [grid[row][col] for row in range(rows) if grid[row][col] != 0]
        # Reverse Column
        remove_zeros.reverse()
        new_col = process_row(remove_zeros, len(grid))
        # Reverse Column Back
        new_col.reverse()
        for row in range(rows):
            grid[row][col] = new_col[row]


def move_left(grid):
    for row in range(len(grid)):
        # Remove Zeros
        remove_zeros = [x for x in grid[row] if x != 0]
        new_row = process_row(remove_zeros, len(grid[0]))
        grid[row] = new_row


def move_right(grid):
    for row in range(len(grid)):
        # Remove Zeros
        remove_zeros = [x for x in grid[row] if x != 0]
        # Reverse Row
        remove_zeros.reverse()
        new_row = process_row(remove_zeros, len(grid[0]))
        # Reverse Row Back
        new_row.reverse()
        grid[row] = new_row


def produce_block_at_edge(grid, direction):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    # Up
    if direction == "up":
        valid = [col for col in range(cols) if grid[rows - 1][col] == 0]
        if not valid:
            return
        random_col = random.choice(valid)
        grid[rows-1][random_col] = 1
    # Down
    elif direction == "down":
        valid = [col for col in range(cols) if grid[0][col] == 0]
        if not valid:
            return
        random_col = random.choice(valid)
        grid[0][random_col] = 1
    # Left
    elif direction == "left":
        valid = [row for row in range(rows) if grid[row][cols - 1] == 0]
        if not valid:
            return
        random_row = random.choice(valid)
        grid[random_row][cols - 1] = 1
    # Right
    elif direction == "right":
        valid = [row for row in range(rows) if grid[row][0] == 0]
        if not valid:
            return
        random_row = random.choice(valid)
        grid[random_row][0] = 1


def get_key():
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8')
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def game_loop():
    new_grid = generate_grid(4, 4)
    # Would be nice to randomise the starting block eventually
    new_grid[len(new_grid) - 1][len(new_grid[0]) - 1] = 1
    start_game = True
    running = True
    while running:
        clear_screen()
        if start_game:
            introduce_game()
            start_game = False
        print("")
        display_grid(new_grid)
        print("What's your next move? [W/A/S/D or Q to quit]:")
        key = get_key()
        if key == 'w':
            move_up(new_grid)
            produce_block_at_edge(new_grid, "up")
        elif key == 'a':
            move_left(new_grid)
            produce_block_at_edge(new_grid, "left")
        elif key == 's':
            move_down(new_grid)
            produce_block_at_edge(new_grid, "down")
        elif key == 'd':
            move_right(new_grid)
            produce_block_at_edge(new_grid, "right")

        # Quit the game
        elif key == 'q':
            running = False

        # Any other key
        else:
            print("Invalid key")
    clear_screen()
    print("")
    print("Thank you for playing Merge Quest!")


game_loop()
