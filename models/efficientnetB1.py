from utils.data_aug import create_data_aug_layer

from utils import utils
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Input, Activation, add, Add, Dropout, BatchNormalization, GlobalAveragePooling2D
from keras import layers


def create_model(
    weights: str = None,
    input_shape: tuple = None,
    dropout_rate: float = None,
    data_aug_layer: dict = None,
    classes: int = None,
):
    if weights == "imagenet":
        input = layers.Input(shape=input_shape, dtype=tf.float32)
        if data_aug_layer:
            x = create_data_aug_layer(data_aug_layer)(input)
        else:
            x = input
        x = keras.applications.efficientnet.preprocess_input(x)

        base_model = tf.keras.applications.EfficientNetB1(
            include_top=False,
            weights=weights,
            pooling='avg',
        )

        # base_model = keras.applications.resnet50.ResNet50(
        #     weights=weights,  # Load weights pre-trained on ImageNet.
        #     input_shape=input_shape,
        #     include_top=False,
        #     pooling='avg',
        # )

        base_model.trainable = False
        x = base_model(x, training=False)
        dropout = layers.Dropout(dropout_rate)(x)
        outputs = keras.layers.Dense(classes, activation='softmax')(dropout)
        model = keras.Model(input, outputs)
    else:
        model = keras.models.load_model(str(weights))
        model.trainable = True

        for layer in model.layers[2].layers:
            if isinstance(layer, layers.BatchNormalization):
                layer.trainable = False
        print("----------------------------------------------------------")
        print("----------------------------------------------------------")
        print("----------------------------------------------------------")
        for lnum, layer in enumerate(model.layers[2].layers[-30:]):

            print(lnum, layer.name, layer.trainable,
                  layer.dtype, layer.dtype_policy)

    return model
