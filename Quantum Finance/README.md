## Product Description 
The Dynamic Quantum Pricing Engine is an algorithm for the dynamic pricing and promotion of online goods that helps accelerate sales turnover. The target niche is small to medium-sized online retailers, with market revenue of $1 mln/month and up.

Pattern extraction and data mining for leveraging sales is the most challenging task for many companies that have invested substantially in collecting and storing massive amounts of data. These patterns can be extracted from a binary data set by identifying clusters in data sets. Our product leverages the quantum properties of the Ising model to go beyond classical clustering and association algorithms, by allowing for dynamic pricing.

## Setup
Set up virtual environment using pyenv. 

Install and configure d-wave 

Run [Quantum Dynamic Pricing Engine.ipynb ](https://github.com/ManinderPanesar/Hackathon2021/blob/Week3-Hackathon/Quantum%20Finance/Quantum%20Dynamic%20Pricing%20Engine.ipynb)

## Challenge(s) You Solved
We devised a dynamic pricing tool using D-Wave stimulated annealeaing sampler. The tool is based on optimizing the prices of the products using the Ising model capturing the probabilisic behvaior. 

![](https://github.com/ManinderPanesar/Hackathon2021/blob/Week3-Hackathon/Quantum%20Finance/Our%20approach.png)

Following this approch, it was concluded that 
- Uniform discount incentivizes people to buy all products.
- Selective discount incentives people to buy the selected product discounted
- 
![](https://github.com/ManinderPanesar/Hackathon2021/blob/Week3-Hackathon/Quantum%20Finance/Uniform%20sale.png)

- Low discount for a less frequently bought product doesn't influence the sell of the product
- High discount for a less frequently bought product does influence the sell of the product (at the expense of other purchases)
![](https://github.com/ManinderPanesar/Hackathon2021/blob/Week3-Hackathon/Quantum%20Finance/Discount%20on%20product.png)


## The quantum pricing advantage

While this type of market data analysis can be performed using classical methods, our model is based on the Ising model in physics, which has a number of advantages. One is that the method is inherently probabilistic, so rather than getting a fixed answer each time the algorithm is run, we can build up a statistical picture of likely behavior. Another is that the quantum approach offers the potential advantage of much faster computation times. The main advantage of the quantum method which our program exploits, however, is that it can be used to infer how behaviour varies as conditions change. In particular, because the Ising model exhibits nonlinear switching-type behaviour, the algorithm can capture sudden changes, such as herd behaviour in markets; or the way that a customer’s preferences will adapt when goods go on sale. 

Our product goes beyond product recommendations, by entering into a kind of negotiation with the customer. Prices are adjusted dynamically in response to individual customer behaviour, using a quantum algorithm which maximises the probability of a successful transaction. To the customer shopping at a website, the experience will be similar to what they are used to, with the difference that prices and recommendations may change after repeat visits. In the background, the algorithm is building up a picture of the customer, nudging their choices through promotions, and enticing their interest with related goods.

While large firms currently dominate the demand for market intelligence, access to data is not limited to such companies, and our service is aimed primarily at small to medium-sized online retailers with market revenue of $1 mln/month and up. Google Analytics allows even small firms to obtain data in the required format. A simple command gives metrics such as quantity and revenue for a particular product and transaction ID. The Dynamic Quantum Pricing Engine can then generate recommendations for related products, and also suggest targeted ads or promotions such as price discounts.

The product will be sold on a subscription basis (monthly or yearly). It will be marketed directly to suitable retailers, and we will also seek other distribution channels, such as engaging with Spotify.


## Contributors 
David Orrell

Uchenna Chukwu

Maninder Kaur
