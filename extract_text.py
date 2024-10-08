import cv2
import easyocr

class TextExtractor:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extract_text_from_image(self, image):
        img = cv2.imread(image)
        res = self.reader.readtext(img)
        return "\n".join([text for (bbox, text, prob) in res])
    

if __name__ == "__main__":
    image_file = "./images/snipped_image.png"
    text_extractor = TextExtractor()
    res =  text_extractor.extract_text_from_image(image_file)
    print(res)
