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

def get_contact_k(contactID:str):
    contact=bitK.call('crm.contact.get', items={'id': contactID})
    return contact

def get_company_k(companyID:str):
    company=bitK.call('crm.company.get', items={'id': companyID})
    return company

def find_contact(phone:str)->bool:
    contact = bit.call('crm.contact.list', items={'filter': {'PHONE': phone}}, raw=True)['result']
    if len(contact)>0:
        return True
    return False

def create_contact(contact:dict):
    phone=contact['PHONE'][0]['VALUE']
    if find_contact(phone):
        return 0
    contact['PHONE']=[{'VALUE':phone,'VALUE_TYPE':'WORK'}]
    contact['NAME']='TEST2'    
    contactID=bit.call('crm.contact.add', items={'fields': contact})
    return contactID 

def find_company(companyName:str)->bool:
    company = bit.call('crm.company.list', items={'filter': {'TITLE': companyName}}, raw=True)['result']
    if len(company)>0:
        return True
    return False

def crate_company(company:dict):
    companyName=company['TITLE']
    if find_company(companyName):
        return 0
    companyID=bit.call('crm.company.add', items={'fields': company})
    return companyID



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

        try:
            dealK=find_deal_k(dealID)
        except:
            dealID=data['a'][2].split('=')[1].split('_')[1]
            print(f"по роботу {dealID=}")
            dealK=find_deal_k(dealID) 
        
        pprint(dealK)
        
        
        product=get_product_rows(dealID)
        pprint(product)
        prod=''
        for i in product:
            prod+=i['PRODUCT_NAME']+'\n'
        print(prod)
        contactID=0
        companyID=0

        if dealK['CONTACT_ID']:
            contactK=get_contact_k(dealK['CONTACT_ID'])
            pprint(contactK)
            contactID=create_contact(contactK)

        if dealK['COMPANY_ID']:
            companyK=get_company_k(dealK['COMPANY_ID'])
            pprint(companyK)
            companyID=crate_company(companyK)

        fields={
            # 'UF_CRM_1634020730':prod,
            'TITLE':dealK['TITLE'],
            'COMMENTS':prod,
            'ASSIGNED_BY_ID':88,
            'OPPORTUNITY':dealK['OPPORTUNITY'],
            'COMPANY_ID':companyID,
            'CONTACT_ID':contactID,
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

        contactID=0
        companyID=0

        if leadK['CONTACT_ID']:
            contactK=get_contact_k(leadK['CONTACT_ID'])
            pprint(contactK)
            contactID=create_contact(contactK)
        
        if leadK['COMPANY_ID']:
            companyK=get_company_k(leadK['COMPANY_ID'])
            pprint(companyK)
            companyID=crate_company(companyK)
        

        fields={
            # 'UF_CRM_1634020730':prod,
            'TITLE':leadK['TITLE'],
            'COMMENTS':prod,
            'ASSIGNED_BY_ID':88,
            'OPPORTUNITY':leadK['OPPORTUNITY'],
            'COMPANY_ID':companyID,
            'CONTACT_ID':contactID,
            # 'CATEGORY_ID':0,


        }
        pprint(fields)
        leadID=bit.call('crm.lead.add', items={'fields':fields})
        # dealID=bit.call('crm.deal.add', items={'fields': fields})
        print(leadID)

        return 'OK'

if __name__ == '__main__':
    
    dealK=find_deal_k('731')
    product=get_product_rows('731')
    pprint(dealK)
    
    contact=get_contact_k(dealK['CONTACT_ID'])
    pprint(contact)
    company=get_company_k(dealK['COMPANY_ID'])
    pprint(company)

    contackID=create_contact(contact) 
    companyID=crate_company(company)

    fields={
            # 'UF_CRM_1634020730':prod,
            'TITLE':dealK['TITLE'],
            'COMMENTS':product,
            'ASSIGNED_BY_ID':88,
            'OPPORTUNITY':dealK['OPPORTUNITY'],
            'COMPANY_ID':companyID,
            'CONTACT_ID':contackID,
            # 'CATEGORY_ID':0,


        }
    leadID=bit.call('crm.deal.add', items={'fields':fields},raw=True)

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
    # contackt=get_contact_k('44')
    # pprint(contackt)
    # create_contact(contackt)
    # app.run(host='0.0.0.0',port='5003',debug=True)
    # 