import pandas as pd
import os, shutil

yolo_folder = '../eu-car-croped_autos/'
merge_folder = "../data/"
os.makedirs(merge_folder,exist_ok=True)

for root in os.listdir(yolo_folder):
    if os.path.isdir(os.path.join(yolo_folder,root)):
        os.makedirs(os.path.join(merge_folder,root),exist_ok=True)
        for vehicle_type in ["car", "truck"]:
            medium_path = os.path.join(yolo_folder,root, vehicle_type)
            if os.path.isdir(medium_path):
                for file in os.listdir(medium_path):
                    if file.endswith('jpg'):
                        in_put = os.path.join(medium_path, file)
                        out_put = os.path.join(merge_folder,root, file)
                        # if os.path.exists(out_put):
                        #     os.rename(in_put, out_put.replace(".jpg", "t.jpg"))    
                        # else:
                        #     os.rename(in_put, out_put)
                        os.link(in_put, out_put)