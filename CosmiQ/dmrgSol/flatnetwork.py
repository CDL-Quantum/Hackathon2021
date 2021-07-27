'''
    @Author: Ushnish Ray
    Copyright (2021) All Rights Reserved.
'''

import numpy as np
import simple_dmrg as dmrg
import scipy.sparse.linalg as las
import scipy.linalg as la

class FlatNetwork():
    
    def __init__(self, L, d):
        
        self.L = L #In format: (N_t, N, N_q)                       
        self.d = d
        
        #Variables needed for graph creation                              
        self.qubitmap = lambda t,i,q: t*L[1]*L[2] + i*L[2] + q
        self.maxl = abs(self.qubitmap(0,0,0) - self.qubitmap(1,L[1],L[2]-1))   #Longest long-range connection 
        print('Max MPO dim: ',self.maxl)
        
        #Parameters
        self.mu = lambda t,i: 1.0 
        self.lam = lambda t,i: 0.0
        self.Sig = lambda t,i,j: (0.01 if i == j else 0.0)
        self.ga = 1.0
        self.rho = 2.0
        self.K = self.d**self.L[2]        
        
        #Store mpos
        self.mpoc = None
    
    def loadParams(self, mus, lams, Sigs, rho, ga, K):
        self.mu = lambda t,i: mus[t,i]
        self.lam = lambda t,i: lams[t,i]
        self.Sig = lambda t,i,j: Sigs[t,i,j]
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
            
                    #print(t,i,q)
                    #Do diagonal pieces for all sites
                    
                    #Term (1)
                    lo.set(targetrow,0,dmrg.N((-self.mu(t,i)-2.0*self.rho)*pds[q], d=self.d)) #on-site term
                    
                    #Term (2-d)
                    lo.add(targetrow,0,dmrg.N2((self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*pds[q]**2/self.K, d = self.d))
                    #Term (3-d)
                    if(t<self.L[0]-1):
                        lo.add(targetrow,0,dmrg.N2((self.lam(t+1,i)**2)*pds[q]**2/self.K,d=self.d))

                    #We are done if it's the last qubit
                    if(t==self.L[0]-1 and i==self.L[1]-1 and q==self.L[2]-1):
                        mpoc.append(lo)
                        continue
                               
                    #now set last row -- for everything all the way to the last qubit
                    #Term 4-d    
                    sep = abs(qm(t+1,i,q) - qm(t,i,q))
                    lo.set(targetrow,sep,dmrg.N(-2.0*self.lam(t,i)**2*pds[q]**2/self.K,d=self.d))
                        
                    #Term 2-b
                    for qp in range(q+1, self.L[2]):
                        sep = abs(qm(t,i,q) - qm(t,i,qp))
                        lo.set(targetrow,sep,dmrg.N(2.0*(self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*self.K*pds[q]*pds[qp],d=self.d))
                        
                        if(t<self.L[0]-1):
                            #Term 3-c
                            sep = abs(qm(t,i,q) - qm(t,i,qp))
                            lo.add(targetrow,sep,dmrg.N(2*self.lam(t+1,i)**2*pds[q]*pds[qp]/self.K,d=self.d))
                            
                            #Term 4-c
                            sep = abs(qm(t+1,i,q) - qm(t,i,qp))
                            lo.set(targetrow,sep,dmrg.N(-4*self.lam(t+1,i)**2*pds[q]*pds[qp]/self.K,d=self.d))
                            
                    for j in range(i+1,self.L[1]):
                        for qp in range(q+1, self.L[2]):
                            #Term 2-a
                            sep = abs(qm(t,j,qp) - qm(t,i,q))
                            lo.set(targetrow,sep,dmrg.N(4.0/self.K*pds[q]*pds[qp]*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho),d=self.d))
                        
                            if(t<self.L[0]-1):
                                #Term 3-a
                                sep = abs(qm(t,i,q) - qm(t,j,qp))
                                lo.add(targetrow,sep,dmrg.N(4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/self.K,d=self.d))
                        
                                #Term 4-a
                                sep = abs(qm(t+1,i,q) - qm(t,j,qp))
                                lo.set(targetrow,sep,dmrg.N(-8*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/self.K,d=self.d))
                        
                        #Term 2-c
                        sep = abs(qm(t,j,q) - qm(t,i,q))
                        lo.set(targetrow,sep,dmrg.N(2.0/self.K*pds[q]**2*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho),d=self.d))    
                                                
                        if(t<self.L[0]-1):                                                
                            #Term 3-b
                            sep = abs(qm(t,i,q) - qm(t,j,q))
                            lo.add(targetrow,sep,dmrg.N(2*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/self.K,d=self.d))       
                                       
                            #Term 4-b
                            sep = abs(qm(t+1,i,q) - qm(t,j,q))
                            lo.set(targetrow,sep,dmrg.N(-4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/self.K,d=self.d))       
                                                
                    mpoc.append(lo)
                    #print(pairs)
                    #lo.show()                    
         
        self.mpoc = mpoc
        return mpoc            
        
    def getHamiltonian(self):
        
        qm = self.qubitmap #local easy calc
        pds = [self.d**i for i in range(self.L[2])] #store power of d's for easy ref
                
        S = {}
        D = {}
        
        for t in range(0,self.L[0]):
            for i in range(0, self.L[1]):
                for q in range(0,self.L[2]):
                    
                    #print(t,i,q)
                    #Do diagonal pieces for all sites
                    
                    #Term (1)
                    S[(qm(t,i,q), qm(t,i,q))] = (-self.mu(t,i)-2.0*self.rho)*pds[q]
                                        
                    #Term (2-d)
                    D[(qm(t,i,q), qm(t,i,q))] = (self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*pds[q]**2/self.K
                    
                    #Term (3-d)
                    if(t<self.L[0]-1):
                        D[(qm(t,i,q), qm(t,i,q))] += (self.lam(t+1,i)**2)*pds[q]**2/self.K                        

                    #We are done if it's the last qubit
                    if(t==self.L[0]-1 and i==self.L[1]-1 and q==self.L[2]-1):                        
                        continue
                                                   
                    #now set last row -- for everything all the way to the last qubit
                    #Term 4-d
                    assert(not(qm(t,i,q),qm(t+1,i,q)) in D)
                    D[(qm(t,i,q),qm(t+1,i,q))] = -2.0*self.lam(t,i)**2*pds[q]**2/self.K
                    
                    for qp in range(q+1, self.L[2]):                                                
                        #Term 2-b
                        assert(not(qm(t,i,q),qm(t+1,i,qp)) in D)
                        D[(qm(t,i,q),qm(t,i,qp))] = 2.0*(self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*self.K*pds[q]*pds[qp]
                        
                        if(t<self.L[0]-1):
                            #Term 3-c                            
                            D[(qm(t,i,q),qm(t,i,qp))] += 2*self.lam(t+1,i)**2*pds[q]*pds[qp]/self.K
                            
                            #Term 4-c                     
                            assert(not(qm(t,i,qp),qm(t+1,i,q)) in D)
                            D[(qm(t,i,qp),qm(t+1,i,q))] = -4*self.lam(t+1,i)**2*pds[q]*pds[qp]/self.K
                           
                    for j in range(i+1,self.L[1]):
                        for qp in range(q+1, self.L[2]):
                            #Term 2-a                        
                            assert(not(qm(t,i,q),qm(t,j,qp)) in D)
                            D[(qm(t,i,q),qm(t,j,qp))] = 4.0/self.K*pds[q]*pds[qp]*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho)     
                            
                            if(t<self.L[0]-1):
                                #Term 3-a
                                D[(qm(t,i,q),qm(t,j,qp))] += 4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/self.K
                            
                                #Term 4-a
                                assert(not(qm(t,j,qp),qm(t+1,i,q)) in D)
                                D[(qm(t,j,qp),qm(t+1,i,q))] = -8*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/self.K 
                                                   
                        #Term 2-c
                        assert(not(qm(t,i,q),qm(t,j,q)) in D)
                        D[(qm(t,i,q),qm(t,j,q))] = 2.0/self.K*pds[q]**2*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho)
                        if(t<self.L[0]-1):
                            #Term 3-b
                            D[(qm(t,i,q),qm(t,j,q))] += 2*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/self.K
                        
                            #Term 4-b
                            assert(not(qm(t,j,q),qm(t+1,i,q)) in D)
                            D[(qm(t,j,q),qm(t+1,i,q))] = -4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/self.K
        
        #Return Single (N) and Double (NN) operators
        return S,D
        
    def initialize(self):
        #Setup DMRG parameters
        dmrgp = dmrg.dmrgParams()
        dmrgp.L = np.prod(self.L)
        dmrgp.d = self.d
        
        #Get MPOS and MPS
        mpos = self.get_mpos()
        mps = dmrg.MPS(dmrgp, allocate=False)        
        dm = dmrg.DMRG(dmrgp,mps,mpos)
        return dm
        
    def run(self, cnvgThreshold = 1.0e-6, **kwargs):
        
        #Setup DMRG parameters
        dmrgp = dmrg.dmrgParams()
        dmrgp.L = np.prod(self.L)
        dmrgp.d = self.d
        
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
            
            '''
            if(dmrgp.L<6):
                amp = np.array(mps.getAmp())        
                ampl = np.where(np.abs(amp)>1.0e-8)[0]
                ampv = amp[ampl]
                config = [bin(x)[2:].zfill(dmrgp.L) for x in ampl]
                print(config)
                print(ampv**2)  
            '''        
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
       
    #Given an arbitary qubit representation return weights    
    def returnWeights(self,x):
        
        if(isinstance(x,str)):
            x = [int(c) for c in x]
        
        L = np.prod(self.L)
        dT = self.L[1]*self.L[2]
        
        vec = np.zeros([self.L[0],self.L[1]], dtype = np.float64)
        for tl,t in enumerate(range(0,L,dT)):
            for il,i in enumerate(range(0,dT,self.L[2])):                
                vec[tl,il] = np.sum([x[t+i+q]*self.d**q for q in range(self.L[2])])/self.K
        
        return vec

def ss(x, d = 3):
    s = ''
    m = x
    while(m>0):
        r = m%d
        s = str(r) + s
        m = int(m/d)
   
    return s
    
if __name__ == '__main__':
    
    d = 4
    
    #Nt x N x N_q
    L = [2,2,2]
    fn = FlatNetwork(L, d)
    
    mpos = fn.get_mpos()
    print('Number of MPOs:',len(mpos))
    #for mpo in mpos:
    #    mpo.show()
        
    #Testing
    '''
    dm = fn.initialize()
    mps = dmrg.MPS.scalarMPS([0,0,0,0], d = 3)
    print(dm.energyWith(mps))
    
    mps = dmrg.MPS.scalarMPS([0,0,0,1], d = 3)
    print(dm.energyWith(mps))
        
    mps = dmrg.MPS.scalarMPS([1,1,1,1], d = 3)
    print(dm.energyWith(mps))
    
    mps = dmrg.MPS.scalarMPS([2,2,2,2], d = 3)
    print(dm.energyWith(mps))
    '''
    
    e, mps = fn.run()
    amp2 = np.array(mps.getAmp())
    ns = d**np.prod(L)
    print(amp2)
    
    print('Number of states: ',ns)
        
    ampl = np.where(np.abs(amp2)>1.0e-8)[0]
    print('Sols size: ',len(ampl))
    ampv = amp2[ampl]
    config = [ss(x).zfill(np.prod(L)) for x in ampl]
    print(config)
    print(ampv**2)  
    print(fn.returnWeights(config[0]))
    
    #Get Hamiltonian
    S,D = fn.getHamiltonian()
    print('Singles: ',S)    
    print('Doubles: ',D)