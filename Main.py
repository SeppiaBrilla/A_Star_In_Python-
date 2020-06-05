from typing import List
import Graph as g
from graphics import * #not mine, just a simple graphic library for python
import time


def main():
    #here I'm just setting up the UI, nothing special or interesting
    xSize = 500
    ySize = 600
    win = GraphWin("shortest path algorithm", xSize, ySize) #the window
    xMax = 41
    yMax = 41
    RectangleList = [[0] * xMax for i in range(yMax)] #all the possible rectangle where the magic happends 
    x = 4
    y = 104
    xr = 0
    yr = 0
    ButtonRed = Rectangle(Point(5, 2), Point(75, 32)) #varius buttons
    TextRed = Text(ButtonRed.getCenter(), "Red")
    ButtonBlack = Rectangle(Point(80, 2), Point(150, 32))
    TextBlack = Text(ButtonBlack.getCenter(), "Black")
    ButtonErase = Rectangle(Point(155, 2), Point(225, 32))
    TextErase = Text(ButtonErase.getCenter(), "Erase")
    ButtonStart = Rectangle(Point(230, 2), Point(300, 32))
    TextStart = Text(ButtonStart.getCenter(), "Shortest")
    ButtonCl = Rectangle(Point(305, 2), Point(375, 32))
    TextCl = Text(ButtonCl.getCenter(), "Clear")
    ButtonFast = Rectangle(Point(380, 2), Point(450, 32))
    TextFast = Text(ButtonFast.getCenter(), "Fastest")
    Text1 = Text(Point(90, 50), "Red: start and finish dots")
    Text2 = Text(Point(60, 70), "Black: obstacle ")
    ButtonRed.draw(win)
    TextRed.draw(win)
    ButtonBlack.draw(win)
    TextBlack.draw(win)
    ButtonErase.draw(win)
    TextErase.draw(win)
    ButtonStart.draw(win)
    TextStart.draw(win)
    ButtonCl.draw(win)
    TextCl.draw(win)
    ButtonFast.draw(win)
    TextFast.draw(win)
    Text1.draw(win)
    Text2.draw(win)
    buttons = [ButtonRed, ButtonBlack, ButtonErase, ButtonStart, ButtonCl, ButtonFast]

    while y + 10 < ySize:
        xr = 0
        while x + 10 < xSize:
            RectangleList[xr][yr] = (Rectangle(Point(x, y), Point(x + 10, y + 10)))
            RectangleList[xr][yr].draw(win)
            xr += 1
            x += 12
        y += 12
        yr += 1
        x = 4

    RedPoint = []
    BlackPoint = []
    button = ButtonErase
    color = None #here everything is ready. Now waiting for red, black blocks and an algorithm to be chose 
    while 1:
        while not (button == ButtonStart or button == ButtonFast):
            mouse = win.checkMouse()
            if mouse is not None:
                button = GetButton(mouse, buttons)
                if button == ButtonRed:
                    color = color_rgb(255, 0, 0)
                if button == ButtonBlack:
                    color = color_rgb(0, 0, 0)
                if button == ButtonErase:
                    color = color_rgb(255, 255, 255)
                if button == ButtonCl:
                    button = ButtonErase
                    Cl(RectangleList, xMax, yMax)
                    RedPoint.clear()
                    BlackPoint.clear()
                r = GetRectangle(mouse, RectangleList, xMax, yMax)
                
                win.checkKey()
                if r is not None and color is not None:
                    if color == color_rgb(255, 0, 0):
                        if len(RedPoint) < 2:
                            r.setFill(color)
                            RedPoint.append(r)
                        else:
                            Error = GraphWin("ERROR", 190, 100)
                            message = Text(Point(95, 50), "No more than 2 red points!")
                            message.draw(Error)
                    else:
                        if r in RedPoint:
                            RedPoint.remove(r)
                        if r in BlackPoint:
                            BlackPoint.remove(r)
                        if color == color_rgb(0, 0, 0):
                            BlackPoint.append(r)
                        r.setFill(color)

        if button == ButtonStart:
            Path = SolveShortest(RectangleList, xr, yr, BlackPoint, RedPoint) #now fun stuff
        if button == ButtonFast:
            Path = SolveFastest(RectangleList, xr, yr, BlackPoint, RedPoint)
        if Path is not None:
            for x in Path:
                x.setFill(color_rgb(0, 255, 0)) #coloring the resolved path
        button = ButtonErase


def Cl(RectangleList, xMax, yMax): #clear all the board, boring
    for x in range(xMax):
        for y in range(yMax):
            RectangleList[x][y].setFill(color_rgb(255, 255, 255))


def GetButton(mouse, buttons): #get the pressed button, boring
    for x in buttons:
        x.setFill(color_rgb(255, 255, 255))
        if x.getP1().x <= mouse.x <= x.getP2().x and x.getP1().y <= mouse.y <= x.getP2().y:
            x.setFill(color_rgb(0, 255, 0))
            return x

    return None

def GetRectangle(mouse, RectangleList, xMax, yMax): #get the pressed rectangle, boring
    for x in range(xMax):
        for y in range(yMax):
            if RectangleList[x][y].getP1().x <= mouse.x <= RectangleList[x][y].getP2().x and RectangleList[x][y].getP1().y <= mouse.y <= RectangleList[x][y].getP2().y:
                return RectangleList[x][y]


def SolveShortest(ListOfElement, maxX, maxY, Erased, RedPoint): #now is fun: this algorithm find the shortest path possible but it takes a bit to complete 
    if len(RedPoint) == 2: #checking if everything is done correctly
        queue = g.PriorityQueue() #creating a queue of node, used for what to check first
        graph = g.Graph(ListOfElement, Erased, maxX, maxY) #creating a graph, all rectangle are a node exept for the black ones
        Start = RedPoint[1] #start and finish points
        Finish = RedPoint[0]
        finished = None
        inizio = graph.GetNode(Start) #take the initial node 
        inizio.SetDistance(abs(inizio.Value.getCenter().getX() - Finish.getCenter().getX()) + abs(inizio.Value.getCenter().getY() - Finish.getCenter().getY())) #setting distance, not the best way but the easier, for this exercise will be ok
        inizio.SetPath([]) #set a path with empty nodes before him
        queue.push(inizio) #enqueue the first node 
        while queue.IsEmpty() == 0 and finished is None:
            node = queue.pop() #take the first node in the queue and removing it 
            for v in node.Neib: #for all nodes connected to him
                vicini = graph.GetNode(v)
                if vicini.distance == -1: #distance is -1 by default. If it is -1 it means that it's never been cheked
                    vicini.SetPath(node.path) # setting up the path for this node as his predecessor + him 

                    if vicini.Value == Finish: #uhm.... maybe he is the one....
                        finished = vicini #oh, it is, cool!
                        break
                    
                    vicini.SetDistance(abs(vicini.Value.getCenter().getX() - Finish.getCenter().getX()) + abs(vicini.Value.getCenter().getY() - Finish.getCenter().getY()) + node.distance) #setting distance for this node. it is equal to his abs distance + his predecessor distance, this way we are sure it does not check only the nearest node in abs value  
                    vicini.Value.setFill(color_rgb(0, 0, 255)) #for visual porpouse colouring it as blue 
                    time.sleep(0.025) #giving you time to understeand what is happening
                    queue.push(vicini) #okay, this needs to be check, pushing it 

        if finished is not None: #YAY! a solution is possible! Giving it to you
            return finished.path 
        else: #are you forcing your pc to work for nothing? You bastard! 
            return None


def SolveFastest(ListOfElement, maxX, maxY, Erased, RedPoint): #this is another way of solve the problem.
    #it is basically the same but it is way faster to complete (if it is possible) but there's the possibilities that it's not the best possible path 
    if len(RedPoint) == 2:
        queue = g.PriorityQueue()
        graph = g.Graph(ListOfElement, Erased, maxX, maxY)
        Start = RedPoint[1]
        Finish = RedPoint[0]
        finished = None
        inizio = graph.GetNode(Start)
        inizio.SetDistance(abs(inizio.Value.getCenter().getX() - Finish.getCenter().getX()) + abs(inizio.Value.getCenter().getY() - Finish.getCenter().getY()))
        inizio.SetPath([])
        queue.push(inizio)
        while queue.IsEmpty() == 0 and finished is None:
            node = queue.pop()
            for v in node.Neib:
                vicini = graph.GetNode(v)
                if vicini.distance == -1:
                    
                    vicini.SetPath(node.path)
                    if vicini.Value == Finish:
                        finished = vicini
                        break
                    vicini.SetDistance(abs(vicini.Value.getCenter().getX() - Finish.getCenter().getX()) + abs(vicini.Value.getCenter().getY() - Finish.getCenter().getY())) #everytihg is the same but this, this just ckeck the nearest possibilities and not the shortest path in general
                    vicini.Value.setFill(color_rgb(0, 0, 255))
                    time.sleep(0.025)
                    queue.push(vicini)

        if finished is not None:
            return finished.path
        else:
            return None





if __name__=="__main__":
    main()
