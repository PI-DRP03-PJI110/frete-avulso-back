import datetime
import decimal
import simplejson as json

from flask_restx import Api, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity

from modules.despesa.dao import get_despesa, add_despesa, get_all_despesa, excluir_despesa_de_viagem


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime.date):
            return o.isoformat()
        return super().default(o)


def use_Despesas_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('despesa', authorizations=auth_schema)
    Despesa_model = api.model('despesa', {
        'ID_despesa': fields.Integer(required=False),
        'descricao': fields.String(required=False),
        'valor': fields.Fixed(decimals=2),
        'viagem': fields.Integer(required=False)
    })

    # Endpoint para login e geração de token
    @module.route('')
    class Despesa(Resource):

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            Despesa = get_all_Despesa()
            if Despesa is None:
                return None, 500

            return json.loads(json.dumps(Despesa, cls=Encoder, use_decimal=True)), 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(Despesa_model)
        def post(self):
            ID_despesa = api.payload.get('ID_despesa', None)
            descricao = api.payload.get('descricao', None)
            valor = api.payload.get('valor', None)
            viagem = api.payload.get('viagem',None)
            if not ID_despesa or not Despesa:
                return {'message': 'o ID e a Despesa são obrigatórios'}, 400

            cpf_user = get_jwt_identity()

            nova_Despesa = add_Despesa(descricao=descricao, valor=valor)

            if nova_Despesa is None:
                return None, 500

            return nova_Despesa, 201

    @module.route('/<int:id>')
    class DespesaOnly(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self, id):
            Despesa = get_Despesa(id)
            if Despesa is None:
                return None, 400

            return json.loads(json.dumps(Despesa, cls=Encoder, use_decimal=True)), 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(Despesa_model)
        def put(self, id):
            ID_despesa = api.payload.get('ID_despesa', None)
            descricao = api.payload.get('descricao', None)
            valor = api.payload.get('valor', None)
            viagem = api.payload.get('viagem',None)

            old_Despesa = get_Despesa(id)
            cpf_usuario = old_Despesa['cpf_usuario']

            if not Despesa:
                Despesa = old_Despesa['despesa']

            if not valor:
                valor = old_valor['valor']

            sucesso = update_Despesa(ID_despesa=ID_despesa, descricao=descricao, valor=valor, viagem=viagem,)

            if sucesso is False:
                return None, 500

            return {}, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def delete(self, id):

            sucesso = excluir_Despesa_de_viagem(ID_despesa=ID_despesa)

            if sucesso is False:
                return None, 500

            return {}, 200