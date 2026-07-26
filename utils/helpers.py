# utils/helpers.py

import numpy as np
from PIL import Image
import tensorflow as tf


# --------------------------------------------------
# Image Preprocessing
# --------------------------------------------------

def preprocess_image(image, target_size=(224, 224)):
    """
    Convert uploaded image into model input.

    Parameters
    ----------
    image : PIL.Image

    target_size : tuple

    Returns
    -------
    numpy.ndarray
        Shape (1,224,224,3)
    """

    image = image.convert("RGB")

    image = image.resize(target_size)

    image = np.array(image, dtype=np.float32)

    image /= 255.0

    image = np.expand_dims(image, axis=0)

    return image


# --------------------------------------------------
# Load Model
# --------------------------------------------------

def load_model(model_path=r"C:\Users\shai\Desktop\ml_projects\GIT\DEEP_LEARNING\X_ray CNN\pneumonia_model.keras"):
    """
    Load trained Keras model.
    """

    return tf.keras.models.load_model(model_path)


# --------------------------------------------------
# Prediction
# --------------------------------------------------

def predict(model, processed_image):
    """
    Predict image class.

    Returns
    -------
    dict
    """

    prediction = model.predict(processed_image, verbose=0)

    pneumonia_probability = float(prediction[0][0])

    normal_probability = 1 - pneumonia_probability

    if pneumonia_probability >= 0.5:

        label = "PNEUMONIA"

        confidence = pneumonia_probability

    else:

        label = "NORMAL"

        confidence = normal_probability

    return {

        "prediction": label,

        "confidence": confidence,

        "normal_probability": normal_probability,

        "pneumonia_probability": pneumonia_probability

    }


# --------------------------------------------------
# Risk Level
# --------------------------------------------------

def get_risk_level(probability):
    """
    Determine pneumonia risk based on pneumonia probability.
    """

    if probability >= 0.80:
        return "High"

    elif probability >= 0.50:
        return "Moderate"

    elif probability >= 0.20:
        return "Low"

    else:
        return "Minimal"

# --------------------------------------------------
# Result Color
# --------------------------------------------------

def result_color(label):
    """
    Return UI color for prediction.
    """

    if label == "PNEUMONIA":
        return "#ef4444"

    return "#22c55e"


# --------------------------------------------------
# Probability Percentage
# --------------------------------------------------

def to_percentage(value):
    """
    Convert probability to percentage.
    """

    return round(value * 100, 2)


# --------------------------------------------------
# AI Recommendation
# --------------------------------------------------

def recommendation(label):
    """
    Generate recommendation based on prediction.
    """

    if label == "PNEUMONIA":

        return (
            "The model detected features associated with pneumonia. "
            "Please consult a qualified physician or radiologist "
            "for further evaluation."
        )

    return (
        "The model did not detect features associated with pneumonia. "
        "Clinical correlation is still recommended."
    )


# --------------------------------------------------
# Model Information
# --------------------------------------------------

def model_information():
    """
    Return information about the AI model.
    """

    return {

        "Model": "Convolutional Neural Network",

        "Framework": "TensorFlow / Keras",

        "Input Size": "224 × 224 × 3",

        "Output Classes": [
            "NORMAL",
            "PNEUMONIA"
        ]
    }