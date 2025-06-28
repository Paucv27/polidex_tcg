import easyocr
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from pprint import pprint

# IMPORT ALL IMAGES FROM DATASET ----------------------------

images = glob('.\\data\\prismatic-evolutions\\*')

# GET TEST IMAGE --------------------------------------------

test_path = images[161]
test_filename = images[161].split('\\')[-1]

img = cv2.imread(test_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print('Filepath: ',test_path)
print('Filename: ',test_filename)

# PRE-PROCESS SECTIONS --------------------------------------

name_section = img[32:90, 134:500].copy()
name_section = cv2.resize(name_section, (name_section.shape[1]*2, name_section.shape[0]*2), interpolation=cv2.INTER_CUBIC)

number_section = img[960:1000, 115:205].copy()
number_section = cv2.resize(number_section, (number_section.shape[1]*5, number_section.shape[0]*5), interpolation=cv2.INTER_CUBIC)
number_section = cv2.GaussianBlur(number_section, (3,3), 0)

# GET RESULTS FROM EASYOCR -----------------------------------

reader = easyocr.Reader(['en'], gpu=False)

full_results = reader.readtext(img)
name_results = reader.readtext(name_section)
number_results = reader.readtext(number_section)

# SHOW DATAFRAME FOR BBOXs -----------------------------------

full_df = pd.DataFrame(full_results, columns=['BBOX','TEXT','CONF'])
name_df = pd.DataFrame(name_results, columns=['BBOX','TEXT','CONF'])
number_df = pd.DataFrame(number_results, columns=['BBOX','TEXT','CONF'])

print(full_df)
print(name_df)
print(number_df)

# DRAW BBOXs -------------------------------------------------

font = cv2.FONT_HERSHEY_SIMPLEX

for result in full_results:

    top_left = tuple(int(coord) for coord in result[0][0])
    bottom_right = tuple(int(coord) for coord in result[0][2])
    text = result[1]

    img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 5)
    img = cv2.putText(img, text, top_left, font, .5, (255,255,255), 2, cv2.LINE_AA)

fig, axs = plt.subplots(1,3, figsize=(15,5))

axs[0].imshow(img)
axs[0].set_title('Full')

axs[1].imshow(name_section)
axs[1].set_title('Name')

axs[2].imshow(number_section)
axs[2].set_title('Number')

plt.show()
