import json

def load_products(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def get_product_by_ndc(ndc):
    products = load_products("db.json")
    for product in products:
        if product.get('product_ndc') in ndc:
            for packaging in product.get('packaging'):
                if packaging.get('package_ndc') == ndc:
                    return product  
    return None 

ndc = input("Enter NDC: ")
product = get_product_by_ndc(ndc)

if product:
    print(f"{json.dumps(product)}")
else:
    print(f"No product found with ndc {ndc}")
