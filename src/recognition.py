import re
import cv2
import easyocr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

def test():

    # IMPORT ALL IMAGES FROM DATASET ----------------------------
    
    DATASETS = { 
                "prismatic": ".\\data\\prismatic-evolutions\\*",
                "surging_sparks": ".\\data\\surging-sparks\\*"
                }
    

    images = glob(DATASETS['prismatic'])

    # GET TEST IMAGE --------------------------------------------
    
    CARD = 161

    # -1 here so that it actually matches the card number in the set
    TEST_PATH = images[CARD-1]
    TEST_FILENAME = images[CARD-1].split('\\')[-1]
    SCALE = 2

    img = cv2.imread(TEST_PATH)
    # resize the image to xSCALE size
    img = cv2.resize(img, (img.shape[1]*SCALE, img.shape[0]*SCALE), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    print('Filepath: ',TEST_PATH)
    print('Filename: ',TEST_FILENAME)

    # SECTIONS ---------------------------------------------------
    
    print(f"Img size: {img.size}")
    # dimensions will probs have to be adjusted once I start testing with real photos
    # same with preprocessing probably though
    name_section = img[0:140*SCALE, 0:500*SCALE].copy()
    name_section = cv2.cvtColor(name_section, cv2.COLOR_RGB2GRAY)
    _, name_section = cv2.threshold(name_section, 40, 255, cv2.THRESH_BINARY_INV)

    number_section = img[960*SCALE:1000*SCALE, 115*SCALE:205*SCALE].copy()
    number_section = cv2.cvtColor(number_section, cv2.COLOR_RGB2GRAY)
    _, number_section = cv2.threshold(number_section, 20, 255, cv2.THRESH_BINARY_INV)
    
    # PREPROCESSING ----------------------------------------------
    name_section = cv2.medianBlur(name_section, 5)
    number_section = cv2.dilate(number_section, (3,3))

    # GET RESULTS FROM EASYOCR -----------------------------------

    reader = easyocr.Reader(['en'])
    name_results = reader.readtext(name_section)
    number_results = reader.readtext(number_section)

    # SHOW DATAFRAME FOR BBOXs -----------------------------------

    name_df = pd.DataFrame(name_results, columns=['BBOX','TEXT','CONFIDENCE'])
    number_df = pd.DataFrame(number_results, columns=['BBOX','TEXT','CONFIDENCE'])

    print("\nNAME AREA READ:\n",name_df)
    print("\nNUMBER AREA READ:\n",number_df)

    # DRAW BBOXs -------------------------------------------------

    fig, axs = plt.subplots(1,3, figsize=(15,5))

    axs[0].imshow(img)
    axs[0].set_title('Full')

    axs[1].imshow(name_section, cmap='gray')
    axs[1].set_title('Name')

    axs[2].imshow(number_section, cmap='gray')
    axs[2].set_title('Number')

    clean_name = process_name(name_results)
    clean_number = process_number(number_results)

    print("\n",clean_name,clean_number)

    plt.show()


def process_card(card_file):
    """
    Reads card file from website upload, and processes the Name and Number regions separately
    to return a string like:
    - UmbreonEX 161/131

    Args:
        card_file (str): The unprocessed card image

    Returns:
        str: Name of card
        str: Number of card
    """
    
    SCALE = 2
    
    # read card image and convert to npimg so cv2 can process it
    # scale up for better OCR results (2 is preferred)
    file = card_file.read()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR_RGB)
    img = cv2.resize(img, (733*SCALE, 1024*SCALE), interpolation=cv2.INTER_CUBIC)

    name_section = img[0:140*SCALE, 0:500*SCALE].copy()
    name_section = cv2.cvtColor(name_section, cv2.COLOR_RGB2GRAY)
    _, name_section = cv2.threshold(name_section, 40, 255, cv2.THRESH_BINARY_INV)
    name_section = cv2.medianBlur(name_section, 5)

    number_section = img[960*SCALE:1000*SCALE, 115*SCALE:205*SCALE].copy()
    number_section = cv2.cvtColor(number_section, cv2.COLOR_RGB2GRAY)
    _, number_section = cv2.threshold(number_section, 20, 255, cv2.THRESH_BINARY_INV)
    number_section = cv2.dilate(number_section, (3,3))

    reader = easyocr.Reader(['en'])

    name_results = reader.readtext(name_section)
    number_results = reader.readtext(number_section)

    clean_name = process_name(name_results)
    clean_number = process_number(number_results)
    
    print("DONE PROCESSING")

    return clean_name, clean_number


def process_name(name_results):
    """
    Uses regex and replace to clean name input
    //
    For example:
    - ~Eevee£X: -> EeveeEX

    Args:
        name_results (str): The unprocessed name of the card

    Returns:
        str: Clean name of card
    """
    
    # low conf for now
    CONF = 0.4
    text = ''
    
    for result in name_results:
        if result[2] > CONF:
            text = result[1]
            break
    
    text = re.sub(r'[^a-zA-Z £€]', '', text)
    text = str.replace(text, "£", "E")
    text = str.replace(text, "€", "E")
    return text


def process_number(number_results):
    """
    Uses regex and replace to clean number input
    //
    For example:
    - 1b63:/A17l8. -> 163/178

    Args:
        number_results (str): The unprocessed number of the card

    Returns:
        str: Clean number of card, or '/'
    """
    
    CONF = 0.4
    text = ""
    
    for result in number_results:
        if result[2] > CONF:
            text = result[1]
            break

    text = re.sub(r'[^0-9/]', '', text)

    if '/' not in text:
        text = text[:3] + '/' + text[3:]

    return text


if __name__ == "__main__":
    # if not imported, run test func
    test()
