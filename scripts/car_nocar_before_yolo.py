import pandas as pd
import os

def transform_path(path):
    return path.replace("dataset","only_autos")

root_0 = "../eu-car-dataset"
dest_0 = transform_path(root_0)
os.makedirs(dest_0,exist_ok=True)

df_0=pd.read_csv("../notebooks_and_EDA/car_distrib_extended.csv")
for x in list(df_0.brand_and_model.unique()):
    os.makedirs(os.path.join(dest_0,x), exist_ok=True)

# here we merge all the diferent years for each car model into one,
# and stick with only the cars with prob>0.7 according to the car_nocar_classifier
for _,car_directory, brand_and_model in df_0[["car_directory", "brand_and_model"]].itertuples():
    root_1 = os.path.join(root_0, car_directory)
    destination = os.path.join(dest_0, brand_and_model)        
    if os.path.isdir(root_1):
        df = pd.read_csv(os.path.join(root_0, car_directory,"car_nocar_class.csv"))
        df = df.loc[df["label"]=="auto"].loc[df["score"]>=0.7]
        df.to_csv(os.path.join(root_0, x,"only_car.csv"),index=False)
        for path in list(df.path.unique()):
            os.link(path, os.path.join(dest_0,brand_and_model,os.path.basename(path))