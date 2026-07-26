import tensorflow as tf

# -------------------------------
# Load Model Only Once
# -------------------------------

_model = None


def load_model(model_path="pneumonia_model.keras"):
    """
    Load the CNN model once and cache it.
    """
    global _model

    if _model is None:
        _model = tf.keras.models.load_model(model_path)

    return _model


# -------------------------------
# Prediction Function
# -------------------------------

def predict_image(image, model=None):
    """
    Predict Pneumonia / Normal.

    Parameters
    ----------
    image : np.ndarray
        Shape (1,224,224,3)

    model : keras model
        Optional

    Returns
    -------
    dict
    """

    if model is None:
        model = load_model()

    prediction = model.predict(image, verbose=0)

    pneumonia_probability = float(prediction[0][0])

    normal_probability = 1 - pneumonia_probability

    if pneumonia_probability >= 0.5:

        predicted_class = "PNEUMONIA"

        confidence = pneumonia_probability

    else:

        predicted_class = "NORMAL"

        confidence = normal_probability

    return {

        "prediction": predicted_class,

        "confidence": confidence,

        "normal_probability": normal_probability,

        "pneumonia_probability": pneumonia_probability

    }