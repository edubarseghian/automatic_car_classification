from utils.data_aug import create_data_aug_layer

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


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
        x = keras.applications.resnet50.preprocess_input(x)

        base_model = tf.keras.applications.ResNet152V2(
            include_top=False,
            weights=weights,
            pooling='avg',
            input_shape=input_shape,
        )

        base_model.trainable = False
        x = base_model(x, training=False)
        dropout = layers.Dropout(dropout_rate)(x)
        outputs = keras.layers.Dense(classes, activation='softmax')(dropout)
        model = keras.Model(input, outputs)
    else:
        model = keras.models.load_model(str(weights))
        model.trainable = True
    return model
