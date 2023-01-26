import os
import pandas as pd

df_aux = X_train.loc[X_train.updated_directory_size<700]

dicci2 = dict()
for car_model in df_aux.car_model.unique():
    dicci2[car_model] = dicci_car_model[car_model]

for car_model, updated_directory_size in dicci2.items():
    number_of_copies  = 700//updated_directory_size
    to_random_sample =  700 - number_of_copies*updated_directory_size
    
    deeper_path = os.path.join(path_0,car_model)
    for single_car in os.listdir(deeper_path):
        for i in range(number_of_copies)