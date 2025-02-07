import cv2
from pyzbar.pyzbar import decode
import numpy as np

image = cv2.imread('capture.jpg') 

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresholded_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

barcodes = decode(thresholded_image)

for barcode in barcodes:
    rect_points = barcode.polygon
    if len(rect_points) == 4:
        points = [tuple(point) for point in rect_points]
    else:
        points = [tuple(barcode.rect[0:2]), 
                  (barcode.rect[0] + barcode.rect[2], barcode.rect[1]),
                  (barcode.rect[0] + barcode.rect[2], barcode.rect[1] + barcode.rect[3]),
                  (barcode.rect[0], barcode.rect[1] + barcode.rect[3])]

    cv2.polylines(image, [np.array(points)], True, (0, 255, 0), 2)

    barcode_data = barcode.data.decode('utf-8')
    barcode_type = barcode.type

    print(f"Found barcode: {barcode_data} (Type: {barcode_type})")

    cv2.putText(image, barcode_data, (points[0][0], points[0][1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow('Barcode Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
