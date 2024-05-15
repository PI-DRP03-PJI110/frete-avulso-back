from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required

from modules.veiculo.dao import get_all_veiculos, get_veiculo, add_veiculo, update_veiculo


def use_veiculo_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('veiculo', authorizations=auth_schema)
    veiculo_model = api.model('Veiculo', {
        'placa': fields.String(required=True),
        'descricao': fields.String(required=True),
        'cpf_motorista': fields.String(required=False),
    })

    # Endpoint para login e geração de token
    @module.route('')
    class Veiculo(Resource):

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            veiculos = get_all_veiculos()
            if veiculos is None:
                return None, 500

            return veiculos, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(veiculo_model)
        def post(self):
            placa = api.payload.get('placa', None)
            descricao = api.payload.get('descricao', None)
            cpf_motorista = api.payload.get('cpf_motorista', None)

            if not placa or not descricao or not placa:
                return {'message': 'A placa e a descrição do veículo são obrigatórios'}, 400

            novo_veiculo = add_veiculo(placa=placa, descricao=descricao, cpf_motorista=cpf_motorista)

            if novo_veiculo is None:
                return None, 500

            return novo_veiculo, 201

    @module.route('/<string:placa>')
    class VeiculoOnly(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self, placa):
            veiculo = get_veiculo(placa)
            if veiculo is None:
                return None, 500

            return veiculo, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(veiculo_model)
        def put(self, placa):
            descricao = api.payload.get('descricao', None)
            cpf_motorista = api.payload.get('cpf_motorista', None)

            old_veiculo = get_veiculo(placa)

            if not descricao:
                descricao = old_veiculo['descricao']

            if not cpf_motorista:
                cpf_motorista = old_veiculo['cpf_motorista']

            sucesso = update_veiculo(placa=placa, descricao=descricao, cpf_motorista=cpf_motorista)

            if sucesso is False:
                return None, 500

            return {}, 200
