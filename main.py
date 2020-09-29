import random
import time
import copy
import glob


def choose_board(path):
    """Chooses which file to load for the AI ship placements."""
    with open(path) as f:
        ships = [ship.split() for ship in f]
    return ships


def print_board(board, hide):
    """Prints out a board and checks if it should hide boats or not."""
    print("  0 1 2 3 4 5 6 7 8 9")
    num = 0
    for row in board:
        if hide:
            print(str(num) + " " + " ".join([check_pos(x) for x in row]))
        else:
            print(str(num) + " " + " ".join(row))
        num += 1
    print("\n")


def check_pos(arg):
    """Changes the boats in the ai board to hide them."""
    if arg == "O":
        return "-"
    else:
        return arg


def shot(board, x, y, is_random, hide_board):
    """Takes the coordinates and then prints out where the shots land."""
    shots = 0
    while True:
        if board[y][x] == "O":
            shots += 1
            board[y][x] = "X"
            print("HIT!")
            time.sleep(1)
            both_boards()
            if has_won(board):
                return board, shots
            x, y = choose_cords(is_random)
        elif board[y][x] == "-":
            shots += 1
            board[y][x] = "*"
            print("MISS!")
            time.sleep(1)
            return board, shots
        elif board[y][x] == "X" or board[y][x] == "*":
            print("There is already a shot there. try again")
            time.sleep(1)
            both_boards()
            x, y = choose_cords(is_random)


def choose_cords(is_random):
    """Decides which coordinates to use for the shot function."""
    if is_random:
        print("AI turn")
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        print("AI deciding where to shoot...")
        time.sleep(3)

    else:
        while True:
            try:
                print("Your turn!")
                x, y = map(int, input("Where do you want to shoot, enter x then y coordinate?(x y):  ").split())
                if x > 9 or x < 0 or y > 9 or x < 0:
                    print("You have to hit the board, please shoot between 0-9.")
                else:
                    break
            except ValueError:
                print("You need to enter a number between 0-9.")
    return x, y


def has_won(board):
    """Checks to see which player has won."""
    for row in board:
        if "O" in row:
            return False
    return True


def both_boards():
    """Prints out both boards."""
    print("\nYOUR BOARD")
    print_board(board_player, False)
    print("AI BOARD")
    print_board(board_ai, True)


# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
def file_browser(ext):
    """Returns files with an extension."""
    return [f for f in glob.glob(f"*{ext}")]


def adding_board(arg, board):
    """Adds a board to a new file."""
    with open(arg, "w+") as f:
        for row in board:
            f.write(" ".join(row) + "\n")
    return board


def chosen_board(board):
    """Chooses file to use as ai board."""
    print(f"Please choose a board for your enemy.\n{files}")
    while True:
        try:
            path = input("Choose a file: ")
            board = choose_board(path)
            break
        except IOError:
            print("can't find file.")
            continue
    return board


board_player = []
for i in range(0, 10):
    board_player.append(["-"] * 10)

boat_1 = 2
boat_2 = 2
boat_3 = 1
boat_4 = 1

print("Welcome to Battleship!\nPlease add your ships to your board.\n")

# adds boats to the player board.
while True:
    if boat_1 == 0 and boat_2 == 0 and boat_3 == 0 and boat_4 == 0:
        print("All ships added!")
        break
    print_board(board_player, False)
    print(f"ships remaining\nsize 1: {boat_1}\nsize 2: {boat_2}\nsize 3: {boat_3}\nsize 4: {boat_4}")
    try:
        size = int(input("choose ship size(1-4): "))
        if size < 1 or size > 4 or (size == 1 and boat_1 < 1) or (size == 2 and boat_2 < 1)\
                or (size == 3 and boat_3 < 1) or (size == 4 and boat_4 < 1):
            print("Choose a size between 1-4.")
            time.sleep(1)
            continue
    except ValueError:
        print("Wrong input, please enter a number between 1-4.")
        time.sleep(1)
        continue
    try:
        x, y = map(int, input("Where do you want to place ship? enter x then y coordinate(x y):  ").split())
        if x < 0 or x > 9 or y < 0 or y > 9:
            print("Coordinates are outside of game board, try again.")
            time.sleep(1)
            continue
    except ValueError:
        print("Wrong input, enter a number between 0-9")
        time.sleep(1)
        continue
    hor_ver = input("choose orientation(H/V): ").upper()
    if hor_ver != "H" and hor_ver != "V":
        print("You have to choose an orientation by pressing H for horizontal or V for vertical.")
        time.sleep(1)
        continue

    is_valid_move = True

    try:
        for i in range(size):
            if hor_ver == "H" and board_player[y][x + i] == "O":
                is_valid_move = False
            if hor_ver == "V" and board_player[y + i][x] == "O":
                is_valid_move = False
        if is_valid_move:
            for i in range(size):
                if hor_ver == "H":
                    board_player[y][x + i] = "O"
                elif hor_ver == "V":
                    board_player[y + i][x] = "O"
        if not is_valid_move:
            print("ALREADY A SHIP PLACED THERE")
            time.sleep(1)
            continue
    except IndexError:
        print("Your ship was placed out of bounds, please try again.")
        time.sleep(1)
        continue

    if size == 1:
        boat_1 -= 1
    elif size == 2:
        boat_2 -= 1
    elif size == 3:
        boat_3 -= 1
    elif size == 4:
        boat_4 -= 1


copy_player = copy.deepcopy(board_player)
files = file_browser(".txt")
shots_player = 0
shots_ai = 0
player_win = 0
ai_win = 0
board_ai = []
board_ai = chosen_board(board_ai)

# taking turns shooting and decides who wins
while True:
    both_boards()
    cords = choose_cords(False)
    board_ai, shots_fired = shot(board_ai, cords[0], cords[1], False, True)
    shots_player += shots_fired
    if has_won(board_ai):
        both_boards()
        print(f"YOU WON WITH {shots_player} SHOTS!!")
        player_win += 1
        with open("statistics", "a+") as f:
            f.write(f"The player won with {shots_player} shots.\n")
            break

    both_boards()
    cords = choose_cords(True)
    board_player, shots_fired = shot(board_player, cords[0], cords[1], True, False)
    shots_ai += shots_fired
    if has_won(board_player):
        both_boards()
        print(f"AI WON WITH {shots_ai} SHOTS!!\n")
        ai_win += 1
        with open("statistics", "a+") as f:
            f.write(f"The AI won with {shots_ai} shots.\n")
        break


end_game = False
# quit or save player board to new file.
while not end_game:
    save_board = input("\nWould you like to save your board to use as AI board in future games?: [Y/N] ").upper()
    if save_board == "Y":
        while True:
            name = input("Choose a name for your save file, end file name with .txt: ")
            check_txt = name[-4:]
            if check_txt == ".txt":
                adding_board(name, copy_player)
                print("board saved for use in future games.\nThanks for playing!")
                time.sleep(1)
                end_game = True
                break
            else:
                print("You have to end name with .txt")

    elif save_board == "N":
        print("Thanks for playing!")
        time.sleep(2)
        break
