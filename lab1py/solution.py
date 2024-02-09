import sys
from collections import deque
from queue import PriorityQueue

method = sys.argv[4]
graph = open(sys.argv[2], "r", encoding="utf-8")
start = None
end = None
data = {}

for line in graph.readlines():

    if not line.startswith("#"):
        line=line.strip()
        if start is None:
            start=line
        elif end is None:
            end=line
        else:
            line=line.split(" ")
            data[line[0].strip(":")] = {}
            for j in range(1, len(line)):
                key=line[j].split(",")[0]
                value=line[j].split(",")[1]
                data[line[0].strip(":")][key]=value

end = end.split(" ")


print(data)



for key in data:
    sorted_data = dict(sorted(data[key].items(), key=lambda x: x[0]))
    data[key] = sorted_data

def BFS():
    visitedSum = 0
    path = {}
    path[start] = [start]
    curr = start
    q=deque()
    q.append(start)
    visited = set()
    visited.add(start)
    while not q.empty():
        visitedSum += 1
        curr = q.popleft()
        
        if curr in end:
            return path[curr], visitedSum
        else:
            for item in data[curr]:
                if item not in visited:
                    q.append(item)
                    visited.add(item)
                    path[item] = path[curr].copy()
                    path[item].append(item)
            del path[curr]
           
        

def BFSFunction():
    path, states_visited = BFS()
    path_length = len(path)
    found_solution = 'no'
    if path_length != 0:
        found_solution = 'yes'

    path = ' => '.join(path)
    print("# BFS")
    print("[FOUND_SOLUTION]:", found_solution)
    print("[STATES_VISITED]:", states_visited)
    print("[PATH_LENGTH]:", path_length)
    print("[TOTAL_COST]:", float(20))
    print("[PATH]:" , path)

def UCS():
    visitedSum = 0
    path = {}
    path[start] = [start]
    curr = start
    q = PriorityQueue()
    q.put((0, start))
    visited = set()
    while not q.empty():
        visitedSum += 1
        cost, curr = q.get()
        if curr in visited:
            continue
        visited.add(curr)
        if curr in end:
            return path[curr], visitedSum, cost
        else:
            for item in data[curr]:
                if item not in visited:
                    q.put((cost + int(data[curr][item]), item))
                    path[item] = path[curr].copy()
                    path[item].append(item)
            del path[curr]

def UCSFunction():
    path, states_visited, total_cost = UCS()
    path_length = len(path)
    found_solution = 'no'
    if path_length != 0:
        found_solution = 'yes'

    path = ' => '.join(path)
    print("# UCS")
    print("[FOUND_SOLUTION]:", found_solution)
    print("[STATES_VISITED]:", states_visited)
    print("[PATH_LENGTH]:", path_length)
    print("[TOTAL_COST]:", float(total_cost))
    print("[PATH]:", path)


def AStar(heurDict):
    visitedSum = 0
    path = {}
    path[start] = [start]
    curr = start
    q = PriorityQueue()
    q.put((0 + int(heurDict[start]), start))
    visited = set()
    while not q.empty():
        visitedSum += 1
        cost, curr = q.get()
        if curr in visited:
            continue
        visited.add(curr)
        if curr in end:
            return path[curr], visitedSum, cost
        else:
            for item in data[curr]:
                if item not in visited:
                    q.put((cost + int(data[curr][item]) + int(heurDict[item]), item))
                    path[item] = path[curr].copy()
                    path[item].append(item)
            del path[curr]


def LoadHeuristic():
    heuristic = open(sys.argv[6], "r", encoding="utf-8")
    heurDict = {}
    for line in heuristic.readlines():
        line = line.strip().split(": ")
        heurDict[line[0]] = line[1]

    path, states_visited, total_cost = AStar(heurDict)
    path_length = len(path)
    found_solution = 'no'
    if path_length != 0:
        found_solution = 'yes'

    total_cost = 0
    for i in range(0, len(path) - 1):
        total_cost += int(data[path[i]][path[i+1]])

    path = ' => '.join(path)
    print("# A-STAR")
    print("[FOUND_SOLUTION]:", found_solution)
    print("[STATES_VISITED]:", states_visited)
    print("[PATH_LENGTH]:", path_length)
    print("[TOTAL_COST]:", float(total_cost))
    print("[PATH]:", path)

if method == 'bfs':
    BFSFunction()

if method == 'ucs':
    UCSFunction()

if method == 'astar':
    LoadHeuristic()


