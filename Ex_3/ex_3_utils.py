# Importe as classes Programmer, Skills e ProgrammerSkills do módulo ex_3_sqlalchemycomflaskesqlite
from ex_3_sqlalchemycomflaskesqlite import Programmer, Skills, ProgrammerSkills


# Função para inserir um novo programador e suas habilidades no banco de dados
def insert_programmer():
    # Solicite ao usuário que insira os detalhes do programador
    programmer = Programmer(name=input('Digite o nome: '), age=int(input('Digite a idade: ')),
                            email=input('Digite o email: '))

    # Solicite as habilidades do programador (separadas por vírgula) e crie objetos Skills para cada uma delas
    skills = Skills(name=input('Digite as habilidades, se mais de uma, coloque vírgulas para separar: '))

    # Crie um objeto ProgrammerSkills para relacionar o programador às suas habilidades
    programmer_and_skills = ProgrammerSkills(programmer=programmer, skills=skills)

    # Salve o programador, suas habilidades e a relação no banco de dados
    programmer.save()
    skills.save()
    programmer_and_skills.save()


# Função para consultar programadores e suas habilidades
def query_programmer():
    # Retorna todos os programadores e suas habilidades dentro de Programmer
    programmers = Programmer.query.all()

    if programmers:
        for programmer in programmers:
            print(f"Programmer: {programmer}")
            # Obtém e imprime as habilidades do programador
            skills = [ps.skills.name for ps in programmer.programmer_skills]
            print(f"Skills: {', '.join(skills)}")
    else:
        print("Programmer not found.")


# Função para alterar informações de um programador existente
def alter_programmer():
    update_programmer_name = input('Digite o nome do programador que quer alterar: ')
    programmer = Programmer.query.filter_by(name=update_programmer_name).first()

    if programmer:
        # Solicita ao usuário que insira as novas informações
        programmer.name = input('Digite o novo nome: ')
        programmer.age = int(input('Digite a nova idade: '))
        programmer.email = input('Digite o novo email: ')

        skills_input = input('Digite as habilidades, se mais de uma, coloque vírgulas para separar: ')
        skills_list = [skill.strip() for skill in skills_input.split(',')]

        # Remove todas as relações ProgrammerSkills existentes para este programador
        ProgrammerSkills.query.filter_by(programmer_id=programmer.id).delete()

        # Adiciona as novas habilidades ao programador e ao banco de dados
        for skill_name in skills_list:
            skill = Skills.query.filter_by(name=skill_name).first()
            if not skill:
                # Se a habilidade não existir no banco de dados, cria uma nova
                skill = Skills(name=skill_name)

            programmer_and_skills = ProgrammerSkills(programmer=programmer, skills=skill)

            # Salva as alterações no banco de dados para cada habilidade e para o programador
            skill.save()
            programmer_and_skills.save()

        # Salva as alterações finais no programador (nome, idade, email)
        programmer.save()

        print('As informações do programador foram atualizadas com sucesso!')
    else:
        print('Esse programador não existe')


# Função para remover um programador do banco de dados
def removing_programmer():
    delete = Programmer.query.filter_by(name=input('Digite o nome da pessoa que deseja excluir os dados: ')).first()
    Programmer.delete(delete)


# Verifica se o script está sendo executado como programa principal
if __name__ == '__main__':
    # Descomente e chame as funções conforme necessário para realizar diferentes operações no banco de dados
    # insert_programmer()  # Insere um novo programador
    alter_programmer()  # Altera informações de um programador existente
    # removing_programmer()  # Remove um programador do banco de dados
    query_programmer()  # Consulta e exibe programadores e suas habilidades
