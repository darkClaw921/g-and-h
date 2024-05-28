from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
from pprint import pprint  
from dotenv import load_dotenv
import os
from fast_bitrix24 import Bitrix

app = Flask(__name__)
api = Api(app, version='1.0', title='G&H API',description='A G&H API',)

load_dotenv()
webhook = os.getenv('WEBHOOK')
webhookKorob = os.getenv('WEBHOOK_KOROB')
bit = Bitrix(webhook)
bitK = Bitrix(webhookKorob)


def find_deal_k(dealID:str):
    deal = bitK.call('crm.deal.get', items={'id': dealID})
    return deal
def find_lead_k(dealID:str):
    deal = bitK.call('crm.lead.get', items={'id': dealID})
    return deal

def get_product_rows(dealID:str):
    products=bitK.call('crm.deal.productrows.get', items={'id': int(dealID)}, raw=True)['result']
    return products

def get_product_rows_lead(leadID:str):
    products=bitK.call('crm.lead.productrows.get', items={'id': int(leadID)}, raw=True)['result']
    return products
  
@api.route('/deal')
@api.doc(description='Дублирет сделку на облако') 
class Lead_redirect(Resource):
    def get(self,):
        """План продаж"""

        data = request.get_json() 
        pprint(data)

        return 'OK'
    def post(self):
        """сделка"""


        pprint(request.__dict__)
        data = request.get_json() 
        pprint(data)
        dealID=data['a'][1].split('=')[1]
        print(f"{dealID=}")
        dealK=find_deal_k(dealID)
        pprint(dealK)
        
        
        product=get_product_rows(dealID)
        pprint(product)
        prod=''
        for i in product:
            prod+=i['PRODUCT_NAME']+'\n'
        print(prod)

        fields={
            # 'UF_CRM_1634020730':prod,
            'TITLE':dealK['TITLE'],
            'COMMENTS':prod,
            'ASSIGNED_BY_ID':88,
            'OPPORTUNITY':dealK['OPPORTUNITY'],
            # 'CATEGORY_ID':0,


        }
        pprint(fields)
        dealID=bit.call('crm.deal.add', items={'fields': fields})
        print(dealID)

        return 'OK'
@api.route('/lead')
@api.doc(description='Дублирет лид на облако') 
class Deal_redirect(Resource):
    def get(self,):
        """План продаж"""

        data = request.get_json() 
        pprint(data)

        return 'OK'
    def post(self):
        """сделка"""


        pprint(request.__dict__)
        data = request.get_json() 
        pprint(data)
        leadID=data['a'][1].split('=')[1]
        print(f"{leadID=}")
        leadK=find_lead_k(leadID)
        pprint(leadK)
        
        
        product=get_product_rows_lead(leadID)
        pprint(product)
        prod=''
        for i in product:
            prod+=i['PRODUCT_NAME']+'\n'
        print(prod)

        fields={
            # 'UF_CRM_1634020730':prod,
            'TITLE':leadK['TITLE'],
            'COMMENTS':prod,
            'ASSIGNED_BY_ID':88,
            'OPPORTUNITY':leadK['OPPORTUNITY'],
            # 'CATEGORY_ID':0,


        }
        pprint(fields)
        leadID=bit.call('crm.lead.add', items={'fields':fields})
        print(leadID)

        return 'OK'

if __name__ == '__main__':
    
    # leadK=find_deal_k('1116')
    # product=get_product_rows(1116)
    # pprint(product)
    # prod=''
    # for i in product:
    #     prod+=i['PRODUCT_NAME']+'\n'
    # print(prod)
    # fields={
    #         # 'UF_CRM_1634020730':prod,
    #         'TITLE':leadK['TITLE'],
    #         'COMMENTS':prod,
    #         'ASSIGNED_BY_ID':88,
    #         'OPPORTUNITY':leadK['OPPORTUNITY'],
    #         # 'CATEGORY_ID':0,


    #     }
    
    # pprint(fields)
    # leadID=bit.call('crm.deal.add', items={'fields':fields},raw=True)
    app.run(host='0.0.0.0',port='5003',debug=True)
    # 