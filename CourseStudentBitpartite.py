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
		course_id = row[0] + row[1]
		student_id = row[7]

		# Add the course section to the course_id.
		if by_section:
			course_id += row[2]

		# Add course if not in graph.
		if course_id not in G.nodes:
			G.add_node(course_id, type='course', x=1)
			courses.append(course_id)

		# Add student if not in graph.
		if student_id not in G.nodes:
			G.add_node(student_id, type='student', x=200)
			students.append(student_id)

		G.add_edge(course_id, student_id)

print("Courses: " + str(len(courses)))
print("Students: " + str(len(students)))
print("Bipartite: " + str(bipartite.is_bipartite(G)))
nx.write_gexf(G, "CourseStudentBipartite.gexf")

plt.figure(figsize=(20, 7))
plt.title("Spring")

ax = plt.gca()
# Spring is cool
pos = nx.spectral_layout(G)

nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=students, node_size=1, node_color='blue')
nx.draw_networkx_nodes(G, pos=pos, ax=ax, nodelist=courses, node_size=1, node_color='red')
nx.draw_networkx_edges(G, ax=ax, pos=pos)

plt.show()

# TODO(dorianjstubblefield): Add Labels