from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
import postgreWork
from pprint import pprint  
from datetime import datetime
import workBitrix

app = Flask(__name__)
api = Api(app, version='1.0', title='G&H API',description='A G&H API',)


@api.route('/update')
class Update_entity(Resource):
    def post(self,):
        """Обновление сущности"""
        
        data = request.get_json() 
        pprint(data)

        return 'OK'
@api.route('/pay')
class task_entity(Resource):
    def post(self,):
        """Обновление сущности"""
        

        # ImmutableMultiDict([('event', 'ONCRMDYNAMICITEMUPDATE'), ('data[FIELDS][ID]', '87'), ('data[FIELDS][ENTITY_TYPE_ID]', '155'), ('ts', '1715004068')])
        data = request.form
        pprint(data)
        dealID=data['data[FIELDS][ID]']
        deal=workBitrix.find_deal(dealID)

        status=deal['STATUS_SEMANTIC_ID']
        if status != 'S': return 'No'

        department=deal[workBitrix.Deal.department]

        #TODO нужно получить/создать поле с метрикой
        metrick=''
        month=datetime.now().month
        plan=postgreWork.get_plan_for_month(product=metrick, month=month,
                                        department=department)
        planID=plan[0].id
        fields={
            'fackt':deal['OPPORTUNITY']
        }
        # TODO: нужно узнать какой диапазон обнавлять месяц или неделя
        # postgreWork.update_plan(planID, fields=fields)

        


        enityID=data['data[FIELDS][ENTITY_TYPE_ID]']
        if enityID != '155': return 'Not pay'
        

        # workBitrix.main(enityID, PAY_ID)
        # print(f"{enityID=}")
        # pprint(data)
        
        # pprint(a)

        return 'OK'   
@api.route('/create')
class Create_entity(Resource):
    def post(self,):
        """Создание сущности"""

        data = request.get_json() 
        pprint(data)

        return 'OK'

@app.route('/sales_plans')
def get_sales_plans():
    sales_plans = [{'start_date':'2021-10-01','price':1000,'type':'Лом'}]
    return render_template('_sales_plans.html', sales_plans=sales_plans)
 
@api.route('/plan')
@api.doc(description='Возвращает список доступных бирж')
class Plan(Resource):
    def get(self,):
        """План продаж"""

        data = request.get_json() 
        pprint(data)

        return 'OK'
    def post(self):
        """План продаж"""

        data = request.get_json() 
        pprint(data)
        #TODO переделать под zip
        for i in range(len(data['start_date'])):
            date=datetime.strptime(data['start_date'][i], '%Y-%m-%d')
            fields={
                'start_date':date,
                'plan':float(data['plan'][i]),
                'product':data['product'][i],
                'department':data['department'][i],
                'fackt':float(data['fackt'][i]) if data['fackt'][i] != '' else 0,
                'metrik':data['metrick'][i],
                'diapazon':data['metrikMonth'][i],
            }

            check=postgreWork.get_plan_for_month_check(product=fields['product'], 
                                                 date=fields['start_date'], 
                                                 department=fields['department'], 
                                                 metrik=fields['metrik'], 
                                                 diapazon=fields['diapazon'])
            if len(check)==0:
                postgreWork.add_plan(fields=fields)
            
            else:    
                if fields['plan'] == 0:
                    fields['plan']=check[0].plan

                if fields['fackt'] == 0:
                    fields['fackt']=check[0].fackt


                postgreWork.update_plan(check[0].id, fields=fields)
            # fields={
            #     'close_date':data['start_date'][i],
                
            # }
            # postgreWork.add_deal(fields=fields)
 
        return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5002',debug=True)
    
