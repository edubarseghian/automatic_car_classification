import os
import pandas as pd
import shutil
import numpy as np


path_0 = '../eu-car-bymodel3/train/'
path_dst = '../eu-car-bymodel3/train_oversample/'

desired_size = 350

os.makedirs(path_dst)
shutil.copytree(path_0, path_dst)

X_train = pd.read_csv("table_for_train.csv")
df_aux = X_train.loc[X_train.train_directory_size < desired_size]

dicci_car_model = dict()
for x in df_aux.car_model.unique():
    dicci_car_model[x] = df_aux.loc[df_aux.car_model == x].nof_photos.sum()

for car_model, updated_directory_size in dicci_car_model.items():
    number_of_copies = desired_size//updated_directory_size
    to_random_sample = desired_size - number_of_copies*updated_directory_size
    number_of_copies = number_of_copies - 1
    deeper_path = os.path.join(path_0, car_model)
    choice_samples = np.random.choice(
        list(os.listdir(deeper_path)), size=to_random_sample, replace=False)
    for x in choice_samples:
        input_route = os.path.join(deeper_path, single_car)
        output_route = os.path.join(
            path_dst, car_model,  '0_' + single_car)
        os.link(input_route, output_route)
    for single_car in os.listdir(deeper_path):
        for i in range(1, number_of_copies+1):
            # make copy of single_car
            input_route = os.path.join(deeper_path, single_car)
            output_route = os.path.join(
                path_dst, car_model, str(i) + '_' + single_car)
            os.link(input_route, output_route)