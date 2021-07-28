import numpy as np
from dimod import BQM
import neal

def solution(y, alpha, nb, lam, numreads):
   
   nc = len(y[0])
   ncons = len (y)
   
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
    
   c = At @ S
   q = S.T @ B @ S

   
   linear_biases = [c[0][i] for i in range(nb*nc)]
   quadratic_biases = ((x, y, q[x,y]) for x in range(nb*nc) for y in range(nb*nc))
   var_type = 'BINARY'
   bqm = BQM(linear_biases, quadratic_biases, var_type) 
    
   sampler = neal.Neal()
   sampleset = sampler.sample(bqm)   
    
    #response = sampler.sample(bqm, num_reads=10000, num_sweeps=1000, initial_states=None, beta_range=[10, 100])
   response = sampler.sample(bqm, num_reads= numreads)
       
   cantidad_energias = response.record.shape[0] 
   energias = np.array([response.record[i][1] for i in range(cantidad_energias)])
   posicion_minimo = energias.argmin()
   x = response.record[posicion_minimo][0]
   p = S @x
   cos_bin = At @ S @ x + x.T @ S.T @ B @ S @ x 
   cos = At @ p + p.T @ B @ p 
   return x, p , cos, cos_bin


# def costo(p):
#         cos = At @ p + p.T @ B @ p 
#         return cos


# def costo_binario(x):
#         cos = At @ S @ x + x.T @ S.T @ B @ S @ x 
#         return cos


# y1= np.array ([[1.0],[1.0],[0.0],[0.0],[0.0], [0.0] ])
# y0= np.array ([[1.0],[1.0],[1.0],[1.0],[1.0], [1.0] ])
# alpha =  np.array ([1.0, 0.7 ])
# y = [y0, y1]
# nb = 8 #cantidad de bits por componente de proba 
# lam = 0.005
# numreads = 10000
# a,b,c,d = solution(y, alpha, nb, lam,numreads )
