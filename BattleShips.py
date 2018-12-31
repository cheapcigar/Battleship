
from Board import Board
from Ship import Ship
from Coordinate import Coordinate
from Player import Player
import os
import platform

# Globals
SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

BOARD_SIZE = 10
# flag for continuing game
running = True
# flag first play through
played = False

# Functions


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


""" Converts players inputted coordinate to
    a coordinate object, if input is not correct
    raises a ValueError """


def convert(input):
    # remove spaces from input
    string = ""
    for char in input:
        if char != " ":
            string += char

    # a coordinate has exactly 2 characters
    # if not 2 then input is invalid
    if len(string) != 2:
        raise ValueError
        ("ERROR: Your input must be 2 characters only (ex. A0)")

    string = string.lower()

    # convert letter to board number
    # letter a is 97
    num1 = ord(string[0]) - 97

    # get number part of input
    # if fails user did not enter a number
    try:
        num2 = int(string[1])
    except ValueError:
        num2 = -1

    # user inputted an out of range letter
    # or a number outside of range
    if ((num1 < 0 or num1 > BOARD_SIZE-1) or (num2 < 0 or num2 > BOARD_SIZE)):
        raise ValueError("ERROR: Invalid Coordinate Entered!")
    return Coordinate(num2, num1)


p1 = Player("player1")
p2 = Player("player2")

board1 = Board(BOARD_SIZE)
board2 = Board(BOARD_SIZE)


"""Main game loop
"""
while(running):

    if not played:
        # get player 1 name, make sure less than 20 characters long
        passed = False
        while(not passed):
            p1.name = input("Player 1, enter your name (20 characters max.): ")
            if len(p1.name) <= 20:
                passed = True
            else:
                input('''ERROR: name contains too many
                characters \nPress Enter to Continue...''')
                clear_screen()

        # get player 2 name, make sure less than 20 characters long
        passed = False
        while(not passed):
            p2.name = input("Player 2, enter your name (20 characters max.): ")
            if len(p2.name) <= 20:
                passed = True
            else:
                input('''ERROR: name contains too many
                characters \nPress Enter to Continue...''')
                clear_screen()

    # Player 1, add all ships to board
    clear_screen()
    input("{0}, Input your ships \nPress Enter to Continue...".format(p1.name))
    for i in range(0, len(SHIP_INFO)):

        # display board
        clear_screen()
        board1.display()

        print('''\nAdd {0} to board, size
            {1}'''.format(SHIP_INFO[i][0], SHIP_INFO[i][1]))

        # determine whether ship is vertical
        vert = input("Is ship vertical? (enter 'y' for yes): ")
        if vert.lower() == 'y':
            vert = True
        else:
            vert = False

        passed = False
        while(not passed):
            clear_screen()
            board1.display()
            print('''\nAdd {0} to board, size
                {1}'''.format(SHIP_INFO[i][0], SHIP_INFO[i][1]))
            # get ship position
            try:
                coord = convert(input("Enter starting location: "))
                board1.add_ship(Ship(SHIP_INFO[i][1], vert, coord))
                passed = True
            except ValueError as e:
                input("{0}\nPress Enter to Continue...".format(e))
            except IndexError as e:
                input("{0}\nPress Enter to Continue...".format(e))

    # Player 2, add all ships to board
    clear_screen()
    input("{0}, Input your ships \nPress Enter to Continue...".format(p2.name))
    for i in range(0, len(SHIP_INFO)):

        # display board
        clear_screen()
        board2.display()

        print('''Add {0} to board,
            size {1}\n'''.format(SHIP_INFO[i][0], SHIP_INFO[i][1]))

        # determine whether ship is vertical
        vert = input("Is ship vertical?(enter 'y' for yes): ")
        if vert.lower() == 'y':
            vert = True
        else:
            vert = False

        passed = False
        while(not passed):
            clear_screen()
            board2.display()
            print('''\nAdd {0} to board,
                size {1}'''.format(SHIP_INFO[i][0], SHIP_INFO[i][1]))
            # get ship position
            try:
                coord = convert(input("Enter starting location: "))
                board2.add_ship(Ship(SHIP_INFO[i][1], vert, coord))
                passed = True
            except ValueError as e:
                input("{0}\nPress Enter to Continue...".format(e))
            except IndexError as e:
                input("{0}\nPress Enter to Continue...".format(e))
    coord = 0
    clear_screen()

    # loop until a players ships have all been sunk
    while board1.count_sunk != len(SHIP_INFO) and board2.count_sunk != len(
            SHIP_INFO):
        input('''{0}, your turn to guess \nPress Enter to
            Continue...'''.format(p1.name))

        # get player1's move
        passed = False
        while(not passed):

            # show both boards, hide ships on player2's board
            board1.display()
            print()
            board2.display(False)

            # get ship position
            try:
                coord = convert(input('''{0}, enter
                    location to fire at: '''.format(p1.name)))
                # mark board2 with user's move, throw error if same move
                result = board2.mark(coord)
                passed = True
            except ValueError as e:
                input("{0}\nPress Enter to Continue...".format(e))

        # update board2
        board2.update()

        # make sure player 1 did not win
        if board2.count_sunk != len(SHIP_INFO):

            # clear screen, show results, and prompt player2
            clear_screen()
            print("{0}, you {1}\n".format(p1.name, result))
            input('''{0}, your turn to guess \nPress Enter to Continue
                ...'''.format(p2.name))

            # get player2's move
            passed = False
            while(not passed):

                # show both boards, hide ships on player2's board
                board2.display()
                print()
                board1.display(False)

                # get ship position
                try:
                    coord = convert(input('''{0}, enter
                        location to fire at: '''.format(p2.name)))
                    # mark board1 with user's move, throw error if same move
                    result = board1.mark(coord)
                    passed = True
                except ValueError as e:
                    input("{0}\nPress Enter to Continue...".format(e))

            # update board1
            board1.update()

            # clear screen, show results, and prompt player1
            clear_screen()
            print("{0}, you{1}\n".format(p2.name, result))

    # show both final boards
    clear_screen()
    print("Final Results")
    board1.display()
    print()
    board2.display()

    # check who won the game and congratulate winner
    if board1.count_sunk == len(SHIP_INFO):
        p2.wins += 1
        print("{0}, Congrats you won Battle Ship!".format(p2.name))
    elif board2.count_sunk == len(SHIP_INFO):
        p1.wins += 1
        print("{0}, Congrats you won Battle Ship!".format(p1.name))

    # show each players wins
    print('''{0} wins: {1}      {2} wins: {3}
        '''.format(p1.name, p1.wins, p2.name, p2.wins))

    # ask to play again, anything other than 'y' means no
    answer = input("Play again? (enter 'y' for yes): ")
    if answer.lower() != 'y':
        running = False

    played = True
    # reset boards
    board1.reset()
    board2.reset()
