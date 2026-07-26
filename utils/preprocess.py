import numpy as np
from PIL import Image


IMG_SIZE = (224, 224)


def preprocess_image(image: Image.Image):
    """
    Preprocess uploaded image for CNN prediction.

    Args:
        image (PIL.Image): Uploaded X-ray image

    Returns:
        numpy.ndarray: Shape (1, 224, 224, 3)
    """

    # Convert grayscale/RGBA images to RGB
    image = image.convert("RGB")

    # Resize
    image = image.resize(IMG_SIZE)

    # Convert to NumPy array
    image = np.array(image, dtype=np.float32)

    # Normalize
    image /= 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image