from flask import Flask, request, jsonify
import json

api = Flask(__name__)

lista_tarefas = [
    {'id': 1, 'responsavel': 'Bartolomeo Kuma', 'tarefa': 'Ajudar os Mugiwara a fugir', 'status': 'Concluído'},
    {'id': 2, 'responsavel': 'Akaino', 'tarefa': 'Matar o ACE', 'status': 'Concluído'},
    {'id': 3, 'responsavel': 'Luffy', 'tarefa': 'Salvar o ACE', 'status': 'Nao-Concluído'},
    {'id': 4, 'responsavel': 'Luffy', 'tarefa': 'Se tornar o Rei dos Piratas', 'status': 'Em Andamento'}]


@api.route('/tarefa/', methods=['GET', 'POST'])
def tarefas():
    try:
        if request.method == 'GET':
            return jsonify(lista_tarefas)

        elif request.method == 'POST':
            dados = json.loads(request.data)
            lista_tarefas.append(dados)
            return (
                f"Nova tarefa '{dados['tarefa']}'"
                f"\nResponsável: {dados['responsavel']}"
                f"\nStatus: Cadastrada com sucesso!")

    except Exception:
        return jsonify(f"Não é possível realizar uma pesquisa individual das tarefas e nem mesmo alterar qualquer"
                       f" coisa além do status")


@api.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def task_manager(id):
    try:
        if request.method == 'GET':
            tarefa = lista_tarefas[id - 1]
            return jsonify(tarefa)

        elif request.method == 'PUT':
            dados = json.loads(request.data)
            tarefa_atual = lista_tarefas[id - 1]

            if 'status' in dados and dados['status'] != tarefa_atual['status']:
                tarefa_atual['status'] = dados['status']
                return jsonify(f"Status da tarefa do responsável {dados['responsavel']} mudados com sucesso!")

            else:
                return jsonify(f"Só é permitido mudar o status da tarefa do responsável!")

        elif request.method == 'DELETE':
            lista_tarefas.pop(id - 1)
            return jsonify(f"Tarefa retirada com sucesso!")

    except IndexError:
        return jsonify(f"O index da URL está fora do tamanho da lista de tarefas, "
                       f"coloque um que esteja dentro da lista!")


if __name__ == '__main__':
    api.run(debug=True)
