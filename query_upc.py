import json

with open('db.json', 'r') as f:
    data = json.load(f)

def find_product_by_upc(upc):
    for product in data:
        if 'upc' in product.get('openfda') and upc in product['openfda']['upc']:
            packagings = []
            for packaging in product.get('packaging'):
                packagings.append({"ndc": packaging.get("package_ndc"), "description": packaging.get("description")})
            return {"generic_name": product.get("generic_name"), "expiry_date": product.get("listing_expiration_date"), "packaging": packagings}


upc_to_search = input("Enter UPC: ")
product = find_product_by_upc(upc_to_search)

if product:
    print(json.dumps(product))
else:
    print("Product not found for UPC:", upc_to_search)
