import shutil, random, os, argparse
import pandas as pd
import numpy as np 

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "data_folder",
        type=str,
        help=(
            "Full path to the directory having all the cars images. Already "
            "splitted in train/test sets. E.g. "
            "`/home/app/src/data/car_ims_v1/`."
        ),
    )
    parser.add_argument(
        "output_data_folder",
        type=str,
        help=(
            "Full path to the directory in which we will store the resulting "
            "cropped pictures. E.g. `/home/app/src/data/car_ims_v2/`."
        ),
    )

    args = parser.parse_args()

    return args

def main(data_folder, output_data_folder):
    random_selections={}
    os.makedirs(output_data_folder)
    for root, dirs, files in os.walk(data_folder, topdown=False):
        for file in files:
            path=os.path.join(root,file)
            dst=os.path.join(output_data_folder,file)
            random_selections[path]=dst
    random_selections_keys = np.random.choice(list(random_selections.keys()), size=1000,replace=False) 

    for key in random_selections_keys:
        #print(( key, random_selections[key]))
        os.link( key, random_selections[key])
                
if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder, args.output_data_folder)