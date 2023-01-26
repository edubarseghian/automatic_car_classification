import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Initial table before dropping folders too big or too small
#df_0 = pd.read_csv("df_for_traintestsplit.csv", index = False)

# iterate over cropped images dataset
path_0 = "../data/"

# instantiate DataFrame to store directories info.
df = pd.DataFrame(columns=["car_model", "single_car_index", "nof_photos"])

# iterate over car models
for car_model in os.listdir(path_0):
    cars_dict = dict()
    # iterate over each car model subfolder
    # count number of repetitions of each single car
    deeper_path = os.path.join(path_0,car_model)
    for single_car in os.listdir(deeper_path):
        if single_car.endswith(".jpg"):
            prefix = single_car.split("_")[0]
            if prefix in cars_dict.keys():
                cars_dict[prefix] += 1
            else:
                cars_dict[prefix] = 1

    # store results in the DataFrame
    for key, value in cars_dict.items():
        df = df.append({"car_model": car_model,
                        "single_car_index": key,
                        "nof_photos": value
                        },ignore_index=True)

# calculate directory size 
dicci = dict()
for x in df.car_model.unique():
    dicci[x] = df.loc[df.car_model==x].nof_photos.sum()
df["directory_size"] = df.car_model.map(dicci)

# cumulative sum per directory to limit subfolder size
df['nof_photos'] = df['nof_photos'].astype(int)
df['cumsum_by_model'] = df.groupby('car_model')['nof_photos'].transform(pd.Series.cumsum)


# filter
df = df.loc[(df.directory_size > 150) & (df.cumsum_by_model < 1500)]

# update directory size after the upper threshold
dicci_car_model = dict()
for x in df.car_model.unique():
    dicci_car_model[x] = df.loc[df.car_model==x].nof_photos.sum()
df["updated_directory_size"] = df.car_model.map(dicci_car_model)


y = df.car_model

df.to_csv("df_for_traintestsplit.csv", index = False)

X_train, X_test, y_train, y_test = train_test_split( df, y, test_size=0.15, 
                                                           random_state = 10,
                                                           shuffle=True
                                                    )

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size =0.18, 
                                                           random_state = 14,
                                                           shuffle=True
                                                  )

X_train.to_csv("table_for_train.csv", index=False)
X_test.to_csv("table_for_test.csv", index=False)
X_val.to_csv("table_for_val.csv", index=False)