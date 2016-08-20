#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

from itertools import izip

from contextlib import contextmanager


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("Connection failed")


@contextmanager
def get_cursor():
    """Query helper function using context lib.  Creates a cursor
    from a database connection object, and performs queries
    using that cursor.
    """
    conn = connect()
    c = conn.cursor()

    try:
        yield c
    except:
        raise
    else:
        conn.commit()
    finally:
        conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as c:
        c.execute('DELETE FROM matches')


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as c:
        c.execute('DELETE FROM players')


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as c:
        c.execute('SELECT count(*) AS num FROM players')
        results = c.fetchone()
        num = results[0]
        return num


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as c:
        c.execute('INSERT INTO players (name) \
                   VALUES (%s)', (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with get_cursor() as c:
        c.execute('SELECT players.id, players.name, scores.wins, scores.matches FROM players join scores ON players.id = scores.player_id ORDER BY scores.wins DESC')
        results = c.fetchall()
        return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as c:
        c.execute('INSERT INTO matches (winner_id, loser_id) \
                   VALUES (%s, %s)', (winner, loser))


def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return izip(a, a)


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

    results = playerStandings()
    players = [{'id': row[0], 'name': row[1]} for row in results]
    pairs = [
        (player1['id'], player1['name'], player2['id'], player2['name'])
        for player1, player2 in pairwise(players)
    ]
    return pairs
