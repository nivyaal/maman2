# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Solution import *

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    dropTables()
    createTables()

    print(addTeam(-1))
    print(addTeam(0))
    print(addTeam(1))
    print(addTeam(2))
    print(addTeam(1))
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
    print(addPlayer(Player(6, 1, 15, 100, 'Left')))

    dropTables()

    # print_hi('PyCharm')


    #dropTables()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
