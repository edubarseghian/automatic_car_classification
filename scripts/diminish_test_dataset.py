import os, shutil
import numpy as np

path_to_test = os.path.join(os.getcwd(), "spr_5_mario/data/")
destiny_path = os.path.join(os.getcwd(), "spr_5_mario/data_20/")
os.makedirs(destiny_path, exist_ok=True)

desired_max_size = 450

for z in os.listdir(path_to_test):
    aux = list(os.listdir(os.path.join(path_to_test, z)))
    size = len(aux)
    if size > desired_max_size:
        os.makedirs(os.path.join(destiny_path, z), exist_ok=True)
        selecteds = np.random.choice(aux, size=desired_max_size, replace=False)
        for file_jpg in selecteds:
            in_path = os.path.join(path_to_test, z, file_jpg)
            out_path  = os.path.join(destiny_path, z, file_jpg)
            os.link(in_path, out_path)
    else:
        print(z)
        shutil.copytree(os.path.join(path_to_test, z), os.path.join(destiny_path, z))