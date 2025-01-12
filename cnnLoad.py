import tensorflow as tf
import numpy as np
import pickle
import keras


    def loadModel(self):
        # Variables required for loading the model
        # Sets the image parameters and batch size
        self.imageHeight = 280
        self.imageWidth = 280
        self.batchSize = 32
        # Loads the model
        self.model = keras.models.load_model(" -->MODEL NAME<-- .keras")
        # Fetches the pickled names file from earlier
        self.namesFile = open("PATH HERE/classNames.pkl", "rb")
        self.classNames = pickle.load(self.namesFile)
        # Closes the file
        self.namesFile.close()

        # loads the image
        self.imagePath = "PATH HERE/temp.jpg"
        self.image = tf.keras.utils.load_img(self.imagePath, target_size=(self.imageHeight, self.imageWidth))
        # change the image into an array so that it can be analysed
        self.imageArray = tf.keras.utils.img_to_array(self.image)
        # Packs it to ensure it is of the required size
        self.imageArray = tf.expand_dims(self.imageArray, 0)
        # uses the model to predict the values of the image
        self.values = self.model.predict(self.imageArray)
