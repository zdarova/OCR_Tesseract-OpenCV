
import cv2
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import *
import csv
import re
import numpy as np
import argparse
import glob
import datetime
import pytz

# def auto_canny(image, sigma=0.33):
#     # compute the median of the single channel pixel intensities
#     v = np.median(image)
#
#     # apply automatic Canny edge detection using the computed median
#     lower = int(max(0, (1.0 - sigma) * v))
#     upper = int(min(255, (1.0 + sigma) * v))
#     edged = cv2.Canny(image, lower, upper)
#
#     # return the edged image
#     return edged

# image_file = 'page.tif'
# image_file = 'table_text.png'
image_file = 'ODL2.png'
img = Image.open(image_file).convert('L')
img_array=cv2.imread(image_file)
# cv2.imshow("Image", img_array)
# load the image, convert it to grayscale, and blur it slightly
# img = cv2.imread(image_file)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # brur it slightly
# blurred = cv2.GaussianBlur(gray, (3, 3), 0)
#
# # apply Canny edge detection using a wide threshold, tight
# # threshold, and automatically determined threshold
# wide = cv2.Canny(blurred, 10, 200)
# tight = cv2.Canny(blurred, 225, 250)
# auto = auto_canny(blurred)
#
# # show the images
# cv2.imshow("Original", image)
# cv2.imshow("Edges", np.hstack([wide, tight, auto]))
# cv2.waitKey(0)
crop_region_1 = img.crop((20, 60, 380, 110))
Image._show(crop_region_1)
#crop_region_1 = img_array[200:400, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400
# cv2.imshow("cropped", crop_region_1)
# cv2.waitKey(0)

text_region_1 = pytesseract.image_to_string(crop_region_1, 'ita', False, None)
# text = pytesseract.image_file_to_string(image_file)
# text = pytesseract.image_file_to_string(image_file, graceful_errors=True)
print "ODL:"
print text_region_1

crop_region_2 = img.crop((500, 60, 700, 105))
Image._show(crop_region_2)
text_region_2 = pytesseract.image_to_string(crop_region_2, 'ita', False, None)
print "Data:"
print text_region_2

# Descrizione ODL
#crop_region_3 = img.crop((131, 120, 250, 141))
#crop_region_3.save('crop_region_3.png','png')
crop_region_3_new = cv2.imread('crop_region_3.png')

crop_region_3_new = cv2.resize(crop_region_3_new, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
# crop_region_3_new = cv2.imread('ODL1.jpg')
# crop_region_3_new = cv2.imread('table_text.png')
crop_region_3_new = cv2.cvtColor(crop_region_3_new, cv2.COLOR_BGR2GRAY)
# crop_region_3_new = cv2.GaussianBlur(crop_region_3_new, (5, 5), 0)
# crop_region_3_new = cv2.Canny(crop_region_3_new,75,200)
#Image._show(crop_region_3)
# cv2.startWindowThread()
# cv2.namedWindow("reg3", cv2.WINDOW_NORMAL)
cv2.imshow("Descrizione", crop_region_3_new)
cv2.waitKey(0)
cv2.destroyAllWindows()
# crop_region_3 = crop_region_3.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(crop_region_3)
# crop_region_3 = enhancer.enhance(2)
# crop_region_3 = crop_region_3.convert('1')
crop_region_3_new_pil = Image.fromarray(crop_region_3_new)
text_region_3 = pytesseract.image_to_string(crop_region_3_new_pil, 'ita', False, None)
print "Descrizione ODL:"
print text_region_3

# write to csv
odl = re.search(r'\d+', text_region_1).group()

data=re.search('([0-9]{2}\\.[0-9]{2}\\.[0-9]{4})', text_region_2).group(0)

print data
# print datetime.datetime.strptime(pre_data, '%d.%m.%Y')
# match_date = re.search(r'\\d{2}.\d{2}.d{4}', text_region_2)
# data = datetime.datetime.strptime(match_date.group(), '%m.%d.%Y').date()
descrizione = text_region_3
# raw_text = raw_input(text)
# raw_text = raw_text.replace('\n', ' ').replace('\r', '')
#
# ''' spamwriter.writerow(['No'] , ['ODL']) '''
index = 1
with open('odl_list.csv', 'a') as csvfile:
     linewriter = csv.writer(csvfile, delimiter=';')
     data = [index, odl, data, descrizione]
     linewriter.writerow(data)
     csvfile.close()
