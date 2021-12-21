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


def toStadium(dict: ResultSetDict) -> Stadium:
    """
    Converts a result set dictionary to a stadium type
    :param dict: the result set dictionary
    :return: a stadium object with the corresponding values
    """
    return Stadium(dict['stadiumid'], dict['capacity'], dict['belongto'])

def createTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute("CREATE TABLE Team(TeamID INTEGER PRIMARY KEY, CHECK(TeamID>0));")

        conn.execute("CREATE TABLE Match(MatchID INTEGER PRIMARY KEY CHECK(MatchID>0), "
                     "Competition VARCHAR(15) NOT NULL CHECK(Competition = 'International' OR  Competition = 'Domestic'), "
                     "HomeTeamID INTEGER NOT NULL REFERENCES Team(TeamID) ON DELETE CASCADE,"
                     "AwayTeamID INTEGER NOT NULL REFERENCES Team(TeamID) ON DELETE CASCADE,"
                     "CHECK(HomeTeamID <> AwayTeamID));")

        conn.execute("CREATE TABLE Player(PlayerID INTEGER PRIMARY KEY CHECK(PlayerID>0),"
                     "TeamID INTEGER NOT NULL REFERENCES Team(TeamID) ON DELETE CASCADE,"
                     "Age INTEGER NOT NULL CHECK (Age>0),"
                     "Height INTEGER NOT NULL CHECK (Height>0),"
                     "PreferredFoot VARCHAR(5) NOT NULL CHECK (PreferredFoot = 'Left' OR PreferredFoot = 'Right'));")

        conn.execute("CREATE TABLE Stadium(StadiumID INTEGER PRIMARY KEY CHECK(StadiumID>0),"
                     "Capacity INTEGER NOT NULL CHECK(Capacity>0),"
                     "BelongTo INTEGER NULL UNIQUE REFERENCES Team(TeamID) ON DELETE CASCADE);")

#TODO: should we check home team and belongs to are related?
        conn.execute("CREATE TABLE InStadium(MatchID INTEGER NOT NULL PRIMARY KEY REFERENCES Match(MatchID) ON DELETE CASCADE,"
                     "StadiumID INTEGER NOT NULL REFERENCES Stadium(StadiumID) ON DELETE CASCADE,"
                     "Attendance INTEGER NOT NULL CHECK(Attendance>=0));")

        conn.execute("CREATE TABLE ScoreIn(MatchID INTEGER NOT NULL REFERENCES Match(MatchID) ON DELETE CASCADE,"
                     "PlayerID INTEGER NOT NULL REFERENCES Player(PlayerID) ON DELETE CASCADE,"
                     "Amount INTEGER NOT NULL CHECK(Amount>0),"
                     "PRIMARY KEY(MatchID, PlayerID));")

################## views#########################
        conn.execute("CREATE VIEW ActiveTallTeams as "
                     "SELECT TeamID FROM Player WHERE Height>190 "
                     "GROUP BY TeamID "
                     "Having COUNT(PlayerID) >= 2 AND TeamID IN ((SELECT HomeTeamID FROM Match) UNION (SELECT AwayTeamID FROM Match));")

        conn.execute("CREATE VIEW PopularHomeTeams as "
                     "SELECT M.HomeTeamID FROM Match AS M "
                    "INNER JOIN InStadium AS I ON M.MatchID = I.MatchID "
                    "GROUP BY M.HomeTeamID "
                    "HAVING MIN(I.Attendance)>40000 ;")

        conn.execute("CREATE VIEW NotHomeTeams as "
                     "(SELECT TeamID FROM Team) EXCEPT (SELECT DISTINCT HomeTeamID FROM Match); ")


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
        conn.execute("DROP VIEW IF EXISTS ActiveTallTeams; "
                     "DROP VIEW IF EXISTS PopularHomeTeams; "
                     "DROP VIEW IF EXISTS NotHomeTeams; "
                     "DROP TABLE IF EXISTS Team CASCADE; "
                     "DROP TABLE IF EXISTS Match CASCADE; "
                     "DROP TABLE IF EXISTS Player CASCADE; "
                     "DROP TABLE IF EXISTS Stadium CASCADE; "
                     "DROP TABLE IF EXISTS InStadium CASCADE; "
                     "DROP TABLE IF EXISTS ScoreIn CASCADE; ")

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
        query = sql.SQL("INSERT INTO Match(MatchID, Competition, HomeTeamID, AwayTeamID) VALUES({id}, {comp}, {home}, {away});")\
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
        if result.size() == 0:
            return Match.badMatch()
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
            "INSERT INTO Player(PlayerID, TeamID, Age, Height, PreferredFoot) VALUES({id}, {team}, {age}, {height}, {foot});") \
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
        if result.size() == 0:
            return Player.badPlayer()
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
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO Stadium(StadiumID, Capacity, BelongTo) VALUES({id}, {cap}, {belong});") \
            .format(id=sql.Literal(stadium.getStadiumID()), cap=sql.Literal(stadium.getCapacity()),
                    belong=sql.Literal(stadium.getBelongsTo()))
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


def getStadiumProfile(stadiumID: int) -> Stadium:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Stadium WHERE StadiumID = {id};").format(id=sql.Literal(stadiumID))
        rows_effected, result = conn.execute(query)
        if result.size() == 0:
            return Stadium.badStadium()
        assert (result.size() == 1)
        return toStadium(result[0])
    except DatabaseException.ConnectionInvalid as e:
        return Stadium.badStadium()
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return Stadium.badStadium()
    except DatabaseException.CHECK_VIOLATION as e:
        return Stadium.badStadium()
    except DatabaseException.UNIQUE_VIOLATION as e:
        return Stadium.badStadium()
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return Stadium.badStadium()
    except Exception as e:
        return Stadium.badStadium()
    finally:
        conn.close()


def deleteStadium(stadium: Stadium) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM Stadium WHERE StadiumID={id};") \
            .format(id=sql.Literal(stadium.getStadiumID()))
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


def playerScoredInMatch(match: Match, player: Player, amount: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO ScoreIn(MatchID, PlayerID, Amount) VALUES({matchid}, {playerid}, {amnt});") \
            .format(matchid=sql.Literal(match.getMatchID()), playerid=sql.Literal(player.getPlayerID()),
                    amnt=sql.Literal(amount))
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
        return ReturnValue.NOT_EXISTS
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def playerDidntScoreInMatch(match: Match, player: Player) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM ScoreIn WHERE MatchID={matchid} AND PlayerID={playerid};") \
            .format(matchid=sql.Literal(match.getMatchID()), playerid=sql.Literal(player.getPlayerID()))
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


def matchInStadium(match: Match, stadium: Stadium, attendance: int) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "INSERT INTO InStadium(MatchID, StadiumID, Attendance) VALUES({matchid}, {stadiumid}, {attend});") \
            .format(matchid=sql.Literal(match.getMatchID()), stadiumid=sql.Literal(stadium.getStadiumID()),
                    attend=sql.Literal(attendance))
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
        return ReturnValue.NOT_EXISTS
    except Exception as e:
        return ReturnValue.ERROR
    finally:
        conn.close()


def matchNotInStadium(match: Match, stadium: Stadium) -> ReturnValue:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL(
            "DELETE FROM InStadium WHERE MatchID={matchid} AND StadiumID={stadiumid};") \
            .format(matchid=sql.Literal(match.getMatchID()), stadiumid=sql.Literal(stadium.getStadiumID()))
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


def averageAttendanceInStadium(stadiumID: int) -> float:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT COALESCE(AVG(Attendance),0) AS avg FROM InStadium WHERE StadiumID = {id};").format(id=sql.Literal(stadiumID))
        _, result = conn.execute(query)
        return result[0]['avg']
    except DatabaseException.ConnectionInvalid as e:
        return -1
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return -1
    except DatabaseException.CHECK_VIOLATION as e:
        return -1
    except DatabaseException.UNIQUE_VIOLATION as e:
        return -1
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return -1
    except Exception as e:
        return -1
    finally:
        conn.close()


def stadiumTotalGoals(stadiumID: int) -> int:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL\
            ("SELECT COALESCE(SUM(Amount),0) AS goals FROM ScoreIn WHERE MatchID IN "
             "(SELECT MatchID FROM InStadium WHERE StadiumID = {id});").format(id=sql.Literal(stadiumID))
        _, result = conn.execute(query)
        return result[0]['goals']
    except DatabaseException.ConnectionInvalid as e:
        return -1
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return -1
    except DatabaseException.CHECK_VIOLATION as e:
        return -1
    except DatabaseException.UNIQUE_VIOLATION as e:
        return -1
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return -1
    except Exception as e:
        return -1
    finally:
        conn.close()


def playerIsWinner(playerID: int, matchID: int) -> bool:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL\
            ("SELECT * FROM ScoreIn WHERE PlayerID={pid} AND MatchID={mid} AND Amount >="
             "0.5*(SELECT SUM(Amount) FROM ScoreIn WHERE MatchID={mid});").\
            format(pid=sql.Literal(playerID), mid=sql.Literal(matchID))
        _, result = conn.execute(query)
        return True if result.size() == 1 else False
    except DatabaseException.ConnectionInvalid as e:
        return False
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return False
    except DatabaseException.CHECK_VIOLATION as e:
        return False
    except DatabaseException.UNIQUE_VIOLATION as e:
        return False
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return False
    except Exception as e:
        return False
    finally:
        conn.close()


def getActiveTallTeams() -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()

        query = sql.SQL \
            ("SELECT TeamID FROM ActiveTallTeams "
            "ORDER BY TeamID DESC LIMIT 5;")

        _, result = conn.execute(query)
        return ([result[i]['teamid'] for i in range(result.size())])
    except DatabaseException.ConnectionInvalid as e:
        return []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return []
    except DatabaseException.CHECK_VIOLATION as e:
        return []
    except DatabaseException.UNIQUE_VIOLATION as e:
        return []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return []
    except Exception as e:
        return []
    finally:
        conn.close()


def getActiveTallRichTeams() -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL \
            ("SELECT TeamID FROM ActiveTallTeams "
             "WHERE TeamID IN (SELECT BelongTo FROM Stadium WHERE Capacity > 55000) "
             "ORDER BY TeamID ASC LIMIT 5;")

        _, result = conn.execute(query)
        return ([result[i]['teamid'] for i in range(result.size())])
    except DatabaseException.ConnectionInvalid as e:
        return []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return []
    except DatabaseException.CHECK_VIOLATION as e:
        return []
    except DatabaseException.UNIQUE_VIOLATION as e:
        return []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return []
    except Exception as e:
        return []
    finally:
        conn.close()

def popularTeams() -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL \
            ("SELECT DISTINCT HomeTeamID AS TeamID "
             "FROM (SELECT HomeTeamID FROM PopularHomeTeams UNION SELECT TeamID FROM NotHomeTeams) AS T "
             "ORDER BY TeamID DESC;")
        _, result = conn.execute(query)
        return ([result[i]['teamid'] for i in range(result.size())])
    except DatabaseException.ConnectionInvalid as e:
        return []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return []
    except DatabaseException.CHECK_VIOLATION as e:
        return []
    except DatabaseException.UNIQUE_VIOLATION as e:
        return []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return []
    except Exception as e:
        return []
    finally:
        conn.close()


def getMostAttractiveStadiums() -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL \
            ("SELECT S.StadiumID ,COALESCE((SELECT SUM(Amount) FROM ScoreIn WHERE MatchID IN "
 				                            "(SELECT MatchID FROM InStadium WHERE StadiumID = S.StadiumID)), 0) AS Goals "
            "FROM Stadium S "
            "ORDER BY Goals DESC, S.StadiumID ASC; ")
        _, result = conn.execute(query)
        return ([result[i]['stadiumid'] for i in range(result.size())])
    except DatabaseException.ConnectionInvalid as e:
        return []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return []
    except DatabaseException.CHECK_VIOLATION as e:
        return []
    except DatabaseException.UNIQUE_VIOLATION as e:
        return []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return []
    except Exception as e:
        return []
    finally:
        conn.close()


def mostGoalsForTeam(teamID: int) -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL \
            ("SELECT P.PlayerID ,COALESCE((SELECT SUM(Amount) FROM ScoreIn WHERE PlayerID = P.PlayerID), 0) AS Goals "
             "FROM Player P WHERE P.PlayerID IN (SELECT PlayerID FROM Player WHERE TeamID = {tid}) "
             "ORDER BY Goals DESC, P.PlayerID DESC LIMIT 5;").\
            format(tid=sql.Literal(teamID))
        _, result = conn.execute(query)
        return ([result[i]['playerid'] for i in range(result.size())])
    except DatabaseException.ConnectionInvalid as e:
        return []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return []
    except DatabaseException.CHECK_VIOLATION as e:
        return []
    except DatabaseException.UNIQUE_VIOLATION as e:
        return []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return []
    except Exception as e:
        return []
    finally:
        conn.close()

def getClosePlayers(playerID: int) -> List[int]:
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL \
            ("SELECT P.PlayerID FROM Player AS P "
            "WHERE P.PlayerID <> {pid} "
            "AND ((SELECT COUNT(*) FROM ScoreIn WHERE PlayerID = {pid}) *0.5 "
        	"<= (SELECT COUNT(*) FROM ((SELECT MatchID FROM ScoreIn WHERE PlayerID = {pid}) "
							  "INTERSECT(SELECT MatchID FROM ScoreIn WHERE PlayerID = P.PlayerID)) AS X)) "
            "ORDER BY P.PlayerID ASC LIMIT 10;"). \
            format(pid=sql.Literal(playerID))
        _, result = conn.execute(query)
        return ([result[i]['playerid'] for i in range(result.size())])
    except DatabaseException.ConnectionInvalid as e:
        return []
    except DatabaseException.NOT_NULL_VIOLATION as e:
        return []
    except DatabaseException.CHECK_VIOLATION as e:
        return []
    except DatabaseException.UNIQUE_VIOLATION as e:
        return []
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        return []
    except Exception as e:
        return []
    finally:
        conn.close()
