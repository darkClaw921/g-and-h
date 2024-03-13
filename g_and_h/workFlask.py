from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
import postgreWork
from pprint import pprint  

app = Flask(__name__)
api = Api(app, version='1.0', title='G&H API',description='A G&H API',)


@api.route('/update')
class Update_entity(Resource):
    def Post(self,):
        """Обновление сущности"""

        data = request.get_json() 
        pprint(data)

        return 'OK'
    
@api.route('/create')
class Create_entity(Resource):
    def Post(self,):
        """Создание сущности"""
        
        data = request.get_json() 
        pprint(data)

        return 'OK'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)