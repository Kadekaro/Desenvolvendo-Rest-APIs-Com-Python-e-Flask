from flask_restful import Resource

habilidades = ['Python', 'Java', 'C', 'Flask']


class Habilidades(Resource):

    @staticmethod
    def get():
        return habilidades
