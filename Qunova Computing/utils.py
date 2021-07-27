import math
import random

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split


def samples(lst, k):
    n = len(lst)
    indices = []
    while len(indices) < k:
        index = random.randrange(n)
        if index not in indices:
            indices.append(index)
    return [lst[i] for i in indices]


def LoadData(TestSize, NumPCs, seed=None):
    cov_related_genes = ['ACE2', 'AGTR1', 'NFKB1', 'RELA', 'IL12A', 'CCL2', 'ISG15', 'IFIH1', 'TBK1', 'C2', 'C3', 'C5',
                         'C1R', 'C1S', 'FGA', 'FGB', 'FGG', 'RPS2', 'RPS3',
                         'RPS3A', 'RPS4X', 'RPS4Y1', 'RPS5', 'RPS6', 'RPS7', 'RPS8', 'RPS9', 'RPS11', 'RPS12', 'RPS13',
                         'RPS14', 'RPS15', 'RPS15A', 'RPS16', 'RPS18', 'RPS19',
                         'RPS20', 'RPS21', 'RPS23', 'RPS24', 'RPS25', 'RPS26', 'RPS27', 'RPS27A', 'RPS28', 'RPS29',
                         'FAU', 'RPSA', 'IRF3', 'STAT1', 'STAT2']

    # Data Preprocessing
    df = pd.read_csv('./GSE147507_Series6,16.csv', index_col=0)
    not_related_genes_ = [x for x in df.index if x not in cov_related_genes]
    random.seed(seed)
    not_related_genes = samples([x for x in not_related_genes_ if 0 not in list(df.loc[x, :])],
                                len(cov_related_genes))

    df_sample = df.loc[cov_related_genes + not_related_genes, :]
    for gene in df_sample.index:
        if gene in cov_related_genes:
            df_sample.loc[gene, 'target'] = 1
        else:
            df_sample.loc[gene, 'target'] = 0

    new_dict = {}
    for gene in df_sample.index:
        Series6_1 = math.log(
            df_sample.loc[gene, 'Series6_A549-ACE2_SARS-CoV-2_1'] / df_sample.loc[gene, 'Series6_A549-ACE2_Mock_1'], 2)
        Series6_2 = math.log(
            df_sample.loc[gene, 'Series6_A549-ACE2_SARS-CoV-2_2'] / df_sample.loc[gene, 'Series6_A549-ACE2_Mock_2'], 2)
        Series6_3 = math.log(
            df_sample.loc[gene, 'Series6_A549-ACE2_SARS-CoV-2_3'] / df_sample.loc[gene, 'Series6_A549-ACE2_Mock_3'], 2)
        Series16_1 = math.log(
            df_sample.loc[gene, 'Series16_A549-ACE2_SARS-CoV-2_1'] / df_sample.loc[gene, 'Series16_A549-ACE2_Mock_1'],
            2)
        Series16_2 = math.log(
            df_sample.loc[gene, 'Series16_A549-ACE2_SARS-CoV-2_2'] / df_sample.loc[gene, 'Series16_A549-ACE2_Mock_2'],
            2)
        Series16_3 = math.log(
            df_sample.loc[gene, 'Series16_A549-ACE2_SARS-CoV-2_3'] / df_sample.loc[gene, 'Series16_A549-ACE2_Mock_3'],
            2)

        if gene in cov_related_genes:
            new_dict[gene] = [Series6_1, Series6_2, Series6_3, Series16_1, Series16_2, Series16_3, 1]
        else:
            new_dict[gene] = [Series6_1, Series6_2, Series6_3, Series16_1, Series16_2, Series16_3, 0]

    df_div = pd.DataFrame.from_dict(new_dict).T
    df_div.columns = ['Series6_1', 'Series6_2', 'Series6_3', 'Series16_1', 'Series16_2', 'Series16_3', 'Target']

    dataset = df_div.to_numpy()
    x_div = dataset[:, 0:6]
    y_div = dataset[:, 6]

    x_div_train, x_div_test, y_div_train, y_div_test = train_test_split(x_div, y_div, test_size=TestSize, random_state=seed)

    pca = PCA(n_components=NumPCs, random_state=seed)
    pca.fit(x_div_train)
    TrainData = pca.transform(x_div_train)
    TestData = pca.transform(x_div_test)

    TrainMins = np.min(TrainData, axis=0)
    TrainMaxs = np.max(TrainData, axis=0)

    TrainData = np.pi * (TrainData - TrainMins) / (TrainMaxs - TrainMins)
    TestData = np.pi * (TestData - TrainMins) / (TrainMaxs - TrainMins)

    return TrainData, y_div_train, TestData, y_div_test
