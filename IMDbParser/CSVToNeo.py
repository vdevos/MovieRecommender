__author__ = 'Thom Hurks'

from py2neo import Graph
# from py2neo.packages.httpstream import http

# Need this for big queries
# http.socket_timeout = 9999

remote = False

graph = None

if remote:
    graph = Graph("http://root@178.62.227.51:7474/db/data")
else:
    graph = Graph()

create_labels = "MATCH (n) " \
                "SET n :Movie " \
                "RETURN n;"

create_index =  "CREATE INDEX ON :Movie(imdb_id);"
create_index2 = "CREATE INDEX ON :Movie(title);"
constraint = "CREATE CONSTRAINT ON (m:Movie) ASSERT m.imdb_id IS UNIQUE;"

query_all = "MATCH (n) " \
            "RETURN n " \
            "LIMIT 10;"

query_relations = "MATCH ( )-[rel]->( ) " \
                  "RETURN rel " \
                  "LIMIT 10;"

query_suggestion = "MATCH (m:Movie)-[:mentions]->(s:Movie) " \
                   "WHERE m.title = {MOVIENAME}" \
                   "RETURN DISTINCT s.title, s.year, s.imdb_id " \
                   "ORDER BY s.year DESC " \
                   "LIMIT 3;"

result = graph.cypher.execute(query_all)
print(result)


#graph.cypher.execute(create_index)
#print("done1")
#graph.cypher.execute(create_index2)
#print("done2")
#graph.cypher.execute(constraint)
print("done all")

#result = graph.cypher.execute(query_all)
#print(result)

#result = graph.cypher.execute(query_relations)
#print(result)

#result = graph.cypher.execute(query_suggestion, {"MOVIENAME" : "Moon"})
#print(result)

#result = graph.cypher.execute(create_index)
#result = graph.cypher.execute(create_index2)
