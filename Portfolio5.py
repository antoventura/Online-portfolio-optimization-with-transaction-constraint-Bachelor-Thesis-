import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from tabulate import tabulate
import Metrics

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
        self.cumulative_cost = [] #initalize to [0], for computation purposes in cumulative_costs
        
        
        #initialize lambda = 0
        self.Lambda = 0
        
        self.eta = eta
        
        self.transaction_cost_budget = 1000 * 10
        self.initial_transaction_cost_budget = 1000 * 10
        
        self.cumulative_wealth = []
        self.daily_returns = []
        
        self.label = label
        
        self.tr = 0 
        
        
        
    def transaction_costs(self,time=2,mode = "percentage",budget = None, 
                         transaction_cost = None, initial_stocks = None, perc = 1, new_stocks = [],visualize = True):
        
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
                
            4.Percentage vector:
                For each single stock you sell or buy add a percentage of the value of the stock to the total transaction 
                cost of the day and returns the vector of costs for each stock
    
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
        
        if mode == "percentage vector":
            if visualize:
                print(f"for time = {time} we had {diff.sum()} transactions")
            return (diff * self.stocks.iloc[time] * perc / 100)
                
        
        
    def rebalance_portfolio(self,t,new_weights,mode = "single transaction",visualize = True):
        
        
        #updating positions and weights using previous function logic 
        self.portfolio = new_weights * (self.budget ) / self.stocks.iloc[t]
        self.portfolio = np.floor(self.portfolio)


        #computing how much budget we have by removing the decimals  
        self.new_remaining_budget = self.budget - np.sum(self.portfolio * self.stocks.iloc[t])
        #self.weights = self.portfolio * self.stocks.loc[t][1:] / (self.budget - self.remaining_budget)
        
        #computing transaction costs
        self.tr = self.transaction_costs(initial_stocks = self.initial_stocks,
                                         new_stocks = self.portfolio,mode = mode, 
                                         time = t, perc = 1, visualize = visualize)
        
        
        #if we have enough budget update the weights
        
        if mode == "percentage vector": #if mode is peercentage vector self.tr is a vector so we need to consider its sum
            if self.transaction_cost_budget >= self.tr.sum():

                #setting the portofolio of t-1
                self.initial_stocks = self.portfolio.copy()

                #updating new remaining budget
                self.remaining_budget = self.new_remaining_budget

                #updating the budget 
                self.budget = np.sum(self.portfolio * self.stocks.iloc[t+1]) + self.remaining_budget #- self.tr

                #updating the weights 
                self.weights = self.portfolio * self.stocks.iloc[t+1] / (self.budget - self.remaining_budget)

                #updating the transaction costs budget
                self.transaction_cost_budget -= self.tr.sum()
            
            #if we don't have enough budget:
            else:
                self.portfolio = self.initial_stocks

                self.budget = np.sum(self.portfolio * self.stocks.iloc[t+1]) + self.remaining_budget

                if visualize:
                    print(f"the transaction cost is too high, the weights did not update")
                
                
        else:
            if self.transaction_cost_budget >= self.tr:

                #setting the portofolio of t-1
                self.initial_stocks = self.portfolio.copy()

                #updating new remaining budget
                self.remaining_budget = self.new_remaining_budget

                #updating the budget 
                self.budget = np.sum(self.portfolio * self.stocks.iloc[t+1]) + self.remaining_budget #- self.tr

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

                if visualize:
                    print(f"the transaction cost is too high, the weights did not update")
    
      
    def benchmark(self,benchmark = [],transaction_cost = True):
        
        '''
        
        Function to plot the returns of the Portfolio optimization method and benchmark it with other methods.
        
        Takes 2 input:
        
            - benchmark : a list of names of other portfolio optimization methods already run
            
            - transaction_cost : a boolean value. If True print plot of transaction cost trend
            
        Returns: plot of portfolio value and expenses over time
        
        '''



        colors = [ "red", "green", "cyan", "magenta", "yellow", "black", "orange","purple","pink","brown","white"]
 
        colors_n = 0
    
 
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 14))
    
        #setting values for y axis values
        min_y = min(self.cumulative_wealth)
        max_y = max(self.cumulative_wealth)
    
        #plotting Portfolio returns
        ax1.plot([i for i in range(1,len(self.stocks)-1)], self.cumulative_wealth,
                 marker='o', linestyle='-',markersize = 3,label=self.label)
        
            
        
        
        
        #Plotting benchmarks
        for port in benchmark:
            
            ax1.plot([i for i in range(1,len(port.stocks)-1)], port.cumulative_wealth, marker='o',
                     linestyle='-',markersize = 3,label=port.label, color = colors[colors_n] ) 
            
            
            
            if transaction_cost:
                ax2.plot([i for i in range(1,len(port.stocks)-1)],port.cumulative_cost, marker='o',
                     linestyle='-',markersize = 3,label=port.label, color = colors[colors_n] ) 
                
                ax3.plot([i for i in range(1,len(port.stocks)-1)], np.array(port.cumulative_wealth) - np.array(port.cumulative_cost), marker='o',
                     linestyle='-',markersize = 3,label=port.label, color = colors[colors_n] ) 
                
                colors_n += 1
                
                if min(port.cumulative_wealth) < min_y:
                    min_y = min(port.cumulative_wealth)
                if max(port.cumulative_wealth) > max_y:
                    max_y = max(port.cumulative_wealth)
            
            
        

        ax1.set_xlabel('t')
        ax1.set_ylabel('Portfolio Budget')
        ax1.set_title('Portfolio Return Over Time')
        ax1.grid(True)
        
        #ax1.set_yticks(np.linspace(round(min_y, -5), round(max_y, -5), num=10))
        ax1.yaxis.get_major_formatter().set_scientific(False)
        ax1.yaxis.get_major_formatter().set_useOffset(False)

        ax1.legend()

      
        
        if transaction_cost:
            ax2.plot([i for i in range(1,len(self.stocks)-1)], self.cumulative_cost , marker='o',
                     linestyle='-',markersize = 3,label=self.label) 
            
            
            ax2.set_ylim(0, 10000)  #fix the rangeof values of the y axis to observe if the budget is well spent
            ax2.set_xlabel('t')
            ax2.set_ylabel('Portfolio Transaction Costs')
            ax2.set_title('Portfolio Costs Over Time')
            ax2.grid(True)
            
            
        #profit graph
            ax3.plot([i for i in range(1,len(self.stocks)-1)], np.array(self.cumulative_wealth) - np.array(self.cumulative_cost), marker='o',
                     linestyle='-',markersize = 3,label=self.label) 
            
            ax3.set_xlabel('t')
            ax3.set_ylabel('Portfolio Return - Transaction Costs')
            ax3.set_title('Portfolio Profit Over Time')
            ax3.grid(True)
        
        # Display the plot
        plt.show()
        
        
    def run_metrics(self,benchmark = [],exclude_metrics = [],benchmark_return = None):
        
        #check that the metrics you want to not consider are present in the metric list:
        allowed_metrics = ["Sharpe Ratio", "Max Drawdown (%)", "Annualized Return",
                           "Sortino Ratio", "Information Ratio", "Ulcer Ratio", "Winning %"]
        if not all(elem in set(allowed_metrics) for elem in exclude_metrics):
            raise Exception(f"the metrics you may exclude are: {allowed_metrics}")
            
        #remove metrix if exclude_metrics is not empty
        metric_functions = {
            "Sharpe Ratio": lambda: Metrics.sharpe_ratio(returns),
            "Max Drawdown (%)": lambda: Metrics.max_drawdown_period(returns, wealth),
            "Annualized Return": lambda: Metrics.annualized_return(np.array(returns)),
            "Sortino Ratio": lambda: Metrics.sortino_ratio(returns),
            "Information Ratio": lambda: Metrics.information_ratio(returns, benchmark_returns),
            "Ulcer Ratio": lambda: Metrics.ulcer(returns),
            "Winning %": lambda: Metrics.winning_percentage(returns)
        }

 
        
        for x in exclude_metrics:
            metric_functions.pop(x) 
            
        

     
        benchmark.append(self)
                            
        #creation of label list
        labels =[x.label for x in benchmark]
        labels.insert(0,'\033[1;' +self.label + '\033[0m')
        
        #creation of wealth list
        scores =[x.budget for x in benchmark]
    
        scores_pct  = list(np.array(scores) / 1000 -100)
        
        #initialize table
        data = []
        
        if "Equally Weighted Portfolio" not in [x.label for x in benchmark] and benchmark_return == None and "information ration" not in exclude_metrics :
            raise Exception("The Information Ratio metric requires EWSP100 Portfolio as the benchmark, but it is not included in the benchmark list. Please add EWSP100 or another benchmark as 'benchmark_return', or exclude the Information Ratio metric in the 'exclude_metrics' parameter.")


        #save benchmark returns for information_ratio  
        for portfolio in benchmark:
            if portfolio.label == "Equally Weighted Portfolio":
                benchmark_returns = portfolio.daily_returns
                
        for portfolio in benchmark:       
            if portfolio == self:
                label =  f"\033[1;31m{portfolio.label}\033[0m"
            else:
                label = portfolio.label
                
            returns = portfolio.daily_returns
            wealth = portfolio.cumulative_wealth


            current_metrics = [func() for func in metric_functions.values()]
            
       
            data.append([label, scores_pct[benchmark.index(portfolio)], *current_metrics])

        

        # Table headers
        headers = ["", "Profit (%)"]
        headers.extend(list(metric_functions.keys()))

        
       # Find the index of the maximum score
        max_score_index = scores.index(max(scores))

        max_indices = np.argmax(np.array(data)[:, 1:].astype(float), axis=0)
        min_indices = np.argmin(np.array(data)[:, 1:].astype(float), axis=0)
        
        #check index of max drawdown and ulcer ratio
        red_index = []
        if "Max Drawdown (%)" in headers:
            red_index.append(headers.index("Max Drawdown (%)")-1)
            
        if "Ulcer Ratio" in headers:
            red_index.append(headers.index("Ulcer Ratio")-1)
            
        self.ind = red_index
 
            
        for i, x in enumerate(max_indices):
            if i in red_index:
                data[x][i + 1] = f"\033[91m\033[1m{data[x][i + 1]}\033[0m"  # Red color for Max Drawdown and Ulcer
            else:
                data[x][i + 1] = f"\033[92m\033[1m{data[x][i + 1]}\033[0m"  # Green color for other indices
                
        for i, x in enumerate(min_indices):
            if i in red_index:
                data[x][i + 1] = f"\033[92m\033[1m{data[x][i + 1]}\033[0m"   
            else:
                data[x][i + 1] = f"\033[91m\033[1m{data[x][i + 1]}\033[0m"  

        # Print the table using tabulate
        print(tabulate(data, headers=headers, tablefmt="fancy_grid", numalign="center"))
        




        