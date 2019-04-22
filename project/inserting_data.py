from py2neo import Node, Relationship, NodeMatcher


def artist_in_db(artist, graph):
    ''' This function looks for the artist in the database
    Input: graph
    Returns True if artist in graph, False otherwise
    '''

    matcher = NodeMatcher(graph)
    artist_in_database = matcher.match("Artist", name=artist).first()

    print(artist_in_database)

    if artist_in_database:
        return True
    return False


def artist_searched_for(artist, graph):
    ''' Checks to see if the artist has been explicitly searched before
    :param artist: artist wanted
    :param graph: graph connection
    :return: True of False
    '''
    query = """
    MATCH (A:Artist)
    WHERE A.name = {artist}
    RETURN A.searched_for
    """

    cursor = graph.run(query, artist=artist).data()
    print(f'CURSOR: {cursor}')

    for row in cursor:
        print(row)
        if row['A.searched_for']:
            return True

    return False

def get_relationships(artist, graph):

    ''' Obtains all connected artists through the 'worked_with' relationship
    :param artist: artist's name to check relationships for
    :param graph: graph connection
    :return: list of connected artists
    '''
    related_artists = []

    # Runs query to database
    query = """
    MATCH (A:Artist)-[:WORKED_WITH]->(B:Artist)
    WHERE A.name = {artist}
    RETURN B.name"""
    cursor = graph.run(query, artist=artist).data()
    for match in cursor:
        related_artists.append(match['B.name'])

    return related_artists


def add_artist_to_db(artist, graph, related_artists):
    ''' Creates Node for artist (searched_for = True)
    :param artist: artist's name to add to database
    :param graph: graph connection
    :param related_artists list of artists that have worked with the main artist
    :return:
    '''

    tx = graph.begin()
    a = Node("Artist", name=artist, searched_for=True)


    # TODO: I'll have to make this search the database for the related artists
    for connected_artist in related_artists:
        if not artist_in_db(connected_artist, graph):
            b = Node("Artist", name=connected_artist)

        else:
            matcher = NodeMatcher(graph)
            b = matcher.match("Artist", name=artist).first()
        WORKED_WITH = Relationship(a, "WORKED_WITH", b)

        tx.create(a)
        tx.create(b)
        tx.create(WORKED_WITH)
        tx.commit()


    return


def update_artist(artist, graph, related_artists):
    ''' Changes artist's 'searched_for' attribute to True and adds connections
    :param artist:
    :param graph:
    :param related_artists: list of connected artists
    :return:
    '''

    matcher = NodeMatcher(graph)
    a = matcher.match("Artist", name=artist).first()
    tx = graph.begin()
    a['searched_for'] = True
    tx.merge(a)
    tx.commit()
    print(a)

    for connected_artist in related_artists:
        if not artist_in_db(connected_artist, graph):
            b = Node("Artist", name=connected_artist)
        else:
            matcher = NodeMatcher(graph)
            b = matcher.match("Artist", name=artist).first()
        WORKED_WITH = Relationship(a, "WORKED_WITH", b)
        graph.create(WORKED_WITH)

    return