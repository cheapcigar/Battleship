class Player(object):

    """The Player class will represent a person playing the game.
       A Player has a name and a counter for wins and losses.
    """
    def __init__(self, name):
        self.name = name
        self.wins = 0

    def __str__(self):
        return self.name
