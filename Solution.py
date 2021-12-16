from typing import List
import Utility.DBConnector as Connector
from Utility.DBConnector import ResultSet
from Utility.DBConnector import ResultSetDict
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Match import Match
from Business.Player import Player
from Business.Stadium import Stadium
from psycopg2 import sql


def toMatch(dict: ResultSetDict) -> Match:
    """
    Converts a result set dictionary to a match type
    :param dict: the result set dictionary
    :return: a match object with the corresponding values
    """
    return Match(dict['matchid'], dict['competition'], dict['hometeamid'], dict['awayteamid'])


def toPlayer(dict: ResultSetDict) -> Player:
    """
    Converts a result set dictionary to a player type
    :param dict: the result set dictionary
    :return: a player object with the corresponding values
    """
    return Player(dict['playerid'], dict['teamid'], dict['age'], dict['height'], dict['preferredfoot'])


def createTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("CREATE TABLE Team(TeamID INTEGER PRIMARY KEY, CHECK(TeamID>0));")

        conn.execute("CREATE TABLE Match(MatchID INTEGER PRIMARY KEY CHECK(MatchID>0), "
                     "Competition VARCHAR(15) NOT NULL CHECK(Competition = 'International' OR  Competition = 'Domestic'), "
                     "HomeTeamID INTEGER REFERENCES Team(TeamID) ON DELETE CASCADE,"
                     "AwayTeamID INTEGER REFERENCES Team(TeamID) ON DELETE CASCADE,"
                     "CHECK(HomeTeamID <> AwayTeamID));")

        # TODO: not sure about null?
        conn.execute("CREATE TABLE Player(PlayerID INTEGER PRIMARY KEY CHECK(PlayerID>0),"
                     "TeamID INTEGER REFERENCES Team(TeamID) ON DELETE CASCADE,"
                     "Age INTEGER CHECK (Age>0),"
                     "Height INTEGER CHECK (Height>0),"
                     "PreferredFoot VARCHAR(5) NOT NULL CHECK (PreferredFoot = 'Left' OR PreferredFoot = 'Right'));")

        # TODO: for each team only one stadium is allowed
        conn.execute("CREATE TABLE Stadium(StadiumID INTEGER PRIMARY KEY CHECK(StadiumID>0),"
                     "Capacity INTEGER CHECK(Capacity>0),"
                     "BelongTo INTEGER NULL REFERENCES Team(TeamID) ON DELETE CASCADE);")  # TODO: Verify CASCADE.

        conn.execute("CREATE TABLE InStadium(MatchID INTEGER PRIMARY KEY REFERENCES Match(MatchID) ON DELETE CASCADE,"
                     "StadiumID INTEGER REFERENCES Stadium(StadiumID) ON DELETE CASCADE,"
                     "Attendance INTEGER CHECK(Attendance>=0));")

        conn.execute("CREATE TABLE ScoreIn(MatchID INTEGER REFERENCES Match(MatchID) ON DELETE CASCADE,"
                     "PlayerID INTEGER REFERENCES Player(PlayerID) ON DELETE CASCADE,"
                     "Amount INTEGER CHECK(Amount>0),"
                     "PRIMARY KEY(MatchID, PlayerID));")

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()


def clearTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DELETE FROM Team;"
                     "DELETE FROM Match;"
                     "DELETE FROM Player;"
                     "DELETE FROM Stadium;"
                     "DELETE FROM InStadium;"
                     "DELETE FROM ScoreIn;")

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()


def dropTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("DROP TABLE IF EXISTS Team CASCADE;"
                     "DROP TABLE IF EXISTS Match CASCADE;"
                     "DROP TABLE IF EXISTS Player CASCADE;"
                     "DROP TABLE IF EXISTS Stadium CASCADE;"
                     "DROP TABLE IF EXISTS InStadium CASCADE;"
                     "DROP TABLE IF EXISTS ScoreIn CASCADE;")

    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()


def addTeam(teamID: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Team(TeamID) VALUES({id})").format(id=sql.Literal(teamID))
        rows_effected, _ = conn.execute(query)
        return ReturnValue.OK
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def addMatch(match: Match) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Match(MatchID, Competition, HomeTeamID, AwayTeamID) VALUES({id}, {comp}, {home}, {away})")\
            .format(id=sql.Literal(match.getMatchID()), comp=sql.Literal(match.getCompetition()),
                    home=sql.Literal(match.getHomeTeamID()), away=sql.Literal(match.getAwayTeamID()))
        rows_effected, _ = conn.execute(query)
        return ReturnValue.OK
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def getMatchProfile(matchID: int) -> Match:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Match WHERE MatchID = {id};").format(id=sql.Literal(matchID))
        rows_effected, result = conn.execute(query)
        assert(result.size() == 1)
        return toMatch(result[0])
    except DatabaseException.ConnectionInvalid as e:
        return Match.badMatch()
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return Match.badMatch()
    except DatabaseException.CHECK_VIOLATION as e:
        return Match.badMatch()
    except DatabaseException.UNIQUE_VIOLATION as e:
        return Match.badMatch()
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return Match.badMatch()
    except Exception as e:
        return Match.badMatch()
    finally:
        conn.close()


def deleteMatch(match: Match) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM Match WHERE MatchID={id};") \
            .format(id=sql.Literal(match.getMatchID()))
        rows_effected, _ = conn.execute(query)
        return ReturnValue.NOT_EXISTS if (rows_effected == 0) else ReturnValue.OK
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return ReturnValue.ERROR
    except DatabaseException.CHECK_VIOLATION as e:
        return ReturnValue.ERROR
    except DatabaseException.UNIQUE_VIOLATION as e:
        return ReturnValue.ERROR
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return ReturnValue.ERROR
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def addPlayer(player: Player) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO Player(PlayerID, TeamID, Age, Height, PreferredFoot) VALUES({id}, {team}, {age}, {height}, {foot})") \
            .format(id=sql.Literal(player.getPlayerID()), team=sql.Literal(player.getTeamID()),
                    age=sql.Literal(player.getAge()), height=sql.Literal(player.getHeight()), foot=sql.Literal(player.getFoot()))
        rows_effected, _ = conn.execute(query)
        return ReturnValue.OK
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return ReturnValue.BAD_PARAMS
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def getPlayerProfile(playerID: int) -> Player:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Player WHERE PlayerID = {id};").format(id=sql.Literal(playerID))
        rows_effected, result = conn.execute(query)
        assert (result.size() == 1)
        return toPlayer(result[0])
    except DatabaseException.ConnectionInvalid as e:
        return Player.badPlayer()
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return Player.badPlayer()
    except DatabaseException.CHECK_VIOLATION as e:
        return Player.badPlayer()
    except DatabaseException.UNIQUE_VIOLATION as e:
        return Player.badPlayer()
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return Player.badPlayer()
    except Exception as e:
        return Player.badPlayer()
    finally:
        conn.close()


def deletePlayer(player: Player) -> ReturnValue:
    # TODO: Check cascading with ScoreIn
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM Player WHERE PlayerID={id};") \
            .format(id=sql.Literal(player.getPlayerID()))
        rows_effected, _ = conn.execute(query)
        return ReturnValue.NOT_EXISTS if (rows_effected == 0) else ReturnValue.OK
    except DatabaseException.ConnectionInvalid as e:
        return ReturnValue.ERROR
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return ReturnValue.ERROR
    except DatabaseException.CHECK_VIOLATION as e:
        return ReturnValue.ERROR
    except DatabaseException.UNIQUE_VIOLATION as e:
        return ReturnValue.ERROR
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return ReturnValue.ERROR
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def addStadium(stadium: Stadium) -> ReturnValue:
    pass


def getStadiumProfile(stadiumID: int) -> Stadium:
    pass


def deleteStadium(stadium: Stadium) -> ReturnValue:
    pass


def playerScoredInMatch(match: Match, player: Player, amount: int) -> ReturnValue:
    pass


def playerDidntScoreInMatch(match: Match, player: Player) -> ReturnValue:
    pass


def matchInStadium(match: Match, stadium: Stadium, attendance: int) -> ReturnValue:
    pass


def matchNotInStadium(match: Match, stadium: Stadium) -> ReturnValue:
    pass


def averageAttendanceInStadium(stadiumID: int) -> float:
    pass


def stadiumTotalGoals(stadiumID: int) -> int:
    pass


def playerIsWinner(playerID: int, matchID: int) -> bool:
    pass


def getActiveTallTeams() -> List[int]:
    pass


def getActiveTallRichTeams() -> List[int]:
    pass


def popularTeams() -> List[int]:
    pass


def getMostAttractiveStadiums() -> List[int]:
    pass


def mostGoalsForTeam(teamID: int) -> List[int]:
    pass


def getClosePlayers(playerID: int) -> List[int]:
    pass
