# D-Wave challenge:  QUTO vs QUBO

## Partitioning Equal Sum 

Let's consider the partitioning equal sum problem where we want to separate a set of values into two groups (*A* and *B*) that have an equal sum. 
For example, [10,3,5,9,9] can be breaken into two groups, [10,3,5] and [9,9].

We decided to solve this problem by mapping it into an Ising model, 

![](https://latex.codecogs.com/gif.latex?%5Cbg_white%20H%20%3D%20%5Csum_%7Bi%3Cj%7D%20%5Calpha_%7Bij%7D%20%5C%3B%5C%3Bx_i%20x_j) 

where ![](https://latex.codecogs.com/gif.latex?x_i%20%5Cin%20%5C%7B-1%2C1%5C%7D).
However, this representation is non-robust, for example, for [1,3,10,2,3,10] the results are A = [1,3,10] and B = [2,3,10], which are invalid.

Our goal is to find a more robust representation where we can have value belonging to an outlier class *O* in addition to the two groups *A* and *B*. 
For example,  A=[1,2,10] B=[3,10] O=[3].

## Robuts Quadratic Unconstrained Binary Optimization (RQUBO)
We define a 3N binary variables such that:
![](https://latex.codecogs.com/gif.latex?x_%7Bi%2CO%7D%20%3D%20i%20%5Cin%20O)

![](https://latex.codecogs.com/gif.latex?x_%7Bi%2C-1%7D%20%3D%20i%20%5Cin%20A)

![](https://latex.codecogs.com/gif.latex?x_%7Bi%2C1%7D%20%3D%20i%20%5Cin%20B)

For this toy problem we have:

1. 1 equality constraint:

![](https://latex.codecogs.com/gif.latex?%5Csum_i%20a_i%20%5C%3B%20x_%7Bi%2C-1%7D%20-%20%5Csum_i%20a_i%20%5C%3B%20x_%7Bi%2C1%7D%20%3D%200)

2. N equality constraints (only one class per value):
 
![](https://latex.codecogs.com/gif.latex?x_%7Bi%2C-1%7D%20&plus;%20x_%7Bi%2C0%7D%20&plus;%20x_%7Bi%2C1%7D%20%3D%201)
 
3. Minimize the quantity of outliers: 

![](https://latex.codecogs.com/gif.latex?H%20%3D%20%5Csum%20x_%7Bi%2C0%7D)

## Robuts Quadratic Unconstrained Ternary Optimization (RQUTO)

We define Ising N ising trinary ![](https://latex.codecogs.com/gif.latex?x_i%20%5Cin%20%5C%7B-1%2C1%5C%7D)
In a qutrit each element can be mapped to a state:

![](https://latex.codecogs.com/gif.latex?x_i%20%3D%200%20%5Cto%20i%20%5Cin%20O)

![](https://latex.codecogs.com/gif.latex?x_i%20%3D%20-1%20%5Cto%20i%20%5Cin%20A)

![](https://latex.codecogs.com/gif.latex?x_i%20%3D%201%20%5Cto%20i%20%5Cin%20B)

For this toy problem we have:

1. 1 constraint

![](https://latex.codecogs.com/gif.latex?%5Csum_i%20x_i%20%3D%200)

2. Maximize the number of inliers

![](https://latex.codecogs.com/gif.latex?%5Cmin%20%5Cleft%20%5C%7B%20-%5Csum_i%20x_i%5E2%20%5Cright%20%5C%7D).

## Comparison

|                     | QUBO | QUTO |
|:-------------------:|:----:|:----:|
|       Variable      |  3N  |   N  |
| Linear constraints  |   N+1  |   1  |
|         Cost        |   1  |   1  |



