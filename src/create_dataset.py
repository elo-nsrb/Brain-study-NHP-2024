import os
import pandas as pd

def createDataset(metadata, path_samples):
    X = []
    for it in range(metadata.shape[0]):
        filename = metadata.loc[it, "File name"]
        path = os.path.join(path_samples, filename)
        tab = pd.read_csv(path, sep="\t", header=1)
        tab["filename"] = filename
        tab["Diet"] = metadata.loc[it, "Diet"]
        tmp = tab["filename"].str.split("_", expand=True)
        tab["Subject_name"] = tmp[7]
        tab["Sample_name"] = tmp[0] + "_"+ tmp[4] + "_" +tmp[7]
        tab["Cohort"] = "batch" + metadata.loc[it, 'Cohort ("BC009"=Cohort1, "BC010"=Cohort2)'].astype(str)
        X.append(tab) 
        
    X = pd.concat(X, axis=0)
    list_to_remove = ['172Yb_Tau_(Yb172Di)','156Gd_NET_(Gd156Di)']
    X.drop(list_to_remove, axis=1, inplace=True)
    
    markers = X.columns[1:31].tolist()
    markers = [it for it in markers if not it in list_to_remove]
    markers_names = [it.split("_")[1] for it in markers ]

    return X, markers
