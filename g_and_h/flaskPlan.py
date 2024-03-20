from flask import Flask, render_template, request
import requests
import postgreWork
app = Flask(__name__)

# Список доступных продуктов
products = ["Лом", "Неликвид"]
departments =  ['Отдел продаж','Отдел закупок','Отдел логистики','Отдел финансов']
months=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
montsDict={1:'Январь',2:'Февраль',3:'Март',4:'Апрель',5:'Май',6:'Июнь',7:'Июль',8:'Август',9:'Сентябрь',10:'Октябрь',11:'Ноябрь',12:'Декабрь'}
montsDict2={'Январь':1,'Февраль':2,'Март':3,'Апрель':4,'Май':5,'Июнь':6,'Июль':7,'Август':8,'Сентябрь':9,'Октябрь':10,'Ноябрь':11,'Декабрь':12}

url='http://10.7.0.4:5002/plan'
@app.route('/', methods=['GET', 'POST'])
def sales_plan():
    if request.method == 'POST':
        start_date = request.form.getlist('start_date[]')
        amount = request.form.getlist('amount[]')
        product = request.form.getlist('product[]')
        # Здесь можно добавить логику сохранения плана продаж в базу данных или файл
        print(f"Start date: {start_date}, Amount: {amount}, Product: {product}")
        requests.post(url, json={'start_date': start_date, 'amount': amount, 'product': product})

        return render_template('success.html', start_date=start_date, amount=amount, product=product)
    
    return render_template('form.html', products=products, departments=departments, months=months)

# @app.route('/sales_plans/<string:start_date?>/<stryng:product>')
@app.route('/sales_plans')
def get_sales_plans():
# def get_sales_plans(start_date,product):
    # request.form.getlist('start_date[]')[0]
    startDate= request.args.get('start_date')
    product=request.args.get('product')
    plan=request.args.get('plan')
    month=montsDict2[request.args.get('month')]
    
    plans=postgreWork.get_plan_for_month(product,month)

    sales_plans=[]
    for plan in plans:
        sales_plans.append({'start_date':plan.start_date,
                            'price':plan.plan,
                            'product':plan.product})
        # print(plan.start_date) 


    # sales_plans = [{'start_date':startDate,'price':price,'product':product}] * 10
    print(sales_plans)
    return render_template('_sales_plans.html', sales_plans=sales_plans)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5008',debug=True)
