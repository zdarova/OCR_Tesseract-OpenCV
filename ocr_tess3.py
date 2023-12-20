
import cv2
from PIL import Image
from pytesseract import *
import csv
import re
import numpy as np
import argparse
import glob


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

# image_file = 'page.tif'
image_file = 'table_text.png'
# im = Image.open(image_file)
# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(image_file)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# brur it slightly
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# apply Canny edge detection using a wide threshold, tight
# threshold, and automatically determined threshold
wide = cv2.Canny(blurred, 10, 200)
tight = cv2.Canny(blurred, 225, 250)
auto = auto_canny(blurred)

# show the images
cv2.imshow("Original", image)
cv2.imshow("Edges", np.hstack([wide, tight, auto]))
cv2.waitKey(0)

text = pytesseract.image_to_string(image)
# text = pytesseract.image_file_to_string(image_file)
# text = pytesseract.image_file_to_string(image_file, graceful_errors=True)
print "=====output=======\n"
print text

odl = re.search(r'\d+', text).group()
raw_text = raw_input(text)
raw_text = raw_text.replace('\n', ' ').replace('\r', '')

''' spamwriter.writerow(['No'] , ['ODL']) '''
index = '1'
with open('odl_list.csv', 'wb') as csvfile:
    linewriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    linewriter.writerow(index, odl)
