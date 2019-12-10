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
			G.add_node(course_id, type='course')
			courses.append(course_id)

		# Add student if not in graph.
		if student_id not in G.nodes:
			G.add_node(student_id, type='student')
			students.append(student_id)

		G.add_edge(course_id, student_id)

print("Courses: " + str(len(courses)))
print("Students: " + str(len(students)))
print("Bipartite: " + str(bipartite.is_bipartite(G)))

student_department_list = dict()
student_department_percentages = dict()

for node in G.nodes():
	if G.nodes()[node]['type'] != "course":
		student_department_list[node] = []
		student_department_percentages[node] = dict(L=0, E=0, T=0, B=0, I=0)
		for course in G.neighbors(node):
			student_department_list[node].append(course[0])
			student_department_percentages[node][course[0]] += 1
		for department,_ in student_department_percentages[node].items():
			student_department_percentages[node][department] /= len(student_department_list[node])

print(student_department_list)
print(student_department_percentages)


Student_G = nx.Graph()

for node in G.nodes():
	if G.nodes()[node]['type'] != "course":
		# Add missing student nodes.
		if not Student_G.has_node(node):
			Student_G.add_node(node)
		continue

	for student_1 in G.neighbors(node):
		for student_2 in G.neighbors(node):
			if student_1 != student_2:
				if not Student_G.has_node(student_1):
					Student_G.add_node(student_1)
				if not Student_G.has_node(student_2):
					Student_G.add_node(student_2)
				if not Student_G.has_edge(student_1, student_2):
					Student_G.add_edge(student_1, student_2, shared_courses=1)
				else:
					Student_G[student_1][student_2]['shared_courses'] += 1



def GenerateT(G, nodes):
	T = []
	for i in range(len(nodes)):
		T.append([])
		neighbors = G.neighbors(nodes[i])
		numNeighbors = len(list(neighbors))
		for j in range(len(nodes)):
			if i == j:
				T[i].append(numNeighbors)
			else:
				if nodes[j] in neighbors:
					T[i].append(1/numNeighbors)
				else:
					T[i].append(0)
	return T


print(GenerateT(Student_G, list(Student_G.nodes())))
