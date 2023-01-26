import os, yaml
import tensorflow as tf
import numpy as np
import pandas as pd
from models import MobilenetV2
from tqdm import tqdm

def validate_config(config):
    if "seed" not in config:
        raise ValueError("Missing experiment seed")
    if "data" not in config:
        raise ValueError("Missing experiment data")
    if "directory" not in config["data"]:
        raise ValueError("Missing experiment training data")

def load_config(config_file_path):
    # TODO
    # Load config here and assign to `config` variable
    with open(config_file_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # Don't remove this as will help you doing some basic checks on config
    # content
    validate_config(config)
    return config

def get_class_names(config):
    return sorted(os.listdir(os.path.join(config["data"]["directory"])))

def walkdir(folder):
    for dirpath, _, files in os.walk(folder):
        for filename in files:
            yield (dirpath, filename)

#predicts car no_car label and creates a csv per folder with predictions for all images inside
def predict_from_folder_batch(folder, input_size, class_names):
    _batch_size = 32
    model = MobilenetV2.create_model('../weights_for_car_nocar_classifier/model.18-0.0782-0.9802.h5')
    for root, dirs, files in tqdm(os.walk(folder, topdown=False)): 
        #checks if csv exists and predictions are done for the folder. Like a resume function
        if 'car_nocar_class.csv' not in files:
            predictions, labels, paths = [], [], []
            df = pd.DataFrame(columns=['path', 'label', 'score', 'detectron'])
            for idx in range(0, len(files), _batch_size):
                batch_imgs = []
                for name in files[idx : idx + _batch_size]:
                    if name.endswith('jpg'):
                        path = os.path.join(root, name)
                        paths = np.append(paths, path)
                        img = tf.keras.utils.load_img(os.path.join(root, name), target_size=input_size)
                        img_array = tf.keras.utils.img_to_array(img)
                        batch_imgs.append(img_array)
                # This is a np.array of shape 32x2. With the probabilities of being auto/no_auto for each image.
                batch_preds = model.predict(np.array(batch_imgs), batch_size=_batch_size) 

                # List of length 32 with the predicted class for each image in the batch.
                batch_labels = [class_names[l_idx] for l_idx in batch_preds.argmax(axis=1)]

                # List with predicted classes fro the entire directory
                labels.extend(batch_labels)

                # This way we get the max probability for each row in the batch_preds array
                batch_scores = np.amax(batch_preds, axis=1)
                predictions.extend(batch_scores)

            df['score'] = predictions
            df['path'] = paths
            df['label'] = labels
            df.to_csv(os.path.join(root,"car_nocar_class.csv"))