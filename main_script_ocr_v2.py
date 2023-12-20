
import cv2
from wand.image import Image as Image2
from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import *
import csv
import re
import numpy as np
import argparse
import glob
import datetime
import pytz
import pandas as pd
import os
#from __future__ import print_function

def scan_pdf(pdf_file_name, output_dir, quality):
    pagine = 0
    with Image2(filename=pdf_file_name, resolution=quality) as img:
        pagine = len(img.sequence)
        print('pages = ', pagine)
        print('width =', img.width)
        print('height =', img.height)
        print('resolution = ', img.resolution)
        with img.convert('png') as converted:
            converted.compression_quality = 99
            output_file = output_dir + 'page.png'
            converted.save(filename = output_file)
            print "pdf convertito in png"
    return pagine

#image_file = 'ODL3.png'
def extract_text(image_file):
    error = "OK"
    # img = Image.open(image_file).convert('L')
    image_odl = cv2.imread(image_file)

    image_odl_array = cv2.resize(image_odl, None, fx=3, fy=3, interpolation = cv2.INTER_CUBIC)
    image_odl_array = cv2.cvtColor(image_odl_array, cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(image_odl_array)
    text_all = pytesseract.image_to_string(img, 'ita', False, None)
    # text = pytesseract.image_file_to_string(image_file)
    # text = pytesseract.image_file_to_string(image_file, graceful_errors=True)
    # print "ODL_doc:"
    # ok:
    # print text_all
    match_date = ""
    equipment = ""
    descrizione = ""

    for line in text_all.split("\n"):
        if "ordine di lavoro" in line:
            # print line
            try:
                data = re.search('([0-9]{2}\\.[0-9]{2}\\.[0-9]{4})', line).group(0)
            except:
                data = ""
            try:
                odl = re.search('([0-9]{12})', line).group(0)
            except:
                continue
            # match_date = re.search(r'\\d{2}.\d{2}.d{4}', line)
        if "escrizione:" in line:
            if descrizione == "":
                #print line
                # descrizione = re.search('escrizione:(.+?)', line)
                descrizione = line[line.index("escrizione:") + len("escrizione:"):]
    #            print descrizione
                continue
        if "Equipment" in line:
            # print line
            try:
                equipment = re.search('([0-9]{6})', line).group(0)
                # print equipment
                treno_veicolo = re.search('600(.+?)', equipment)
                if treno_veicolo:
                    veicolo = treno_veicolo.group(1)
                    treno = equipment[-2:]
                    # print "veicolo:"
                    # print veicolo
                    # print "treno:"
                    # print treno
                    break
            except:
                continue
    print "Odl:"
    try:
        print odl
    except:
        error = "ODL non riconosciuto"
        return error

    print "Data:"
    try:
        print data
    except:
        data = "00.00.0000"
        error = "veicolo non riconosciuto"
        print error
    print data

    print "veicolo:"
    try:
        print veicolo
    except:
        veicolo = 0
        error = "veicolo non riconosciuto"
        print error

    print "treno:"
    try:
        print treno
    except:
        treno = 0
        error = "treno non riconosciuto"
        print error
    # print descrizione

    #fieldnames = ["odl", "data", "treno", "veicolo", "descrizione"]
    #reader = ""
    # read csv
    csvfile = "odl_list_3.csv"
    temp_table = pd.read_csv(csvfile, sep=",", dtype={'odl':int, 'descrizione':str})
    #print temp_table.loc[temp_table["odl"]==odl, "descrizione"]
    # temp_table.loc[temp_table["odl"]==odl, "descrizione"] = descrizione
    try:
        array=temp_table.loc[temp_table['odl']==100007948463, 'descrizione'].values
    except:
        print "error finding Descrizione"
    try:
        test_field = ''.join(array.astype(str))
    except:
        print "error converting to string"
    # print test_field
    if test_field and test_field in descrizione:
        print "update descrizione!"
        temp_table['descrizione'] = temp_table['descrizione'].astype('str')
        temp_table.loc[temp_table['odl'] == 100007948463, 'descrizione'] = descrizione
        temp_table.to_csv(csvfile, index=False)
    else:
        #temp_table.to_csv(csvfile, index=False)
        # aggiungi riga:
        with open(csvfile, 'ab') as csvfile_temp:
            linewriter = csv.writer(csvfile_temp, delimiter=',')
            new_row = [odl, data, treno, veicolo, descrizione]
            print new_row
            linewriter.writerow(new_row)
            csvfile_temp.close()
    return error

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))


# Globals
input_pdf_path = '/home/zdarova/ocr/Input_ODL/'
temp_img_dir = "working/"
root_dir = "/home/zdarova/ocr/"
set_image_quality = 200



# Main function:
for pdf_file_name in absoluteFilePaths(input_pdf_path):
    if len(pdf_file_name) >= 4 and pdf_file_name[-4:] == ".pdf":
        print 'Scanning pdf files:'
        print pdf_file_name
        # temp img files:
        pages = scan_pdf(pdf_file_name, temp_img_dir, set_image_quality)
        if pages is not 0:
            for page in range(pages):
                image_file=root_dir + temp_img_dir + "page-" + str(page) + ".png"
                print image_file
                extract_text(image_file)







# if  test_field == treno:
#     print "sono uguali"
# else:
#     print "sono diversi"

# with open('odl_list_2.csv', 'r') as csvfile:
#     try:
#         reader = csv.reader(csvfile, delimiter=';')
#     except:
#         None
#     print "odl:"
#     print reader[0][1]
# #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# #     if reader:
# #         for row in reader:
# #             print row
# #             if odl == row['odl']:
# #                 writer.writerow({'odl': row['odl'], 'data': row['data'], 'treno': row['treno'], 'veicolo': row['veicolo'], 'descrizione': row['descrizione']})
# #                 append = 0
# #                 break
# #     csvfile.close()
# if append == 1:
#     with open('odl_list_2.csv', 'a') as csvfile:
#         linewriter = csv.writer(csvfile, delimiter=';')
#         linewriter.writerow(new_row)
#         csvfile.close()

####
    # linewriter = csv.writer(csvfile, delimiter=';')
    # for row in csvfile:
    #     if row[0] == odl:
    #         csvfile.seek(0)
    #         linewriter.writerow(new_row)
    #         csvfile.close()
    #         break


# ----------------------
# img_array=cv2.imread(image_file)
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
# crop_region_1 = img.crop((20, 60, 380, 110))
# Image._show(crop_region_1)

# crop_region_1 = img_array[200:400, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400
# cv2.imshow("cropped", crop_region_1)
# cv2.waitKey(0)

# text_region_1 = pytesseract.image_to_string(crop_region_1, 'ita', False, None)
# text = pytesseract.image_file_to_string(image_file)
# text = pytesseract.image_file_to_string(image_file, graceful_errors=True)
# print "ODL:"
# print text_region_1

# crop_region_2 = img.crop((500, 60, 700, 105))
#Image._show(crop_region_2)

# text_region_2 = pytesseract.image_to_string(crop_region_2, 'ita', False, None)
# print "Data:"
#print text_region_2

# Descrizione ODL
#crop_region_3 = img.crop((131, 120, 250, 141))
#crop_region_3.save('crop_region_3.png','png')
# crop_region_3_new = cv2.imread('crop_region_3.png')

# crop_region_3_new = cv2.resize(crop_region_3_new, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
# crop_region_3_new = cv2.imread('ODL1.jpg')
# crop_region_3_new = cv2.imread('table_text.png')
# crop_region_3_new = cv2.cvtColor(crop_region_3_new, cv2.COLOR_BGR2GRAY)
# crop_region_3_new = cv2.GaussianBlur(crop_region_3_new, (5, 5), 0)
# crop_region_3_new = cv2.Canny(crop_region_3_new,75,200)
#Image._show(crop_region_3)
# cv2.startWindowThread()
# cv2.namedWindow("reg3", cv2.WINDOW_NORMAL)
#cv2.imshow("Descrizione", crop_region_3_new)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# crop_region_3 = crop_region_3.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(crop_region_3)
# crop_region_3 = enhancer.enhance(2)
# crop_region_3 = crop_region_3.convert('1')
# crop_region_3_new_pil = Image.fromarray(crop_region_3_new)
# text_region_3 = pytesseract.image_to_string(crop_region_3_new_pil, 'ita', False, None)
# print "Descrizione ODL:"
# print text_region_3

# write to csv
# ok
# odl = re.search(r'\d+', text_region_1).group()

# ok:
# data=re.search('([0-9]{2}\\.[0-9]{2}\\.[0-9]{4})', text_region_2).group(0)

#print data
# print datetime.datetime.strptime(pre_data, '%d.%m.%Y')
# match_date = re.search(r'\\d{2}.\d{2}.d{4}', text_region_2)
# data = datetime.datetime.strptime(match_date.group(), '%m.%d.%Y').date()
# descrizione = text_region_3
# raw_text = raw_input(text)
# raw_text = raw_text.replace('\n', ' ').replace('\r', '')
#
# ''' spamwriter.writerow(['No'] , ['ODL']) '''
# index = 1
# with open('odl_list.csv', 'a') as csvfile:
#      linewriter = csv.writer(csvfile, delimiter=';')
#      data = [index, odl, data, descrizione]
#      linewriter.writerow(data)
#      csvfile.close()
