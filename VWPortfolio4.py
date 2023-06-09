import numpy as np
import pandas as pd

class ValueWeightedPortfolio:
    def __init__(self,stock):
        self.stocks = stock
        self.num_stocks = len(stock.columns) 

        self.budget = 100000
        
        weights = np.array([1 / (len(stock.columns)) ] * (len(stock.columns)))   #uniform distribution at the start 
        initial_stocks = weights * self.budget / self.stocks.iloc[0]
        self.initial_stocks = np.floor(initial_stocks)
        self.remaining_budget = self.budget - np.sum(self.initial_stocks * self.stocks.iloc[0])
        self.weights = self.initial_stocks * self.stocks.iloc[0] / (self.budget - self.remaining_budget)
        
        
        self.transaction_cost = 10

    def calculate_weights(self,t):
        total_value = np.sum(self.weights * self.stocks.iloc[t])
        return self.weights * self.stocks.iloc[t] / total_value
        
    def transaction_costs(self,time=2,mode = "single transaction",budget = None, 
                         transaction_cost = None, initial_stocks = None, perc = 0.2, new_stocks = [],visualize = True):
        
        if budget is None:
            budget = self.budget
        if transaction_cost is None:
            transaction_cost = self.transaction_cost
        if initial_stocks is None:
            initial_stocks = self.initial_stocks


        diff = np.abs(initial_stocks - new_stocks)

        #Counting each transaction as unique, without considering the amount of stocks, but just how many different stocks we trade
        if mode == "single transaction":
            if visualize:
                print(f"for time = {time} we had {(diff != 0).sum()} transactions")
            return (diff != 0).sum() * transaction_cost

        #Counting each stock as a transaction
        if mode == "single stock":
            if visualize:
                print(f"for time = {time} we had {diff.sum()} transactions")
            return  diff.sum() *transaction_cost

        #Counting each stock as a transaction but with the percentage of the value of the stock
        if mode == "percentage":
            if visualize:
                print(f"for time = {time} we had {diff.sum()} transactions")
            return (diff * self.stocks.iloc[time] * perc / 100).sum()
    
    def rebalance_portfolio(self,time,mode = "Single Transaction",visualize = True):
        
        self.weights = self.calculate_weights(time)
        self.portfolio = self.weights * (self.budget) / self.stocks.iloc[time]    #rimettere il budget intero ogni volta ?
        self.portfolio = np.floor(self.portfolio)


        #computing how much budget we have by removing the decimals  
        self.new_remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.iloc[time])
        #self.weights = self.portfolio * self.stocks.loc[t][1:] / (self.budget - self.remaining_budget)
        
        #computing transaction costs
        self.tr = self.transaction_costs(initial_stocks = self.initial_stocks, new_stocks = self.portfolio,mode = mode, time = time, perc = 0.2,visualize = visualize)
        
        #setting the portofolio of t-1
        self.initial_stocks = self.portfolio.copy()

        #updating new remaining budget
        self.remaining_budget = self.new_remaining_budget

        #updating the budget 
        self.budget = np.sum(self.portfolio * self.stocks.iloc[time+1]) + self.remaining_budget - self.tr

        #updating the weights 
        self.weights = self.portfolio * self.stocks.iloc[time+1] / (self.budget - self.remaining_budget)

        #updating the transaction costs budget
        #self.transaction_cost_budget -= self.tr
        
        
        #return (stocks.loc[time][1:] * self.weights).sum(axis=1)


