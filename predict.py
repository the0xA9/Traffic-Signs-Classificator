# import the necessary packages
# from tensorflow.keras.models import load_model
from skimage import transform
from skimage import exposure
from skimage import io
import numpy as np

def makePrediction(model):

    # load the label names
    dictionary = open("signnames.csv").read().strip().split("\n")[1:]
    # labelNames = [l.split(",")[1] for l in labelNames]

    # load the image, resize it to 32x32 pixels, and then apply
    # Contrast Limited Adaptive Histogram Equalization (CLAHE),
    # just like we did during training
    image = io.imread("image/image.jpg")
    image = transform.resize(image, (32, 32))
    image = exposure.equalize_adapthist(image, clip_limit=0.1)

    # preprocess the image by scaling it to the range [0, 1]
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    # make predictions using the traffic sign recognizer CNN
    prediction = model.predict(image)
    index = prediction.argmax(axis=1)[0]

    detectedSign = dictionary[index]
    # print(detectedSign)
    return (detectedSign)