import datetime
import decimal
import simplejson as json

from flask_restx import Api, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity

from modules.despesa.dao import get_despesa, add_despesa, get_all_despesa, update_despesa, excluir_despesa_de_viagem


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
        'ID_viagem': fields.Integer(required=False)
    })

    @module.route('')
    class Despesa(Resource):

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            despesa = get_all_despesa()
            if despesa is None:
                return None, 500

            return json.loads(json.dumps(despesa, cls=Encoder, use_decimal=True)), 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(Despesa_model)
        def post(self):
            descricao = api.payload.get('descricao', None)
            valor = api.payload.get('valor', None)
            ID_viagem = api.payload.get('ID_viagem', None)

            if not ID_viagem:
                return {'message': 'O id da viagem é obrigatório'}, 400

            if not valor:
                return {'message': 'O valor da despesa é obrigatório'}, 400

            if not descricao or len(descricao) == 0:
                return {'message': 'A descrição da despesa é obrigatório'}, 400

            cpf_user = get_jwt_identity()

            nova_despesa = add_despesa(descricao=descricao, valor=valor, viagem=ID_viagem)

            if nova_despesa is None:
                return None, 500

            return nova_despesa, 201

    @module.route('/<int:id>')
    class DespesaOnly(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self, id):
            Despesa = get_despesa(id)
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
            viagem = api.payload.get('ID_viagem',None)

            old_Despesa = get_despesa(id)

            if not descricao:
                descricao = old_Despesa['descricao']

            if not valor:
                valor = old_Despesa['valor']

            if not viagem:
                viagem = old_Despesa['ID_viagem']

            sucesso = update_despesa(id=ID_despesa, descricao=descricao, valor=valor, viagem=viagem,)

            if sucesso is False:
                return None, 500

            return {}, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def delete(self, id):

            sucesso = excluir_despesa_de_viagem(id)

            if sucesso is False:
                return None, 500

            return {}, 200