import os
import pandas as pd

X_train = pd.read_csv("table_for_train.csv")
X_test = pd.read_csv("table_for_test.csv")
X_val = pd.read_csv("table_for_val.csv")

X_train = X_train.loc[X_train.directory_size > 150]
X_test = X_test.loc[X_test.directory_size > 150]
X_val = X_val.loc[X_val.directory_size > 150]

path_0 = '../data'
path_out = '../data'
dicci = {"test":X_test, "train":X_train, "val":X_val}

# create train-test-val intermediate directories
for sub in list(dicci.keys()):
    os.makedirs(os.path.join(path_out, sub), exist_ok=True)
    for car_model in X_train.car_model.unique():
        os.makedirs(os.path.join(path_out, sub, car_model), exist_ok=True)

for subset_name, subset in dicci.items():
    for car_model in subset["car_model"].unique():
        #print(car_model, subset.nunique(), subset_name)
        deeper_path = os.path.join(path_0, car_model)
        for single_car in os.listdir(deeper_path):
            if single_car.endswith(".jpg"):
                prefix = single_car.split("_")[0]
                if int(prefix) in list(subset.loc[subset.car_model == car_model].single_car_index):
                    input_route = os.path.join(deeper_path, single_car)
                    output_route = os.path.join(path_out, subset_name, car_model, single_car)
                    try:
                        os.rename(input_route, output_route)
                    except FileExistsError:
                        print(input_route)
                        continue
                    
# remove empty subdirectories
for subset_name, subset in dicci.items():
    for car_model in subset["car_model"].unique():
        #print(car_model, subset.nunique(), subset_name)
        deeper_path = os.path.join(path_0, car_model)
        if len(os.listdir(deeper_path))==0:
            os.rmdir(deeper_path)
