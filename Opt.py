import numpy as np
import pandas as pd

class HedgeAlgorithm:
    def __init__(self, num_stocks):
        self.num_stocks = num_stocks
        self.weights = np.ones(num_stocks) / num_stocks
    
    def update_weights(self, weights, loss_vector, learning_rate):
        exponentiated_losses = np.exp(-learning_rate * loss_vector)
        self.weights = weights * exponentiated_losses / np.sum(weights * exponentiated_losses)
    
    def get_weights(self):
        return self.weights


class OnlineGradientDescent:
    def __init__(self, num_stocks, learning_rate):
        self.num_stocks = num_stocks
        self.learning_rate = learning_rate
        self.weights = np.ones(num_stocks) / num_stocks
        self.Lambda = 0
    
    def update_lambda(self, p,cost):
        
        new_lambda = self.Lambda + self.learning_rate * (p - cost)
        
        if new_lambda <0 :
            self.Lambda = 0 

        if new_lambda > 1/ p:
            self.Lambda = 1/ p
            
        else:
            self.Lambda = new_lambda
            

    def get_lambda(self):
        return self.Lambda


