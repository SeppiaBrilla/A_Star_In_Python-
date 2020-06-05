from graphics import Point


class Graph: #definition of a custom graph for my needs. Nothing facny or whatever it just do his job and not in the best way but this was the easiest way for me to implement this
    def __init__(self, ListOfElement, Erased, maxX, maxY):
        self.ListOfNode = [] 
        for x in range(maxX): #esaminating all nodes...
            for y in range(maxY):
                if not ListOfElement[x][y] in Erased: #if the node is not a black one...
                    Neib = [] #okay, he as some neighbors, maybe
                    if x + 1 < maxX: #if it is not the last in x 
                        if ListOfElement[x + 1][y] not in Erased: #and his x successor is not a black one
                            Neib.append(ListOfElement[x + 1][y]) #adding it to the list of neighbors 
                    if x > 0: #if it is not the firts in the x
                        if ListOfElement[x - 1][y] not in Erased: # and his x predecessor is not a black one 
                            Neib.append(ListOfElement[x - 1][y]) # adding it to the list of neighbors
                    if y + 1 < maxY: #same as x but on y
                        if ListOfElement[x][y + 1] not in Erased:
                            Neib.append(ListOfElement[x][y + 1])
                    if y > 0:
                        if ListOfElement[x][y - 1] not in Erased:
                            Neib.append(ListOfElement[x][y - 1])

                    self.ListOfNode.append(Node(ListOfElement[x][y], Neib)) ##adding the new node to the graph


    def GetNode(self, Node): #serch the required node by his value 
        for node in self.ListOfNode:
            if node.Value == Node:
                return node


class Node: #The node of the graph, nothing special. I'm lazy so there's no edges, just a list of attached nodes
    def __init__(self, Value, Neib):
        self.Value = Value
        self.Neib = Neib[:]
        self.distance = -1
        self.path = []

    def SetDistance(self, distance):
        self.distance = distance

    def SetPath(self, path):
        self.path = path[:]
        self.path.append(self.Value)


class PriorityQueue: #defining a custom priorityqueue because why not. It use the distance as priority, lowest is better 
    def __init__(self):
        self.Coda = []

    def push(self, node): #just append 
        self.Coda.append(node)

    def pop(self): #pop the lowest distance 
        Min = self.Coda[0]
        for node in self.Coda:
            if Min.distance > node.distance:
                Min = node

        self.Coda.remove(Min)
        return Min

    def IsEmpty(self):
        return not len(self.Coda)
