import cv2
import easyocr

def extract_text_from_image(image_path):

    """
    input: path to image file
    output: the test extracted from the image separated by '/n'
    """

    reader = easyocr.Reader(['en'])
    img = cv2.imread(image_path)
    result = reader.readtext(image=img)
    return "/n".join([text for (bbox, text, prob) in result])