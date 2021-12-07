import numpy as np
from numpy import *


def sigmoid(x):
    return 1 / (1 + exp(-x))


def dsigmoid(x):
    return x * (1 - x)


class NeuralNet:
    def __init__(self):
        self.hiddenLayerW = None
        self.outputLayerW = None
        self.output = None
        self.MSE = None
        self.trained = False

    def predict(self, X):
        ##  activation of input layer
        alpha_0 = np.hstack(([1], X))

        ## compute activation of output layer
        return sigmoid(np.dot(sigmoid(np.dot(alpha_0, self.hiddenLayerW)), self.outputLayerW))

    def train(self, X, Y, hiddenLayerSize, epochs):
        ## size of input layer (number of inputs plus bias)
        ni = X.shape[1] + 1

        ## size of hidden layer (number of hidden nodes plus bias)
        nh = hiddenLayerSize + 1

        # size of output layer
        no = 10

        ## initialize weight matrix for hidden layer
        self.hiddenLayerW = 2 * random.random((ni, nh)) - 1

        ## initialize weight matrix for output layer
        self.outputLayerW = 2 * random.random((nh, no)) - 1

        ## learning rate
        alpha = 0.001

        ## Mark as not trained
        self.trained = False
        ## Set up MSE array
        self.MSE = [0] * epochs

        for epoch in range(epochs):
            ## activation of input layer
            alpha_0 = np.hstack((np.ones((X.shape[0], 1)), X))

            ## input to hidden layer
            in_0 = np.dot(alpha_0, self.hiddenLayerW)

            ## activation of hidden layer
            alpha_1 = sigmoid(in_0)

            ## set bias unit for hidden layer
            alpha_1[:, 0] = 1

            ## input to output layer
            in_1 = np.dot(alpha_1, self.outputLayerW)

            ## activation of output layer
            alpha_2 = sigmoid(in_1)

            ## observed error on output
            error_out = Y - alpha_2

            ## direction of target
            delta_out = error_out * dsigmoid(alpha_2)

            ## Record MSE
            self.MSE[epoch] = mean(list(map(lambda x: x ** 2, error_out)))

            ## contribution of hidden nodes to error
            error_hidden = np.dot(delta_out, self.outputLayerW.T)

            ## direction of target for hidden layer
            delta_hidden = error_hidden * dsigmoid(alpha_1)

            ## hidden layer weight update
            self.hiddenLayerW = self.hiddenLayerW + alpha * np.dot(alpha_0.T, delta_hidden)

            ## output layer weight update
            self.outputLayerW = self.outputLayerW + alpha * np.dot(alpha_1.T, delta_out)

        ## Update trained flag
        self.trained = True
