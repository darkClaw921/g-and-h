from flask import Flask, render_template, request, before_render_template, jsonify,redirect, url_for
import requests
import postgreWork
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()
URL=os.environ.get('POSTGRES_URL')
app = Flask(__name__)

# Список доступных продуктов
products = ["ЛОМ", "Неликвид"]
departments =  ['Отдел огнеупор','Отдел стекло','Отдел оборудование','Отдел демонтаж','Отдел проектирования и изготовления оборудования']
metrikMonth=['Неделя','Месяц']
months=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
montsDict={1:'Январь',2:'Февраль',3:'Март',4:'Апрель',5:'Май',6:'Июнь',7:'Июль',8:'Август',9:'Сентябрь',10:'Октябрь',11:'Ноябрь',12:'Декабрь'}
montsDict2={'Январь':1,'Февраль':2,'Март':3,'Апрель':4,'Май':5,'Июнь':6,'Июль':7,'Август':8,'Сентябрь':9,'Октябрь':10,'Ноябрь':11,'Декабрь':12}
planFakt=['План','Факт']

departmentsProduct={'Отдел огнеупор':{
                        'metrick':{
                                    # '<--Выбрать-->':['Основное'],
                                    'План/факт продаж':['ЛОМ','Неликвид'],
                                   '⁠Количество новых клиентов':['Основное'],
                                   'Количество успешных креативных решений':['Основное'],
                                   'Количество холодных звонков':['Основное'],
                                   'Количество новых объектов':['ЛОМ','Неликвид'],
                                #    'Продажа невостребованного':['Основное']
                                   }},
                    
                    'Отдел стекло':{
                        'metrick':{
                                    # '<--Выбрать-->':['Основное'],
                                    # 'План/факт продаж':['ЭРКЛЕЗ','ЩЕБЕНЬ','ШАРИКИ'],
                                    'План/факт продаж':['Обработанное','Необработанное'],
                                   'Количество новых клиентов/партнеров':['НОВЫЕ','ПОВТОРНЫЕ'],
                                   'Количество холодных звонков':['Основное'],
                                   '⁠Количество новых рынков':['Основное'],
                                   'Количество успешных креативных решений':['Основное']}},
                    
                    'Отдел оборудование':{
                        'metrick':{
                                    # '<--Выбрать-->':['Основное'],
                            'План/факт продаж':['Основное'],
                                   '⁠Количество новых клиентов':['Основное'],
                                   'Количество новых объектов':['Основное'],
                                   'Количество холодных звонков':['Основное'],
                                   'Количество успешных креативных решений':['Основное'],
                                   }},
                    
                    'Отдел демонтаж':{
                        'metrick':{
                                    # '<--Выбрать-->':['Основное'],
                            'Улучшение способов демонтажа':['Основное'],
                                   '% эффективности по срокам':['Основное'],
                                   'Повышение маржинальности проектов':['Основное'],
                                   '⁠Количество новых объектов':['Основное'],
                                   '⁠Экономия на креативности (в рублях)':['Основное'],
                                   }},
                    
                    'Отдел проектирования и изготовления оборудования':{
                        'metrick':{
                                    # '<--Выбрать-->':['Основное'],
                            'Количество холодных звонков':['Проектирование оборудования','Изготовление оборудования'],
                                   '% эффективности по срокам':['Проектирование оборудования','Изготовление оборудования'],
                                   'Повышение маржинальности проектов':['Проектирование оборудования','Изготовление оборудования'],
                                   'Количество новых объектов':['Проектирование оборудования','Изготовление оборудования'],
                                   'Экономия на креативности (в рублях)':['Проектирование оборудования','Изготовление оборудования'],}}
                    }

url=f'http://{URL}:5002/plan'
@app.route('/', methods=['GET', 'POST'])
def sales_plan():
    if request.method == 'POST':
        start_date = request.form.getlist('start_date[]')
        plan = request.form.getlist('plan[]') # план факт
        fackt=request.form.getlist('fackt[]')
        product = request.form.getlist('product[]')
        department = request.form.getlist('department[]')
        # month=request.form.getlist('month[]')
        metrik=request.form.getlist('metrik[]')
        metrikMonthOtv=request.form.getlist('metrikMonth[]')
        number=request.form.getlist('planFakt[]')

        # month=montsDict2[month[0]]
        # pprint(f'{fackt=}')
        

        if number==['План']:
            fackt=['0']
        
        if number==['Факт']:
            fackt=plan
            plan=['0']
        # if fackt==['']:
            # fackt=['0']
        
        # if plan==['']:
            # plan=['0']
        # Здесь можно добавить логику сохранения плана продаж в базу данных или файл
        plan[0]=plan[0].replace('_','').replace(' ','')
        fackt[0]=fackt[0].replace('_','').replace(' ','')

        json={'start_date':start_date,'plan':plan,
              'fackt':fackt,'product':product,
              'department':department, 
            #   'month':month,
              'metrick':metrik,'metrikMonth':metrikMonthOtv}
        pprint(json)
        requests.post(url, json=json)

        return render_template('success.html', start_date=start_date, plan=plan, 
                               product=product, metrik=metrik,
                               metrikMonth=metrikMonthOtv,)
    
    # startDate= request.args.get('start_date')
    # product=request.args.get('product')
    # plan=request.args.get('plan')
    # fackt=request.args.get('fackt')
    # month=montsDict2[request.args.get('month')]
    department=request.args.get('department')

    # department1=request.form.getlist('department[]')
    print(f'{department=}')
    # print(f'{department1=}')
    pprint(request.__dict__)
    # pprint(request.form)
    try:
        # department = request.args.get('department')
        # metrik=request.args.get('metrik')
        # products = departmentsProduct[department]['metrik'][metrik] 
        products = ["ЛОМ", "Неликвид"]
        # metrik=departmentsProduct[department]['metrik'].keys()
        # print(f'{metrik=}')

        # metrik=products
        print('замене')
    except:
        products=['Лом','Неликвид']
    
    metriks = departmentsProduct['Отдел огнеупор']['metrick'].keys() 

    print(products)
    return render_template('form.html', products=products, departments=departments, 
                           months=months, metriks=metriks,
                           metrikMonths=metrikMonth,
                           planFakts=planFakt,)

# @app.route('/sales_plans/<string:start_date?>/<stryng:product>')
@app.route('/sales_plans')
def get_sales_plans():
# def get_sales_plans(start_date,product):
    # request.form.getlist('start_date[]')[0]
    startDate= request.args.get('start_date')
    product=request.args.get('product')
    plan=request.args.get('plan')
    fackt=request.args.get('fackt')
    month=montsDict2[request.args.get('month')]
    department=request.args.get('department')
    metrik=request.args.get('metrik')
    metrikMonth=request.args.get('metrikMonth')
    
    print(product)
    print(month)
    print(department)
    print(metrik)

    plans=postgreWork.get_plan_for_month(product,month,department,metrik)
    pprint(plans)

    sales_plans=[]
    for plan in plans:
        print('plan',plan.start_date)
        dateStr=plan.start_date.strftime("%d-%m-%Y")
        sales_plans.append({'start_date':dateStr,
                            'plan':plan.plan,
                            'fackt':plan.fackt,
                            'product':plan.product
                            })
    if len(sales_plans)==0:
        sales_plans = [{'start_date':0,'plan':0,'fackt':0,'product':0}]

    print(sales_plans)

    # return render_template('form.html', products=products, departments=departments, months=months)
    return render_template('_sales_plans.html', sales_plans=sales_plans,metrikMonths=metrikMonth)


@app.route('/get_products_for_department')
def get_products_for_department():
    department = request.args.get('department')
    metrik=request.args.get('metrik')
    print(f'{department=}')
    print(f'{metrik=}')
    try:
        products = departmentsProduct[department]['metrick'][metrik]       
    except:
        metrick=departmentsProduct[department]['metrick'].keys()
        print(f'{metrick=}')
        products = departmentsProduct[department]['metrick'][list(metrick)[0]]

    print(products)
    return products


@app.route('/get_metrik_for_department')
def get_metrik_for_department():
    department = request.args.get('department')
    # print('///'+department)
    metriks = departmentsProduct[department]['metrick'].keys() 
    # print(list(metriks))
    return list(metriks)


@app.route('/go-to-main-page')
def go_to_main_page():
    # return render_template('form.html', products=products, departments=departments, months=months, metriks=metriks,metrikMonths=metrikMonth) 
    return redirect(url_for('sales_plan'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5008',debug=True)
