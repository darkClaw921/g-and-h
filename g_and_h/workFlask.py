from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
import postgreWork
from pprint import pprint  

app = Flask(__name__)
api = Api(app, version='1.0', title='G&H API',description='A G&H API',)


@api.route('/update')
class Update_entity(Resource):
    def post(self,):
        """Обновление сущности"""

        data = request.get_json() 
        pprint(data)

        return 'OK'
    
@api.route('/create')
class Create_entity(Resource):
    def post(self,):
        """Создание сущности"""

        data = request.get_json() 
        pprint(data)

        return 'OK'

    
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
        
            fields={
                'start_date':data['start_date'][i],
                'price':data['amount'][i],
                'type':data['product'][i]
            }
            postgreWork.add_plan(fields=fields)
            # fields={
            #     'close_date':data['start_date'][i],
                
            # }
            # postgreWork.add_deal(fields=fields)
 
        return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5002',debug=True)