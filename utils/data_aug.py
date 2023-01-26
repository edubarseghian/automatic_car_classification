from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

def create_data_aug_layer(data_aug_layer):
    """
    Use this function to parse the data augmentation methods for the
    experiment and create the corresponding layers.

    It will be mandatory to support at least the following three data
    augmentation methods (you can add more if you want):
        - `random_flip`: keras.layers.RandomFlip()
        - `random_rotation`: keras.layers.RandomRotation()
        - `random_zoom`: keras.layers.RandomZoom()

    See https://tensorflow.org/tutorials/images/data_augmentation.

    Parameters
    ----------
    data_aug_layer : dict
        Data augmentation settings coming from the experiment YAML config
        file.

    Returns
    -------
    data_augmentation : keras.Sequential
        Sequential model having the data augmentation layers inside.
    """
    # Parse config and create layers
    # You can use as a guide on how to pass config parameters to keras
    # looking at the code in `scripts/train.py`
    # TODO
    # Append the data augmentation layers on this list
    data_aug_layers = []
    if 'random_flip' in data_aug_layer:
        data_aug_layers.append(layers.RandomFlip(mode=data_aug_layer['random_flip']['mode'],name=data_aug_layer['random_flip']['name']))
    if 'random_rotation' in data_aug_layer:
        data_aug_layers.append(layers.RandomRotation(factor=data_aug_layer['random_rotation']['factor'],name=data_aug_layer['random_rotation']['name']))
    if 'random_zoom' in data_aug_layer:
        data_aug_layers.append(layers.RandomZoom(height_factor=data_aug_layer['random_zoom']['height_factor'],width_factor=data_aug_layer['random_zoom']['width_factor'],name=data_aug_layer['random_zoom']['name']))
    # Return a keras.Sequential model having the the new layers created
    # Assign to `data_augmentation` variable
    # TODO
    data_augmentation = Sequential(data_aug_layers)
    return data_augmentation
