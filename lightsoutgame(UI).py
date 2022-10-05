 #Song Yuhan (JAIST)
#Lightsout game (UI version)
#Updated on October 23rd

import random
from tkinter import * #This is for UI

####################################################
class Light:                                        #This is the class of each light on the gamepad

    def __init__(self, row, colum, status,adjacents):
        self.row = row                              # index
        self.colum = colum                          # index
        self.status = status                        # status:0 for off,1 for on
        self.name = str(row) + "_" + str(colum)     # Name of this light
        self.adjacents = adjacents                  # Neighbors of this light

    def addadjs(self,node):                         # Add the adjacent lights
        self.adjacents.append(node)

    def press(self):                                # Pressing this light will reverse the status of current light and adjacent lights
        self.status = self.status ^ 1

        for nodes in self.adjacents:
            nodes.status = nodes.status ^ 1

###################################################

def initialize():
    panel = [[] for x in range(0, 4)]                               # Create the gamepad

    for i in range(0, 4):                                           # Add the lights to the gamepad
        for k in range(0, 4):
            locals()["light"+str(i)+"_"+str(k)] = Light(i,k,0,[])
            panel[i].append(locals()["light"+str(i)+"_"+str(k)])

    for i in range(0, 4):                                           # Find the adjacent lights for each light
        for k in range(0, 4):
            if i - 1 >= 0:
                panel[i][k].addadjs(panel[i-1][k])

            if k - 1 >= 0:
                panel[i][k].addadjs(panel[i][k-1])

            if i + 1 <= 3:
                panel[i][k].addadjs(panel[i+1][k])

            if k + 1 <= 3:
                panel[i][k].addadjs(panel[i][k+1])

    for i in range(3):
        panel[random.randint(0,3)][random.randint(0,3)].press()     # Initialize the gamepad(panel) randomly

    return panel


############################################################

def nextstatus(gamepad):                                     # This function is to detect if the next step will solve the problem. I wrote this function during the early time when I need to check the solution manually, it is not used in the final program.

    stset = [[None,None,None,None] for x in range(0, 4)]

    for i in range(0,4):
        for k in range(0,4):

            gamepad[i][k].press()
            stset[i][k] = getstatus(gamepad)
            gamepad[i][k].press()

    return stset

def getstatus(gamepad):                                      # This function can give the current statuses of the lights.
    sttable = [[] for x in range(0, 4)]

    for x in range(0, 4):
        for y in range(0, 4):
            sttable[x].append(gamepad[x][y].status)
    return sttable

def checktable(goal,statustable):                            # This function can check if two status tables are the same.This function is also for early developing, not used in the final program.

    for i in range(0,4):
        for k in range(0,4):
            if goal == statustable[i][k]:
                return (True,(i,k))
    return (False,False)

#############################################################

def getsolution(gamepad):                                       # First layer of the solution

    goal = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]            # Our goal is to turn all the lights off
    explored = []                                               # This includes the status we have already explored
    frontier = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]        # These are the lights expected to be pressed. In the first step, we will try to press all the lights.
    if getstatus(gamepad) == goal:                              # Check if we already get the goal.
        return None
    for depth in range(1,10):                                   # Explore the potential status within the depth. I set a maximum depth here in case my PC goes down, you can change it to a while loop if you have enough computing power.
        path = solve(depth,frontier, goal, gamepad, explored)   # Enter the second layer
        if path != False:
            return path


def solve(depth,frontier,goal,gamepad,explored):             # Solve the puzzle with the parameters

    for x in range(int(len(frontier)/depth)):                # If depth == 1， we will explore one step, two steps for depth ==2 and so on.

        currentpath = []                                     # Record the current exploring path
        temp = []                                            # Record how we have changed the gamepad so that we can return to the original status after we conduct an unsuccessful try.

        for i in range(depth):                               # Get the path we need to try.
            temp.append(frontier.pop(0))

        for x in temp:                                       # Change the gamepad by the given path.
            gamepad[x[0]][x[1]].press()
            currentpath.append((x[0],x[1]))

        if getstatus(gamepad) not in explored:               # Skip it if we have already explored current status.
            explored.append(getstatus(gamepad))

            if goal == getstatus(gamepad):                   # Check if we reach the goal
                for x in temp:
                    gamepad[x[0]][x[1]].press()
                return currentpath                           # If succeed, return the right path. Do not forget to restore the gamepad even if it is a successful search !!!!!!!!.
            else:
                for i in range(0, 4):
                    for k in range(0,4):                     # If fail, create a new path to explore in next depth.
                        currentpath.append((i,k))
                        frontier.extend(currentpath)
                        currentpath.pop()

        for x in temp:                                       # Restore the gamepad.
            gamepad[x[0]][x[1]].press()

    return False

#################################################################   From here is the UI part || The following buttons can be regarded as lights on the gamepad.

def check(i,k):                                              # Make sure the color of each button is decided by the status of the gamepad.
    if panel[i][k].status == 1:
         return "white"
    else:
         return "black"


def turncolor(i,k):                                          # Press a "light", and update the colors of the buttons.

    panel[i][k].press()

    for x in range(0,4):
        for y in range(0,4):
            buttons[x][y].configure(bg=check(x,y))


def showhint():                                              # Show the solution path, make the lights on the solution path change their color to green.

    print (getstatus(panel))
    result = getsolution(panel)
    if result != None:
        button40.configure(text="Hint!")
        print (result)
        for x in result:
            buttons[x[0]][x[1]].configure(bg="green")
    else:
        button40.configure(text="Already There!")

panel = initialize()

window = Tk()                                                # This part is to create the game window.
frame1 = Frame(window,bg="grey")

button00 = Button(frame1,height=5,width=15,bg=check(0,0),command=lambda:turncolor(0,0))
button00.grid(row=0,column=0)
button01 = Button(frame1,height=5,width=15,bg=check(0,1),command=lambda:turncolor(0,1))
button01.grid(row=0,column=1)
button02 = Button(frame1,height=5,width=15,bg=check(0,2),command=lambda:turncolor(0,2))
button02.grid(row=0,column=2)
button03 = Button(frame1,height=5,width=15,bg=check(0,3),command=lambda:turncolor(0,3))
button03.grid(row=0,column=3)
button10 = Button(frame1,height=5,width=15,bg=check(1,0),command=lambda:turncolor(1,0))
button10.grid(row=1,column=0)
button11 = Button(frame1,height=5,width=15,bg=check(1,1),command=lambda:turncolor(1,1))
button11.grid(row=1,column=1)
button12 = Button(frame1,height=5,width=15,bg=check(1,2),command=lambda:turncolor(1,2))
button12.grid(row=1,column=2)
button13 = Button(frame1,height=5,width=15,bg=check(1,3),command=lambda:turncolor(1,3))
button13.grid(row=1,column=3)
button20 = Button(frame1,height=5,width=15,bg=check(2,0),command=lambda:turncolor(2,0))
button20.grid(row=2,column=0)
button21 = Button(frame1,height=5,width=15,bg=check(2,1),command=lambda:turncolor(2,1))
button21.grid(row=2,column=1)
button22 = Button(frame1, height=5, width=15, bg=check(2,2),command=lambda:turncolor(2,2))
button22.grid(row=2, column=2)
button23 = Button(frame1, height=5, width=15, bg=check(2,3),command=lambda:turncolor(2,3))
button23.grid(row=2, column=3)
button30 = Button(frame1, height=5, width=15, bg=check(3,0),command=lambda:turncolor(3,0))
button30.grid(row=3, column=0)
button31 = Button(frame1, height=5, width=15, bg=check(3,1),command=lambda:turncolor(3,1))
button31.grid(row=3, column=1)
button32 = Button(frame1, height=5, width=15, bg=check(3,2),command=lambda:turncolor(3,2))
button32.grid(row=3, column=2)
button33 = Button(frame1, height=5, width=15, bg=check(3,3),command=lambda:turncolor(3,3))
button33.grid(row=3, column=3)
buttons=[[button00,button01,button02,button03],[button10,button11,button12,button13],[button20,button21,button22,button23],[button30,button31,button32,button33]]
frame1.grid(row=0)

frame2 = Frame(window)
button40 = Button(frame2,height=2,width=64,bg="gold",activebackground="pink",text="Hint!",command=lambda:showhint())
button40.grid()
frame2.grid(row=1)

window.mainloop()

# Please be patient after you click "Hint!", it takes some time to find the solution.#

# If you still have any confusion, please feel free to contact me.#



