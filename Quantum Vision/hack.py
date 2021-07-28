import numpy as np

#Inputs:
#Opcion - 1 constraints
# nc = 10  
# y0 = np.ones ([nc,1]) # normalizacion
# y = [y0]
# alpha =  np.array ([1.0])

#opcion - 2 constraints moneda
# y1= np.array ([[0.0],[1.0] ])
# nc = len(y1) #cantidad de caras
# y0 = np.ones ([nc,1]) # normalizacion
# alpha =  np.array ([1.0, 0.8 ])
# y = [y0, y1]

#opcion - 2 constraints dado
# y1= np.array ([[1.0],[2.0],[3.0],[4.0],[5.0], [6.0] ])
# nc = len(y1) #cantidad de caras
# y0 = np.ones ([nc,1]) # normalizacion
# alpha =  np.array ([1.0, 4 ])
# y = [y0, y1]

#opcion - 2 constraints dado bis
y1= np.array ([[1.0],[0.0],[0.0],[0.0],[0.0], [0.0] ])
nc = len(y1) #cantidad de caras
y0 = np.ones ([nc,1]) # normalizacion
alpha =  np.array ([1.0, 0.5 ])
y = [y0, y1]



#Parametros:
nb = 8 #cantidad de bits por componente de proba 
lam = 0.005


#Main
ncons = len (y)

#A tiene shape (nc,)
At = np.zeros ([1,nc])
for j in range(ncons):
    At = At + (-2)* alpha[j] *y[j].T 

B = 2 * lam  * np.identity(nc)
for j in range(ncons):
    B = B + (y[j]@ y[j].T)


S = np.zeros ([nc,nc* nb])
for i in range(nc):
    for j in range (nc * nb):
       if j>=(i)*nb and j<(i+1)*nb: S[i,j]=2**(-((j%nb)+1))

def costo(p):
    cos = At @ p + p.T @ B @ p 
    return cos


def costo_binario(x):
    cos = At @ S @ x + x.T @ S.T @ B @ S @ x 
    return cos


c = At @ S
q = S.T @ B @ S


from dimod import BQM
linear_biases = [c[0][i] for i in range(nb*nc)]
quadratic_biases = ((x, y, q[x,y]) for x in range(nb*nc) for y in range(nb*nc))
var_type = 'BINARY'
bqm = BQM(linear_biases, quadratic_biases, var_type) 

import neal
sampler = neal.Neal()
sampleset = sampler.sample(bqm)   


#response = sampler.sample(bqm, num_reads=10000, num_sweeps=1000, initial_states=None, beta_range=[10, 100])
response = sampler.sample(bqm, num_reads=10000)


cantidad_energias = response.record.shape[0] 
energias = np.array([response.record[i][1] for i in range(cantidad_energias)])
posicion_minimo = energias.argmin()
x = response.record[posicion_minimo][0]
p = S @x
print(x)
print(p)
print('Suma de p: ' , sum(p))
print(costo(p),costo_binario(x) )
