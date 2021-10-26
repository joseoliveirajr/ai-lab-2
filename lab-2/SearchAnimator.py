
##
## CS 4222/5222 Artificial Intelligence
## Fall 2021
##
## Lab 2: path finding. This is the animation module for the graph
## search algorithms
##
##

import math
import pickle
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from time import time, sleep


from SearchProblem import *

## spherical Mercator projection of lat/lon coords
def merc(coords,mapw,maph):
    x = (coords[1]+180)*(mapw/360.0)
    latRad = coords[0]*math.pi/180.0
    mercN = math.log(math.tan((math.pi/4.0)+(latRad/2.0)))
    y = maph/2.0 - (maph*mercN)/(2.0*math.pi)
    return (x,y)

## transform coordinates from graph locations to fit on canvas
## margin is pixels of padding from canvas bounding box
def transform(coords,graph,canvas):
    margin=50    
    wfactor = canvas.winfo_reqwidth() - 2*margin
    hfactor = canvas.winfo_reqheight() - 2*margin

    if graph.geo:
        maxproj = merc((graph.xmax,graph.ymax),wfactor,hfactor)
        minproj = merc((graph.xmin,graph.ymin),wfactor,hfactor)
        x,y = merc(coords,wfactor,hfactor)
        rx = wfactor/(maxproj[0]-minproj[0])
        ry = hfactor/(maxproj[1]-minproj[1])
        return (rx*(x-minproj[0])+margin,hfactor-ry*(y-minproj[1])+margin)
    else:
        x,y = coords
        rx = wfactor/(graph.xmax-graph.xmin)
        ry = hfactor/(graph.ymax-graph.ymin)    
        return (rx*(x-graph.xmin)+margin,hfactor-ry*(y-graph.ymin)+margin)

class SearchAnimator:
    def __init__(self,algos):
        self.algos = algos
        
    ## Draw the graph on the main canvas
    def draw(self,graph):
        for v in graph.nodes():
            x1,y1 = transform(graph.locations[v],graph,self.canvas)
            for u in graph.dict[v]:
                x2,y2 = transform(graph.locations[u],graph,self.canvas)
                self.canvas.create_line(x1,y1,x2,y2)
        for node in graph.locations:
            x,y = transform(graph.locations[node],graph,self.canvas)
            self.canvas.create_rectangle( x-1, y-1, x+1, y+1, fill = "gray" )
            if len(graph.nodes()) < 50: self.canvas.create_text(x-2,y-2,text=node)

    ## Trace the path (list of nodes) in red on the canvas
    def draw_path(self,graph,path):
        coords = list(map(lambda v: transform(graph.locations[v.state],graph,self.canvas),path))
        x,y = coords[0]
        self.canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "red" )
        for xnext,ynext in coords[1:]:
            self.canvas.create_line(x,y,xnext,ynext,width=4,fill="red")
            x,y = xnext,ynext

    ## Retrieve the solution from the path, calculate its cost and display
    def get_solution(self,graph,path):
        cost=0;
        statePath = list(map(lambda v: v.state,path))
        statePath.reverse()
        for i in range(len(statePath)-1):
            cost = cost+graph.get(statePath[i],statePath[i+1])
        self.pathCostStr.set(str(cost))

    ## Mark all the nodes in the fringe set with blue
    def draw_fringe(self,graph,fringe):
        coords = map(lambda v: graph.locations[v.state],fringe)
        for x,y in coords:
            x,y = transform((x,y),graph,self.canvas)
            self.canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "blue" )

    ## Mark all the nodes in the closed set with black
    def draw_closed(self,graph,closed):
        coords = list(map(lambda state: transform(graph.locations[state],graph,self.canvas),closed))
        for x,y in coords:
            self.canvas.create_rectangle( x-3, y-3, x+3, y+3, fill = "black" )

    ## Display the number of nodes generated since search began
    def display_nodecount(self):
        self.nodeCountStr.set(str(Node.nodecount))

    ## Callback registered with search algorithm to be called in each
    ## iteration to display the search state
    def callback(self,graph,node,fringe,closed,halt):
        self.canvas.delete("all")
        self.draw(graph)
        self.draw_fringe(graph,fringe)
        self.draw_path(graph,node.path())
        self.draw_closed(graph,closed)
        self.display_nodecount()
        if halt: self.get_solution(graph,node.path())
        self.root.update_idletasks()
        sleep(self.speed.get())

    ## Create a search problem on the graph, with initial state and goal,
    ## and run the selected search algorithm
    def run_search_alg(self,graph):
        self.speedLabel['state']=DISABLED
        self.speedSlider['state'] = DISABLED
        prob = SearchProblem(self.start.get(),self.goal.get(),graph)
        self.pathCostStr.set("")
        alg = self.algos[self.algo.get()]
        alg(prob,self.callback)
        self.speedLabel['state'] = NORMAL
        self.speedSlider['state'] = NORMAL

    def loadInstance(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        with open(filename,'rb') as f: self.graph= pickle.load(f)
        f.close()

        ## compute bounding box corners
        self.graph.xmin = min([x for (x,y) in self.graph.locations.values()])
        self.graph.xmax = max([x for (x,y) in self.graph.locations.values()])
        self.graph.ymin = min([y for (x,y) in self.graph.locations.values()])
        self.graph.ymax = max([y for (x,y) in self.graph.locations.values()])

        ## Populate menus
        self.startNodeMenu['menu'].delete(0,'end')
        self.startNodeMenu['state']=NORMAL
        self.startNodeLabel['state']=NORMAL
        for node in self.graph.nodes():
            self.startNodeMenu['menu'].add_command(label=node, command=lambda x=node:self.start.set(x))
        self.start.set(self.graph.default_start)
        self.goalNodeMenu['menu'].delete(0,'end')
        self.goalNodeMenu['state']=NORMAL
        self.goalNodeLabel['state']=NORMAL
        for node in self.graph.nodes():
            self.goalNodeMenu['menu'].add_command(label=node, command=lambda x=node:self.goal.set(x))
        self.goal.set(self.graph.default_goal)
        self.canvas.delete("all")
        self.draw(self.graph)
        self.go.configure(command=lambda x=self.graph:self.run_search_alg(self.graph))
        self.go['state'] = NORMAL

    def run(self):
        ## Initialize environment
        self.root = Tk()
        windowWidth = 1200
        windowHeight = 700
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)

        # Positions the window in the center of the page.
        self.root.geometry("{}x{}".format(windowWidth, windowHeight) + "+{}+{}".format(positionRight, positionDown))
        self.root.title( "Search Animator" )

        ## Set up canvas for input window
        self.canvas = Canvas( self.root, width=windowWidth-300, height=windowHeight )
        self.canvas.place(x=0,y=0)

        ## Set up canvas for control panel
        controlFrame = Frame(self.root, height=windowHeight-180,width=275,borderwidth=2,relief=SUNKEN)
        controlFrame.place(x=900,y=200/2);
        controlFrame.propagate(0)
        self.control = Canvas(controlFrame)
        self.control.pack(expand=YES,fill=BOTH)


        ## Start node menu (this needs to be populated after load)
        self.start = StringVar(self.root)
        self.startNodeMenu = OptionMenu(self.control,self.start,None)
        self.startNodeMenu.grid(row=2,column=2,sticky=W,padx=5,pady=5)
        self.startNodeLabel = Label(self.control,text="Start:")
        self.startNodeLabel.grid(row=2,column=1,sticky=E,padx=5,pady=5)
        self.startNodeMenu["state"]=DISABLED
        self.startNodeLabel["state"]=DISABLED

        ## Goal node menu (this needs to be populated after load)
        self.goal = StringVar(self.root)
        self.goalNodeMenu = OptionMenu(self.control,self.goal,None)
        self.goalNodeMenu.grid(row=3,column=2,sticky=W,padx=5,pady=5)
        self.goalNodeLabel = Label(self.control,text="Goal:")
        self.goalNodeLabel.grid(row=3,column=1,sticky=E,padx=5,pady=5)
        self.goalNodeMenu["state"]=DISABLED
        self.goalNodeLabel["state"]=DISABLED

        ## Algo menu
        #self.algos = ["graph search", "BFS", "DFS", "greedy best-first", "A*", "IDS"]

        ## self.algos is a dictionary of search functions keyed by string
        self.algo = StringVar(self.root)
        self.algo.set(list(self.algos.keys())[0])
        self.algoMenu = OptionMenu(self.control,self.algo,*self.algos.keys())
        self.algoMenu.grid(row=4,column=2,sticky=W,padx=5,pady=5)
        Label(self.control,text="Algo:").grid(row=4,column=1,sticky=E,padx=5,pady=5)

        self.graph=None

        ## Go button
        self.go = Button(self.control,text="Go",width=10)
        self.go.grid(row=1,column=1,sticky='w',padx=5,pady=5)
        self.go["state"] = DISABLED
        self.go.propagate(0)

        ## Load button
        self.load = Button(self.control,text='Load',width=10,command=self.loadInstance)
        self.load.grid(row=1,column=2,sticky='w',padx=5,pady=5)
        self.load.propagate(0)

        ## Nodes generated display
        self.nodeCountStr = StringVar(self.root)
        Label(self.control,text="Nodes generated:").grid(row=5,column=1,sticky=E,padx=5,pady=5)
        Label(self.control,textvariable=self.nodeCountStr).grid(row=5,column=2,sticky=W,padx=5,pady=5)
        self.nodeCountStr.set("0")

        ## Solution cost display
        self.pathCostStr = StringVar(self.root)
        Label(self.control,text="Solution cost:").grid(row=6,column=1,sticky=E,padx=5,pady=5)
        Label(self.control,textvariable=self.pathCostStr).grid(row=6,column=2,sticky=W,padx=5,pady=5)
        self.pathCostStr.set("")

        self.speed = DoubleVar(self.root)
        self.speedLabel  = Label(self.control,text="Speed:")
        self.speedSlider = Scale(self.control,from_=1,to=0.01,resolution=0.01,variable=self.speed,orient=HORIZONTAL,
                            showvalue=False)
        self.speed.set(1)
        self.speedLabel.grid(row=7,column=1,sticky=E,padx=5,pady=5)
        self.speedLabel.propagate(0)
        self.speedSlider.grid(row=7,column=2,sticky=W,padx=5,pady=5)
        self.speedSlider.propagate(0)

        self.root.mainloop()

