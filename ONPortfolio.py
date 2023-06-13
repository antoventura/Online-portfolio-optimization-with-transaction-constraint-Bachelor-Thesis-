import numpy as np
import pandas as pd
from Portfolio5 import Portfolio
from Opt import HedgeAlgorithm, OnlineGradientDescent

class OnlinePortfolioSelection(Portfolio):
    
    def __init__(self,stock,returns,eta):
        super().__init__(stock,returns,eta,"Online Portfolio")
        self.stocks = stock
        self.returns = returns
        

    def loss(self,t):
        
        #this because I have to understand how to calculate transaction_cost without new weights
        p = 1000 / len(self.stocks.columns)
        if self.Lambda != 0:
            #loss = self.returns.iloc[t] + (self.Lambda * (self.budget - self.tr))
            loss = self.returns.iloc[t] + (self.Lambda * (p - self.tr))
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
        
    def rebalance_portfolio(self,t,new_weights,mode = "single transaction",visualize = True):
        
        
        #updating positions and weights using previous function logic 
        self.portfolio = new_weights * (self.budget ) / self.stocks.iloc[t]
        self.portfolio = np.floor(self.portfolio)


        #computing how much budget we have by removing the decimals  
        self.new_remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.iloc[t])
        #self.weights = self.portfolio * self.stocks.loc[t][1:] / (self.budget - self.remaining_budget)
        
        #computing transaction costs
        self.tr = self.transaction_costs(initial_stocks = self.initial_stocks, new_stocks = self.portfolio,mode = mode, time = t, perc = 0.2, visualize = visualize)
        
        
        #if we have enough budget update the weights
        if self.transaction_cost_budget >= self.tr:
            
            #setting the portofolio of t-1
            self.initial_stocks = self.portfolio.copy()
            
            #updating new remaining budget
            self.remaining_budget = self.new_remaining_budget

            #updating the budget 
            self.budget = np.sum(self.portfolio * self.stocks.iloc[t+1]) + self.remaining_budget - self.tr

            #updating the weights 
            self.weights = self.portfolio * self.stocks.iloc[t+1] / (self.budget - self.remaining_budget)
            
            #updating the transaction costs budget
            self.transaction_cost_budget -= self.tr
            
            if visualize:
                print(f"The weights have been updated and the new cost budget is {self.transaction_cost_budget}")
            
        #if we don't have enough budget:
        else:
            self.portfolio = self.initial_stocks
            
            self.budget = np.sum(self.portfolio * self.stocks.iloc[t+1]) + self.remaining_budget
  
            print(f"the transaction cost is too high, the weights did not update")
    
    
    def run(self):
        
        hedgeSP100 = HedgeAlgorithm(len(self.stocks.columns) )
        ogdSP100 = OnlineGradientDescent(num_stocks = len(self.stocks.columns) , learning_rate = self.eta )
        
        p = self.transaction_cost_budget / len(self.stocks.columns)
        
        for t in range(1,len(self.stocks)-1):
            
            self.cumulative_wealth.append(self.budget)
            #find new weights using hedge
            hedgeSP100.update_weights(self.weights,self.loss(t), learning_rate = self.eta)  
            hedge_weights = hedgeSP100.get_weights()

            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(t=t,new_weights = hedge_weights,mode = "percentage",visualize = False)

            #Update dual player strategy
            ogdSP100.update_lambda(p,self.tr)   
            self.Lambda = ogdSP100.get_lambda()
            
        

