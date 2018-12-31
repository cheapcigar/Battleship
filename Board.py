
VERTICAL_SHIP = ' | '
HORIZONTAL_SHIP = ' - '
EMPTY = ' O '
MISS = ' . '
HIT = ' * '
SUNK = ' # '


class Board(object):

    """The Board class manages the battle ship game.
    """
    def __init__(self, size):
        self.size = size
        self.grid = [[EMPTY]*size for i in range(size+1)]
        self.ships = []
        self.count_sunk = 0

    """Display the board to the console, pass in False to hide ships
    """
    def display(self, show_all=True):
        print("  " + "  ".join([chr(c) for c in range(
            ord('A'), ord('A') + self.size)]))
        for row in range(0, self.size):
            print(row, end="")
            for col in range(0, self.size):
                # flag for whether to hide ships
                if show_all:
                    print(self.grid[row][col], end="")
                # print everything that is not a ship
                elif self.grid[row][col] != VERTICAL_SHIP and self.grid[
                        row][col] != HORIZONTAL_SHIP:
                    print(self.grid[row][col], end="")
                # it is a ship, so print an empty space to hide ship
                else:
                    print(EMPTY, end="")
            print()

    # empty board
    def reset(self):
        self.ships = []
        self.grid = [[EMPTY]*self.size for i in range(self.size+1)]
        self.count_sunk = 0

    # takes a user defined target and marks board accordingly
    # returns result as a string
    def mark(self, coord):

        location = self.grid[coord.x][coord.y]

        # user missed
        if location == EMPTY:
            self.grid[coord.x][coord.y] = MISS
            return "missed"

        # user hit
        if (location == VERTICAL_SHIP or
                location == HORIZONTAL_SHIP):
            self.grid[coord.x][coord.y] = HIT
            return "hit"

        # user guessed same location
        if (location == HIT or
                location == MISS or location == SUNK):
            raise ValueError("ERROR: You already guessed that location")

    # determine if a ship has been sunk
    def update(self):
        self.count_sunk = 0

        # go through all ships
        for ship in self.ships:
            count_hits = 0
            # go through each ships position and check for hit
            for pos in ship.positions:
                if self.grid[pos.x][pos.y] == HIT:
                    count_hits += 1

            # ship has been sunk, change symbol
            if count_hits == ship.length:
                ship.isSunck = True
                for pos in ship.positions:
                    self.grid[pos.x][pos.y] = SUNK

            # check if ship is sunken
            if ship.isSunck:
                self.count_sunk += 1

    # add a ship to the board, chekc for an overlap of ships
    def add_ship(self, ship):
        if(not self.overlap(ship)):
            self.ships.append(ship)

            if ship.vertical:
                for coord in ship.positions:
                    self.grid[coord.x][coord.y] = VERTICAL_SHIP
            else:
                for coord in ship.positions:
                    self.grid[coord.x][coord.y] = HORIZONTAL_SHIP
        else:
            raise ValueError("ERROR: Ships Overlap!")

    # return true if two ships overlap
    # throws an error if ship is off the board
    def overlap(self, ship):
        try:
            for coord in ship.positions:
                if self.grid[coord.x][coord.y] != EMPTY:
                    return True
        except IndexError:
            raise IndexError("ERROR: Ship is off board!")
        return False
