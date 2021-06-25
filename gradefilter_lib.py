import json
import requests
import pandas as pd

def select_grade(data_input,data_product, data_category):

    # data_input = data_json.get('spec_input')
    # companyId = data_input['companyID']

    # headers = {"Authorization": "Bearer 2a97baff-ac4c-4a83-b43b-685976461b88"}

    # response = requests.get(f"https://office.smarttradzt.com:8001/buy-ecommerce-service/product/searchCombination?_page=0&_pageSize=10&companyId={companyId[0]}", headers=headers)

    # data_product = response.json() # type dict

    res = data_product.get('results')   # type list

    #product_names = [item.get('name') for item in res]
    product_id = [item.get('id') for item in res]

    # product_application = [item.get('productApplication').replace('<ul><li>', '').replace('</li></ul>', '').split('</li><li>') for item in res]

    product_application = [
        item.get('productApplication').replace('<ul><li>', '').replace('</li></ul>', '').split('</li><li>') if item.get(
            'productApplication') else "" for item in res]

    # productspec_list = [item.get('specificationValues') for item in res]

    productspec_list = [item.get('specificationValues') if item.get('specificationValues') else "" for item in res]


    ###############################################
    # THINK ABOUT HOW TO MODIFY BELOW (ID) IN FUTURE - FOR GENERALISATION
    # Check with ammar 'code' is it hardcoded?

    
    cat_gradings = data_category.get('object').get('gradings')
    
    cat_specs = data_category.get('object').get('specifications')

    gradenames = [item.get('gradeName') for item in cat_gradings]
    
    

    # category_res = res[0].get('category')
    # spec_res = category_res.get('specifications')

    spec_code_list = []
    spec_id_list = []
    spec_name_list = []
    for item in cat_specs:
        spec_code_list.append(item.get('code'))
        spec_id_list.append(item.get('id'))
        spec_name_list.append(item.get('name'))

    # selected_code = ['mar001', 'mar007'] # selected spec code for grading
    
    for code, id in zip(spec_name_list,spec_id_list):
        if gradenames[0] in code:
            print(code)
            print(id)
            viscosity_id = id
        elif gradenames[1] in code:
            print(code)
            print(id)
            wet_hard_id = id


    ###############################################

    viscosity_list = []
    wet_hard_list = []

    for item in productspec_list:

        if item == "":

            # If entire specification list is empty
            viscosity_list.append(0)
            wet_hard_list.append(0)

        else:

            visc_flag = False
            wet_flag = False

            for spec_item in item:
                # print(spec_item)


                if spec_item.get('specification').get('id') == viscosity_id:
                    # print(spec_item.get('value'))
                    viscosity_list.append(float(spec_item.get('value')))
                    visc_flag = True

                if spec_item.get('specification').get('id') == wet_hard_id:
                    # print(spec_item.get('value'))
                    wet_hard_list.append(float(spec_item.get('value')))
                    wet_flag = True

            if not visc_flag:
                viscosity_list.append(0)

            if not wet_flag:
                wet_hard_list.append(0)

    # Compile into Dataframe

    df=pd.DataFrame({"product_id": product_id, "visco": viscosity_list, "wet_hard":wet_hard_list, "application":product_application})

    application_select = [data_input['application'] in item for item in df["application"]]

    if data_input['viscoMin'] == "":
        data_input['viscoMin']=min(df["visco"])

    if data_input['viscoMax'] == "":
        data_input['viscoMax']=max(df["visco"])

    if data_input['wethardMin'] == "":
        data_input['wethardMin']=min(df["wet_hard"])

    if data_input['wethardMax'] == "":
        data_input['wethardMax']=max(df["wet_hard"])

    out = df["product_id"][
        (df["visco"] >= data_input['viscoMin'])
        & (df["visco"] <= data_input['viscoMax'])
        & (df["wet_hard"] >= data_input['wethardMin'])
        & (df["wet_hard"] <= data_input['wethardMax'])
        & application_select
        ]


    df2 = pd.DataFrame(out)

    retJSON = {"selected_grade": json.loads(df2.to_json(orient="records"))}

    return retJSON
