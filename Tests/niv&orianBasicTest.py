
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
    assert(getMatchProfile(-1).getMatchID() is None)
    assert(getMatchProfile(2) .getMatchID() is None)

    assert(deleteMatch(Match(1, None, None, None)) == ReturnValue.OK)
    assert(deleteMatch(Match(-1, None, None, None)) == ReturnValue.NOT_EXISTS)
    assert(deleteMatch(Match(22, None, None, None)) == ReturnValue.NOT_EXISTS)

    assert(addPlayer(Player(5, 1, 15, 100, 'Left')) == ReturnValue.OK)
    assert(addPlayer(Player(6, 3, 15, 100, 'Left')) == ReturnValue.BAD_PARAMS)
    assert(addPlayer(Player(6, 1, 25, 10, 'Right')) == ReturnValue.OK)
    assert(addPlayer(Player(7, 2, 15, 10, 'Right')) == ReturnValue.OK)
    assert(addPlayer(Player(7, 1, 15, 10, 'Right')) == ReturnValue.ALREADY_EXISTS)
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
    assert(deleteStadium(Stadium(3, None, None)) == ReturnValue.NOT_EXISTS)

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

    assert(addMatch(Match(1, 'International', 1, 2)) == ReturnValue.OK)
    assert (addMatch(Match(2, 'International', 1, 2)) == ReturnValue.OK)

    assert(playerScoredInMatch(Match(1, None, None, None), Player(5), 15) == ReturnValue.OK)

    assert (playerScoredInMatch(Match(1, None, None, None), Player(5), 30) == ReturnValue.ALREADY_EXISTS)

    assert (playerScoredInMatch(Match(2, None, None, None), Player(5), -5) == ReturnValue.BAD_PARAMS)

    assert (playerScoredInMatch(Match(3, None, None, None), Player(5), 5) == ReturnValue.NOT_EXISTS)
    assert (playerScoredInMatch(Match(2, None, None, None), Player(6), 5) == ReturnValue.NOT_EXISTS)
    assert (playerScoredInMatch(Match(2, None, None, None), Player(5), 5) == ReturnValue.OK)

    assert (playerDidntScoreInMatch(Match(1, None, None, None), Player(5)) == ReturnValue.OK)
    assert (playerDidntScoreInMatch(Match(3, None, None, None), Player(5)) == ReturnValue.NOT_EXISTS)
    assert (playerDidntScoreInMatch(Match(1, None, None, None), Player(50)) == ReturnValue.NOT_EXISTS)
    assert (playerDidntScoreInMatch(Match(1, None, None, None), Player(7)) == ReturnValue.NOT_EXISTS)



    assert (addStadium(Stadium(1, 1000, 1)) == ReturnValue.OK)
    assert (addStadium(Stadium(2, 3000, None)) == ReturnValue.OK)

    assert (matchInStadium(Match(1, None, None, None), Stadium(1, None, None), 500) == ReturnValue.OK)
    assert (matchInStadium(Match(1, None, None, None), Stadium(2, None, None), 500) == ReturnValue.ALREADY_EXISTS)
    assert (matchInStadium(Match(2, None, None, None), Stadium(2, None, None), -1) == ReturnValue.BAD_PARAMS)
    assert (matchInStadium(Match(2, None, None, None), Stadium(3, None, None), 0) == ReturnValue.NOT_EXISTS)
    assert (matchInStadium(Match(2, None, None, None), Stadium(1, None, None), 0) == ReturnValue.OK)
    assert (matchInStadium(Match(3, None, None, None), Stadium(1, None, None), 0) == ReturnValue.NOT_EXISTS)



    assert(matchNotInStadium(Match(2, None, None, None), Stadium(1, None, None)) == ReturnValue.OK)

    # TODO: Verify that if the match is in a stadium, but not the given stadium, then NOT_EXISTS
    assert (matchNotInStadium(Match(1, None, None, None), Stadium(2, None, None)) == ReturnValue.NOT_EXISTS)
    assert (matchNotInStadium(Match(3, None, None, None), Stadium(1, None, None)) == ReturnValue.NOT_EXISTS)

    assert (matchInStadium(Match(2, None, None, None), Stadium(2, None, None), 300) == ReturnValue.OK)

    assert(averageAttendanceInStadium(1) == 500)
    assert(averageAttendanceInStadium(2) == 300)
    assert(averageAttendanceInStadium(3) == 0)

    clearTables()

    assert (addTeam(1) == ReturnValue.OK)
    assert (addTeam(2) == ReturnValue.OK)
    assert (addTeam(3) == ReturnValue.OK)
    assert (addTeam(4) == ReturnValue.OK)
    assert (addTeam(5) == ReturnValue.OK)

    assert (addPlayer(Player(10, 1, 5, 200, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(11, 1, 5, 200, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(12, 1, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(13, 1, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(20, 2, 5, 200, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(21, 2, 5, 191, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(22, 2, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(23, 2, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(30, 3, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(31, 3, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(32, 3, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(33, 3, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(40, 4, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(41, 4, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(42, 4, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(43, 4, 5, 5, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(50, 5, 5, 200, 'Left')) == ReturnValue.OK)
    assert (addPlayer(Player(51, 5, 5, 200, 'Left')) == ReturnValue.OK)

    assert (addMatch(Match(1, 'Domestic', 1, 2)) == ReturnValue.OK)
    assert (addMatch(Match(2, 'Domestic', 3, 4)) == ReturnValue.OK)
    assert (addMatch(Match(3, 'Domestic', 1, 4)) == ReturnValue.OK)
    assert (addMatch(Match(4, 'Domestic', 2, 3)) == ReturnValue.OK)

    assert (addStadium(Stadium(1, 60000, 1)) == ReturnValue.OK)
    assert (addStadium(Stadium(2, 1200, None)) == ReturnValue.OK)

    assert (matchInStadium(Match(1, None, None, None), Stadium(1, None, None), 510) == ReturnValue.OK)
    assert (matchInStadium(Match(2, None, None, None), Stadium(1, None, None), 520) == ReturnValue.OK)
    assert (matchInStadium(Match(3, None, None, None), Stadium(1, None, None), 530) == ReturnValue.OK)
    assert (matchInStadium(Match(4, None, None, None), Stadium(2, None, None), 540) == ReturnValue.OK)

    # 15 pts in M1
    assert (playerScoredInMatch(Match(1, None, None, None), Player(10, None, None, None, None), 5) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(1, None, None, None), Player(11, None, None, None, None), 4) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(1, None, None, None), Player(12, None, None, None, None), 6) == ReturnValue.OK)

    # 30 pts in M2
    assert (playerScoredInMatch(Match(2, None, None, None), Player(20, None, None, None, None), 10) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(2, None, None, None), Player(21, None, None, None, None), 8) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(2, None, None, None), Player(22, None, None, None, None), 12) == ReturnValue.OK)

    # 60 pts in M3
    assert (playerScoredInMatch(Match(3, None, None, None), Player(30, None, None, None, None), 20) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(3, None, None, None), Player(31, None, None, None, None), 16) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(3, None, None, None), Player(32, None, None, None, None), 24) == ReturnValue.OK)

    # 120 pts in M4
    assert (playerScoredInMatch(Match(4, None, None, None), Player(40, None, None, None, None), 20) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(4, None, None, None), Player(41, None, None, None, None), 40) == ReturnValue.OK)
    assert (playerScoredInMatch(Match(4, None, None, None), Player(30, None, None, None, None), 60) == ReturnValue.OK)

    assert (stadiumTotalGoals(1) == 105)
    assert (stadiumTotalGoals(2) == 120)
    assert (stadiumTotalGoals(3) == 0)

    assert (playerIsWinner(30, 4) == True)
    assert (playerIsWinner(30, 3) == False)
    assert (playerIsWinner(40, 4) == False)
    assert (playerIsWinner(41, 4) == False)

    assert (playerIsWinner(45, 4) == False)
    assert (playerIsWinner(45, 40) == False)
    assert (playerIsWinner(41, 40) == False)

    assert(getActiveTallTeams() == [2, 1])
    assert(getActiveTallRichTeams() == [1])

    assert (addMatch(Match(5, 'Domestic', 5, 2)) == ReturnValue.OK)
    assert (addMatch(Match(6, 'Domestic', 3, 5)) == ReturnValue.OK)
    assert (addMatch(Match(7, 'Domestic', 5, 4)) == ReturnValue.OK)

    assert (matchInStadium(Match(5, None, None, None), Stadium(1, None, None), 45000) == ReturnValue.OK)
    assert (matchInStadium(Match(6, None, None, None), Stadium(1, None, None), 3000) == ReturnValue.OK)
    assert (matchInStadium(Match(7, None, None, None), Stadium(1, None, None), 50000) == ReturnValue.OK)
    assert (popularTeams() == [5])

    assert (addStadium(Stadium(3, 30000, 2)) == ReturnValue.OK)

    stadiumsGoals = [stadiumTotalGoals(1), stadiumTotalGoals(2), stadiumTotalGoals(3)]
    assert (getMostAttractiveStadiums() == [2, 1, 3])








    dropTables()
