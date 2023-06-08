import numpy as np
import pandas as pd


class EquallyWeightedPortfolio:
    def __init__(self, stocks):
        self.stocks = stocks
        self.num_stocks = len(stocks.columns) -1
        self.weights = self.calculate_weights()
        self.budget = 100000
        
        initial_stocks = self.weights * self.budget / self.stocks.loc[0][1:]
        self.initial_stocks = np.floor(initial_stocks)
        self.remaining_budget = self.budget - np.sum(self.initial_stocks * self.stocks.loc[2][1:])
        
        self.transaction_cost = 10

    def calculate_weights(self):
        return np.array([1 / self.num_stocks] * self.num_stocks)
    
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

    def rebalance_portfolio(self,time,mode = "Single Transaction"):
        self.weights = self.calculate_weights()
        self.portfolio = self.weights * (self.budget - self.remaining_budget) / self.stocks.loc[time][1:]
        self.portfolio = np.floor(self.portfolio)


        #computing how much budget we have by removing the decimals  
        self.new_remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.loc[time][1:])
        #self.weights = self.portfolio * self.stocks.loc[t][1:] / (self.budget - self.remaining_budget)
        
        #computing transaction costs
        self.tr = self.transaction_costs(initial_stocks = self.initial_stocks, new_stocks = self.portfolio,mode = mode, time = time, perc = 0.2)
        
        #setting the portofolio of t-1
        self.initial_stocks = self.portfolio.copy()

        #updating new remaining budget
        self.remaining_budget = self.new_remaining_budget

        #updating the budget 
        self.budget = np.sum(self.portfolio * self.stocks.loc[time+1][1:]) + self.remaining_budget - self.tr

        #updating the weights 
        self.weights = self.portfolio * self.stocks.loc[time+1][1:] / (self.budget - self.remaining_budget)

        #updating the transaction costs budget
        #self.transaction_cost_budget -= self.tr
        
        
        #return (stocks.loc[time][1:] * self.weights).sum(axis=1)

