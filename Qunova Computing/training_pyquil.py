import numpy as np
from pyquil_circuits import PauliFeatureMap, VariationalCircuit
from QVC import PyquilVariationalClassifier
from utils import load_data

if __name__ == '__main__':
    def bf(bs):
        if len([i for i in bs if i == '0']) > len([i for i in bs if i == '1']):
            return 1
        else:
            return -1

    seed = 30
    qfm = PauliFeatureMap(num_qubits=3, rep=2)
    vc = VariationalCircuit(num_qubits=3, rep=2)

    TrainData, TrainLabels, TestData, TestLabels = load_data(0.2, 3, seed)
    qvc = PyquilVariationalClassifier(qfm, vc, bf, False)
    print("Start training")

    point, value, nfev = qvc.train(TrainData, (-1) ** TrainLabels, 'zzzpfm_c12v3_pyquil',
                                   test_data=TestData, test_label=(-1) ** TestLabels)

    print("Training Done")
    print(f"optimal params       = {point}")
    print(f"final_training_loss  = {value}")
    print(f"function evaluations = {nfev}")

    np.save('./npy_files/TrainData_zzpfmc12_pyquil.npy', TrainData)
    np.save('./npy_files/TestData_zzpfmc12_pyquil.npy', TestData)
    np.save('./npy_files/TrainLabels_zzpfmc12_pyquil.npy', TrainLabels)
    np.save('./npy_files/TestLabels_zzpfmc12_pyquil.npy', TestLabels)
    np.save('./npy_files/Optimal_param_zzpfmc12_pyquil.npy', qvc.optimal_params)
