import re
import cv2
import easyocr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

def test():

    # IMPORT ALL IMAGES FROM DATASET ----------------------------

    images = glob('.\\data\\prismatic-evolutions\\*')

    # GET TEST IMAGE --------------------------------------------

    test_path = images[161]
    test_filename = images[161].split('\\')[-1]

    img = cv2.imread(test_path)
    img = cv2.resize(img, (img.shape[1]*3, img.shape[0]*3), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print('Filepath: ',test_path)
    print('Filename: ',test_filename)

    # SECTIONS ---------------------------------------------------

    name_section = img[0:140*3, 0:500*3].copy()
    name_section = cv2.cvtColor(name_section, cv2.COLOR_RGB2GRAY)
    _, name_section = cv2.threshold(name_section, 40, 255, cv2.THRESH_BINARY_INV)

    number_section = img[960*3:1000*3, 115*3:205*3].copy()
    number_section = cv2.cvtColor(number_section, cv2.COLOR_RGB2GRAY)
    _, number_section = cv2.threshold(number_section, 30, 255, cv2.THRESH_BINARY_INV)

    # GET RESULTS FROM EASYOCR -----------------------------------

    reader = easyocr.Reader(['en'], gpu=False)

    name_results = reader.readtext(name_section)
    number_results = reader.readtext(number_section)

    # SHOW DATAFRAME FOR BBOXs -----------------------------------

    name_df = pd.DataFrame(name_results, columns=['BBOX','TEXT','CONF'])
    number_df = pd.DataFrame(number_results, columns=['BBOX','TEXT','CONF'])

    #print(full_df)
    print(name_df)
    print(number_df)

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

    print(clean_name,clean_number)

    plt.show()


def process_card(card_file):
    
    file = card_file.read()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR_RGB)
    img = cv2.resize(img, (733*3, 1024*3), interpolation=cv2.INTER_CUBIC)

    name_section = img[0:140*3, 0:500*3].copy()
    name_section = cv2.cvtColor(name_section, cv2.COLOR_RGB2GRAY)
    _, name_section = cv2.threshold(name_section, 40, 255, cv2.THRESH_BINARY_INV)

    number_section = img[960*3:1000*3, 115*3:205*3].copy()
    number_section = cv2.cvtColor(number_section, cv2.COLOR_RGB2GRAY)
    _, number_section = cv2.threshold(number_section, 30, 255, cv2.THRESH_BINARY_INV)

    reader = easyocr.Reader(['en'], gpu=True)

    name_results = reader.readtext(name_section)
    number_results = reader.readtext(number_section)

    clean_name = process_name(name_results)
    clean_number = process_number(number_results)
    
    print("DONE PROCESSING")

    return clean_name, clean_number


def process_name(name_results):

    text = ''
    results_popped = 0

    for result in name_results:

        text = text+result[1]+' '
        results_popped += 1

        if results_popped == 1:
            break
    
    text = re.sub(r'[^a-zA-Z ]', '', text)

    return text


def process_number(number_results):

    text = ''

    for result in number_results:

        filtered = re.sub(r'[^0-9/]', '', result[1])
        text += filtered+' '

    if '/' not in text:
        text = text[:3] + '/' + text[3:]

    return text


if __name__ == "__main__":

    test()
