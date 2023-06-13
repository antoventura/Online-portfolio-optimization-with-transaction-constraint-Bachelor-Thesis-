import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

class Portfolio:
 
    def __init__(self,stock,returns = 0,eta = 0.05,label = "Portfolio"):
        
        '''
        Initialize Portfolio class with uniform weights and rounding up the number of stocks
        Set the Portfolio budget to 100'000 and the transaction budget to 1'000

        '''
    
        self.stocks = stock
        self.budget = 10**5
        self.transaction_cost = 10
        
        if type(returns) != int:
            self.returns = returns
        
        weights = np.array([1 / (len(stock.columns)) ] * (len(stock.columns)))   #uniform distribution at the start 
        initial_stocks = weights * self.budget / self.stocks.iloc[0]
        self.initial_stocks = np.floor(initial_stocks)
        self.remaining_budget = self.budget - np.sum(self.initial_stocks * self.stocks.iloc[0])
        self.weights = self.initial_stocks * self.stocks.iloc[0] / (self.budget - self.remaining_budget)
        
        self.cumulative_regret = 0
        
        
        #initialize lambda = 0
        self.Lambda = 0
        
        self.eta = eta
        
        self.transaction_cost_budget = 1000
        
        self.cumulative_wealth = []
        
        self.label = label
    def transaction_costs(self,time=2,mode = "single transaction",budget = None, 
                         transaction_cost = None, initial_stocks = None, perc = 0.2, new_stocks = [],visualize = True):
        
        '''
        Function to compute transaction costs for each day trades.
        It takes as input the present portfolio composition and the possible new portfolio composition with the new weights
        It returns the cost for the transactions
    
        
        Three methods:
        
            1. Single transaction:
                For every asset for which you sell or buy any amount of stocks add the transaction constant to the total 
                transaction cost of the day
                
            2. Single stock:
                For each single stock you sell or buy add the transaction constant to the total transaction cost of the day
                
            3. Percentage:
                For each single stock you sell or buy add a percentage of the value of the stock to the total transaction 
                cost of the day
    
        '''
        
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
        
    
      
    def benchmark(self,benchmark = []):
        '''
        Function to plot the returns of the Portfolio optimization method and benchmark it with other methods
        
        '''



        #average s&p100 returns
        avg_returns = []
        avg_budget = 100000
        
        colors = [ "red", "green", "cyan", "magenta", "yellow", "black", "white", "orange","purple","pink","brown"]
 
        colors_n = 0
    
        plt.figure(figsize=(20, 7))
    
        #plotting Portfolio returns
        plt.plot([i for i in range(1,len(self.stocks)-1)], self.cumulative_wealth,
                 marker='o', linestyle='-',markersize = 4,label=self.label)
        
        #Plotting benchmarks
        for port in benchmark:
            
            plt.plot([i for i in range(1,len(port.stocks)-1)], port.cumulative_wealth, marker='o',
                     linestyle='-',markersize = 4,label=port.label, color = colors[colors_n] ) 
            
            colors_n += 1
        

        plt.xlabel('t')
        plt.ylabel('Portfolio Budget')
        plt.title('Portfolio Profit Over Time')
        plt.grid(True)

        plt.legend()

        plt.figure(figsize=(13, 7))

        # Display the plot
        plt.show()