from flask import Flask, render_template, request, before_render_template, jsonify
import requests
import postgreWork
from pprint import pprint
from dotenv import load_dotenv
import os
load_dotenv()
URL=os.environ.get('POSTGRES_URL')
app = Flask(__name__)

# Список доступных продуктов
products = ["Лом", "Неликвид"]
departments =  ['Отдел продаж','Отдел закупок','Отдел логистики','Отдел финансов']

months=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
montsDict={1:'Январь',2:'Февраль',3:'Март',4:'Апрель',5:'Май',6:'Июнь',7:'Июль',8:'Август',9:'Сентябрь',10:'Октябрь',11:'Ноябрь',12:'Декабрь'}
montsDict2={'Январь':1,'Февраль':2,'Март':3,'Апрель':4,'Май':5,'Июнь':6,'Июль':7,'Август':8,'Сентябрь':9,'Октябрь':10,'Ноябрь':11,'Декабрь':12}

departmentsProduct={'Отдел продаж':['Лом','Неликвид'],
                    'Отдел закупок':['Лом12','asd','Неликвид1'],
                    'Отдел логистики':['Лом','Неликвид'],
                    'Отдел финансов':['Лом','Неликвид']}

url=f'http://{URL}:5002/plan'
@app.route('/', methods=['GET', 'POST'])
def sales_plan():
    if request.method == 'POST':
        start_date = request.form.getlist('start_date[]')
        plan = request.form.getlist('plan[]')
        fackt=request.form.getlist('fackt[]')
        product = request.form.getlist('product[]')
        department = request.form.getlist('department[]')
        month=request.form.getlist('month[]')
        month=montsDict2[month[0]]

        # Здесь можно добавить логику сохранения плана продаж в базу данных или файл
        
        json={'start_date':start_date,'plan':plan,
              'fackt':fackt,'product':product,
              'department':department, 'month':month}
        pprint(json)
        requests.post(url, json=json)

        return render_template('success.html', start_date=start_date, plan=plan, product=product)
    
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
        products=departmentsProduct[department]
        print('замене')
    except:
        products=['Лом1','Неликвид']
    
    print(products)
    return render_template('form.html', products=products, departments=departments, months=months)

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
    
    print(product)
    print(month)
    print(department)

    plans=postgreWork.get_plan_for_month(product,month,department)
    pprint(plans)

    sales_plans=[]
    for plan in plans:
        print('plan',plan.start_date)
        dateStr=plan.start_date.strftime("%d-%m-%Y")
        sales_plans.append({'start_date':dateStr,
                            'plan':plan.plan,
                            'fackt':plan.fackt,
                            'product':plan.product})
    if len(sales_plans)==0:
        sales_plans = [{'start_date':0,'plan':0,'fackt':0,'product':0}]

    print(sales_plans)

    # return render_template('form.html', products=products, departments=departments, months=months)
    return render_template('_sales_plans.html', sales_plans=sales_plans)

@app.route('/get_products_for_department')
def get_products_for_department():
    department = request.args.get('department')
    products = departmentsProduct[department]  # Функция, которую нужно реализовать
    # return jsonify({'products': products})
    return products
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5008',debug=True)
