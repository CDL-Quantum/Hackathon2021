'''
    @Author: Ushnish Ray
    Copyright (2021) All Rights Reserved.
'''
  
'''
    Structure for DMRG Parameters
'''
import numpy as np
import scipy.linalg as la
import scipy.sparse.linalg as las

class dmrgParams():
    
    def __init__(self):    
        self.d = 3
        self.D = 10        
        self.L = 10
        
        self.maxi = 100        
    
'''
    Class for a simple MPS
    and relevant functions
'''
def asa(x):
    return np.asarray(x)

def initRandom(bdim, eps, d = 2):
    psi = []
    le = []
    L = len(bdim) + 1
    
    for ld in range(d):
        le.append(np.random.rand(1,bdim[0])*eps)
    psi.append(le)
    for i in range(L-2):
        le=[]
        for ld in range(d):
            le.append(np.random.rand(bdim[i],bdim[i+1])*eps)
        psi.append(le)
    le = []
    for ld in range(d):
        le.append(np.random.rand(bdim[L-2],1)*eps)
    psi.append(le)
    return psi


def initUniform(bdim, eps, d = 2):
    psi = []
    le = []
    L = len(bdim) + 1
    
    le = []
    for ld in range(d):
        le.append(np.ones([1,bdim[0]])*eps)
    psi.append(le) 
    for i in range(L-2):
        le = []
        for ld in range(d):
            le.append(np.ones([bdim[i],bdim[i+1]])*eps)
        psi.append(le)
    le = []
    for ld in range(d):
        le.append(np.ones([bdim[L-2],1])*eps)
    psi.append(le) 
    return psi


'''
    Class for a simple MPS
    and relevant functions
'''  
class MPS:
    def __init__(self, dmrgp, initfn = initRandom, eps = 1.0e-6, allocate = True):
        
        self.dmrgp = dmrgp
        
        if(allocate):
            self.bdim = self.initdv(dmrgp.D)
            self.psi = initfn(self.bdim, eps, d=dmrgp.d)
        else:
            self.bdim = None
            self.psi = None

        self.initfn = initfn
        
    @staticmethod
    def scalarMPS(phystate):
        dmrgp = dmrgParams()
        dmrgp.L = len(phystate)
        dmrgp.D = 1
        
        mps = MPS(dmrgp, initfn = initUniform, eps = 1.0)
        
        for i in range(dmrgp.L):
            mps.psi[i][1-phystate[i]][0] = 0.0
        
        return mps
    
    @staticmethod
    def contractWithMPO(mps1,mpos,mps2):
        
        psi1 = mps1.psi
        psi2 = mps2.psi
        
        intm = np.einsum('txy,lrtb->yrb',psi1[0],mpos[0].op)
        intm = np.einsum('yrb,bxz->yrz',intm,asa(psi2[0]).conj())        
        for i in range(1,mps1.dmrgp.L):
            intm = np.einsum('yrz,dyj->rzdj',intm,psi1[i])
            intm = np.einsum('lztj,lrtb->zjrb',intm, mpos[i].op)
            intm = np.einsum('zjrb,bzk->jrk',intm,asa(psi2[i]).conj())
        
        intm = np.einsum('jjj->j',intm)
        return intm
                       
    def initdv(self, D):
        
        bdim = np.ones([self.dmrgp.L-1], dtype=np.int16)*D
        N = self.dmrgp.L - 1
        mw = int(np.floor(self.dmrgp.d*np.log(D)/np.log(2)))
        
        if(N<mw):            
            ds = self.dmrgp.d
            for i in range(int(np.floor(N/2))):
                bdim[i] = ds 
                ds *= self.dmrgp.d
            ds = ds/self.dmrgp.d if N%2 == 0 else ds
            
            for i in range(int(np.floor(N/2)),N):
                bdim[i] = ds
                ds /= self.dmrgp.d
        else:
            ds = self.dmrgp.d
            for i in range(int(np.floor(mw/2))):
                bdim[i] = ds
                ds *= self.dmrgp.d
            ds/=2
            for i in range(N-int(np.floor(mw/2)),N):
                bdim[i] = self.dmrgp.d
                ds /= self.dmrgp.d
                
        return bdim      
            
    def setnewbd(self, D, noise=0.0):        
        newbd = self.initdv(D)
        if(self.psi is None):
            self.psi = self.initfn(newbd, noise, d = self.dmrgp.d)        
        
        le = []
        for ld in range(self.dmrgp.d):
            le.append(np.random.rand(1,newbd[0])*noise)
        il = self.psi[0][0].shape[1] if (newbd[0]>self.psi[0][0].shape[1]) else newbd[0]
        for ld in range(self.dmrgp.d):
            le[ld][0][:il] = self.psi[0][ld][0][:il]
        self.psi[0] = le
        
        for i in range(self.dmrgp.L-2):
            site = i + 1
            
            le = []
            for ld in range(self.dmrgp.d):
                le.append(np.random.rand(newbd[i],newbd[i+1])*noise)
            il = self.psi[site][0].shape[0] if (newbd[i]>self.psi[site][0].shape[0]) else newbd[i]
            ipl = self.psi[site][0].shape[1] if (newbd[i+1]>self.psi[site][0].shape[1]) else newbd[i+1]
            
            for ld in range(self.dmrgp.d):
                for r in range(il):
                    for c in range(ipl):
                        le[ld][r][c] = self.psi[site][ld][r][c]
            
            self.psi[site] = le
        
        le = []
        site = self.dmrgp.L - 1
        i = self.dmrgp.L - 2
        for ld in range(self.dmrgp.d):
            le.append(np.random.rand(newbd[i],1)*noise)
        il = self.psi[site][0].shape[0] if (newbd[i] > self.psi[site][0].shape[0]) else newbd[i]
        for ld in range(self.dmrgp.d):
            le[ld][0][:il] = self.psi[site][ld][0][:il]
        self.psi[site] = le
        self.bdim = newbd

    def rightNormalize(self, idx=None):
        
        '''
        Right normalize up to idx
        '''    
        if(idx is None): 
            idx = -1
        elif(idx>=self.dmrgp.L-1):
            return -1

        def lsvd(a):
            u,s,v = la.svd(a,full_matrices=False)
            tl = len(s)
            s = np.diag(s[:tl])
            u = u[:,:tl]
            v = v[:tl,:] 
    
            #Shape v correctly after getting right sector
            v = v.reshape([tl,self.dmrgp.d,-1]).swapaxes(0,1)
            return u,s,v
    
        psi = self.psi
        
        u,s,v = lsvd(asa(psi[self.dmrgp.L-1]).reshape([self.dmrgp.d,-1]).T)
        aux = np.dot(u,s)
        for ld in range(self.dmrgp.d):
            psi[self.dmrgp.L-1][ld] = v[ld]
        self.bdim[self.dmrgp.L-2] = v.shape[1]
        
        u,s,v = lsvd(asa(psi[self.dmrgp.L-1]).reshape([self.dmrgp.d,-1]).T)
        aux = np.dot(u,s)
        for ld in range(self.dmrgp.d):
            psi[self.dmrgp.L-1][ld] = v[ld]
        self.bdim[self.dmrgp.L-2] = v.shape[1]

        for i in range(self.dmrgp.L-2,idx,-1): 
            for ld in range(self.dmrgp.d):
                psi[i][ld] = np.dot(psi[i][ld],aux)
            if(i>0):
                self.bdim[i-1] = psi[i][0].shape[0]
            #print i,(self.psi[i]).shape,intm.shape

            #This intermediate will be at most [DxdD] and v is shaped correctly -- ordering tricky 
            intm = asa(psi[i]).swapaxes(0,1).reshape([self.psi[i][0].shape[0],self.dmrgp.d*aux.shape[1]])
            u,s,v = lsvd(intm)
            for ld in range(self.dmrgp.d):
                self.psi[i][ld] = v[ld]
            aux = np.dot(u,s)
            
    def norm(self):
        ften = np.einsum('pki,pkj->ij',asa(self.psi[0]),asa(self.psi[0]).conj())    
        for i in range(1,self.dmrgp.L-1):
            ften = np.einsum('ij,dik->djk',ften,asa(self.psi[i]))
            ften = np.einsum('dij,dik->jk',ften,asa(self.psi[i]).conj())
        cr = np.einsum('pik,pjk->ij',asa(self.psi[self.dmrgp.L-1]),asa(self.psi[self.dmrgp.L-1]).conj())
        nrm = np.einsum('ij,ij',ften,cr)
        return nrm
    
    def contractWith(self, mps):
        psi = mps.psi
        ften = np.einsum('pki,pkj->ij',asa(self.psi[0]),asa(psi[0]))    
        for i in range(1,self.dmrgp.L-1):
            ften = np.einsum('ij,dik->djk',ften,asa(self.psi[i]))
            ften = np.einsum('dij,dik->jk',ften,asa(psi[i]))
        cr = np.einsum('pik,pjk->ij',asa(self.psi[self.dmrgp.L-1]),asa(psi[self.dmrgp.L-1]))
        nrm = np.einsum('ij,ij',ften,cr)
        return nrm
    
    def getAmp(self):
        
        amp = []
        for i in range(self.dmrgp.d**self.dmrgp.L):
            state = [int(x) for x in bin(i)[2:].zfill(self.dmrgp.L)]
            scalarmps = MPS.scalarMPS(state)
            amp.append(self.contractWith(scalarmps))
            
        return amp
    
    
'''
    Class for a simple MPO
    and relevant functions
'''        
class MPO:
    
    def __init__(self, opil, opir, d = 2):
        self.shape = [opil,opir]
        self.d = d        
        self.op = np.zeros([opil,opir,d,d])        
        self.ops = [['' for j in range(opir)] for i in range(opil)]
        self.coeff = np.zeros([opil,opir])
    
    #Format is (ex)it -> (en)try
    def set(self, ex, en, lop):
        self.op[ex,en] = lop.op
        
        self.ops[ex][en] = lop.label
        self.coeff[ex,en] = lop.coeff
    
    def add(self, en, ex, lop):
        cpy = self.op[ex,en] + lop.op
        self.op[ex,en] = cpy

    def show(self):
        print(np.array(self.ops))
        print(self.coeff)
    
    # do mpo1 x mpo2
    @staticmethod
    def outer(mpo1, mpo2):
        
        assert(mpo1.shape[1] == mpo2.shape[0])
        
        op = np.zeros([mpo1.shape[0],mpo2.shape[1],mpo1.op.shape[2]*mpo2.op.shape[2],mpo1.op.shape[3]*mpo2.op.shape[3]])
        newmpo = MPO(op.shape[0],op.shape[1])
        newmpo.op = op
        
        for i in range(op.shape[0]):
            for j in range(op.shape[1]):
                for k in range(mpo1.shape[1]):
                    op[i,j] += np.kron(mpo1.op[i,k],mpo2.op[k,j])
                                        
                    newmpo.ops[i][j] = newmpo.ops[i][j].strip() + ' ' + ('(' + mpo1.ops[i][k].strip() + ')' + '(' + mpo2.ops[k][j].strip() + ')' if(mpo1.ops[i][k].strip() != '' and mpo2.ops[k][j].strip() != '') else '') + (' + ' if (k<mpo1.shape[1]-1 and (mpo1.ops[i][k].strip() != '' and mpo2.ops[k][j].strip() != '')) else ' ' ) 
                    newmpo.coeff[i,j] += mpo1.coeff[i,k]*mpo2.coeff[k,j]
                    
        return newmpo
                    
'''
    Operators for our problem
'''
class N:
    def __init__(self,v,d=2):
        self.op = np.zeros([d,d])
        for i in range(1,d):
            self.op[i,i] = i*v
        
        self.label = 'N'
        self.coeff = v
        
class I:
    def __init__(self, v=1.0,d=2):
        self.op = np.eye(d)*v
        
        self.label = 'I'
        self.coeff = v
        
'''
    Class for running DMRG                
'''
class DMRG:
    
    def __init__(self, dmrgp, mps, mpos):
        
        self.dmrgp = dmrgp
        self.mps = mps      
        self.mpos = mpos
        
        #State Variables
        self.lintms = []
        self.rintms = []
    
        self.rintc = False
        self.lintc = False
        self.lastsweep = None
        self.fsweep = 0
                
        #Eigensolver    
        self.eigsolver = las.eigsh
        self.target = 'SA'
        self.eigmethod = 'arpack'
        
    def calcintR(self):
        
        psi = self.mps.psi
        self.rintms = []
        
        intm = np.einsum('txr,lrtb->xlb',psi[self.dmrgp.L-1],self.mpos[self.dmrgp.L-1].op)
        intm = np.einsum('byz,xlb->xly',asa(psi[self.dmrgp.L-1]).conj(),intm)
        self.rintms.append(np.copy(intm))
        
        for i in range(self.dmrgp.L-2,0,-1):
            intm = np.einsum('dij,jok->diok',psi[i],intm)
            intm = np.einsum('tirk,lrtb->ikbl',intm,self.mpos[i].op)
            intm = np.einsum('ikbl,bmk->ilm',intm,asa(psi[i]).conj())
            self.rintms.append(np.copy(intm))
            
        self.rintms.reverse()
        self.rintc = True
    
    def calcintL(self):
        psi = self.mps.psi
        self.lintms = []
        
        intm = np.einsum('txy,lrtb->yrb',psi[0],self.mpos[0].op)
        intm = np.einsum('yrb,bxz->yrz',intm,psi[0])
        self.lintms.append(np.copy(intm))
        
        for i in range(1,self.dmrgp.L-1):
            intm = np.einsum('yrz,dyj->rzdj',intm,psi[i])
            intm = np.einsum('lztj,lrtb->zjrb',intm, self.mpos[i].op)
            intm = np.einsum('zjrb,bzk->jrk',intm,psi[i].conj())
            self.lintms.append(np.copy(intm))
            
        self.lintc = True
        self.rintc = False
    
    def energy(self):

        if(self.lastsweep == ''):
            self.calcintR()
            self.rintc = True
    
        psi = (self.mps.psi)
        if(self.lastsweep == 'R'): 
            #If lastsweep was right then must use left intermediates to compute energy
            intm = self.lintms[len(self.lintms)-1]
            intm1 = np.einsum('ioj,dik->djok',intm,(psi[self.dmrgp.L-1]))
            intm2 = np.einsum('djok,okdb->bj',intm1,self.mpos[self.dmrgp.L-1].op)
            energy = np.einsum('bj,bjm->m',intm2,asa(psi[self.dmrgp.L-1]).conj())
        elif(self.lastsweep == 'L'):
            #If lastsweep was left or no sweeps just use right intermediates to compute energy
            intm = self.rintms[0]
            intm1 = np.einsum('dij,jok->doki',(psi[0]),intm)
            intm2 = np.einsum('doki,iodb->bk',intm1,self.mpos[0].op)
            energy = np.einsum('bk,bmk->m',intm2,asa(psi[0]).conj())
        else:
            energy = 0.0    
        nrm = self.mps.norm()
        return energy/nrm

    
    def sweepleft(self, tol=1.0e-8):
        if(not self.lintc):
            self.calcintL()
            
        def lsvd(a):
            u,s,v = la.svd(a, full_matrices=False)
            tl = len(s)
            s = np.diag(s[:tl])
            u = u[:,:tl]
            v = v[:tl,:]
            
            v = v.reshape([tl,self.dmrgp.d,-1]).swapaxes(0,1)
            return u,s,v
        
        evs = []
        self.rintms = []
        psi = self.mps.psi
        
        lidx = len(self.lintms)-1
        site = self.dmrgp.L-1
        
        #Construct local eigenvalue problem and solve it
        lh = np.einsum('xly,lrtb->txby',self.lintms[lidx],self.mpos[site].op)
        lh = lh.reshape([self.dmrgp.d*lh.shape[1],self.dmrgp.d*lh.shape[3]])
        [ev,lmps] = self.eigsolver(lh,k=1,which=self.target,maxiter=lh.shape[0]*10,tol=tol,ncv=100)
        lmps = lmps.reshape([self.dmrgp.d,-1]).swapaxes(0,1)
        evs.append(ev[0])

        #Create right normalized matrix
        u,s,v = lsvd(lmps)
        aux = np.dot(u,s)
        for ld in range(self.dmrgp.d):
            psi[site][ld] = v[ld]
        self.mps.bdim[site-1] = v.shape[1]

        #Compute right intermediates
        intm = np.einsum('txy,lrtb->xlb',(psi[site]),self.mpos[site].op)
        intm = np.einsum('byz,xlb->xly',asa(psi[site]).conj(),intm)
        self.rintms.append(np.copy(intm))
        
        
        #Now do remaining sites up to first site
        for i in range(self.dmrgp.L-2,0,-1):
            lidx -= 1 #Shift left intermediate index

            #Absorb normalization
            for ld in range(self.dmrgp.d):
                psi[i][ld] = np.dot(psi[i][ld],aux)
            self.mps.bdim[i-1] = psi[i][0].shape[0]

            #Create local operator and solve local problem
            lh = np.einsum('xly,lrtb->txbyr',self.lintms[lidx],self.mpos[i].op)
            lh = np.einsum('txbyr,prq->txpbyq',lh,intm)
            lsz = lh.shape[1]
            rsz = lh.shape[2]
            lh = lh.reshape([self.dmrgp.d*lh.shape[1]*lh.shape[2],self.dmrgp.d*lh.shape[4]*lh.shape[5]])
            [ev,lmps] = self.eigsolver(lh,k=1,which=self.target,maxiter=lh.shape[0]*10,tol=tol,ncv=100)
            
            lmps = lmps.reshape([self.dmrgp.d,lsz,rsz]).swapaxes(0,1).reshape([lsz,self.dmrgp.d*rsz])
            evs.append(ev[0])

            u,s,v = lsvd(lmps)
            aux = np.dot(u,s)
            for ld in range(self.dmrgp.d):
                psi[i][ld] = v[ld]           

            #Compute right intermediate
            intm = np.einsum('dij,jok->diok',asa(psi[i]),intm)
            intm = np.einsum('diok,lodb->ilkb',intm,self.mpos[i].op)
            intm = np.einsum('ilkb,bmk->ilm',intm,asa(psi[i]).conj())
            self.rintms.append(np.copy(intm))
                    
        self.rintms.reverse() 
        i = 0
        for ld in range(self.dmrgp.d):
            psi[i][ld] = np.dot(psi[i][ld],aux)
        
        self.rintc = True
        self.lintc = False
        self.lastsweep = 'L'
        return evs
    
    def sweepright(self,tol=1.0e-8):
        #Cannot sweep right without right intermediates
        if(not self.rintc):
            self.calcintR()

        def lsvd(a):
            u,s,v = la.svd(a,full_matrices=False)
            #Truncation logic here    
            tl = len(s)
            s = np.diag(s[:tl])
            v = v[:tl,:]

            #Shape u correctly after getting right sector
            u = u[:,:tl]
            u = u.reshape([self.dmrgp.d,-1,tl])
            return u,s,v

        self.lintms = []
        evs = []
        psi = self.mps.psi
       
        #Left-most site
        #Construct local eigenvalue problem and solve it
        lh = np.einsum('lrtb,xry->txby',self.mpos[0].op,self.rintms[0])
        lh = lh.reshape([self.dmrgp.d*lh.shape[1],self.dmrgp.d*lh.shape[3]])
        [ev,lmps] = self.eigsolver(lh,k=1,which=self.target,maxiter=lh.shape[0]*10,tol=tol,ncv=100)
        lmps = lmps.reshape([self.dmrgp.d,-1])
        
        #Create left normalized matrix
        u,s,v = lsvd(lmps)
        aux = np.dot(s,v)
        for ld in range(self.dmrgp.d):
            psi[0][ld] = u[ld]
        self.mps.bdim[0] = u.shape[2]              
        evs.append(ev[0])

        #Compute left intermediates
        intm = np.einsum('tlx,lrtb->xrb',(psi[0]),self.mpos[0].op)
        intm = np.einsum('byz,xrb->xrz',asa(psi[0]).conj(),intm)
        self.lintms.append(np.copy(intm))        

        #Now do remaining sites
        for i in range(1,self.dmrgp.L-1):
            
            #Absorb normalization
            psi[i] = np.einsum('sa,dab->dsb',aux,asa(psi[i]))
            self.mps.bdim[i] = psi[i][0].shape[1]
              
            #Create local operator and solve local problem
            lh = np.einsum('xly,lrtb->txbyr',intm,self.mpos[i].op)
            lh = np.einsum('txbyr,prq->txpbyq',lh,self.rintms[i])
            lsz = lh.shape[1]
            rsz = lh.shape[2]

            lh = lh.reshape([self.dmrgp.d*lh.shape[1]*lh.shape[2],self.dmrgp.d*lh.shape[4]*lh.shape[5]])
            ev = None
            lmps = None
            [ev,lmps] = self.eigsolver(lh,k=1,which=self.target,maxiter=lh.shape[0]*10,tol=tol,ncv=100)
            lmps = lmps.reshape([self.dmrgp.d*lsz,rsz])
            evs.append(ev[0])

            u,s,v = lsvd(lmps)
            aux = np.dot(s,v)
            for ld in range(self.dmrgp.d):                
                psi[i][ld] = u[ld]
            

            #Compute left intermediate
            intm = np.einsum('dij,iok->djok',(psi[i]),intm)
            intm = np.einsum('djok,ordb->jrkb',intm,self.mpos[i].op)
            intm = np.einsum('jrkb,bkm->jrm',intm,asa(psi[i]).conj())
            self.lintms.append(np.copy(intm))
            
        
        #Final site -- Don't need left intermediate
        i = self.dmrgp.L-1
        for ld in range(self.dmrgp.d):
            psi[i][ld] = np.dot(aux,psi[i][ld])

        self.lintc = True
        self.rintc = False
        self.lastsweep = 'R'
        return evs
        
    
    def sweep(self,fdir='R',tol=1.0e-8):
        if(fdir=='R'):
            evrs = self.sweepright(tol=tol)
            evls = self.sweepleft(tol=tol)
            self.fsweep += 1
            return evls
        else:
            evls = self.sweepleft(tol=tol)
            evrs = self.sweepright(tol=tol)
            self.fsweep += 1
            return evrs

    
if __name__ == '__main__':
    
    dmrgp = dmrgParams()
    dmrgp.L = 10
    dmrgp.D = 30
    
    #Create MPO collection
    mpoc = []
    u = 1.35
    
    lo = MPO(1,3)
    lo.set(0,0,N(-1.0))
    lo.set(0,1,N(u))
    lo.set(0,2,I())
    mpoc.append(lo)
    
    lo = MPO(3,3)
    lo.set(0,0,I())
    lo.set(1,0,N(1.0))
    lo.set(2,0,N(-1.0))
    
    lo.set(2,1,N(u))
    lo.set(2,2,I())
    for i in range(1,dmrgp.L-1):
        mpoc.append(lo)
        
    lo = MPO(3,1)
    lo.set(0,0,I())
    lo.set(1,0,N(1.0))
    lo.set(2,0,N(-1.0))
    mpoc.append(lo)
    
    #Create MPS
    mps = MPS(dmrgp)
    mps.rightNormalize()
    print('Norm is: ',mps.norm())

    dm = DMRG(dmrgp,mps,mpoc)
    for i in range(5):
        sweepe = dm.sweep()
        lenergy = dm.energy()
        
        amp = np.array(mps.getAmp())        
        ampl = np.where(np.abs(amp)>1.0e-8)[0]
        ampv = amp[ampl]
        config = [bin(x)[2:].zfill(dmrgp.L) for x in ampl]
        print(config)
        print(ampv**2)
    
        print("Sweep Energy = ",lenergy)
    
    amp = np.array(mps.getAmp())        
    ampl = np.where(np.abs(amp)>1.0e-8)[0]
    ampv = amp[ampl]
    config = [bin(x)[2:].zfill(dmrgp.L) for x in ampl]
    
    print(config)
    print(ampv**2)