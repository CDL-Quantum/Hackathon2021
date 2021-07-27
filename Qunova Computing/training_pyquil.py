import pickle as pkl

from pyquil_circuits import PauliFeatureMap, VariationalCircuit
from QVC import PyquilVariationalClassifier
from utils import LoadData

if __name__ == '__main__':
    def bf(bs):
        if len([i for i in bs if i == '0']) > len([i for i in bs if i == '1']):
            return 1
        else:
            return -1

    seed = 30
    qfm = PauliFeatureMap(num_qubits=3, rep=2)
    vc = VariationalCircuit(num_qubits=3, rep=2)

    TrainData, TrainLabels, TestData, TestLabels = LoadData(0.2, 3, seed)
    qvc = PyquilVariationalClassifier(qfm, vc, bf, False)
    print("Start training")

    point, value, nfev = qvc.train(TrainData, (-1) ** TrainLabels, 'zzzpfm_c12v3_pyquil')

    print("Training Done")
    print(point, value, nfev)

    with open("zzzpfm_c12v3.pkl") as of:
        pkl.dump((point, value, nfev), of)
