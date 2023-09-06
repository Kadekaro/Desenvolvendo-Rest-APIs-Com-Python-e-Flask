from flask_httpauth import HTTPBasicAuth
from flask import Flask, make_response, request
from flask_restful import Api, Resource
from flask_restful.representations import json
from models import People, Activities, Users

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# user = {'wesley': '123',
#         'kadekaro': '321'}
#
#
# @auth.verify_password
# def verification(username, password):
#     print('Validando usuário:')
#     print(user.get(username) == password)
#     if not (username, password):
#         return False
#     return user.get(username) == password


@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Users.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, name):
        try:
            person = People.query.filter_by(name=name).first()
            if person:
                response = {
                    'name': person.name,
                    'age': person.age,
                    'id': person.id
                }
            else:
                response = {'status': 'error', 'mensagem': 'Pessoa não encontrada'}
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        return response

    @staticmethod
    def post(name):
        try:
            person = People.query.filter_by(name=name).first()
            dados = request.json
            if 'name' in dados:
                person.name = dados['name']
            if 'age' in dados:
                person.age = dados['age']
            person.save()
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    @staticmethod
    def delete(name):
        try:
            person = People.query.filter_by(name=name).first()
            if person:
                mensagem = f'Pessoa {person.name} excluída com sucesso!'
                person.delete()
                response = {'Status': 'Sucesso!', 'mensagem': mensagem}
            else:
                response = {'status': 'error', 'mensagem': 'Pessoa não encontrada'}
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp


class ListPeople(Resource):
    @auth.login_required()
    def get(self):
        try:
            people = People.query.all()
            response = [{'id': person.id, 'name': person.name, 'age': person.age} for person in people]
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp


class ListActivities(Resource):
    @auth.login_required
    def get(self):
        try:
            activities = Activities.query.all()
            response = [{'id': activitie.id, 'name': activitie.name} for activitie in activities]
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    @staticmethod
    def post():
        try:
            dados = request.json
            person = People.query.filter_by(name=dados['person']).first()
            activitie = Activities(name=dados['name'], person=person)
            activitie.save()
            response = {
                'person': activitie.person.name,
                'name': activitie.name,
                'id': activitie.id
            }
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    @staticmethod
    def put():
        try:
            dados = request.json
            activity_id = dados.get('id')

            # Verifique se a atividade com o ID fornecido existe
            activity = Activities.query.get(activity_id)
            if not activity:
                return {'status': 'error', 'mensagem': 'Atividade não encontrada'}, 404

            # Atualize o nome da atividade com o novo valor
            new_name = dados.get('name')
            activity.name = new_name
            activity.save()

            response = {
                'id': activity.id,
                'name': activity.name,
                'person': activity.person.name  # Adicione o nome da pessoa relacionada, se necessário
            }
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    @staticmethod
    def delete():
        try:
            dados = request.json
            activity_id = dados.get('id')

            # Verifique se a atividade com o ID fornecido existe
            activity = Activities.query.get(activity_id)
            if not activity:
                return {'status': 'error', 'mensagem': 'Atividade não encontrada'}, 404

            # Exclua a atividade
            activity.delete()

            # Retorne uma mensagem de sucesso
            response = {'Status': 'Atividade excluída com sucesso'}
        except Exception as e:
            response = {'status': 'error', 'mensagem': str(e)}

        # Crie uma resposta com cabeçalho indicando a codificação UTF-8
        resp = make_response(json.dumps(response, ensure_ascii=False).encode('utf8'))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp


api.add_resource(Pessoa, '/pessoa/<string:name>/')
api.add_resource(ListPeople, '/listpeople/')
api.add_resource(ListActivities, '/listactivities/')

if __name__ == '__main__':
    app.run(debug=True)
