import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pauca\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

card = cv2.imread(r"data\prismatic-evolutions\sv8-5_en_161_std.jpg")
name_region = card[30:100, 140:430]
number_region = card[960:1000, 110:210]

# processes a region
def process_region(region):
    # Convert to grayscale
    grey = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    
    # Apply a light Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(grey, (3, 3), 0)

    # Apply adaptive thresholding (light)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return thresh

name_processed = process_region(name_region)
number_processed = process_region(number_region)

# Extract text from the processed regions
name_text = pytesseract.image_to_string(name_processed, config="--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/")
number_text = pytesseract.image_to_string(number_processed, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/")

print("Name: ", name_text)
print("Number: ", number_text)

# Display the processed images
cv2.imshow("Name Region Processed", name_processed)
cv2.imshow("Number Region Processed", number_processed)
cv2.waitKey(0)
cv2.destroyAllWindows()