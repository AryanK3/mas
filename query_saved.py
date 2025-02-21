import json

def get_record(ndc):
    with open("saved_prods.json", "r") as file:
        file_data = json.load(file)

        for prod in file_data:
            if (len(prod.get('ndc').replace('-', '')) == 10 and prod.get('ndc').replace('-', '') == ndc.replace('-', '')):
                return {"generic_name": prod.get("generic_name"), "labeler_name": prod.get("labeler_name"), "brand_name": prod.get("brand_name"), "expiry_date": prod.get("listing_expiration_date"), "ndc": prod.get("ndc"), "description": prod.get("description"), "count": prod.get('count')}

            elif (prod.get('upc') == ndc):
                return {"generic_name": prod.get("generic_name"), "labeler_name": prod.get("labeler_name"), "brand_name": prod.get("brand_name"), "expiry_date": prod.get("listing_expiration_date"), "packaging": prod.get('packaging'), "count": prod.get('count')}
        return {"message": "No data found"}
print(get_record("5976237191"))