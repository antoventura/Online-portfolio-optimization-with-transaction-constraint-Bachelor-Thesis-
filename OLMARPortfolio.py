import numpy as np
import pandas as pd
from Portfolio5 import Portfolio

class OLMARPortfolio(Portfolio):
    
    
    '''
    On-Line Portfolio Selection with Moving Average Reversion

    Reference:
        B. Li and S. C. H. Hoi.
        On-line portfolio selection with moving average reversion, 2012.
        http://icml.cc/2012/papers/168.pdf
    
    
    Ispiration from 
    https://github.com/Marigold/universal-portfolios/blob/master/universal/algos/olmar.py
    '''
    
    def __init__(self,stock,returns,eta,window = 5, eps = 50, alpha = 0.5):
        super().__init__(stock,returns,eta,"OLMAR Portfolio")
        self.stocks = stock
        self.returns = returns
        self.p =  self.transaction_cost_budget / len(self.stocks)
        self.num_stocks = len(self.stocks.columns) 
        self.eta = eta
        
        self.window = window
        self.eps = eps
        self.alpha = alpha  # Smoothing factor for EMA
        

        self.ema_returns = np.zeros(self.num_stocks)
        self.b = self.weights.copy()
        self.x_pred = returns.iloc[0, :]  #initialize first prediction
        
  
        
    def calculate_weights(self,t):
        asset_returns = self.stocks[:t]

        # Compute the Exponential Moving Average for each asset
        if len(asset_returns) < self.window:
            self.x_pred = np.mean(asset_returns, axis=0)
        else:
            real_x = asset_returns.iloc[-1, :] / asset_returns.iloc[-2, :]
            x_pred = self.alpha + (1 - self.alpha) * np.divide(self.x_pred, real_x)
            self.x_pred = x_pred

        # Apply the OLMAR algorithm
        excess_return = self.x_pred - np.mean(self.x_pred)
        denominator = (excess_return * excess_return).sum()
        if denominator != 0:
            lam = max(0.0, (self.eps - np.dot(self.b, self.x_pred)) / denominator)
        else:
            lam = 0

        # Update b with the constraint
        self.b = self.b + lam * excess_return
        self.b = np.maximum(self.b, 0)
        self.b = self.b / np.sum(self.b)


        return self.b
    '''
    
        #new_weights = self.weights.copy()
         
        asset_returns = self.returns[:t]
    
     # Compute the Exponential Moving Average for each asset
        if len(asset_returns) < self.window:
            self.x_pred = np.mean(asset_returns, axis=0)

        else:
            real_x = asset_returns.iloc[-1, :] / asset_returns.iloc[-2, :]
            if t == 9:
                print(real_x)
            x_pred = self.alpha + (1 - self.alpha) * np.divide(self.x_pred, real_x)
            self.x_pred = x_pred
            
            #self.ema_returns = self.alpha * asset_returns.iloc[-1] + (1 - self.alpha) * self.ema_returns

        # Compute the normalized difference between current returns and EMA
       # normalized_diff = asset_returns.iloc[-1] / self.ema_returns - 1

        # Update portfolio weights using exponential gradient descent
    
        #new_weights *= np.exp(-self.eta * normalized_diff)
        if t < 13 and self.x_pred.isna().sum() > 0:
            print(f"at t = {t}:", self.x_pred)
        #new_weights /= np.sum(new_weights)
        
       
        
        
         # Apply the constraint logic to update the portfolio weights
        x_pred_mean = np.mean(self.x_pred)
        excess_return = self.x_pred - x_pred_mean
        denominator = (excess_return * excess_return).sum()
        
        if denominator != 0:
            lam = max(0.0, (self.eps - np.dot(self.b, self.x_pred)) / denominator)
        else:
            lam = 0

        # Update b with the constraint
        self.b = self.b + lam * excess_return
        
        #last_b = b.copy()

       
        
        return self.b
    
    '''
        
    def run(self,mode = "percentage"):
        
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
            new_weights = self.calculate_weights(t = t)

            #Check if the new weights don't exceed the cost budget and update the portfolio
            self.rebalance_portfolio(t=t, new_weights=new_weights, mode = mode,visualize = False)

            
            
            
