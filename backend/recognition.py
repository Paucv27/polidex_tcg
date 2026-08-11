import re
import cv2
import easyocr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test():
    logger.info("Running test function...")

    # IMPORT ALL IMAGES FROM DATASET ----------------------------

    images = glob('..\\data\\prismatic-evolutions\\*')

    # GET TEST IMAGE --------------------------------------------

    test_image_cardnum = 161

    test_path = images[test_image_cardnum - 1] #bcs 0-index
    test_filename = images[test_image_cardnum - 1].split('\\')[-1]

    img = cv2.imread(test_path)
    img = cv2.resize(img, (733, 1024), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    logger.info('Filepath: %s', test_path)
    logger.info('Filename: %s', test_filename)

    # SECTIONS ---------------------------------------------------

    name_resize_factor = 2
    number_resize_factor = 4

    name_section = img[0:140, 0:500].copy()
    name_section = cv2.resize(name_section, (500*name_resize_factor, 140*name_resize_factor), interpolation=cv2.INTER_CUBIC)
    #name_section = cv2.cvtColor(name_section, cv2.COLOR_RGB2GRAY)
    _, name_section = cv2.threshold(name_section, 40, 255, cv2.THRESH_BINARY)
    name_section = cv2.medianBlur(name_section, 3)
    

    number_section = img[960:1000, 115:205].copy()
    number_section = cv2.resize(number_section, (90*number_resize_factor, 40*number_resize_factor), interpolation=cv2.INTER_CUBIC)
    #number_section = cv2.cvtColor(number_section, cv2.COLOR_RGB2GRAY)
    _, number_section = cv2.threshold(number_section, 40, 255, cv2.THRESH_BINARY)

    # GET RESULTS FROM EASYOCR -----------------------------------

    reader = easyocr.Reader(['en'], gpu=False)

    name_results = reader.readtext(name_section)
    number_results = reader.readtext(number_section)

    # SHOW DATAFRAME FOR BBOXs -----------------------------------

    name_df = pd.DataFrame(name_results, columns=['BBOX','TEXT','CONF'])
    number_df = pd.DataFrame(number_results, columns=['BBOX','TEXT','CONF'])

    #print(full_df)
    logger.info("Name DF:\n%s\n", name_df)
    logger.info("Number DF:\n%s\n", number_df)

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

    logger.info("Clean Name: %s", clean_name)
    logger.info("Clean Number: %s", clean_number)

    plt.show()


def process_card(card_file):
    """
    Process a card image file and extract name and number information.

    Args:
        card_file: An image object representing the card image (accepts jpg, png, ...)
    Returns:
        A tuple containing the extracted name and number as strings.
    """
    logger.info("Processing card...")
    
    file = card_file.read()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR_RGB)
    img = cv2.resize(img, (733, 1024), interpolation=cv2.INTER_CUBIC)

    name_resize_factor = 2
    number_resize_factor = 4

    name_section = img[0:140, 0:500].copy()
    name_section = cv2.resize(name_section, (500*name_resize_factor, 140*name_resize_factor), interpolation=cv2.INTER_CUBIC)
    #name_section = cv2.cvtColor(name_section, cv2.COLOR_RGB2GRAY)
    _, name_section = cv2.threshold(name_section, 40, 255, cv2.THRESH_BINARY)
    name_section = cv2.medianBlur(name_section, 3)
    
    # NOTE: Number section is more important than name, might not even need name for searching the specific card
    number_section = img[960:1000, 115:205].copy()
    number_section = cv2.resize(number_section, (90*number_resize_factor, 40*number_resize_factor), interpolation=cv2.INTER_CUBIC)
    #number_section = cv2.cvtColor(number_section, cv2.COLOR_RGB2GRAY)
    _, number_section = cv2.threshold(number_section, 40, 255, cv2.THRESH_BINARY)

    reader = easyocr.Reader(['en'], gpu=True)

    name_results = reader.readtext(name_section)
    number_results = reader.readtext(number_section)

    clean_name = process_name(name_results)
    clean_number = process_number(number_results)
    logger.info("Processed Name: %s | Processed Number: %s", clean_name, clean_number)
    
    logger.info("DONE PROCESSING")

    return clean_name, clean_number


def process_name(name_results):
    logger.info("Processing name results...")
    logger.info("^^^ This only processes the first result, as this is most likely to be the name")

    top_result = name_results[0][1]
    text = re.sub(r'[^a-zA-Z ]', '', top_result)

    return text


def process_number(number_results):
    logger.info("Processing number results...")
    logger.info("^^^ This processes all results, as the number might be split across multiple detections")
    text = ''

    for result in number_results:

        filtered = re.sub(r'[^0-9/]', '', result[1])
        text += filtered+' '

    # hopes and prayers in case the OCR misreads the number and doesnt include a slash
    if '/' not in text:
        text = text[:3] + '/' + text[3:]

    return text


if __name__ == "__main__":

    test()
