"""
This script will be used to remove noisy background from cars images to
improve the quality of our data and get a better model.
The main idea is to use a vehicle detector to extract the car
from the picture, getting rid of all the background, which may cause
confusion to our CNN model.
We must create a new folder to store this new dataset, following exactly the
same directory structure with its subfolders but with new images.
"""
import argparse, cv2, os
from utils.detection import get_vehicle_coordinates
import pandas as pd
from tqdm import tqdm

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
    args = parser.parse_args()
    return args

def main(data_folder):
    detectron_only_cars(data_folder)
    crops_and_links(data_folder)

def detectron_only_cars(input_folder, threshold=0.7):
    df_paths = pd.DataFrame(columns=['path_without_csv'])
    path_no_csv=[]
    for root, dirs, files in tqdm(os.walk(input_folder, topdown=False)):
        if 'car_nocar_class.csv' in files:
            coordinates=[]
            df=pd.read_csv(os.path.join(root,"car_nocar_class.csv"),index_col=False)
            df=df[(df['label']=='auto') & (df['score']>threshold)]
            df.reset_index(inplace=True)
            for path in df['path']:
                im = cv2.imread(path)
                coordinates.append(get_vehicle_coordinates(im))
            df2=pd.DataFrame(coordinates,columns=['v0','v1','v2','v3'])
            df=df.merge(df2,right_index=True,left_index=True)
            df.to_csv(os.path.join(root,"car_detectron.csv"))
        else:
            path_no_csv.append(root)
    df_paths['path_without_csv']= path_no_csv
    df_paths.to_csv("paths_no_csv.csv")

#This function crops auto labeled images in every folder and makes os.link to the output folder
def crops_and_links(input_folder):
    for root, dirs, files in tqdm(os.walk(input_folder, topdown=False)):
        path_no_crop=[]
        df_paths_no_crop = pd.DataFrame(columns=['path_no_crop'])
        if 'car_detectron.csv' in files:
            df=pd.read_csv(os.path.join(root,"car_detectron.csv"),index_col=False)
            os.makedirs(root.replace("dataset", "detectron"), exist_ok=True)
            for path, v0,v1,v2,v3 in df[["path", "v0","v1","v2","v3"]].itertuples(index=False):
                im = cv2.imread(path)
                v0 = max(0, v0)
                v1 = max(0, v1)
                v2 = min(im.shape[1], v2)
                v3 = min(im.shape[0], v3) 
                cropped_im = im[v1:v3,v0:v2,:]
                a=path.replace("dataset", "detectron")
                cv2.imwrite(a, cropped_im)
        df_paths_no_crop['path_no_crop']= path_no_crop
        df_paths_no_crop.to_csv(os.path.join(root,"paths_no_crop.csv"))         

if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder)
