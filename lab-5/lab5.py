from numpy import *
from NeuralNet import *
from tkinter import *
import threading

train = array(loadtxt("train.dat"))
test = array(loadtxt("test.dat"))

Ytrain = train[:,[0]]
Xtrain = train[:,1:]
Ytrain = array([[0]*10]*train.shape[0])
for i in range(train.shape[0]):
    Ytrain[i,int(train[i,[0]])] = 1


Ytest = test[:,[0]]
Ytest = array([[0]*10]*test.shape[0])
for i in range(test.shape[0]):
    Ytest[i,int(test[i,[0]])] = 1
Xtest = test[:,1:]

def pixval(x):
    x = int((1-(x+1)/2)*255)
    return '#'+'{0:02x}'.format(x)+'{0:02x}'.format(x)+'{0:02x}'.format(x)

class Application:
    def __init__(self):

        ## initialize root window
        self.root = Tk()
        self.root.title( "Live handwriting recognition lab" )
        self.root.geometry( "500x500" )
        self.root.resizable(False,False)

        ## register validator for numbers only input
        vcmd = (self.root.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        ## Set up canvas for input window
        self.input = Canvas( self.root, width=160, height=160 )
        self.input.place(x=0,y=0)
        # bind mouse clicks to canvas
        self.input.bind("<Button-1>", self.paint)
        # bind mouse dragging event to canvas
        self.input.bind( "<B1-Motion>", self.paint )
        # bind right mouse click to clear
        self.input.bind( "<Button-3>", self.clear )

        ## Set up test load interface
        self.testEntry = Frame(self.root)
        self.testEntry.place(x=200,y=10)
        self.loadTestEntry = Entry(self.testEntry,width=4,validate="key",validatecommand=vcmd)
        self.loadTestEntry.pack(side=RIGHT)
        self.labTestEntry = Label(self.testEntry, width=15, text="Load test instance:", anchor="w")
        self.labTestEntry.pack(side=LEFT)
        self.loadTestEntry.bind("<Return>",self.loadTest)
        self.loadTestEntry.bind("<KP_Enter>",self.loadTest)
        self.display = Canvas( self.root, width=500,height=500-160)
        self.display.place(x=0,y=160)

        ## Create a neural network
        self.nnet = NeuralNet()
        self.nnetInput = [0]*256

        ## set up nerual net control
        self.nnetControl = Frame(self.root)
        self.nnetControl.place(x=170,y=30)
        self.nnetTrainEpochsEntry = Entry(self.nnetControl,width=5,validate="key",validatecommand=vcmd)
        self.nnetTrainEpochsEntry.grid(row=0,column=0,sticky=E)
        self.nnetTrainEpochsLabel = Label(self.nnetControl,width=6,text="epochs")
        self.nnetTrainEpochsLabel.grid(row=0,column=1,sticky=W)
        self.nnetTrainHLSizeEntry = Entry(self.nnetControl,width=5)
        self.nnetTrainHLSizeEntry.grid(row=1,column=0,sticky=E)
        self.nnetTrainHLSizeLabel = Label(self.nnetControl,width=13,text="hidden layer size")
        self.nnetTrainHLSizeLabel.grid(row=1,column=1,sticky=W)

        self.nnetTrainButton = Button(self.nnetControl,text="Train",width=6,command=self.spawn_train_thread)
        self.nnetTrainButton.grid(row=2,column=0,sticky=W)

        self.nnetShowMSEButton = Button(self.nnetControl,text="MSE",width=6,command=self.showMSE,state='disabled')
        self.nnetShowMSEButton.grid(row=3,column=0,sticky=W)

        self.nnetStatusLabel = Label(self.nnetControl,width=6)
        self.nnetStatusLabel.configure(text="STATUS:",anchor=E)
        self.nnetStatusLabel.grid(row=4,column=0,sticky=E)
        self.nnetStatusText = Label(self.nnetControl,width=20)
        self.nnetStatusText.configure(text="Ready to train",anchor=W)
        self.nnetStatusText.grid(row=4,column=1,sticky=W)


        ## clear everything
        self.clear(None)

    ## run training in background
    def spawn_train_thread(self):
        thread = threading.Thread(target=self.train)
        thread.start()

    ## neural net training callback
    def train( self ):

        ## get parameters from text entry
        if self.nnetTrainEpochsEntry.get() == '': return
        if self.nnetTrainHLSizeEntry.get() == '': return
        epochs = int(self.nnetTrainEpochsEntry.get())
        hlsize = int(self.nnetTrainHLSizeEntry.get())

        ## app bookkeeping
        self.clear(None)
        self.nnetTrainButton['state'] = "disabled"
        self.input['state'] = "disabled"
        self.nnetShowMSEButton['state'] = "disabled"
        self.nnetTrainEpochsEntry['state'] = "disabled"
        self.nnetTrainHLSizeEntry['state'] = "disabled"
        self.nnetStatusText.configure(text="Training...")
        self.nnetStatusText.update()

        ## train neural net
        self.nnet.train(Xtrain,Ytrain,hlsize,epochs)

        ## app bookkeeping
        self.nnetStatusText.configure(text="Trained")
        self.nnetTrainButton['state'] = "normal"
        self.input['state'] = "normal"
        self.nnetShowMSEButton['state'] = "normal"
        self.nnetTrainEpochsEntry['state'] = "normal"
        self.nnetTrainHLSizeEntry['state'] = "normal"

    ## write a prediction barchart in the display
    def predict( self ):
        if not self.nnet.trained: return ## not trained yet
        h = self.nnet.predict(self.nnetInput)
        self.display.delete("all")
        pos=(100,320)
        scale = (pos[1]-1)
        barw = 30
        for i in range(10):
            self.display.create_text(pos[0]+(i+0.5)*barw,pos[1]+10,justify=CENTER,text=str(i))
            self.display.create_rectangle(pos[0]+i*barw,pos[1],pos[0]+(i+1)*barw,pos[1]-h[i]*scale,fill="blue")

    ## write a MSE plot in the display
    def showMSE( self ):
        if not self.nnet.trained: return ## not trained yet
        self.clear(None)

        ## plot dimensions and scaling factors
        xmax = 460
        xmin = 10
        ymax = 330
        ymin = 10
        maxMSE = max(self.nnet.MSE)
        lenMSE = len(self.nnet.MSE)

        ## plot area
        self.display.create_rectangle(xmin,ymin,xmax,ymax,fill="white")
        self.display.create_text((xmax-xmin)/2,ymin+10,text="Mean-squared error / time")

        ## axes
        ticks=10
        ypos = list(map(int,linspace(start=ymax,stop=ymin,num=ticks)))
        ylab = linspace(start=0,stop=maxMSE,num=ticks)
        print(ylab)
        for i in range(ticks):
            self.display.create_text(xmax+5,ypos[i],text='{:.2f}'.format(ylab[i]),font=('fixed',8),anchor="w")
            self.display.create_line(xmax-5,ypos[i],xmax-2,ypos[i])
        self.display.create_line(xmax-2,ypos[0],xmax-2,ypos[len(ypos)-1])

        ## draw the plot
        for i in range(1,lenMSE):
            x1 = (xmax-xmin)*float(i-1)/(lenMSE-1) + xmin
            y1 = (ymin-ymax)*float(self.nnet.MSE[i-1])/maxMSE + ymax
            x2 = (xmax - xmin)*float(i)/(lenMSE-1) + xmin
            y2 = (ymin - ymax)*float(self.nnet.MSE[i])/maxMSE + ymax
            self.display.create_line(x1,y1,x2,y2,width=2,fill='blue')

    ## routine for painting in the input window    
    def paint( self, event ):
        if not self.nnet.trained: return ## not trained yet
        if event.x < 160 and event.y < 160:

            ## calculate which element of the 16x16 grid was clicked
            sqx = event.x/10
            sqy = event.y/10

            ## activate the neural net input for the corresponding pixel
            self.nnetInput[int(sqx + 16*sqy)] = 1;

            ## draw on the display
            x1, y1 = (10*sqx), (10*sqy)
            x2, y2 = (10*sqx + 10 ), (10*sqy + 10 )
            self.input.create_rectangle( x1, y1, x2, y2, fill = "black" )

            ## use the neural net to predict the digit
            self.predict()

            ## clear the test entry text box
            self.loadTestEntry.delete(0)

    def clear( self, event ):
        self.nnetInput = [-1]*256;
        self.input.delete("all")
        self.input.create_rectangle(1,1,160,160,fill="white")
        self.display.delete("all")


    def loadTest( self ,entry=None):
        self.clear(None)
        s = self.loadTestEntry.get()
        if s.isdigit() and int(s) < Xtest.shape[0]:
            k=int(s)
            for i in range(Xtest.shape[1]):
                self.input.create_rectangle((i%16)*10,(i/16)*10,(i%16)*10+10,(i/16)*10+10,fill=pixval(Xtest[k,i]),outline=pixval(Xtest[k,i]));
            ## Set input of neural network
            self.nnetInput = Xtest[k,]
            self.predict()
        else:
            self.loadTestEntry.delete(0,END)
        self.input.create_rectangle(1,1,160,160)

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if len(value_if_allowed) == 0: return True
        if text in '0123456789':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
