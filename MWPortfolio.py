import numpy as np
import pandas as pd
from Portfolio5 import Portfolio
from scipy.optimize import minimize


class MarkowitzPortfolio(Portfolio):
    
    def __init__(self,stock,returns,eta):
        super().__init__(stock,returns,eta,"Markowitz Portfolio")
        self.stocks = stock
        self.returns = returns
        self.p =  self.transaction_cost_budget / len(self.stocks)
        self.num_stocks = len(self.stocks.columns) 
        
        
    def calculate_weights(self, t):
        # Select data up to day t
        returns_t = self.returns[:t + 7]

        # Calculate the mean returns and covariance matrix
        mean_returns = returns_t.mean(axis=0)
        cov_matrix = np.cov(returns_t.T)

        # Calculate the optimal weights using Markowitz optimization with positive weights constraint
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        ones_vector = np.ones(self.num_stocks)
        bounds = [(0, None)] * self.num_stocks  # Positive weights constraint
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]  # Constraint to ensure the weights sum up to 1
        
        risk_free_rate = 0.00

        def objective_function(w):
            portfolio_return = np.dot(mean_returns, w)
            portfolio_stddev = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_stddev #* (252 ** 0.5) 
            return -sharpe_ratio



        result = minimize(objective_function, ones_vector, method='SLSQP',
                          options={'maxiter': 10000},constraints = constraints, bounds=bounds)


        new_weights = result.x

       # if np.array_equal(new_weights, self.pesi) == False:
            #print(new_weights)

       # self.pesi = new_weights

        return new_weights


    def run(self,mode="percentage"):
        
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
            
            #find new weights 
            if self.transaction_cost_budget > 300:  #to not waste time in computing weights that cannot be updated
                new_weights = self.calculate_weights(t=t)
            
            else:
                new_weights = self.weights 
            

            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(t=t, new_weights = new_weights, mode = mode,visualize = False)
        