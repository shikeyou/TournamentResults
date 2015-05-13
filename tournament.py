#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL db.  Returns a db connection and cursor."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    return (DB, c)

def deleteMatches():
    """Remove all the match records from the database."""

    # connect to database and obtain a cursor
    DB, c = connect()

    # prepare SQL statement and execute it
    sql = """
        DELETE FROM matches
    """
    c.execute(sql)

    # commit immediately
    DB.commit()

    # close the database connection
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""

    # connect to database and obtain a cursor
    DB, c = connect()

    # prepare SQL statement and execute it
    sql = """
        DELETE FROM players
    """
    c.execute(sql)

    # commit immediately
    DB.commit()

    # close the database connection
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""

    # connect to database and obtain a cursor
    DB, c = connect()

    # prepare SQL statement and execute it
    sql = """
        SELECT COUNT(*)
        FROM players
    """
    c.execute(sql)

    # fetch the result
    count = c.fetchone()[0]

    # close the database connection
    DB.close()

    # return the result
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    # connect to database and obtain a cursor
    DB, c = connect()

    # prepare SQL statement and execute it
    sql = """
        INSERT INTO players(name)
        values (%s)
    """
    name = bleach.clean(name)  #sanitize user input first
    c.execute(sql, (name,))  #supply value as an arg to prevent SQLi

    # commit immediately
    DB.commit()

    # close the database connection
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # connect to database and obtain a cursor
    DB, c = connect()

    # prepare SQL statement and execute it
    sql = """
        SELECT id, name, wins, wins+loses as matches
        FROM score
        ORDER BY wins DESC
    """
    c.execute(sql)

    # fetch results from query
    results = c.fetchall()

    # close the database connection
    DB.close()

    # return the results
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # connect to database and obtain a cursor
    DB, c = connect()

    # prepare SQL statement and execute it
    sql = """
        INSERT INTO matches(winner, loser)
        VALUES (%s, %s)
    """
    winner = bleach.clean(winner)  #sanitize user input first
    loser = bleach.clean(loser)  #sanitize user input first
    c.execute(sql, (winner, loser))  #supply values as args to prevent SQLi

    # commit immediately
    DB.commit()

    # close the database connection
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # all we have to do here is to get the standings data first
    results = playerStandings()

    # then group the result into pairs based on ranking
    # e.g. first and second, third and fourth etc
    return [(results[x][0], results[x][1], results[x+1][0], results[x+1][1])
    	for x in range(0, len(results), 2)]
