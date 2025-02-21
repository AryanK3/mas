import cv2
from pyzbar.pyzbar import decode
import numpy as np

image = cv2.imread('thic.jpeg') 
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

barcodes = decode(image)

for barcode in barcodes:
    barcode_data = barcode.data.decode('utf-8')
    barcode_type = barcode.type
    print(f"{barcode_data}")
