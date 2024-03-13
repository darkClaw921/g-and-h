from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime
# import urllib3
import urllib.request
import time
import asyncio
load_dotenv()
webhook = os.getenv('WEBHOOK')
bit = Bitrix(webhook)

@dataclass
class Lead:
    userName:str
    title:str='TITLE'
    userID:str='UF_CRM_1709220784686'
    photos:str='UF_CRM_1709223951925'
    urlUser:str='UF_CRM_1709224894080'
    messageURL:str='UF_CRM_1709293438392'

    description:str='COMMENTS'

@dataclass
class Deal:
    id:str='ID'
    title:str='TITLE'
    categoryID:str='CATEGORY_ID'
    statusID:str='STATUS_ID'
    comments:str='COMMENTS'
    responsibleID:str='ASSIGNED_BY_ID'


# async def te
def find_deal(dealID:str):
    deal = bit.call('crm.deal.get', params={'id': dealID})
    return deal

def find_lead(leadID:str):
    lead = bit.call('crm.lead.get', params={'id': leadID})
    return lead


# async def find_lead(userID:str):
#     lead = await bit.get_all(
#         'crm.deal.list',
#         params={
#             'select': ['*', 'UF_*'],
#             'filter': {Deal.id: f'{userID}'}
#     },)
#     pprint(lead)
#     if lead==[]:
#         return None
#     else:
#         print('лид уже есть')
#         # pprint(lead)
#         lead=lead[-1]
#         return lead




