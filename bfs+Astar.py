import numpy as np
import matplotlib.pyplot as plt
import copy as cpy
import heapq
import math

path = []
AstarPath = []

def manhattandist(point, findx):
	dx = abs(point[1]-findx[1])*abs(point[1]-findx[1])
	dy = abs(point[0]-findx[0])*abs(point[1]-findx[1])
	return math.sqrt(dx+dy);
	
def isAdjacent(prev, next):
	return ((abs(next[0]-prev[0]) == 1 and next[1] == prev[1]) 
		or (abs(next[1]-prev[1]) == 1 and next[0] == prev[0]))
	
def bfs(maze, start, finish):
	queue = []
	queue.append(start)
	curLoc = queue.pop(0)
	while (curLoc != finish):
		maze[curLoc[0]][curLoc[1]] = 1
		try:
			#UP
			if (maze[curLoc[0]-1][curLoc[1]] == 0):
				if ((curLoc[0]-1) >= 0):
					queue.append((curLoc[0]-1, curLoc[1]))
			#RIGHT
			if (maze[curLoc[0]][curLoc[1]+1] == 0):
				queue.append((curLoc[0], curLoc[1]+1))
			#DOWN
			if (maze[curLoc[0]+1][curLoc[1]] == 0):
				queue.append((curLoc[0]+1, curLoc[1]))
			#LEFT
			if (maze[curLoc[0]][curLoc[1]-1] == 0):
				if (curLoc[1]-1 >= 0):
					queue.append((curLoc[0], curLoc[1]-1))
		except IndexError:
			pass

		path.append(curLoc)
		curLoc = queue.pop(0)
	path.append(finish)

	finalPath = []
	finalPath.append(finish)
	i = len(path)-1 #idx terakhir pada path
	tracking = False
	while (i >= 1):
		if (isAdjacent(path[i-1], path[i])):
			finalPath.append(path[i-1])
		else:
			tracking = True
			for j in range(i-1, -1, -1):
				if (isAdjacent(path[j], path[i])):
					finalPath.append(path[j])
					i = j
					break
		if (not(tracking)):
			i -= 1
		else:
			tracking = False
	finalPath.reverse()

	return finalPath


def AstarFunc(maze, start, finish):
	queue = []
	heapq.heapify(queue)
	heapq.heappush(queue, ((manhattandist(start, finish)) + 0, start))
	curLoc = heapq.heappop(queue)
	while (curLoc[1] != finish):
		maze[curLoc[1][0]][curLoc[1][1]] = 1
		try:
			#UP
			if (maze[curLoc[1][0]-1][curLoc[1][1]] == 0):
				prevgn = curLoc[0] - manhattandist((curLoc[1][0], curLoc[1][1]), finish)
				if (curLoc[1][0]-1 >= 0):
					heapq.heappush(queue, (manhattandist((curLoc[1][0]-1, curLoc[1][1]), finish) + prevgn + 1, (curLoc[1][0]-1, curLoc[1][1])))
			#RIGHT
			if (maze[curLoc[1][0]][curLoc[1][1]+1] == 0):
				prevgn = curLoc[0] - manhattandist((curLoc[1][0], curLoc[1][1]), finish)
				heapq.heappush(queue, (manhattandist((curLoc[1][0], curLoc[1][1]+1), finish) + prevgn + 1, (curLoc[1][0], curLoc[1][1]+1)))
			#DOWN
			if (maze[curLoc[1][0]+1][curLoc[1][1]] == 0):
				prevgn = curLoc[0] - manhattandist((curLoc[1][0], curLoc[1][1]), finish)
				heapq.heappush(queue, (manhattandist((curLoc[1][0]+1, curLoc[1][1]), finish) + prevgn + 1, (curLoc[1][0]+1, curLoc[1][1])))
			#LEFT
			if (maze[curLoc[1][0]][curLoc[1][1]-1] == 0):
				prevgn = curLoc[0] - manhattandist((curLoc[1][0], curLoc[1][1]), finish)
				if (curLoc[1][1]-1 >= 0):
					heapq.heappush(queue, (manhattandist((curLoc[1][0], curLoc[1][1]-1), finish) + prevgn + 1, (curLoc[1][0], curLoc[1][1]-1)))
		except IndexError:
			pass

		AstarPath.append(curLoc[1])
		curLoc = heapq.heappop(queue)
	AstarPath.append(finish)

	finalPath = []
	finalPath.append(finish)
	i = len(AstarPath)-1 #idx terakhir pada AstarPath
	tracking = False
	while (i >= 1):
		if (isAdjacent(AstarPath[i-1], AstarPath[i])):
			finalPath.append(AstarPath[i-1])
		else:
			tracking = True
			for j in range(i-1, -1, -1):
				if (isAdjacent(AstarPath[j], AstarPath[i])):
					finalPath.append(AstarPath[j])
					i = j
					break
		if (not(tracking)):
			i -= 1
		else:
			tracking = False
	finalPath.reverse()

	return finalPath


	
def display(maze, path):
	for i in range(len(path)):
		maze[path[i][0]][path[i][1]] = 9

def main():
	fil = open("query.txt", "r+")
	lines = [line for line in fil.readlines()]
	fil.close()
	
	maze = np.zeros((len(lines), len(lines[0])-1), int)
	copy = np.zeros((len(lines), len(lines[0])-1), int)
	for i in range(len(lines)):
		for j in range(len(lines[i])-1):
			maze[i][j] = lines[i][j]
			copy[i][j] = lines[i][j]

	#Find start and finish
	entry = -1
	fin = -1
	
	i = 0
	while (entry == -1):
		if (maze[i][0] == 0):
			entry = i
		else:
			i += 1
	
	i = 0
	while (fin == -1):
		if (maze[i][len(maze[0])-1] == 0):
			fin = i
		else:
			i += 1
	#Start and finish found

	start = (entry, 0)
	finish = (fin, len(maze[0])-1)
	print(finish)
	#BFS
	BFSMaze = cpy.copy(maze)
	finalPath = bfs(BFSMaze, start, finish)

	finalCopy = cpy.copy(copy)
	BFSAnim = cpy.copy(copy)

	BFS = plt.figure('BFS')
	for i in range(len(path)):
		BFS.clf()
		BFSAnim[path[i][0]][path[i][1]] = 9
		plt.imshow(BFSAnim)
		plt.pause(0.001)
	BFS.clf()
	display(finalCopy, finalPath)
	plt.imshow(finalCopy)
	#BFS DONE

	#ASTAR
	AstarFinalPath = AstarFunc(maze, start, finish)

	AstarAnim = cpy.copy(copy)

	Astar = plt.figure('A*')
	for i in range(len(AstarPath)):
		Astar.clf()
		AstarAnim[AstarPath[i][0]][AstarPath[i][1]] = 9
		plt.imshow(AstarAnim)
		plt.pause(0.001)
	Astar.clf()
	display(copy, AstarFinalPath)
	plt.imshow(copy)
	print('BFS step :' + str(len(path)))
	print('A*  step :' + str(len(AstarPath)))
	plt.show()

if __name__ == '__main__':
    main()
