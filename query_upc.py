import json

with open('db.json', 'r') as f:
    data = json.load(f)

def find_product_by_upc(upc):
    for product in data:
        if 'upc' in product.get('openfda', {}) and upc in product['openfda']['upc']:
            return product
    return None

upc_to_search = input("Enter UPC: ")
product = find_product_by_upc(upc_to_search)

if product:
    print("Product found:", json.dumps(product, indent=4))
else:
    print("Product not found for UPC:", upc_to_search)
