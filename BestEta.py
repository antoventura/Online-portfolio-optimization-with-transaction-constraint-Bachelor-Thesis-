from ONPortfolio import OnlinePortfolioSelection

def bestEta(stock, returns):
    
    '''
    Params:
    -stock: Series of stock prices
    -returns: Series of daily stock returns
    
    Returns: best eta parameter to maximize budget
    '''
    #not used in the notebook
    
    #eta grid search for best budget

    best_budget = -1
    best_eta = -1
    for eta in [x * 0.01 for x in range(50,100)]:
        PortfolioSP100_hp = OnlinePortfolioSelection(stock = stock, returns = returns * 2.5,eta =eta)
        PortfolioSP100_hp.run(mode="percentage")
        #print(f"for eta = {eta}, the final budget is {PortfolioSP100_hp.budget} ")
        if PortfolioSP100_hp.budget > best_budget:
            best_budget= PortfolioSP100_hp.budget
            best_eta = PortfolioSP100_hp.eta
            
    PortfolioSP100_hp = OnlinePortfolioSelection(stock = stock, returns = returns * 2.5,eta =best_eta)
    PortfolioSP100_hp.run(mode="percentage")    
    PortfolioSP100_hp.benchmark()
    
    return best_eta