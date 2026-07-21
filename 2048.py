import curses
from curses import window
import random 

#constants
ROW_SIZE = 4
COLUMN_SIZE = 4

def adding_random_2(values):
    zero_positions = []
    for r in range(ROW_SIZE):
        for c in range(COLUMN_SIZE):
            if values[r][c] == 0:
                pos = [r, c]
                zero_positions.append(pos)
    if len(zero_positions) == 1:
        r_index, c_index = zero_positions[0][0], zero_positions[0][1]
    elif len(zero_positions) == 0:
        return values
    else:
        indexes_position = random.randint(0, len(zero_positions)-1)
        r_index, c_index = zero_positions[indexes_position][0], zero_positions[indexes_position][1]
    chance = random.randint(1,10)
    if chance == 1:
        values[r_index][c_index] = 4
    else:
        values[r_index][c_index] = 2
    return values

def move_left_row(values_row):
    values = []
    for i in values_row:
        if i != 0:
            values.append(i)
    for i in range(len(values)-1):
        if values[i] == values[i+1]:
            values[i] *= 2
            values[i+1] = 0
    values_row.clear()
    for i in values:
        if i != 0:
            values_row.append(i)
    if len(values_row) != ROW_SIZE:
        zeros = ROW_SIZE - len(values_row)
        for i in range(zeros):
            values_row.append(0)
    return values_row

def move_left(values):
    for row in values:
        row = move_left_row(row)
    return values

def move_right(values):
    for r in values:
        r.reverse()
    values = move_left(values)
    for r in values:
        r.reverse()
    return values

def turn_up(values):
    values_turned = []
    row = []
    for c in range(4):
        row = []
        for r in range(ROW_SIZE - 1, -1, -1):
            row.append(values[r][c])
        values_turned.append(row)
    return values_turned

def turn_down(values):
    values_turned = []
    row = []
    for c in range(3,-1, -1):
        row = []
        for r in range(ROW_SIZE):
            row.append(values[r][c])
        values_turned.append(row)
    return values_turned

def move_up(values):
    values = turn_down(values)
    values = move_left(values)
    values = turn_up(values)
    return values

def move_down(values):
    values = turn_up(values)
    values = move_left(values)
    values = turn_down(values)
    return(values)
    
def can_move(values):
    for r in range(ROW_SIZE):
        for c in range(COLUMN_SIZE - 1):
            if values[r][c] == values[r][c+1]:
                return True
    for c in range(COLUMN_SIZE):
        for r in range(ROW_SIZE - 1):
            if values[r][c] == values[r+1][c]:
                return True
    return False

moves = {
    curses.KEY_LEFT: move_left, curses.KEY_RIGHT: move_right, curses.KEY_UP: move_up, curses.KEY_DOWN: move_down
}

def check_changes(key, values):
    new_values = [row[:] for row in values]
    new_values = moves[key](new_values)
    if new_values != values:
        return new_values
    return None

def the_game(stdscr: window):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.curs_set(0)

    value_color = {0:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:8, 512:8, 1024:8, 2048:8}

    stdscr.keypad(True)
    height, width = stdscr.getmaxyx()
    horizontal_line, vertical_line = height // COLUMN_SIZE, width // ROW_SIZE
    values = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    first_coordinate_y, first_coordinate_x = horizontal_line // 2, vertical_line // 2

    values = adding_random_2(values)
    while True:
        stdscr.erase()
        stdscr.bkgd(' ', curses.color_pair(1))
        for i in range(3):
            stdscr.hline(horizontal_line + i * horizontal_line, 0, curses.ACS_HLINE, width, curses.color_pair(1))
            stdscr.vline(0, vertical_line + i * vertical_line, curses.ACS_HLINE, height, curses.color_pair(1))
        for r in range(ROW_SIZE):
            for c in range(COLUMN_SIZE):
                stdscr.addstr(first_coordinate_y, first_coordinate_x + c * vertical_line, str(values[r][c]), curses.color_pair(value_color[values[r][c]]))
            first_coordinate_y += horizontal_line
        first_coordinate_y = horizontal_line // 2
        key = stdscr.getch()
        stdscr.refresh()
        if key in moves:
            new_values = check_changes(key, values)
            if new_values is not None:
                values = new_values
                adding_random_2(values)
        elif key == ord('q') or key == ord('Q'):
            return key
        else:
            pass
        if any(2048 in row for row in values):
            while True:
                stdscr.erase()
                stdscr.bkgd(' ', curses.color_pair(5))
                stdscr.addstr(height//2, (width-7)//2, 'VICTORY!', curses.color_pair(5))
                stdscr.addstr(height//18*16, 0, 'continue playing - 1', curses.color_pair(2))
                stdscr.addstr(height//18*17, 0, 'home - 2')
                answer = stdscr.getch()
                if answer == ord('q') or answer == ord('Q') or answer == ord('1') or answer == ord('2'):
                    return answer
        elif not any(0 in row for row in values) and not can_move(values):
            while True:
                stdscr.erase()
                stdscr.bkgd(' ', curses.color_pair(8))
                stdscr.addstr(height//2, (width-7)//2, 'DEFEAT!', curses.color_pair(8))
                stdscr.addstr(height//18*16, 0, 'continue playing - 1', curses.color_pair(2))
                stdscr.addstr(height//18*17, 0, 'home - 2')
                answer = stdscr.getch()
                if answer == ord('q') or answer == ord('Q') or answer == ord('1') or answer == ord('2'):
                    return answer

def home_page(stdscr: window):
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
    while True:
        stdscr.erase()
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.addstr(height//18*9, (width-8)//2, 'PLAY - 1', curses.color_pair(2))
        stdscr.addstr(height//18*10, (width-9)//2, 'RULES - 2', curses.color_pair(2))
        stdscr.addstr(height//18*17, 0, 'if you want to quit, press "q"', curses.color_pair(1))
        answer = stdscr.getch()
        if answer == ord('1') or answer == ord('2') or answer == ord('q') or answer == ord('Q'):
            return answer
        stdscr.refresh()

def show_rules(stdscr: window):
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)   
    curses.curs_set(0)
    stdscr.erase()
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.addstr(height * 3 // 10, (width-15)//2, 'Rules of 2048:', curses.color_pair(2))
    stdscr.addstr(height * 5 // 10, 0, 'Use the arrow keys on your keyboard to slide all numbered tiles simultaneously.', curses.color_pair(2))
    stdscr.addstr(height * 6 // 10, 0, 'Matching numbers merge into one tile with double the value when they collide.', curses.color_pair(2))
    stdscr.addstr(height * 7 // 10, 0, 'Every keyboard stroke spawns a new random "2" or "4" tile on the board.', curses.color_pair(2))
    stdscr.addstr(height * 8 // 10, 0, 'Combine your tiles continuously to reach the ultimate goal of the 2048 tile.', curses.color_pair(2))
    stdscr.addstr(height * 9 // 10, 0, 'You lose the game when the grid is full and no valid moves remain.', curses.color_pair(2))
    stdscr.getch()

key = None
while True:
    answer = curses.wrapper(home_page)
    if answer == ord('q') or answer == ord('Q') or key == ord('Q') or key == ord('q'):
        break
    elif answer == ord('1'):
        while True:
            key = curses.wrapper(the_game)
            if key == ord('q') or key == ord('Q') or key == ord('2'):
                break
        if key == ord('q') or key == ord('Q'):
            break
    else:
        curses.wrapper(show_rules)
