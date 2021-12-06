from numpy import *

def sigmoid(x):
    return 1 / (1+exp(-x))

def dsigmoid(x):
    return x * (1 - x)

class NeuralNet:
    def __init__(self):
        self.hiddenLayerW = None
        self.outputLayerW = None
        self.output = None
        self.MSE = None
        self.trained = False
        
    def predict( self, X ):
        ### ... YOU FILL IN THIS CODE ....
        
    def train(self,X,Y,hiddenLayerSize,epochs):    
        ## size of input layer (number of inputs plus bias)
        ni = X.shape[1] + 1

        ## size of hidden layer (number of hidden nodes plus bias)
        nh = hiddenLayerSize + 1

        # size of output layer
        no = 10

        ## initialize weight matrix for hidden layer
        self.hiddenLayerW = 2*random.random((ni,nh)) - 1

        ## initialize weight matrix for output layer
        self.outputLayerW = 2*random.random((nh,no)) - 1

        ## learning rate
        alpha = 0.001

        ## Mark as not trained
        self.trained = False
        ## Set up MSE array
        self.MSE = [0]*epochs

        for epoch in range(epochs):

            ### ... YOU FILL IN THIS CODE ....

            ## Record MSE
            self.MSE[epoch] = mean(list(map(lambda x:x**2,error_out)))

            ### ... YOU FILL IN THIS CODE

        ## Update trained flag
        self.trained = True

