import json
import requests
from gradefilter_lib import select_grade

with open('input.json','r') as f:
    data_json = json.load(f)

## Add function
data_input = data_json.get('spec_input')

companyId = data_input['companyID']

## FROM HERE################
headers = {"Authorization": "Bearer c38bdf06-333f-4fb3-9231-7c7908c4ee3a"}

response = requests.get(f"https://office.smarttradzt.com:8001/buy-ecommerce-service/product/searchCombination?_page=0&_pageSize=100&companyId={companyId[0]}", headers=headers)

data_product = response.json()

category_id = data_product.get('results')[0].get('category').get('id')

resp = requests.get(f"https://office.smarttradzt.com:8001/buy-ecommerce-service/category/{category_id}", headers=headers)

data_category = resp.json()



## TO HERE, JUST REPLACE WITH ONE LINE BELOW IN MICROSERVICE####################
# data_product = product_service.get(headers,companyId)

# with open('data_product.json', 'w') as outfile:            
#     json.dump(data_product, outfile, indent = 3)


retJSON = select_grade(data_input, data_product, data_category)

print(retJSON)
