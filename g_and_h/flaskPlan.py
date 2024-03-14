from flask import Flask, render_template, request
import requests
app = Flask(__name__)

# Список доступных продуктов
products = ["ЛОМ", "НЕЛИКВИД"]
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
    return render_template('form.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5008',debug=True)
