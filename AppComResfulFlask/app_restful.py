import json
from flask import Flask, request
from flask_restful import Resource, Api
from habilidades import Habilidades

app = Flask(__name__)
api = Api(app)

desenvolvedores = [
    {'id': 1, 'name': 'Wesley', 'idade': 28, 'habilidades': ['Python', 'Machine Learning', 'Deep Learning']},
    {'id': 2, 'name': 'Amanda', 'idade': 26, 'habilidades': ['Python', 'Pandas', 'Flask']},
    {'id': 3, 'name': 'José', 'idade': 58, 'habilidades': ['Java', 'Kotlin', 'JS']}
]


# Devolve um desenvolvedor pelo id, também altera e deleta ele da lista:
class Desenvolvedor(Resource):

    @staticmethod
    def get(id):
        try:
            desenvolvedor = desenvolvedores[id - 1]
            return desenvolvedor
        except IndexError:
            return f"Status de erro: ID da URL inexistente!"
        except Exception:
            return f"Erro inesperado, tente novamente e se atente a URL"

    @staticmethod
    def put(id):
        try:
            dados = json.loads(request.data)
            desenvolvedor = desenvolvedores[id - 1]
            desenvolvedores[id - 1] = dados

            return (f"O desenvolvedor {desenvolvedor['name']} foi alterado para o desenvolvedor {dados['name']}"
                    f"\nTodos os dados do desenvolvedor: {dados}").split('\n')
        except IndexError:
            return f"Status de erro: ID da URL inexistente!"
        except Exception:
            return f"Erro inesperado, tente novamente e se atente a URL"

    @staticmethod
    def delete(id):
        try:
            desenvolvedor = desenvolvedores.pop(id - 1)
            return f"Status: o desenvolvedor -> {desenvolvedor['name']} <- foi removido com sucesso"
        except IndexError:
            return f"Status de erro: ID da URL inexistente!"
        except Exception:
            return f"Erro inesperado, tente novamente e se atente a URL"


# Retorna todos os devs dentro da lista e inseri desenvolvedores:
class ManagerDevs(Resource):

    @staticmethod
    def post():
        dados = json.loads(request.data)
        posicao = len(desenvolvedores)
        dados['id'] = posicao + 1
        desenvolvedores.append(dados)
        return f"O desenvolvedor {dados['name']} foi adicionado com sucesso!"

    @staticmethod
    def get():
        return desenvolvedores


api.add_resource(Desenvolvedor, '/dev/<int:id>/')
api.add_resource(ManagerDevs, '/manager/')
api.add_resource(Habilidades, '/habilidades/')

if __name__ == '__main__':
    app.run(debug=True)
