# D-Wave challenge:  QUTO vs QUBO

## Partitionin Equal Sum 

Let's consider the partitionin equal sum problem where we want to separate a set of values into two groups (*A* and *B*) that have an equal sum. 
For example, A = [10,3,5,9,9] and it can be break into group  [10,3,5] and [9,9].

We decided to solve this problem by mapping it into an Ising model, 

![](https://latex.codecogs.com/gif.latex?%5Cbg_white%20H%20%3D%20%5Csum_%7Bi%3Cj%7D%20%5Calpha_%7Bij%7D%20%5C%3B%5C%3Bx_i%20x_j) 

where ![](https://latex.codecogs.com/gif.latex?x_i%20%5Cin%20%5C%7B-1%2C1%5C%7D).
However, this representation is non-robust, for example, for [1,3,10,2,3,10] the results are 
[1,3,10] and [2,3,10], which are invalid.

Our goal is to find a more robust representation where we can have value belonging to outlier class *O* in addition to the two groups *A* and *B*. 
For example,  A=[1,2,10] B=[3,10] O=[3].
 A=[1,2,10] B=[3,10] O=[3].

## Robuts QUBO
We define a 3N binary variables such that:
![](https://latex.codecogs.com/gif.latex?x_%7Bi%2CO%7D%20%3D%20i%20%5Cin%20O)

![](https://latex.codecogs.com/gif.latex?x_%7Bi%2C-1%7D%20%3D%20i%20%5Cin%20A)

![](https://latex.codecogs.com/gif.latex?x_%7Bi%2C1%7D%20%3D%20i%20%5Cin%20B)

