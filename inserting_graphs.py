from py2neo import Graph, Node, Relationship
import cgi

###get artist name from html form
form = cgi.FieldStorage()
artist =  form.getvalue('artistname')

###connect to host
uri = "bolt://localhost:7687"
user = "neo4j"
password = "leah123"

###create graph
g = Graph(uri=uri, user=user, password=password)

### optionally clear the graph
# g.delete_all()

### THIS PRINTS TOTAL NUMBER OF NODES & RELATIONSHIPS
print(len(g.nodes))
print(len(g.relationships))

### begin a transaction
tx = g.begin()

### define some nodes and relationships
a = Node("Artist", name="Taylor Swift")
b = Node("Artist", name="Bruno Mars")
ab = Relationship(a, "Collabed with", b)

### create the nodes and relationships
tx.create(a)
tx.create(b)
tx.create(ab)

### commit the transaction
tx.commit()

###TEST PRINTS


#print(g.exists(ab))
#print(len(g.nodes))
#print(len(g.relationships))
print(a)
print(b)
print(ab)
print(artist)

#print(g.run("UNWIND range(1, 3) AS n RETURN n, n * n as n_sq").to_table())