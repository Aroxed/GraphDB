from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "1"))
session = driver.session()

# clear all nodes and relations
session.run("MATCH (n)-[r]-() DELETE n,r")
session.run("MATCH (n) DELETE n")
session.run("CREATE (a1:Person {name:'John', age:20})")
session.run("CREATE (a2:Person {name:'Paul', age: 22})")
session.run("CREATE (a3:Person {name:'Ann', age: 19})")
session.run("CREATE (a4:Person {name:'Bob', age: 25})")
session.run("CREATE (a5:Person {name:'Orphan', age: 0})")

# nodes labels can be the same therefore WHERE
session.run(
    "MATCH (a1:Person) WHERE a1.name='John' MATCH (a2:Person) WHERE a2.name='Paul' CREATE (a1)-[:IS_FRIEND_OF]->(a2)")
session.run(
    "MATCH (a2:Person) WHERE a2.name='Paul' MATCH (a3:Person) WHERE a3.name='Ann' CREATE (a2)-[:IS_FRIEND_OF]->(a3)")
session.run(
    "MATCH (a3:Person) WHERE a3.name='Ann' MATCH (a4:Person) WHERE a4.name='Bob' CREATE (a3)-[:IS_FRIEND_OF]->(a4)")
# we can add relations simplier directly when creating them
# session.run("MERGE (a1:Person {name:'John'})-[:IS_FRIEND_OF]->(a2:Person {name:'Paul'})")

print("all nodes")
result = session.run("MATCH (a:Person) RETURN a.name AS name, a.age AS age")
record: object
for record in result:
    print("%s %s" % (record["name"], record["age"]))

print("all relations")
result = session.run("MATCH (n)-[r]->(m) RETURN n.name as n ,type(r) as r,m.name as m")
for record in result:
    print("%s %s %s" % (record['n'], record['r'], record['m']))

print("Paul's direct friends")
result = session.run("MATCH (n:Person)-[:IS_FRIEND_OF]->(m:Person) WHERE n.name='Paul' RETURN m.name +' ' + m.age as m")
for record in result:
    print("%s" % (record['m'],))

print("Paul's all friends in straight direction")
result = session.run("MATCH (n:Person)-[*]->(m:Person) WHERE n.name='Paul' RETURN m.name +' ' + m.age as m")
for record in result:
    print("%s" % (record['m'],))

print("Paul's all friends in any direction")
result = session.run("MATCH (n:Person)-[*]-(m:Person) WHERE n.name='Paul' RETURN m.name +' ' + m.age as m")
for record in result:
    print("%s" % (record['m'],))

print("Paul's friends, path len = 2")
result = session.run(
    "MATCH (n:Person)-[:IS_FRIEND_OF*2]-(m:Person) WHERE n.name='Paul' RETURN m.name +' ' + m.age as m")
for record in result:
    print("%s" % (record['m'],))

print("No friend node")
result = session.run("MATCH (n:Person) WHERE NOT (n)-[*]-() RETURN n.name +' ' + n.age as n")
for record in result:
    print("%s" % (record['n'],))
