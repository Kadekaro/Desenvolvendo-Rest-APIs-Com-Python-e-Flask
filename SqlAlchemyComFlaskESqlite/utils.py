import html
from models import People, Activities, Users


def insert_people():
    person = People(name=html.escape('Chaves'), age=90)
    print(person)
    person.save()


def insert_users(login, senha):
    user = Users(login=login, senha=senha)
    user.save()


def query_users():
    user = Users.query.all()
    print(user)


def alter_people():
    person = People.query.filter_by(name='Chaves').first()
    person.name = html.escape('Alessandra')
    person.age = 35
    person.save()


def query_people():
    person = People.query.all()
    # person = People.query.filter_by(name='Chaves').first()
    # print(person.age)
    # print(f"ID:{person.id}, Name: {person.name}, Age: {person.age}")
    print(person)


def removing_people():
    person = People.query.filter_by(name='Alessandra').first()
    print(person)
    People.delete(person)


def query_activities():
    activities = Activities.query.all()
    print(activities)


if __name__ == '__main__':
    # insert_people()
    insert_users('marcos', 'mecanico')
    insert_users('marcia', 'chata')
    query_users()
    # query_people()
    # alter_people()
    # removing_people()
    # query_activities()
