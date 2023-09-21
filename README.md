# TESI

In 2021 Celli, Castiglioni and Kroer proposed their paper "Online Learning with Knapsacks: the Best of Both Worlds", dedicated to studying online learning problems. The focus was on maximizing expected rewards without violating a finite set of resource constraints. The research provided a novel framework, ensuring no-regret guarantees in both stochastic and ad- versarial scenarios. Today we are going to apply their algorithm in the realm of finance to introduce an innovative portfolio optimization method. This method aims to strike a balance between maximizing expected profits and minimizing transactions costs. This framework in- troduces two players: the decision maker and the dual player. The decision maker allocates resources to maximize rewards, while the dual player penalizes excessive transactions, striking a balance between strategy changes and cost management. We evaluate our online algorithm against established strategies, including the modern portfolio and buy-and-hold. Notably, our top-performing algorithm, which excludes the dual player, capitalizes on Tesla’s exceptional performance, delivering remarkable profits but with increased risk. The PrimalDual Portfolio, incorporating both players, maintains a consistent transaction budget, harmoniously balancing risk and reward, and excelling in diversification.



The notebook simulation.ipynb contains all the commands to run the online portfolio simulation and the other benchmark models.
Each Portfolio Optimization method has its own py file. 
The models used as benchmark include:

1. Markowitz Mean-Variance
2. Buy and Hold Strategy
3. Constant Weight Rebalanced
4. Equal Weight
5. Value Weight
6. Online Moving Average Regression (OLMAR)
 
All Portfolio are initialized with a uniform distribution of the stocks from s&p100. The weights are modified daily for a duration of 5 years.

