
from Solution import *

if __name__ == '__main__':

    dropTables()
    createTables()

    assert(addTeam(-1) == ReturnValue.BAD_PARAMS)
    assert(addTeam(0) == ReturnValue.BAD_PARAMS)
    assert(addTeam(1) == ReturnValue.OK)
    assert(addTeam(2) == ReturnValue.OK)
    assert(addTeam(1) == ReturnValue.ALREADY_EXISTS)
    assert(addMatch(Match(1, 'Domestic', 1, None)) == ReturnValue.BAD_PARAMS)
    assert(addMatch(Match(1, None, 1, 2)) == ReturnValue.BAD_PARAMS)
    assert(addMatch(Match(1, 'Domestic', 1, 2)) == ReturnValue.OK)

    assert(getMatchProfile(1).getMatchID() is not None)
    assert (getMatchProfile(-1).getMatchID() is None)
    assert(getMatchProfile(2) .getMatchID() is None)

    assert(deleteMatch(Match(1, None, None, None)) == ReturnValue.OK)
    assert(deleteMatch(Match(-1, None, None, None)) == ReturnValue.NOT_EXISTS)
    assert(deleteMatch(Match(22, None, None, None)) == ReturnValue.NOT_EXISTS)

    assert(addPlayer(Player(5, 1, 15, 100, 'Left')) == ReturnValue.OK)
    assert(addPlayer(Player(6, 3, 15, 100, 'Left')) == ReturnValue.BAD_PARAMS)
    assert(addPlayer(Player(6, 1, 25, 10, 'Right')) == ReturnValue.OK)
    assert(addPlayer(Player(7, 2, 15, 10, 'Right')) == ReturnValue.OK)
    assert (addPlayer(Player(7, 1, 15, 10, 'Right')) == ReturnValue.ALREADY_EXISTS)
    assert(getPlayerProfile(5).getPlayerID() is not None)
    assert(getPlayerProfile(6).getPlayerID() is not None)
    assert(getPlayerProfile(7).getPlayerID() is not None)
    assert(deletePlayer(Player(6, None, None, None, None)) == ReturnValue.OK)
    assert(getPlayerProfile(5).getPlayerID() is not None)
    assert(getPlayerProfile(6).getPlayerID() is None)
    assert(getPlayerProfile(7).getPlayerID() is not None)
    assert(deletePlayer(Player(6, None, None, None, None)) == ReturnValue.NOT_EXISTS)
    assert(getPlayerProfile(5).getPlayerID() is not None)
    assert(getPlayerProfile(6).getPlayerID() is None)
    assert(getPlayerProfile(7).getPlayerID() is not None)

    assert(addStadium(Stadium(1, 1000, 1)) == ReturnValue.OK)
    assert(addStadium(Stadium(2, 1000, 2)) == ReturnValue.OK)
    assert(addStadium(Stadium(3, 1000, 1)) == ReturnValue.ALREADY_EXISTS)
    assert(addStadium(Stadium(2, 1000, 1)) == ReturnValue.ALREADY_EXISTS)

    assert(getStadiumProfile(1).getStadiumID() is not None)
    assert(getStadiumProfile(2).getStadiumID() is not None)
    assert(getStadiumProfile(3).getStadiumID() is None)

    assert(deleteStadium(Stadium(1, None, None)) == ReturnValue.OK)
    assert (deleteStadium(Stadium(3, None, None)) == ReturnValue.NOT_EXISTS)

    assert(getStadiumProfile(1).getStadiumID() is None)
    assert(getStadiumProfile(2).getStadiumID() is not None)
    assert(getStadiumProfile(3).getStadiumID() is None)

    assert(deleteStadium(Stadium(2, None, None)) == ReturnValue.OK)

    assert(getStadiumProfile(1).getStadiumID() is None)
    assert(getStadiumProfile(2).getStadiumID() is None)
    assert(getStadiumProfile(3).getStadiumID() is None)

    assert (deleteStadium(Stadium(1, None, None)) == ReturnValue.NOT_EXISTS)
    assert (deleteStadium(Stadium(2, None, None)) == ReturnValue.NOT_EXISTS)
    assert (deleteStadium(Stadium(3, None, None)) == ReturnValue.NOT_EXISTS)

    dropTables()
