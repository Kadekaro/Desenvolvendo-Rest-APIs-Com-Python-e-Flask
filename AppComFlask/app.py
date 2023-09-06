from flask import Flask, jsonify, request
import json

app = Flask(__name__)

desenvolvedores = [
    {'id': 1, 'name': 'Wesley', 'idade': 28, 'habilidades': ['Python', 'Machine Learning', 'Deep Learning']},
    {'id': 2, 'name': 'Amanda', 'idade': 26, 'habilidades': ['Python', 'Pandas', 'Flask']},
    {'id': 3, 'name': 'José', 'idade': 58, 'habilidades': ['Java', 'Kotlin', 'JS']}
]


@app.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def desenvolvedor(id):
    try:
        if request.method == 'GET':
            desenvolvedor_id = desenvolvedores[id - 1]
            # usando:  200, {'Content-Type': 'application/json; charset=utf-8'} ACEITA ACENTOS NO RETORNO DO JSON
            return jsonify(desenvolvedor_id), 200, {'Content-Type': 'application/json; charset=utf-8'}
        elif request.method == 'PUT':
            dados = json.loads(request.data)
            desenvolvedores[id - 1] = dados
            # usando:  200, {'Content-Type': 'application/json; charset=utf-8'} ACEITA ACENTOS NO RETORNO DO JSON
            return jsonify(dados), 200, {'Content-Type': 'application/json; charset=utf-8'}
        elif request.method == 'DELETE':
            desenvolvedor_id = desenvolvedores.pop(id - 1)
            return jsonify(f"Status: {desenvolvedor_id['name']}, ID:{desenvolvedor_id['id']}, deletado com sucesso!")
    except IndexError:
        print(jsonify(f'Desenvolvedor de ID: {id} não existe!'))


@app.route('/<int:id>/dev/', methods=['GET', 'POST'])
def lista_devs():
    try:
        if request.method == 'POST':
            dados = json.loads(request.data)
            desenvolvedores.append(dados)
            return jsonify(f"Status: {dados['name']} adicionado com sucesso!")
        elif request.method == 'GET':
            return jsonify(desenvolvedores)
    except Exception:
        return jsonify(f'Tipo de erro : Parâmetro de URL errado, ou pode ser outra coisa,'
                       f' avalie a estrutura de requisição')


if __name__ == '__main__':
    app.run(debug=True)
