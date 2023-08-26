import numpy as np
import pandas as pd
from Portfolio5 import Portfolio
from Opt import HedgeAlgorithm, OnlineGradientDescent

class OnlinePortfolioSelection(Portfolio):
    
    def __init__(self,stock,returns,eta,label = "Online Portfolio"):
        super().__init__(stock,returns,eta,label)
        self.stocks = stock
        self.returns = returns
        self.p =  self.transaction_cost_budget / len(self.stocks)
        

    def loss(self,t):
        
        #this because I have to understand how to calculate transaction_cost without new weights
        if self.Lambda != 0:
            #loss = self.returns.iloc[t] + (self.Lambda * (self.budget - self.tr))
            loss = self.returns.iloc[t] + (self.Lambda * (self.p - self.tr))
           
        else:
            loss = self.returns.iloc[t]
            

        return loss
    
    
    #for now useless
    def regret(self,t):
        
        #to change with best expected stratgey weights (?)
        best_return = np.argmax((self.stocks.iloc[t+1]  - self.stocks.iloc[t]) / self.stocks.iloc[t])
        best_weight = np.zeros(10)
        best_weight[best_return] = 1
         
        return (best_weight * stocks.iloc[t+1]) - (self.weights * stocks.iloc[t+1])
        
  
    
    
    def run(self,mode="percentage"):
        
        hedgeSP100 = HedgeAlgorithm(len(self.stocks.columns) )
        ogdSP100 = OnlineGradientDescent(num_stocks = len(self.stocks.columns) , learning_rate = 1/(np.sqrt(len(self.stocks))) )
        
        p = self.transaction_cost_budget / len(self.stocks)
        
        self.lambda_list = [] 
        self.ford = []
        a = 0
        for t in range(1,len(self.stocks)-1):
            
            #Compute daily returns
            if len(self.cumulative_wealth)> 0:
                daily_r = (-self.cumulative_wealth[-1] + self.budget) / self.cumulative_wealth[-1]
                self.daily_returns.append(daily_r)
            else: 
                daily_r = (-10**5 + self.budget) / 10**5
                self.daily_returns.append(daily_r)
                
            
            self.cumulative_wealth.append(self.budget)
             
            self.cumulative_cost.append(self.initial_transaction_cost_budget - self.transaction_cost_budget)
            
            #find new weights using hedge
            hedgeSP100.update_weights(self.weights,self.loss(t), learning_rate = self.eta) 
             
            hedge_weights = hedgeSP100.get_weights()
            
            if len(hedge_weights[hedge_weights != 0]) == 1 and a == 0:
                a= 1
                self.prova = self.loss(t)
                print(self.loss(t))
          


            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(t=t,new_weights = hedge_weights,mode = mode,visualize = False)

            #Update dual player strategy
            ogdSP100.update_lambda(self.p,self.tr)   
            self.Lambda = ogdSP100.get_lambda()
            self.lambda_list.append(self.Lambda)
            self.ford.append(self.initial_stocks["F"])
        
