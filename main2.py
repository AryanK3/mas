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
            return {"generic_name": product.get("generic_name"), "labeler_name": product.get("labeler_name"), "brand_name": product.get("brand_name"), "expiry_date": product.get("listing_expiration_date"), "packaging": packagings}
    return None

def brute_ndc(ndc, data):
    for product in data:
        for packaging in product.get('packaging'):
            if ((len(packaging.get('package_ndc').replace('-','')) == 10) and packaging.get('package_ndc').replace('-','') in ndc):
                return {"generic_name": product.get("generic_name"), "labeler_name": product.get("labeler_name"), "brand_name": product.get("brand_name"), "expiry_date": product.get("listing_expiration_date"), "ndc": packaging.get("package_ndc"), "description": packaging.get("description")}
    return None

def decode_barcode(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f"Decoded barcode data: {barcode_data}")
        return barcode_data

    return None

import json

def save_record_to_file(product):
    with open("saved_prods.json", "r+") as file:
        file_data = json.load(file)

        for prod in file_data:
            if (len(prod.get('ndc').replace('-', '')) == 10 and prod.get('ndc').replace('-', '') == product.get('ndc').replace('-', '')):
                prod['count'] += 1  
                file.seek(0)
                json.dump(file_data, file, indent=4)
                print('Saved data')
                return

            elif ('upc' in product.get('upc', {}) and prod.get('upc') == product.get('upc')):
                prod['count'] += 1
                file.seek(0)
                json.dump(file_data, file, indent=4)
                print('Saved data')
                return
        
        product['count'] = 1
        file_data.append(product)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        print('Saved data')

def main(db_path):
    data = load_products(db_path)
    
    cap = cv2.VideoCapture(0)  
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        barcode_data = decode_barcode(frame)
        
        if barcode_data:
            product = brute_ndc(barcode_data, data)
            if product:
                print(json.dumps(product, indent=4))
                inp = input("Enter (y) to continue, (s) to save: ")
                if inp.lower() == 'y':
                    continue 
                elif inp.lower() == 's':
                    save_record_to_file(product)
                    continue  
                else:
                    break
            product = query_upc(barcode_data, data)
            if product:
                print(json.dumps(product, indent=4))
                inp = input("Enter (y) to continue: ")
                if inp.lower() != 'y':
                    break
        cv2.imshow("Video Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

db_path = 'db.json' 
main(db_path)
