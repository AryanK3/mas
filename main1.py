import cv2
import json
from pyzbar.pyzbar import decode

def load_products(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def query_upc(upc, data):
    for product in data:
        if 'upc' in product.get('openfda') and upc in product['openfda']['upc']:
            packagings = []
            for packaging in product.get('packaging'):
                packagings.append({"ndc": packaging.get("package_ndc"), "description": packaging.get("description")})
            return {"generic_name": product.get("generic_name"), "expiry_date": product.get("listing_expiration_date"), "packaging": packagings}
    return None

def brute_ndc(ndc, data):
    for product in data:
        for packaging in product.get('packaging'):
            if packaging.get('package_ndc').replace('-','') in ndc:
                return {"generic_name": product.get("generic_name"), "expiry_date": product.get("listing_expiration_date"), "description": packaging.get("description")}
    return None

def decode_barcode(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(image)

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f"{barcode_data}")
        return barcode_data

    return None

def main(image_path, db_path):
    data = load_products(db_path)
    barcode_data = decode_barcode(image_path)
    
    if barcode_data:
        product = brute_ndc(barcode_data, data)
        if product:
            return json.dumps(product)

        product = query_upc(barcode_data, data)
        if product:
            return json.dumps(product)

    return json.dumps({"message": "No product found"})

image_path = 'sample.jpg' 
db_path = 'db.json'        
result = main(image_path, db_path)
print(result)

