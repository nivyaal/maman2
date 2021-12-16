
from Solution import *

if __name__ == '__main__':

    dropTables()
    createTables()

    print(addTeam(-1))
    print(addTeam(0))
    print(addTeam(1))
    print(addTeam(2))
    print(addTeam(1))
    print(addMatch(Match(1, 'Domestic', 1, None)))
    print(addMatch(Match(1, None, 1, 2)))
    print(addMatch(Match(1, 'Domestic', 1, 2)))
    print(getMatchProfile(1))
    print(getMatchProfile(-1))
    print(getMatchProfile(2))

    print(deleteMatch(Match(1, None, None, None)))
    print(deleteMatch(Match(-1, None, None, None)))
    print(deleteMatch(Match(22, None, None, None)))

    print(addPlayer(Player(5, 1, 15, 100, 'Left')))
    print(addPlayer(Player(6, 3, 15, 100, 'Left')))
    print(addPlayer(Player(6, 1, 25, 10, 'Right')))
    print(addPlayer(Player(7, 2, 15, 10, 'Right')))
    print(getPlayerProfile(5))
    print(getPlayerProfile(6))
    print(getPlayerProfile(7))
    print(deletePlayer(Player(6, None, None, None, None)))
    print(getPlayerProfile(5))
    print(getPlayerProfile(6))
    print(getPlayerProfile(7))
    print(deletePlayer(Player(6, None, None, None, None)))
    print(getPlayerProfile(5))
    print(getPlayerProfile(6))
    print(getPlayerProfile(7))

    print(addStadium(Stadium(1, 1000, 1)))
    print(addStadium(Stadium(2, 1000, 2)))
    print(addStadium(Stadium(3, 1000, 1)))
    print(addStadium(Stadium(2, 1000, 1)))

    dropTables()
