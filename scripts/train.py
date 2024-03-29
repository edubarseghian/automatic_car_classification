"""
This script will be used for training our CNN. The only input argument it
should receive is the path to our configuration file in which we define all
the experiment settings like dataset, model output folder, epochs,
learning rate, data augmentation, etc.
"""
import argparse
import tensorflow as tf
from tensorflow import keras
from models import resnet_50, MobilenetV2
from utils import utils

# Prevent tensorflow to allocate the entire GPU
# https://www.tensorflow.org/api_docs/python/tf/config/experimental/set_memory_growth
physical_devices = tf.config.list_physical_devices("GPU")
try:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass

# Supported optimizer algorithms
OPTIMIZERS = {
    "adam": keras.optimizers.Adam,
    "sgd": keras.optimizers.SGD,
}


# Supported callbacks
CALLBACKS = {
    "model_checkpoint": keras.callbacks.ModelCheckpoint,
    "tensor_board": keras.callbacks.TensorBoard,
    "early_stopping": keras.callbacks.EarlyStopping,
}


def parse_args():
    """
    Use argparse to get the input parameters for training the model.
    """
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "config_file",
        type=str,
        help="Full path to experiment configuration file.",
    )

    args = parser.parse_args()

    return args


def parse_optimizer(config):
    """
    Get experiment settings for optimizer algorithm.

    Parameters
    ----------
    config : str
        Experiment settings.
    """
    opt_name, opt_params = list(config["compile"]["optimizer"].items())[0]
    optimizer = OPTIMIZERS[opt_name](**opt_params)

    del config["compile"]["optimizer"]

    return optimizer


def parse_callbacks(config):
    """
    Add Keras callbacks based on experiment settings.

    Parameters
    ----------
    config : str
        Experiment settings.
    """
    callbacks = []
    if "callbacks" in config["fit"]:
        for callbk_name, callbk_params in config["fit"]["callbacks"].items():
            callbacks.append(CALLBACKS[callbk_name](**callbk_params))

        del config["fit"]["callbacks"]

    return callbacks


def main(config_file):
    config = utils.load_config(config_file)
    class_names = utils.get_class_names(config)
    print(len(class_names))
    if len(class_names) != config["model"]["classes"]:
        raise ValueError(
            "The number classes between your dataset and your model"
            "doen't match."
        )

    train_ds = keras.preprocessing.image_dataset_from_directory(
        subset="training",
        class_names=class_names,
        seed=config["seed"],
        **config["data"],
    )
    val_ds = keras.preprocessing.image_dataset_from_directory(
        subset="validation",
        class_names=class_names,
        seed=config["seed"],
        **config["data"],
    )

    #Es necesario?
    # AUTOTUNE = tf.data.AUTOTUNE
    # train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    # val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Creates a Resnet50 model for finetuning
    cnn_model = MobilenetV2.create_model(**config["model"])
    print(cnn_model.summary())

    # Compile model, prepare for training
    optimizer = parse_optimizer(config)
    cnn_model.compile(
        optimizer=optimizer,
        **config["compile"],
    )

    # Start training!
    callbacks = parse_callbacks(config)
    cnn_model.fit(
        train_ds, validation_data=val_ds, callbacks=callbacks, **config["fit"]
    )


if __name__ == "__main__":
    args = parse_args()
    main(args.config_file)
