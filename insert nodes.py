from neo4jrestclient.client import GraphDatabase
 
db = GraphDatabase("http://localhost:7687", username="neo4j", password="mypassword")
 
# Create some nodes with labels
Artist = db.labels.create("Artist")
u1 = db.nodes.create(name="")
Artist.add(u1)
u2 = db.nodes.create(name="")
Artist.add(u2)
 
Songs = db.labels.create("Song")
b1 = db.nodes.create(name="")
b2 = db.nodes.create(name="")
# You can associate a label with many nodes in one go
Songs.add(b1, b2)


u1.relationships.create("wrote", b2)

u1.relationships.create("worked_with", u2)
