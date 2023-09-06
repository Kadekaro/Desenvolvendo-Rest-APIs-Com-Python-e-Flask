import json

from flask import request, Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

habilidades = ['Python', 'Java', 'C', 'Flask']


class Habilidades(Resource):

    @staticmethod
    def get():
        return habilidades

    @staticmethod
    def post():
        dados = json.loads(request.data)
        if len(dados) == 1:
            habilidades.append(dados)
        elif len(dados) > 1:
            habilidades.extend(dados)
        return f"{habilidades}"


class ManagerAbility(Resource):

    @staticmethod
    def put(id):
        dados = json.loads(request.data)
        habilidades[id-1] = dados
        return f"A habilidade no índice {id} foi substituída por: {dados}"

    @staticmethod
    def delete(id):
        habilidade = habilidades.pop(id-1)
        return f"Status: Habilidade {habilidade} deletado com sucesso!"


api.add_resource(Habilidades, '/habilidades/')
api.add_resource(ManagerAbility, '/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
