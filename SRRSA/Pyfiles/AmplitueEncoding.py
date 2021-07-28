import numpy as np

import random
from toolz import partition
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit import transpile, assemble
from qiskit import BasicAer, Aer, execute
from qiskit.quantum_info import state_fidelity
from qiskit.visualization import *
from qiskit.quantum_info.operators import Operator

nqubits=8;
nshot=1000;

def normlaizeData(data):
    #Create Array of pixel value
    testdata=data
    arr_data=testdata.flatten()/max(testdata.flatten());
    encoding_data= np.array([np.round(x,6) for x in arr_data]);
    sum_const=np.sqrt(sum(encoding_data*encoding_data))
    encoding_norm=encoding_data/sum_const
    return encoding_norm

def buildCicuit(encoding):
    qr = QuantumRegister(nqubits)
    cr = ClassicalRegister(nqubits)

    qc = QuantumCircuit(qr, name='Initialization')
    qc.initialize(encoding, range(nqubits))
    my_inst = qc.to_instruction()


    my_circuit = QuantumCircuit(qr,cr)
    my_circuit.append(my_inst, range(nqubits))
    my_circuit.measure(qr[:],cr[:])
    return my_circuit

def runCircuit(circuit):
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=nshot)
    result = job.result()
    count =result.get_counts()
    return count

def countBitstring(count):
    f=[]
    for i in range(2**nqubits):
        if format(i, '#010b')[2:10] in count:
            f.append(count[format(i, '#010b')[2:10]])
        else:
            f.append(0)
    return np.array(list(f))

def imgize(listdata):
    out_img=np.array(list(partition(16, listdata)));
    return out_img/max(listdata)

def findCutOff(img,target):
    f=[]
    for i in range(100):
        f.append(1-sum(sum((abs(target - 1.0 * (img > i/100)))/(2**nqubits))))
    mx=max(f);
    index=f.index(mx);
    rethres=1.0 * (img > index/100)
    return rethres  

def accuracy(img,target):
    acc=1-sum(sum((abs(target-img))))/(2**nqubits)
    return acc

def AmpltudeEncoding(input,target):
    encoding_norm=normlaizeData(input)
    qc=buildCicuit(encoding_norm)
    count = runCircuit(qc)
    listcount=countBitstring(count)
    img=imgize(listcount)

    acc=accuracy(img,target)
    return img,acc    


#filter is in %
def countBitstringFilter(count,filter):    
    f=[]
    thrs = nshot*filter
    for i in range(2**nqubits):
        if format(i, '#010b')[2:10] in count:
            if count[format(i, '#010b')[2:10]] > thrs:
                f.append(1)
            else:
                f.append(0)        
        else:
            f.append(0)
    return np.array(list(f))    

def AmpltudeEncodingFilter(input,filter):
    encoding_norm=normlaizeData(input)
    qc=buildCicuit(encoding_norm)
    count = runCircuit(qc)
    listcount=countBitstringFilter(count,filter)
    img=imgize(listcount)
    return img    


#filter is in %
def countBitstringFilter32(count,filter):
    nqubits=10;
    nshot=10000;    
    f=[]
    thrs = nshot*filter
    for i in range(2**nqubits):
        if format(i, '#012b')[2:12] in count:
            if count[format(i, '#012b')[2:12]] > thrs:
                f.append(1)
            else:
                f.append(0)        
        else:
            f.append(0)
    return np.array(list(f))

def imgize32(listdata):
    out_img=np.array(list(partition(32, listdata)));
    return out_img/max(listdata)

def AmpltudeEncodingFilter32(input,filter):
    nqubits=10;
    nshot=10000;
    encoding_norm=normlaizeData(input)
    qc=buildCicuit32(encoding_norm)
    count = runCircuit(qc)
    listcount=countBitstringFilter32(count,filter)
    img=imgize32(listcount)
    return img            


def buildCicuit32(encoding):
    nqubits=10;
    nshot=10000;
    qr = QuantumRegister(nqubits)
    cr = ClassicalRegister(nqubits)

    qc = QuantumCircuit(qr, name='Initialization')
    qc.initialize(encoding, range(nqubits))
    my_inst = qc.to_instruction()


    my_circuit = QuantumCircuit(qr,cr)
    my_circuit.append(my_inst, range(nqubits))
    my_circuit.measure(qr[:],cr[:])
    return my_circuit    