import pandas as pd
import os
from tqdm import tqdm

def transform_path(path):
    return path.replace("only_autos", "croped_autos")

def main():
    root_0 = '/home/app/src/eu-car-only_autos/'
    destinationpath =  transform_path(root_0)
    #os.makedirs(destinationpath,exist_ok=True)
    # print('---')
    os.system('pip install seaborn')
    for x in tqdm(os.listdir(root_0)):
        #os.makedirs(os.path.join(destinationpath, x),exist_ok=True)
        print(x)
        if os.path.isdir(os.path.join(root_0, x)):
            execscript = f'python3 yolov5/detect.py --weights yolov5m.pt --save-txt --save-crop --source {os.path.join(root_0,x) }/ --name {os.path.join(destinationpath,x)} --classes 2 7'
            os.system(execscript)
        
if __name__ == '__main__':
    main()
