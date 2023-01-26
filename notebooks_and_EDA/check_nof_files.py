import os
import pandas as pd

nof_images, nof_cars, = 0, 0
root_0 = "../eu-car-dataset/"
df_0 = pd.DataFrame(columns=["car_directory", "cars", "total", "cars_70", "cars_90"])
for x in os.listdir(root_0):
    try:
        df = pd.read_csv(os.path.join(root_0, x,"car_nocar_class.csv"))
        dicci = {"car_directory":x, "total": len(df)}
        df = df.loc[df["label"]=="auto"]
        dicci["cars"] = len(df)
        df = df.loc[df["score"]>0.699]
        dicci["cars_70"] = len(df)
        df = df.loc[df["score"]>0.899]
        dicci["cars_90"] = len(df)
        df_0 = df_0.append(dicci, ignore_index=True)
    except:
        print(x)
        continue
df_0.to_csv("car_distribution.csv", index=False)
