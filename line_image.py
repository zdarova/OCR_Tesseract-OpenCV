#!/usr/bin/env python

import urllib

from PIL import Image, ImageDraw
import pytesseract
from resizeimage import resizeimage
import os
import sys
sys.path.append('/opt/ros/hydro/lib/python2.7/dist-packages')
import cv2
import numpy as np

src_path = "~/ocr/"


def get_string(img_path):

    # Read image with opencv
    img = cv2.imread(img_path)
    print 'img_path: %s ' % (img_path)
    # Convert to gray
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    cv2.imwrite(src_path + "removed_noise.png", img)

    # Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "thres.png", img)
    print 'img_path: %s ' % (img_path)
    
    # draw = ImageDraw.Draw(img)
    # c_info = props_for_contours(contours, edges)
    # for c in c_info:
    #     this_crop = c['x1'], c['y1'], c['x2'], c['y2']
    #     draw.rectangle(this_crop, outline='blue')
    # draw.rectangle(crop, outline='red')
    # im.save(out_path)
    # draw.text((50, 50), path, fill='red')
    # orig_im.save(out_path)
    # img.show()
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))

    # os.remove(temp)
    return result

print '--- Start recognize text from image ---'
print get_string(src_path + "2.png")

print "------ Done -------"
