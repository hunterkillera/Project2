from py2neo import Graph,Node,Relationship

graph = Graph("bolt://localhost:7687",username="neo4j",password="1234")

a = Node("Person",name="Alice")
b = Node("Person", name="Bob")
r = Relationship(a, "KNOWS", b)

a["age"]=20
b["age"]=21
r["time"]="2017/01/01"
s = a|b|r
graph.create(s)

