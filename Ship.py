from Coordinate import Coordinate


class Ship(object):

    """The Ship class represents a ship that can be placed on the baord.
       A ship has a length, the number of spaces it takes up, and a
       bool for whether or no the ship has been sunk. verticle is a bool
       that is True if the ship is verticle and false if it is horizontal.
       positions holds the positions on the board the ship occupies.
    """
    def __init__(self, length, orientation, position):
        self.length = length
        self.isSunck = False
        self.vertical = orientation
        self.positions = []
        self.fill_positions(position)

    # Once a ship is placed on the board it fills an array positions
    # with the positions on the board the ship occupies
    def fill_positions(self, coord):
        if self.vertical:
            for i in range(0, self.length):
                self.positions.append(Coordinate(coord.x + i, coord.y))

        else:
            for i in range(0, self.length):
                self.positions.append(Coordinate(coord.x, coord.y + i))
