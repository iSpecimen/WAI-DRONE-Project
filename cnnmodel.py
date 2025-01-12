import tensorflow as tf
import pathlib
import keras
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pickle


class AIModel:
    def __init__(self):
        # Defining the image and batch parameters and setting the directory for the dataset
        self.imageHeight = 280
        self.imageWidth = 280
        self.batchSize = 32

        self.datasetPath = "file:///  -->PATH GOES HERE<--"
        self.datasetDirectory = keras.utils.get_file("  -->DATASET HERE<--  .rar", origin=self.datasetPath, extract=True)
        self.datasetDirectory = pathlib.Path(self.datasetDirectory).with_suffix('')

        # Defining the training dataset parameters
        self.trainingDataset = keras.utils.image_dataset_from_directory(self.datasetDirectory,
                                                                           subset="training",
                                                                           batch_size=self.batchSize,
                                                                           validation_split=0.2,# 80/20: training/validation split usually used but can change obv
                                                                           seed=389564, 
                                                                           image_size=(self.imageHeight, self.imageWidth))
        # Defining the validation dataset parameters
        self.validationDataset = keras.utils.image_dataset_from_directory(self.datasetDirectory,
                                                                             subset="validation",
                                                                             batch_size=self.batchSize,
                                                                             validation_split=0.2,
                                                                             seed=195639,
                                                                             image_size=(self.imageHeight, self.imageWidth))
        self.classNames = self.trainingDataset.class_names
        self.numClasses = len(self.classNames)

        # creates the file where the class names will be stored
        self.namesFile = open("classNames.pkl", "wb")
        # writes the class names into the file
        pickle.dump(self.classNames, self.namesFile)
        # closes the file
        self.namesFile.close()

        self.autotune = tf.data.AUTOTUNE
###This part is the model itself, some things here are for optimisaiton like dropout and the actual amount of layers, what they do and types can be changed to make it recognise better.####
###Used with 2 ~600 image datasets of people and no people and icl i think it needed to be bigger, cnns take pretty humungous datasets to train well
        self.model = Sequential([
            layers.Rescaling(1. / 255, input_shape=(self.imageHeight, self.imageWidth, 3)),
            layers.Conv2D(filters=16, kernel_size=3, strides=(1, 1), padding="same", activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.1),

            layers.Conv2D(filters=32, kernel_size=3, strides=(1, 1), padding="same", activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.1),

            layers.Conv2D(filters=64, kernel_size=3, strides=(1, 1), padding="same", activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.1),

            layers.Conv2D(filters=128, kernel_size=3, strides=(1, 1), padding="same", activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.1),

            layers.Flatten(),
            layers.Dense(units=512, activation="sigmoid"),
            layers.Dense(self.numClasses)
        ])

## Can change this, more may/may not be good == takes longer and may lead to overfitting, used earlyStop to get this value, different between models and datasets
        self.epochs = 10


    def train(self):
        # Model compilation
        self.model.compile(optimizer="adam",
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                           metrics=["accuracy"]) ## can add a bunch of optimisers here to make it train faster/better

        #Callback to determine best epochs num
        earlyStop = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            mode="min",
            baseline=None,
            restore_best_weights=True,
            start_from_epoch=0
        )


        # Model training
        self.model.fit(
            self.trainingDataset,
            validation_data=self.validationDataset,
            epochs=self.epochs,
           # callbacks=[earlyStop]
        )

    def summary(self):
        self.model.summary()


model = AIModel()
model.train()

# Saves the model --- the file for how to use the compiled model should also be uploaded somewhere
model.model.save("CNN model.keras")

