from datetime import datetime
from dataclasses import dataclass
import pytz
from workGS import Sheet
from workBitrix import get_deals, get_products, get_users, get_departments   
import postgreWork
from pprint import pprint
import pytz

@dataclass
class CSheet:
    week1:str='B7'
    week2:str='B8'
    week3:str='B9'
    week4:str='B10'
    week5:str='B11'
    
    week1_nelicvid:str='E7'
    week2_nelicvid:str='E8'
    week3_nelicvid:str='E9'
    week4_nelicvid:str='E10'
    week5_nelicvid:str='E11'
weekLicvid = {
    1: 'C8',
    2: 'C9',
    3: "C10",
    4: 'C11',
    5: 'C12',
    6: 'C13',
}
weekNelicvid = {
    1: 'G8',
    2: 'G9',
    3: 'G10',
    4: 'G11',
    5: 'G12',
    6: 'G13',
}

tz = pytz.timezone('Europe/Moscow')

def get_week_of_day(date):
    first_day = date.replace(day=1)
    iso_day_one = first_day.isocalendar()[1]
    iso_day_date = date.isocalendar()[1]
    adjusted_week = (iso_day_date - iso_day_one) + 1
    return adjusted_week

def get_col_name():
    current_date = datetime.today()
    current_date_msk = current_date.astimezone(tz)
    # print(f'{current_date_msk=}')
    today = current_date_msk.weekday()
    # print(today)  # 1
    today1 = current_date_msk.today().astimezone(tz)
    # print(f'{today=}')
    # print(f'{today1=}')
    week_number = get_week_of_day(today1)
    print('week_number: ', week_number)
    return week_number
    # col = week[week_number][today]
    # return col

PATH_JSON_ACCAUNT='profzaboru-5f6f677a3cd8.json'
SHEET_NAME='ooo_sk'

def get_moscow_date():
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    return moscow_time.strftime('%Y-%m')

def get():
    listName = get_moscow_date()
    print(listName)
    sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)
    return sheet.get_cell(CSheet.plan)

def add_deals():
    deals = get_deals()
    for deal in deals:
        products=deal['product']
        deal=deal['deal']

        d={
            'id':int(deal['ID']),
            'assigned_by_id':int(deal['ASSIGNED_BY_ID']),
            'category_id':deal['CATEGORY_ID'],
            'status':deal['STAGE_SEMANTIC_ID'],
            'created_date':datetime.strptime(deal['DATE_CREATE'], '%Y-%m-%dT%H:%M:%S%z'),
            'close_date':datetime.strptime(deal['CLOSEDATE'], '%Y-%m-%dT%H:%M:%S%z'),
            'price':float(deal['OPPORTUNITY']),
            # 'stage_id':int(deal['STAGE_ID']),
            # 'products':[[product['ID'],product['PRICE']] for product in products]
        }
        pprint(d)

        # postgreWork.add_deal(d)
        if products:
            for product in products:
                d={
                    'product_id':int(product['PRODUCT_ID']),
                    'name':product['PRODUCT_NAME'],
                    'price':float(product['PRICE']),
                    'deal_id':int(deal['ID']),
                    'created_date':datetime.strptime(deal['CLOSEDATE'], '%Y-%m-%dT%H:%M:%S%z'),
                    'plan':postgreWork.get_now_plan(product['PRODUCT_NAME'])['price']
                }
                postgreWork.add_product(d)

def add_products():
    products = get_products()
    for product in products:
        d={
            'id':int(product['ID']),
            'created_date':datetime.strptime(product['DATE_CREATE'], '%Y-%m-%dT%H:%M:%S%z'),
            'name':product['NAME'],
            'price':float(product['PRICE']),
            'category':product['MEASURE']
        }
        postgreWork.add_product(d)

def add_plan():
    # listName = get_moscow_date()
    # sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)
    # sheet.send_cell(CSheet.plan, 1000)
    a={ 
       'start_date': datetime(2024, 3, 1, 0, 0), 
       'name': 'Лом', 
       'price': 3_000_000}
    
    postgreWork.add_plan(a)
    a={ 
       'start_date': datetime(2024, 3, 4, 0, 0), 
       'name': 'Неликвид', 
       'price': 1_000_000}
    
    postgreWork.add_plan(a)
    a={ 
       'start_date': datetime(2024, 3, 11, 0, 0), 
       'name': 'Неликвид', 
       'price': 1_000_000}
    
    postgreWork.add_plan(a)
    a={ 
       'start_date': datetime(2024, 3, 18, 0, 0), 
       'name': 'Лом', 
       'price': 3_000_000}
    
    postgreWork.add_plan(a)
    
    a={ 
       'start_date': datetime(2024, 3, 25, 0, 0), 
       'name': 'Лом', 
       'price': 3_000_000}
    
    postgreWork.add_plan(a)
    
    a={ 
       'start_date': datetime(2024, 3, 25, 0, 0), 
       'name': 'Лом', 
       'price': 3_000_000}
    
    postgreWork.add_plan(a)
    


def update_fackt():
    lickvid=[]
    nelickvid=[]
    sumLickvid=0
    sumNelickvid=0
    templ={'licvid':{},'nelicvid':{}}
    
    deals= get_deals()
    for deal in deals:
        for product in deal['product']:
            if product['PRODUCT_ID']==16:
                sumLickvid+=product['PRICE']
                a=datetime.strptime(deal['deal']['CLOSEDATE'], '%Y-%m-%d')
                week=get_week_of_day(a)
                if week in templ['licvid']:
                    templ['licvid'][week]+=product['PRICE']
                else:
                    templ['licvid'][week]=product['PRICE']
            
            elif product['PRODUCT_ID']==20:
                a=datetime.strptime(deal['deal']['CLOSEDATE'], '%Y-%m-%dT')
                week=get_week_of_day(a)
                if week in templ['nelicvid']:
                    templ['nelicvid'][week]+=product['PRICE']
                else:
                    templ['nelicvid'][week]=product['PRICE'] 
                # nelickvid.append(deal)
        
    pprint(templ)
    # get_week_of_day(datetime.today())
    listName = get_moscow_date()
    print(listName)
    sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)
    
    for week, price in templ['licvid'].items():
        cell=weekLicvid[week]
        print(cell) 
        print(price)
        # sheet.send_cell("C10", '5')
        sheet.update_cell(10, 3, price)
        #TODO 


    for week, price in templ['nelicvid'].items():
        cell=weekNelicvid[week]
        print(cell) 
        print(price)
        # sheet.send_cell(cell, str(price))
        sheet.update_cell(10, 7, price)

    # lst=['План','факт','тип','отдел','неделя','месяц']       
    # sheet.insert_cell(data=lst)

    return templ

def add_users():

    users = get_users()
    for user in users:

        d={
            'id':int(user['ID']),
            'name':user.get('NAME','None'),
            'last_name':user.get('LAST_NAME','None'),
            'department':user['UF_DEPARTMENT'][0]
        }
        pprint(d)
        postgreWork.add_user(d)

def add_departments():
    departments = get_departments()
    for department in departments:
        d={
            'id':int(department['ID']),
            'name':department['NAME'],
            # 'parent_id':department['PARENT'],
            # 'uf_head':department['UF_HEAD']
        }
        postgreWork.add_department(d)

def first_start():
    add_deals()
    # add_products()
    # add_users()
    # add_departments()
    # add_plan()

if __name__ == '__main__':
    # print(add_deals())
    # print(add_products())
    # add_plan()
    first_start()
    # update_fackt()
    # get_col_name()
    
    
    # get_week_of_day(datetime.today())

# listName = get_moscow_date()
# sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)