from py2neo import Node, Relationship, NodeMatcher
from project import graph

def artist_in_db(artist):
    ''' Checks to see if the artist has already been searched for
    :param artist: artist searched for
    :return:
    '''
    matcher = NodeMatcher(graph)
    if matcher.match("Artist", major="yes", name=artist).first():
        return True

    return False


def get_connected_artists_from_db(artist):
    ''' Queries database to find all artists related to the main artist
    through the "Collbaed_With" Relationship
    :param artist: artist searched for
    :return: list of all artists that have worked with the artist queries
    '''

    matcher = NodeMatcher(graph)
    nodes = list(matcher.match("Artist", collab=artist))

    '''generates list of the names of artists that worked with the main artist
     We want this to return the name of the artists along with the song they collaborated on 
     to do this, you will have to adjust the query above.  I'm not sure if you will be able to use the NodeMatcher
     function, so you may have to execute it another way. Just google how to run py2neo queries.
     To understand what the database contains, run the website and search for artists then go look at the graph in neo4j
     run "MATCH (a:Artist) RETURN a;" '''
    collaborators = [ collab['name'] for collab in nodes]

    return collaborators



