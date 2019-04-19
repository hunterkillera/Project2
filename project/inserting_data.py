from py2neo import Node, Relationship, NodeMatcher


def search_nodes_for_artist(artist, graph):
    ''' This function looks for the artist in the database
    Input: graph
    Returns True if artist in graph, False otherwise
    '''
    matcher = NodeMatcher(graph)
    artist_in_database = matcher.match("Artist", name=artist).first()

    if artist_in_database:
        return True

    return False


def get_relationships(artist, graph):
    ''' Obtains all connected artists through the 'worked_with' relationship
    :param artist: artist's name to check relationships for
    :param graph: graph connection
    :return: list of connected artists
    '''

    return


def add_artist_to_db(artist, graph, related_artists):
    ''' Creates Node for artist (searched_for = True)
    :param artist: artist's name to add to database
    :param graph: graph connection
    :param related_artists list of artists that have worked with the main artist
    :return:
    '''
    a = Node("Artist", name=artist, searched_for=True)

    for artist in related_artists:
        #TODO: Check to see if artist is in


    return