import json

def load_products(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def get_product_by_ndc(ndc):
    products = load_products("db.json")
    for product in products:
        for packaging in product.get('packaging'):
            if packaging.get('package_ndc').replace('-','') in ndc:
                return {"generic_name": product.get("generic_name"), "expiry_date": product.get("listing_expiration_date"), "description": packaging.get("description")}  

ndc = input("Enter NDC: ")
product = get_product_by_ndc(ndc)

if product:
    print(f"{json.dumps(product)}")
else:
    print(f"No product found with ndc {ndc}")
