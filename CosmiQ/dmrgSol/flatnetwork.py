'''
    @Author: Ushnish Ray
    Copyright (2021) All Rights Reserved.
'''

import numpy as np
import simple_dmrg as dmrg
import scipy.sparse.linalg as las
import scipy.linalg as la

class FlatNetwork():
    
    def __init__(self, L):
        
        self.L = L #In format: (N_t, N, N_q)                       
        self.d = 3
        
        #Variables needed for graph creation                
        self.maxl = qubitmap((0,0,0)) - qubitmap((1,L[1],L[2]-1))   #Longest long-range connection       
        self.qubitmap = lambda ((t,i,q)): t*L[1]*L[2] + i*L[2] + q
        
        #Parameters
        self.mu = lambda(t,i): 1.0
        self.lam = lambda(t,i): 1.0
        self.Sig = lambda(t,i,j): 1.0
        self.ga = 1.0
        self.rho = 1.0
        self.K = self.d**self.L[2]        
        
        #Store mpos
        self.mpoc = None
    
    def loadParams(self, mus, lams, Sigs, rho, ga, K):
        self.mu = lambda(t,i): mus[t,i]
        self.lam = lambda(t,i): lams[t,i]
        self.Sig = lambda(t,i,j): Sigs[t,i,j]
        self.rho = rho
        self.ga = ga
        self.K = K
    
    #Given graph construct MPO collection
    def get_mpos(self):
        if(not self.mpoc is None):
            return self.mpoc
        
        qm = self.qubitmap #local easy calc
        pds = [self.d**i for i in range(self.L[2])] #store power of d's for easy ref
        
        mpoc = []
        
        I = dmrg.I(d = self.d)        
        N2 = dmrg.N(1.0, d = self.d)
        
        for t in range(0,self.L[0]):
            for i in range(0, self.L[1]):
                for q in range(0,self.L[2]):
                    #Skip first and last qubits
                    if(t==0 and i==0 and q==0):
                        lo = dmrg.MPO(1,2+self.maxl, d = self.d)
                        lo.set(0,self.maxl+1,I)
                        targetrow = 0       
                        
                    elif(t==self.L[0]-1 and i==self.L[1]-1 and q==self.L[2]-1):
                        lo = dmrg.MPO(2+self.maxl,1,d = self.d)
                        lo.set(0,0,I)
                        lo.set(1,0,N2)
                        targetrow = 1+self.maxl                        
                    else:                               
                        lo = dmrg.MPO(2+self.maxl,2+self.maxl, d = self.d)
                        lo.set(0,0,I) 
                        lo.set(1+self.maxl,1+self.maxl,I) 
                
                        #Must set transition states no matter what
                        lo.set(1,0,N2)
                        for j in range(self.maxl-1):
                            lo.set(j+2,j+1,I)
                        
                        targetrow = self.maxl+1                            
            
                    #Do diagonal pieces for all sites
                    lo.set(targetrow,0,dmrg.N((-self.mu(t,i)+2.0*self.rho)*pds[q], d=self.d) #on-site term
                    lo.add(targetrow,0,dmrg.N2((self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*pds[q]**2/self.K, d = self.d)
                    if(t>0):
                        lo.add(targetrow,0,dmrg.N2((2.*self.lam(t-1,i)**2)*pds[q]**2/self.K,d=self.d)

                    #We are done if it's the last qubit
                    if(t==self.L[0]-1 and i==self.L[1]-1 and q==self.L[2]-1):
                        continue
                    
                               
                    #now set last row -- for everything all the way to the last qubit
                    for qp in range(q+1, self.L[2]):
                        sep = abs(qm(t,i,q) - qm(t,i,qp))
                        lo.set(targetrow,sep,dmrg.N((self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*2/self.K*pds[q]*pds[qp],d=self.d))
                               
                    if(t>0):
                        for j in range(i+1,self.L[1]):
                            for qp in range(q+1, self.L[2]):
                                sep = abs(qm(t,i,q) - qm(t,j,qp))
                                lo.set(targetrow,sep,dmrg.N(4*self.lam(t-1,i)*self.lam(t-1,j)*pds[q]*pds[qp]/self.K,d=self.d))
                            
                            sep = abs(qm(t,i,q) - qm(t,j,q))
                            lo.set(targetrow,sep,dmrg.N(2*self.lam(t-1,i)*self.lam(t-1,j)*pds[q]*pds[q]/self.K,d=self.d))       
                        for qp in range(q+1, self.L[2]):
                            sep = abs(qm(t,i,q) - qm(t,i,qp))
                            lo.set(targetrow,sep,dmrg.N(4*self.lam(t-1,i)**2*pds[q]*pds[qp]/self.K,d=self.d))
                                   
                    if(t<self.L[0]-1):
                        for j in range(i+1,self.L[1]):
                            for qp in range(q+1, self.L[2]):
                                sep = abs(qm(t+1,j,qp) - qm(t,i,q))
                                lo.set(targetrow,sep,dmrg.N(-8.0*self.lam(t,i)*self.lam(t,j)*pds[q]*pds[qp]/self.K,d=self.d))
                            
                            sep = abs(qm(t+1,j,q) - qm(t,i,q))
                            lo.set(targetrow,sep,dmrg.N(-4.0*self.lam(t,i)*self.lam(t,j)*pds[q]*pds[q]/self.K,d=self.d))
                         
                        sep = abs(qm(t+1,i,q) - qm(t,i,q))
                        lo.set(targetrow,sep,dmrg.N(-4.0*self.lam(t,i)**2*pds[q]**2/self.K,d=self.d))
                               
                        for qp in range(q+1, self.L[2]):
                            sep = abs(qm(t+1,i,qp) - qm(t,i,q))
                            lo.set(targetrow,sep,dmrg.N(-8.0*self.lam(t,i)**2*pds[q]*pds[qp]/self.K,d=self.d))
                        
                    for j in range(i+1,self.L[1]):
                        for qp in range(q+1, self.L[2]):
                            sep = abs(qm(t,j,qp) - qm(t,i,q))
                            lo.set(targetrow,sep,dmrg.N(4.0/self.K*pds[q]*pds[qp]*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho),d=self.d))
                                   
                        sep = abs(qm(t,j,q) - qm(t,i,q))
                        lo.set(targetrow,sep,dmrg.N(2.0/self.K*pds[q]*pds[qp]*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho),d=self.d))
                                                
            mpoc.append(lo)
            #print(pairs)
            #lo.show()                    
         
        self.mpoc = mpoc
        return mpoc            
        
    def run(self, cnvgThreshold = 1.0e-6, **kwargs):
        
        #Setup DMRG parameters
        dmrgp = dmrg.dmrgParams()
        dmrgp.L = self.L
        
        #Get MPOS and MPS
        mpos = self.get_mpos()
        mps = dmrg.MPS(dmrgp, allocate=False)
        
        dm = dmrg.DMRG(dmrgp,mps,mpos)
        
        #Sweep Schedule
        #sweepd = [2,5,10,15,20]
        #sweepi = [100,20,5,5,5]
        #sweepn = [1.0e-3,1.0e-4, 1.0e-4, 1.0e-4, 1.0e-5, 1.0e-5]
        
        sweepd = kwargs['sweepd'] if ('sweepd' in kwargs) else [1,2,2,2,3]
        sweepi = kwargs['sweepi'] if ('sweepi' in kwargs) else [5,5,5,5,5]
        sweepn = kwargs['sweepn'] if ('sweepn' in kwargs) else [1.0e-2,1.0e-3,1.0e-4,1.0e-5,1.0e-6]
        sweepmin = kwargs['sweepmin'] if ('sweepmin' in kwargs) else [None]*len(sweepi)
        
        #Run
        sch = 0
        mps.setnewbd(sweepd[sch], noise=sweepn[sch])                
        mps.rightNormalize()        
            
        olde = 0.0
        for sch in range(len(sweepd)):
            print('Schedule: ',sch,' D = ', sweepd[sch])
            
            for i in range(sweepi[sch]):
                print('Beginning sweep: ',i,'of',sweepi[sch])
                newes = dm.sweep()
                newe = dm.energy()[0]                
                print(f'Sweep Energy: {newe:.8f}')
                if(abs(newe-olde)<cnvgThreshold and (sweepmin[sch] is None or i>=sweepmin[sch] )):
                    olde = newe
                    break
                olde = newe
            
            if(self.L<6):
                amp = np.array(mps.getAmp())        
                ampl = np.where(np.abs(amp)>1.0e-8)[0]
                ampv = amp[ampl]
                config = [bin(x)[2:].zfill(self.L) for x in ampl]
                print(config)
                print(ampv**2)  
                        
            print('-----------')
        
            if(sch<len(sweepd)-1):
                mps.setnewbd(sweepd[sch+1])
                mps.rightNormalize()                
                dm.calcintR()
                olde = 0.0
       
        #return final mps for postprocessing
        return olde, mps
    
    #This is only for testing purposes. Do NOT use more than L = 12
    def runED(self, tol=1.0e-6, nstates = 1):        
        mpos = self.get_mpos()        
        newmpo = dmrg.MPO.outer(mpos[0],mpos[1])
        #print(newmpo.ops[0][0])
        for i in range(2,self.L):            
            newmpo = dmrg.MPO.outer(newmpo,mpos[i])
            #print(newmpo.ops[0][0])
        #print('Final Hamiltonian is: ',newmpo.ops[0][0])
        
        lh = newmpo.op[0,0]
        [ev, psi0] = las.eigsh(lh,k=nstates,which='SA',maxiter=lh.shape[0]*10,tol=tol,ncv=100)        
        return ev, psi0
    
    #Also do a mean-field calculation
    def runMF(self, u = 1.35, threshold = 1.0e-6, maxiter=50, seed = 0):
                        
        #Seed
        np.random.seed(seed)
        
        #Start with random guess
        cs = np.random.randint(0,2,self.L)        
        #Compute MF values
        mfN = np.zeros(self.L)
        
        lastE = [0.0,0.0]
        lastState = [[],[]]
        
        for i in range(self.L):
            fjs = [x[1] for x in self.edges if(x[0] == i)] #Get all connected neighbors            
            sjs = [x[0] for x in self.edges if(x[1] == i)] #Sorted edge list so have to be careful                
            js = fjs + sjs                     
            mfN[i] = np.sum(cs[js])            
        
        for n in range(maxiter):
            
            #Solve local problem with MF guess            
            for i in range(self.L):                            
                le = -1.0 + u*mfN[i]                
                cs[i] = 1 if (le<0) else 0
            
            #Compute Energy
            uE = 0.0
            for pair in self.edges:
                uE += cs[pair[0]]*cs[pair[1]]*self.edges[pair]                
            tE = -1.0*sum(cs) + uE
            #print('** Current Energy: ',tE, 'for state: ',cs)                                                          
            print('** Current Energy: ',tE, end='')
            
            
            
            #Compute new MF values
            new_mfN = np.zeros(self.L)
            for i in range(self.L):
                fjs = [x[1] for x in self.edges if(x[0] == i)] #Get all connected neighbors            
                sjs = [x[0] for x in self.edges if(x[1] == i)] #Sorted edge list so have to be careful                
                js = fjs + sjs                     
                new_mfN[i] = np.sum(cs[js])            
            
            #print('Old MF: ',mfN, 'New MF: ',new_mfN)
            nrm1 = la.norm(new_mfN - mfN)            
            mfN = new_mfN
                        
            print(' Delta(mf) ',nrm1)                                    
            if(nrm1<threshold):
                break                        
            
            if(n>10 and abs(lastE[0]-tE)<1.0e-8): 
                break
            
            lastE[0] = lastE[1]
            lastE[1] = tE
            
            lastState[0] = lastState[1]
            lastState[1] = cs
        
        if(lastE[0]<lastE[1]):
            tE = lastE[0]
            cs = lastState[0]
        else:
            tE = lastE[1]
            cs = lastState[1]
            
        return tE,cs
    
if __name__ == '__main__':
    
    L = [6,20,8]
    fn = FlatNetwork(L)
   
        