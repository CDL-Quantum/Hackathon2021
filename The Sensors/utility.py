import strawberryfields as sf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm

import seaborn as sns


def OneModeCoherentHO(Ns,t,nth,shots):
    """
    Function that performs sensing using a single coherent state and performing homodyne measurements
    
    Args:
    
        Ns (float) : Average number of photons in the #1 mode
        t,nth (float,float) : channel transmittivity and number of thermal photons for the thermal loss channel
        shots (integer) : number of repeated iid measurements to perform
    
    Returns:
    
        list, list (complex,complex): returns the complex signal <X>+i<P> of both modes
    
    
    
    """
    s1 = np.zeros(shots)

    alpha = np.sqrt(Ns/4)
    
    for i in range(shots):
        prog= sf.Program(1)
        
        with prog.context as q:
        
            sf.ops.Coherent(alpha) | q[0] # State preparation
            sf.ops.ThermalLossChannel(t,nth) | q[0] # Thermal loss channel mimicing target
     
            sf.ops.MeasureX | q[0] # Het. Msmnt of signal 1


        # Need to run twice because of bug in the bosonic backend in dealing with repeated HD measurements
    
        eng = sf.Engine("bosonic")
        results = eng.run(prog)
    
        #Collecting the samples
        samples = results.all_samples
    
        #Creating the measurement records
        s1[i] = samples[0][0]
    
    # Interation over number of shots is done, outputing the records
    
    return s1

def OneModeCoherentHD(Ns,t,nth,shots):
    """
    Function that performs sensing using a single coherent state and performing heterodyne measurements

    Args:
    
        Ns (float) : Average number of photons in the #1 mode
        t,nth (float,float) : channel transmittivity and number of thermal photons for the thermal loss channel
        shots (integer) : number of repeated iid measurements to perform
    
    Returns:
    
        list, list (complex,complex): returns the complex signal <X>+i<P> of both modes
    
    
    
    """
    s1 = (1+1j)*np.zeros(shots)

    alpha = np.sqrt(Ns/4)
    
    for i in range(shots):
        prog= sf.Program(1)
        
        with prog.context as q:
        
            sf.ops.Coherent(alpha) | q[0] # State preparation
            sf.ops.ThermalLossChannel(t,nth) | q[0] # Thermal loss channel mimicing target
     
            sf.ops.MeasureHD | q[0] # Het. Msmnt of signal 1


        # Need to run twice because of bug in the bosonic backend in dealing with repeated HD measurements
    
        eng = sf.Engine("bosonic")
        results = eng.run(prog)
        
    
        #Collecting the samples
        samples = results.all_samples
    
        #Creating the measurement records
        s1[i] = samples[0][0]
    
    # Interation over number of shots is done, outputing the records
    
    return s1


def TwoModeSqueezedHD(Ns,t,nth,shots):
    
    """
    Function that performs sensing using two-mode squeezing and performing heterodyne measurements
    
    Args:
    
        Ns (float) : Average number of photons in the #1 mode
        t,nth (float,float) : channel transmittivity and number of thermal photons for the thermal loss channel
        shots (integer) : number of repeated iid measurements to perform
    
    Returns:
    
        list, list (complex,complex): returns the complex signal <X>+i<P> of both modes
    
    
    
    """
    
    s1 = (1+1j)*np.zeros(shots)
    s2 = (1+1j)*np.zeros(shots)
    
    r = np.arcsinh(np.sqrt(Ns/2))
    
    for i in range(shots):
        prog= sf.Program(2)
        
        with prog.context as q:
        
            sf.ops.S2gate(r,0) | (q[0],q[1]) # State preparation
            sf.ops.ThermalLossChannel(t,nth) | q[0] # Thermal loss channel mimicing target
     
            sf.ops.MeasureHD | q[0] # Het. Msmnt of signal 1
            sf.ops.MeasureHD | q[1] # Het. Msmnt of signal 2

        # Need to run twice because of bug in the bosonic backend in dealing with repeated HD measurements
    
        eng = sf.Engine("bosonic")
        results = eng.run(prog)
        eng = sf.Engine("bosonic")
        results = eng.run(prog)
    
        #Collecting the samples
        samples = results.all_samples
    
        #Creating the measurement records
        s1[i] = samples[0][0]
        s2[i] = samples[1][0]
    
    # Interation over number of shots is done, outputing the records
    
    return s1,s2

def TwoModeThermalHD(Ns,t,nth,shots):
    
    """
    Function that performs sensing using two-mode thermal states that are classically correlated and performing heterodyne measurements
    
    Args:
    
        Ns (float) : Average number of photons in the #1 mode
        t,nth (float,float) : channel transmittivity and number of thermal photons for the thermal loss channel
        shots (integer) : number of repeated iid measurements to perform
    
    Returns:
    
        list, list (complex,complex): returns the complex signal <X>+i<P> of both modes
    
    
    
    """
    
    s1 = (1+1j)*np.zeros(shots)
    s2 = (1+1j)*np.zeros(shots)
    

    
    for i in range(shots):
        prog= sf.Program(2)
        
        with prog.context as q:
        
            sf.ops.Thermal(Ns) | q[0] # State preparation
            sf.ops.BSgate() | (q[0],q[1])
            
            sf.ops.ThermalLossChannel(t,nth) | q[0] # Thermal loss channel mimicing target
     
            sf.ops.MeasureHD | q[0] # Het. Msmnt of signal 1
            sf.ops.MeasureHD | q[1] # Het. Msmnt of signal 2

        # Need to run twice because of bug in the bosonic backend in dealing with repeated HD measurements
    
        eng = sf.Engine("bosonic")
        results = eng.run(prog)
        eng = sf.Engine("bosonic")
        results = eng.run(prog)
    
       
        
        #Collecting the samples
        samples = results.all_samples
    
        #Creating the measurement records
        s1[i] = samples[0][0]
        s2[i] = samples[1][0]
    
    # Interation over number of shots is done, outputing the records
    
    return s1,s2

def SNR(op0, op1):
    """ Function that evaluates the signal-to-noise ratio of a given operator depending 
    on the msmt statistics on a binary outcome repeated over N independant and inditically distributed measurements.
    
        We define SNR as
        SNR = N* |<op1> - <op0>|^2 / ((Var[op0]+ Var[op1])/2)
        
        <x> statistical average of operator x
        Var[x] denotes the variance of x
        N = len(x) : the number of samples in the measurement records
        
    Args:
    
        op0, op1 (complex array length N ) : array N elements with the expectation values over N iids of an operator op given the binary outcome 0 or 1
        
    
    Returns:
    
        float: SNR calculation from the above equation
        
        
        
    
    """
    result = len(op0)*np.abs(np.mean(op1) - np.mean(op0))**2/((np.var(op1)+np.var(op0))/2)
    
    return result
