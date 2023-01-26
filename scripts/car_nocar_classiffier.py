from utils import utils
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument("data_folder",
                        type=str,
                        help=("Full path to the directory having all the cars images.\
                               Already splitted in train/test sets.\
                               E.g. /home/app/src/data/car_ims_v1/."
                              ),
                        )
    args = parser.parse_args()
    return args

def main(data_folder):
    utiles.predict_from_folder_batch(data_folder,
                                     input_size=[224, 224],
                                     class_names=["auto", "no_auto"]
                                     )

if __name__ == "__main__":
    args = parse_args()
    main(args.data_folder)