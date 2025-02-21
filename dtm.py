from pylibdmtx.pylibdmtx import decode
from PIL import Image

img = Image.open("dmi.jpeg")
decoded_objects = decode(img)

if decoded_objects:
    for obj in decoded_objects:
        print("Data:", obj.data.decode('utf-8'))
else:
    print("No Data Matrix code found.")

