from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required

from modules.motorista.dao import get_all_motoristas, get_motorista, add_motorista, update_motorista


def use_motorista_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('motorista', authorizations=auth_schema)
    motorista_model = api.model('Motorista', {
        'cpf': fields.String(required=True),
        'nome': fields.String(required=True),
    })

    # Endpoint para login e geração de token
    @module.route('')
    class Motorista(Resource):

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            motoristas = get_all_motoristas()
            if motoristas is None:
                return None, 500

            return motoristas, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(motorista_model)
        def post(self):
            cpf = api.payload.get('cpf', None)
            nome = api.payload.get('nome', None)

            if not nome or not cpf or not nome:
                return {'message': 'O cpf e o nome do motorista são obrigatórios'}, 400

            novo_motorista = add_motorista(cpf=cpf, nome=nome)

            if novo_motorista is None:
                return None, 500

            return novo_motorista, 201

    @module.route('/<string:cpf>')
    class MotoristaOnly(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self, cpf):
            motorista = get_motorista(cpf)
            if motorista is None:
                return None, 500

            return motorista, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(motorista_model)
        def put(self, cpf):
            nome = api.payload.get('nome', None)

            sucesso = update_motorista(cpf=cpf, nome=nome)

            if sucesso is False:
                return None, 500

            return {}, 200
