'''
from mitreattack.stix20 import MitreAttackData


def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    #tactics = mitre_attack_data.get_tactics(remove_revoked_deprecated=True)
    #tactics = mitre_attack_data.get_techniques(remove_revoked_deprecated=True)
    matrices = mitre_attack_data.get_matrices(remove_revoked_deprecated=True)
    print(matrices)

    print(f"Retrieved {len(tactics)} ATT&CK tactics.")


if __name__ == "__main__":
    main()
'''

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

dataset = pd.read_csv("Dataset/test.csv")
labels = np.unique(dataset['attack_cat']).ravel()
dataset.drop(['attack_cat', 'Label'], axis = 1,inplace=True)
dataset = dataset.drop_duplicates(subset=['sport'], keep='first')

label_encoder = []
columns = dataset.columns
types = dataset.dtypes.values
for j in range(len(types)):
    name = types[j]
    if name == 'object': #finding column with object type
        le = LabelEncoder()
        dataset[columns[j]] = pd.Series(le.fit_transform(dataset[columns[j]].astype(str)))#encode all str columns to numeric
        label_encoder.append([columns[j], le])
        
correlation = dataset.T.corr().mean()
print(correlation)
correlation = correlation.ravel()
correlation = np.argwhere(correlation > 0.8)
print(correlation)
print(len(correlation))

dataset.drop(index=correlation, inplace=True)
print(dataset)
print(dataset.shape)












