from py2neo import NodeMatcher, RelationshipMatcher
from project import graph
from collections import OrderedDict

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
    through the "Collabedd_With" Relationship
    :param artist: artist searched for
    :return: dictionary of all artists that have worked with the main artist along with the songs they worked on
    '''

    matcher = NodeMatcher(graph)
    start_node = matcher.match("Artist", major="yes", name=artist).first()
    end_nodes = list(matcher.match("Artist", collab=artist))

    matcher = RelationshipMatcher(graph)

    collaborations = {}
    for end_node in end_nodes:
        rel = dict(matcher.match(nodes=(start_node, end_node), r_type="Collabed with").first())
        songs = rel['song']
        songs = list(OrderedDict.fromkeys(songs))
        end_node = dict(end_node)
        collabed_artist = end_node['name']


        print("song:", songs, "with: ", collabed_artist)
        collaborations[collabed_artist] = songs

    print(collaborations)


    return collaborations



