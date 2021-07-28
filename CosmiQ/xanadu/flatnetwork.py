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
        self.lam = lambda t,i: 0.00
        self.Sig = lambda t,i,j: (0.00 if i == j else 0.0)
        self.ga = 0.0
        self.rho = 1000.0
        self.K = self.d**self.L[2]        
        self.Kscale = 1.0       
 
        #Flash best rho
        constmax = (self.K-1)/2.0 - 1
        if(constmax>0):
            print('\Delta:',self.maxSplit(), 'Min rho: ',self.maxSplit()/constmax, 'Supplied rho: ',self.rho)
        #self.rho = self.maxSplit()/constmax*2.0 

        self.offset = self.L[0]*self.rho
        #Store mpos
        self.mpoc = None
        self.make_mpos() 
    
    def loadParams(self, mus, lams, Sigs, rho, ga):
        self.mu = mus
        self.lam = lams
        self.Sig = Sigs
        self.rho = rho
        self.ga = ga
                
        self.offset = self.L[0]*self.rho
        self.mpoc = None
   
    def maxSplit(self):
       
        maxe = None
        for t in range(self.L[0]): 
            for i in range(self.L[1]):
                for n in range(self.K):
                    ce = self.mu(t,i)*n/self.K
                    maxe = ce if (maxe is None or ce>maxe) else maxe
        
        return maxe

        return 
    def make_mpos(self):
        if(not self.mpoc is None):
            return self.mpoc
        
        qm = self.qubitmap #local easy calc
        pds = [self.d**i for i in range(self.L[2])] #store power of d's for easy ref
        K = self.K*self.Kscale
        K2 = K*K      

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
                    lo.set(targetrow,0,dmrg.N((-self.mu(t,i)-2.0*self.rho)*pds[q]/K, d=self.d)) #on-site term
                    
                    #Term (2-d)
                    lo.add(targetrow,0,dmrg.N2((self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*pds[q]**2/K2, d = self.d))
                    #Term (3-d)
                    if(t<self.L[0]-1):
                        lo.add(targetrow,0,dmrg.N2((self.lam(t+1,i)**2)*pds[q]**2/K2,d=self.d))
                    
                    #Term(0) constant
                    #    lo.add(targerrow,0,I*self.offset, d=self.d)

                    #We are done if it's the last qubit
                    if(t==self.L[0]-1 and i==self.L[1]-1 and q==self.L[2]-1):
                        mpoc.append(lo)
                        continue
                               
                    #now set last row -- for everything all the way to the last qubit
                    #Term 4-d    
                    sep = abs(qm(t+1,i,q) - qm(t,i,q))
                    lo.set(targetrow,sep,dmrg.N(-2.0*self.lam(t,i)**2*pds[q]**2/K2,d=self.d))
                        
                    #Term 2-b
                    for qp in range(q+1, self.L[2]):
                        sep = abs(qm(t,i,q) - qm(t,i,qp))
                        lo.set(targetrow,sep,dmrg.N(2.0*(self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)/K2*pds[q]*pds[qp],d=self.d))
                        
                        if(t<self.L[0]-1):
                            #Term 3-c
                            sep = abs(qm(t,i,q) - qm(t,i,qp))
                            lo.add(targetrow,sep,dmrg.N(2*self.lam(t+1,i)**2*pds[q]*pds[qp]/K2,d=self.d))
                            
                            #Term 4-c
                            sep = abs(qm(t+1,i,q) - qm(t,i,qp))
                            lo.set(targetrow,sep,dmrg.N(-4*self.lam(t+1,i)**2*pds[q]*pds[qp]/K2,d=self.d))
                            
                    for j in range(i+1,self.L[1]):
                        for qp in range(q+1, self.L[2]):
                            #Term 2-a
                            sep = abs(qm(t,j,qp) - qm(t,i,q))
                            lo.set(targetrow,sep,dmrg.N(4.0/K2*pds[q]*pds[qp]*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho),d=self.d))
                        
                            if(t<self.L[0]-1):
                                #Term 3-a
                                sep = abs(qm(t,i,q) - qm(t,j,qp))
                                lo.add(targetrow,sep,dmrg.N(4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/K2,d=self.d))
                        
                                #Term 4-a
                                sep = abs(qm(t+1,i,q) - qm(t,j,qp))
                                lo.set(targetrow,sep,dmrg.N(-8*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/K2,d=self.d))
                        
                        #Term 2-c
                        sep = abs(qm(t,j,q) - qm(t,i,q))
                        lo.set(targetrow,sep,dmrg.N(2.0/K2*pds[q]**2*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho),d=self.d))    
                                                
                        if(t<self.L[0]-1):                                                
                            #Term 3-b
                            sep = abs(qm(t,i,q) - qm(t,j,q))
                            lo.add(targetrow,sep,dmrg.N(2*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/K2,d=self.d))       
                                       
                            #Term 4-b
                            sep = abs(qm(t+1,i,q) - qm(t,j,q))
                            lo.set(targetrow,sep,dmrg.N(-4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/K2,d=self.d))       
                                                
                    mpoc.append(lo)
                    #print(pairs)
                    #lo.show()                    
         
        self.mpoc = mpoc
        return mpoc
 
    def getHamiltonian(self , threshold = 1.0e-8):
        
        qm = self.qubitmap #local easy calc
        pds = [self.d**i for i in range(self.L[2])] #store power of d's for easy ref
        K = self.K*self.Kscale
        K2 = K*K      
        
        S = {}
        D = {}
        
        for t in range(0,self.L[0]):
            for i in range(0, self.L[1]):
                for q in range(0,self.L[2]):
                    
                    #print(t,i,q)
                    #Do diagonal pieces for all sites
                    
                    #Term (1)
                    S[(qm(t,i,q), qm(t,i,q))] = (-self.mu(t,i)-2.0*self.rho)*pds[q]/K
                                        
                    #Term (2-d)
                    D[(qm(t,i,q), qm(t,i,q))] = (self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)*pds[q]**2/K2
                    
                    #Term (3-d)
                    if(t<self.L[0]-1):
                        D[(qm(t,i,q), qm(t,i,q))] += (self.lam(t+1,i)**2)*pds[q]**2/K2  

                    #We are done if it's the last qubit
                    if(t==self.L[0]-1 and i==self.L[1]-1 and q==self.L[2]-1):                        
                        continue
                                                   
                    #now set last row -- for everything all the way to the last qubit
                    #Term 4-d
                    assert(not(qm(t,i,q),qm(t+1,i,q)) in D)
                    D[(qm(t,i,q),qm(t+1,i,q))] = -2.0*self.lam(t,i)**2*pds[q]**2/K2
                    
                    for qp in range(q+1, self.L[2]):                                                
                        #Term 2-b
                        assert(not(qm(t,i,q),qm(t+1,i,qp)) in D)
                        D[(qm(t,i,q),qm(t,i,qp))] = 2.0*(self.ga/2*self.Sig(t,i,i) + self.lam(t,i)**2 + self.rho)/K2*pds[q]*pds[qp]
                        
                        if(t<self.L[0]-1):
                            #Term 3-c                            
                            D[(qm(t,i,q),qm(t,i,qp))] += 2*self.lam(t+1,i)**2*pds[q]*pds[qp]/K2
                            
                            #Term 4-c                     
                            assert(not(qm(t,i,qp),qm(t+1,i,q)) in D)
                            D[(qm(t,i,qp),qm(t+1,i,q))] = -4*self.lam(t+1,i)**2*pds[q]*pds[qp]/K2
                           
                    for j in range(i+1,self.L[1]):
                        for qp in range(q+1, self.L[2]):
                            #Term 2-a                        
                            assert(not(qm(t,i,q),qm(t,j,qp)) in D)
                            D[(qm(t,i,q),qm(t,j,qp))] = 4.0/K2*pds[q]*pds[qp]*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho)     
                            
                            if(t<self.L[0]-1):
                                #Term 3-a
                                D[(qm(t,i,q),qm(t,j,qp))] += 4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/K2
                            
                                #Term 4-a
                                assert(not(qm(t,j,qp),qm(t+1,i,q)) in D)
                                D[(qm(t,j,qp),qm(t+1,i,q))] = -8*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]*pds[qp]/K2 
                                                   
                        #Term 2-c
                        assert(not(qm(t,i,q),qm(t,j,q)) in D)
                        D[(qm(t,i,q),qm(t,j,q))] = 2.0/K2*pds[q]**2*(self.ga/2*self.Sig(t,i,j) + self.lam(t,i)*self.lam(t,j) + self.rho)
                        if(t<self.L[0]-1):
                            #Term 3-b
                            D[(qm(t,i,q),qm(t,j,q))] += 2*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/K2
                        
                            #Term 4-b
                            assert(not(qm(t,j,q),qm(t+1,i,q)) in D)
                            D[(qm(t,j,q),qm(t+1,i,q))] = -4*self.lam(t+1,i)*self.lam(t+1,j)*pds[q]**2/K2
    
        #Trim
        St = {key: S[key] for key in S if(abs(S[key]) > threshold)}
        Dt = {key: D[key] for key in D if(abs(D[key]) > threshold)}
    
        #Return Single (N) and Double (NN) operators
        return St,Dt
        
    def initialize(self):
        #Setup DMRG parameters
        dmrgp = dmrg.dmrgParams()
        dmrgp.L = np.prod(self.L)
        dmrgp.d = self.d
        
        #Get MPOS and MPS
        mpos = self.make_mpos()
        mps = dmrg.MPS(dmrgp, allocate=False)        
        dm = dmrg.DMRG(dmrgp,mps,mpos)
        return dm
        
    def run(self, cnvgThreshold = 1.0e-6, **kwargs):
        
        #Setup DMRG parameters
        dmrgp = dmrg.dmrgParams()
        dmrgp.L = np.prod(self.L)
        dmrgp.d = self.d
        
        #Get MPOS and MPS
        mpos = self.make_mpos()
        mps = dmrg.MPS(dmrgp, allocate=False)        
        dm = dmrg.DMRG(dmrgp,mps,mpos)
        
        #Sweep Schedule
        #sweepd = [2,5,10,15,20]
        #sweepi = [100,20,5,5,5]
        #sweepn = [1.0e-3,1.0e-4, 1.0e-4, 1.0e-4, 1.0e-5, 1.0e-5]
        
        sweepd = kwargs['sweepd'] if ('sweepd' in kwargs) else [1,2,2,2,3]
        sweepi = kwargs['sweepi'] if ('sweepi' in kwargs) else [10,10,10,10,10]
        sweepn = kwargs['sweepn'] if ('sweepn' in kwargs) else [1.0e-2,1.0e-3,1.0e-4,1.0e-5,1.0e-6]
        sweepmin = kwargs['sweepmin'] if ('sweepmin' in kwargs) else [5,5,2,2,2]
        
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
                newe = dm.energy()[0] + self.offset                
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
        mpos = self.make_mpos()        
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

        K = self.K*self.Kscale       
 
        vec = np.zeros([self.L[0],self.L[1]], dtype = np.float64)
        for tl,t in enumerate(range(0,L,dT)):
            for il,i in enumerate(range(0,dT,self.L[2])):                
                vec[tl,il] = np.sum([x[t+i+q]*self.d**q for q in range(self.L[2])])/K
        
        return vec


    #Compute relevant expectation values to understand answer:
    def computeWeights(self, mps):

        N = dmrg.N(1.0,d=self.d)
        I = dmrg.I(1.0,d=self.d)

        nopl = dmrg.MPO(1,2,d=self.d)
        nopl.set(0,0,N)  
        nopl.set(0,1,I)

        nopr = dmrg.MPO(2,1,d=self.d)
        nopr.set(0,0,I)
        nopr.set(1,0,N)

        nopm = dmrg.MPO(2,2,d=self.d)
        nopm.set(0,0,I)
        nopm.set(1,1,I)
        nopm.set(1,0,N)
                    
        mpsnorm = mps.norm()        
        bitv = [self.d**x/self.K/mpsnorm for x in range(self.L[2])]

        '''
        #022020
        for b1 in range(3):
            for b2 in range(3):
                for b3 in range(3):
                    print(b1,b2,b3)
                    mps = dmrg.MPS.scalarMPS([b1,b2,b3], d = 3)

       
                    N = dmrg.N(1.0,d=self.d)
                    I = dmrg.I(1.0,d=self.d)

                    nopl = dmrg.MPO(1,2,d=self.d)
                    nopl.set(0,0,N)  
                    nopl.set(0,1,I)

                    nopr = dmrg.MPO(2,1,d=self.d)
                    nopr.set(0,0,I)
                    nopr.set(1,0,N)

                    nopm = dmrg.MPO(2,2,d=self.d)
                    nopm.set(0,0,I)
                    nopm.set(1,1,I)
                    nopm.set(1,0,N)
       
                     
                    #Quick and dirty way
                    mI = dmrg.MPO(2,2,d=self.d)
                    mI.set(0,0,I)
                    mI.set(1,1,I)
                    mI.set(1,0,I)

                    lI = dmrg.MPO(1,2,d=self.d)
                    lI.set(0,0,I)
                    lI.set(0,1,I)
                    
                    rI = dmrg.MPO(2,1,d=self.d)
                    rI.set(0,0,I)
                    rI.set(1,0,I)
                    
                    fvs = {}
                    mpoc = [lI] + [mI]*(mps.dmrgp.L-2) + [rI]

                    idx = 0
                    for t in range(self.L[0]):
                        for i in range(self.L[1]):                
                            for q in range(self.L[2]):
                                if idx==0:
                                    mpoc[idx] = nopl
                                    val = dmrg.MPS.contractWithMPO(mps,mpoc,mps)
                                    mpoc[idx] = lI
                                    print(idx,val)                 
                                elif idx==mps.dmrgp.L-1:
                                    mpoc[idx] = nopr
                                    val = dmrg.MPS.contractWithMPO(mps,mpoc,mps)
                                    mpoc[idx] = rI
                                    print(idx,val)                 
                                else:
                                    mpoc[idx] = nopm
                                    val = dmrg.MPS.contractWithMPO(mps,mpoc,mps)
                                    mpoc[idx] = mI
                                    print(idx,val)                 
                                idx += 1 
        return fvs
        '''

        #Cal    culate right intermediates
        rintms = []

        psi = mps.psi
        

        def asa(x):
            return np.asarray(x)
        
        nopr.set(1,0,I)
        intm = np.einsum('txr,lrtb->xlb',psi[mps.dmrgp.L-1],nopr.op)
        intm = np.einsum('byz,xlb->xly',asa(psi[mps.dmrgp.L-1]).conj(),intm)
        rintms.append(np.copy(intm))
        nopr.set(1,0,N)        

        nopm.set(1,0,I)
        for i in range(mps.dmrgp.L-2,-1,-1):
            intm = np.einsum('dij,jok->diok',psi[i],intm)
            intm = np.einsum('tirk,lrtb->ikbl',intm,nopm.op)
            intm = np.einsum('ikbl,bmk->ilm',intm,asa(psi[i]).conj())
            rintms.append(np.copy(intm))
        nopm.set(1,0,N)    
        rintms.reverse()

        #Now do operator calculations
        lintms = []
        idx = 0


        fvs = {}
        for t in range(self.L[0]):
            for i in range(self.L[1]):                
                for q in range(self.L[2]):
                    if(idx==0):
                        intm = np.einsum('txy,lrtb->yrb',psi[0],nopl.op)
                        intm = np.einsum('yrb,bxz->yrz',intm,asa(psi[0]).conj())
        
                        val = np.einsum('yrz,yrz',intm,rintms[idx+1]) - (mps.dmrgp.L-1)                                
                        #print(idx,val) 
                        fvs[(t,i)] = fvs[(t,i)] + val*bitv[q] if (t,i) in fvs else val*bitv[q]

                        #Also compute left intermediate
                        nopl.set(0,0,I)
                        intm = np.einsum('txy,lrtb->yrb',psi[0],nopl.op)
                        intm = np.einsum('yrb,bxz->yrz',intm,asa(psi[0]).conj())
                        lintms.append(intm)
                        nopl.set(0,0,N)

                    elif(idx==mps.dmrgp.L-1):
                        intm = np.einsum('txy,lrtb->xlb',psi[idx],nopr.op)
                        intm = np.einsum('xlb,byz->xly',intm,asa(psi[idx]).conj())
                        val = np.einsum('xly,xly',intm,lintms[idx-1]) - (mps.dmrgp.L-1)                                 
                        #print(idx,val) 
                        fvs[(t,i)] = fvs[(t,i)] + val*bitv[q] if (t,i) in fvs else val*bitv[q]

                        #Also compute left intermediate
                        nopr.set(1,0,I)
                        intm = np.einsum('txy,lrtb->yrb',psi[idx],nopl.op)
                        intm = np.einsum('yrb,bxz->yrz',intm,asa(psi[idx]).conj())
                        intm = np.einsum('yrz,yrz',intm,lintms[idx-1])
                        lintms.append(intm) #Just a norm really
                        nopr.set(1,0,N)
                    else:
                        intm = np.einsum('lyz,blr->rbyz',lintms[idx-1],psi[idx])
                        intm = np.einsum('rbyz,yxbu->rxuz',intm,nopm.op)
                        intm = np.einsum('rxuz,uzy->rxy',intm,asa(psi[idx]).conj())

                        val = np.einsum('rxy,rxy',intm,rintms[idx+1]) - (mps.dmrgp.L-1)       
                        #print(idx,val) 
                        fvs[(t,i)] = fvs[(t,i)] + val*bitv[q] if (t,i) in fvs else val*bitv[q]
                   
                        #Also compute left intermediate
                        nopm.set(1,0,I)
                        intm = np.einsum('lyz,blr->rbyz',lintms[idx-1],psi[idx])
                        intm = np.einsum('rbyz,yxbu->rxuz',intm,nopm.op)
                        intm = np.einsum('rxuz,uzy->rxy',intm,asa(psi[idx]).conj())
                        lintms.append(intm)
                        nopm.set(1,0,N)
 
                    idx+=1

        return fvs 

def ss(x, d = 3):
    s = ''
    m = x
    while(m>0):
        r = m%d
        s = str(r) + s
        m = int(m/d)
   
    return s
    
if __name__ == '__main__':
    
    d = 3
    #Nt x N x N_q
    L = [1,3,1]
    fn = FlatNetwork(L, d)
    print('Resolution: ',1.0/d**L[2])   
 
    mpos = fn.mpoc
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
    #print(amp2)
    
    print('Number of states: ',ns)
        
    ampl = np.where(np.abs(amp2)>1.0e-8)[0]
    print('Sols size: ',len(ampl))
    ampv = amp2[ampl]
    config = [ss(x).zfill(np.prod(L)) for x in ampl]
    print(config)
    print(ampv**2)  
    print(fn.returnWeights(config[0]))
    
    #Get Hamiltonian
    #S,D = fn.getHamiltonian()
    #print('Singles: ',S)    
    #print('Doubles: ',D)
    
    #--------------
    res = fn.computeWeights(mps)
    print(res)
