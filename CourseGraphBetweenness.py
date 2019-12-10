import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import csv
import numpy as np

by_section = False

G = nx.Graph()

courses = []
students = []

# Read in entities
with open('Fall2016.csv') as file:
	rows = csv.reader(file, delimiter=',')

	# Skip the first line (description) in the CSV.
	next(rows)
	for row in rows:
		dep = row[0][0]
		course_id = row[0] + row[1]
		student_id = row[7]

		# Add the course section to the course_id.
		if by_section:
			course_id += row[2]

		# Add course if not in graph.
		if course_id not in G.nodes:
			G.add_node(course_id, type='course')
			courses.append(course_id)
			G.nodes[course_id]['dep'] = dep

		# Add student if not in graph.
		if student_id not in G.nodes:
			G.add_node(student_id, type='student')
			students.append(student_id)

		G.add_edge(course_id, student_id)

print("Courses: " + str(len(courses)))
print("Students: " + str(len(students)))
print("Bipartite: " + str(bipartite.is_bipartite(G)))

Course_G = nx.Graph()

for node in G.nodes():
	if G.nodes()[node]['type'] != "student":
		# Add missing course nodes.
		if not Course_G.has_node(node):
			Course_G.add_node(node)
			Course_G.nodes[node]['dep'] = G.nodes[node]['dep']
		continue

	for course_1 in G.neighbors(node):
		for course_2 in G.neighbors(node):
			if course_1 != course_2:
				if not Course_G.has_node(course_1):
					Course_G.add_node(course_1)
					Course_G.nodes[course_1]['dep'] = G.nodes[course_1]['dep']
				if not Course_G.has_node(course_2):
					Course_G.add_node(course_2)
					Course_G.nodes[course_2]['dep'] = G.nodes[course_2]['dep']
				if not Course_G.has_edge(course_1, course_2):
					Course_G.add_edge(course_1, course_2, shared_students=1)
				else:
					Course_G[course_1][course_2]['shared_students'] += 1

'''for node1 in G.nodes():
	for node2 in G.nodes():
		if Course_G.has_edge(node1, node2):
			Course_G[node1][node2]['shared_students'] = 1/Course_G[node1][node2]['shared_students']'''

node_betweenness = nx.algorithms.centrality.betweenness_centrality(Course_G, k=len(Course_G.nodes()), normalized=True, weight='shared_students', endpoints=False, seed=None)

for node in Course_G.nodes():
	Course_G.nodes[node]['betweenness'] = node_betweenness[node]

communities = list(nx.algorithms.community.modularity_max.greedy_modularity_communities(Course_G))

for i in range(len(communities)):
	for node in communities[i]:
		Course_G.nodes[node]['community'] = i

nx.write_gexf(Course_G, "CourseGraphBetweenness.gexf")