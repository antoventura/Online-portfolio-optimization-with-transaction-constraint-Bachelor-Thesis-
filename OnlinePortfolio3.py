import numpy as np
import pandas as pd

class OnlinePortfolioSelection:
    
    def __init__(self,stock,returns):
        self.stocks = stock
        self.budget = 10**5
        self.transaction_cost = 10
        self.returns = returns
        
        weights = np.array([1 / (len(stock.columns) -1) ] * (len(stock.columns) -1))   #uniform distribution at the start 
        initial_stocks = weights * self.budget / self.stocks.loc[0][1:]
        self.initial_stocks = np.floor(initial_stocks)
        self.remaining_budget = self.budget - np.sum(self.initial_stocks * self.stocks.loc[0][1:])
        self.weights = self.initial_stocks * self.stocks.loc[0][1:] / (self.budget - self.remaining_budget)
        
        self.cumulative_regret = 0
        
        
        #initialize lambda = 0
        self.Lambda = 0
        
        self.eta = 0.005
        
        self.transaction_cost_budget = 1000
        
        
        
    def transaction_costs(self,time=2,mode = "single transaction",budget = None, 
                         transaction_cost = None, initial_stocks = None, perc = 0.2, new_stocks = []):
        
        if budget is None:
            budget = self.budget
        if transaction_cost is None:
            transaction_cost = self.transaction_cost
        if initial_stocks is None:
            initial_stocks = self.initial_stocks


        diff = np.abs(initial_stocks - new_stocks)

        #Counting each transaction as unique, without considering the amount of stocks, but just how many different stocks we trade
        if mode == "single transaction":
            print(f"for time = {time} we had {(diff != 0).sum()} transactions")
            return (diff != 0).sum() * transaction_cost

        #Counting each stock as a transaction
        if mode == "single stock":
            print(f"for time = {time} we had {diff.sum()} transactions")
            return  diff.sum() *transaction_cost

        #Counting each stock as a transaction but with the percentage of the value of the stock
        if mode == "percentage":
            print(f"for time = {time} we had {diff.sum()} transactions")
            return (diff * self.stocks.loc[time][1:] * perc / 100).sum()
    
    
    
    def loss(self,t):
        
        #this because i have to udnerstand how to calculate transaction_cost without new weights
        if self.Lambda != 0:
            loss = self.returns.iloc[t] + (self.Lambda * (self.budget - self.tr))
        else:
            loss = self.returns.iloc[t]
        return loss
    
    
    #for now useless
    def regret(self,t):
        
        #to change with best expected stratgey weights (?)
        best_return = np.argmax((self.stocks.loc[t+1][1:]  - self.stocks.loc[t][1:]) / self.stocks.loc[t][1:])
        best_weight = np.zeros(10)
        best_weight[best_return] = 1
         
        return (best_weight * stocks.loc[t+1][1:]) - (self.weights * stocks.loc[t+1][1:])
        
    def rebalance_portfolio(self,t,new_weights,mode = "single transaction"):
        
        
        #updating positions and weights using previous function logic 
        self.portfolio = new_weights * (self.budget - self.remaining_budget) / self.stocks.loc[t][1:]
        self.portfolio = np.floor(self.portfolio)


        #computing how much budget we have by removing the decimals  
        self.new_remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.loc[t][1:])
        #self.weights = self.portfolio * self.stocks.loc[t][1:] / (self.budget - self.remaining_budget)
        
        #computing transaction costs
        self.tr = self.transaction_costs(initial_stocks = self.initial_stocks, new_stocks = self.portfolio,mode = mode, time = t, perc = 0.2)
        
        
        #if we have enough budget update the weights
        if self.transaction_cost_budget >= self.tr:
            
            #setting the portofolio of t-1
            self.initial_stocks = self.portfolio.copy()
            
            #updating new remaining budget
            self.remaining_budget = self.new_remaining_budget

            #updating the budget 
            self.budget = np.sum(self.portfolio * self.stocks.loc[t+1][1:]) + self.remaining_budget - self.tr

            #updating the weights 
            self.weights = self.portfolio * self.stocks.loc[t+1][1:] / (self.budget - self.remaining_budget)
            
            #updating the transaction costs budget
            self.transaction_cost_budget -= self.tr
            
            print(f"The weights have been updated and the new cost budget is {self.transaction_cost_budget}")
            
        #if we don't have enuough budget:
        else:
            self.portfolio = self.initial_stocks
            
            self.budget = np.sum(self.portfolio * self.stocks.loc[t+1][1:]) + self.remaining_budget


            
            print(f"the transaction cost is too high, the weights did not update")
            
        
        
        
    
    
    
        
        #remaining_budget = budget - np.sum(positions)
        #self.weights = positions / np.sum(positions)
        