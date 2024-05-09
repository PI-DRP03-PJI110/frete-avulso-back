import datetime
import decimal
import simplejson as json

from flask_restx import Api, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity

from modules.viagem.dao import get_viagem, add_viagem, update_viagem, get_all_viagens


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime.date):
            return o.isoformat()
        return super().default(o)


def use_viagem_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('viagem', authorizations=auth_schema)
    viagem_model = api.model('Viagem', {
        'id': fields.Integer(required=False),
        'origem': fields.String(required=True),
        'destino': fields.String(required=True),
        'placa': fields.String(required=True),
        'data_viagem': fields.Date(format="iso", ),
        'valor': fields.Decimal(),
        'cpf_motorista': fields.String(required=True),
        'carga': fields.String(required=False),
        'nf': fields.String(required=False),
        'despesa': fields.String(required=False),
        'cpf_user': fields.String(required=True),
    })

    # Endpoint para login e geração de token
    @module.route('')
    class Viagem(Resource):

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            viagens = get_all_viagens()
            if viagens is None:
                return None, 500

            return json.loads(json.dumps(viagens, cls=Encoder, use_decimal=True)), 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(viagem_model)
        def post(self):
            origem = api.payload.get('origem', None)
            destino = api.payload.get('destino', None)
            placa = api.payload.get('placa', None)
            data_viagem = api.payload.get('data_viagem', None)
            valor = api.payload.get('valor', None)
            cpf_motorista = api.payload.get('cpf_motorista', None)
            carga = api.payload.get('carga', None)
            nf = api.payload.get('nf', None)
            despesa = api.payload.get('despesa', None)

            if origem is None or destino is None:
                return {'message': 'A origem e destino da viagem são obrigatórios'}, 400

            if placa is None or cpf_motorista is None:
                return {'message': 'A placa e o motorista da viagem são obrigatórios'}, 400

            if data_viagem is None or valor is None:
                return {'message': 'O valor e a data da viagem são obrigatórios'}, 400

            if origem is None or destino is None:
                return {'message': 'A origem e destino da viagem são obrigatórios'}, 400

            cpf_user = get_jwt_identity()

            nova_viagem = add_viagem(origem=origem, destino=destino, valor=valor, NF=nf, data_viagem=data_viagem,
                                     carga=carga, despesa=despesa, placa=placa, cpf_motorista=cpf_motorista,
                                     cpf_usuario=cpf_user)

            if nova_viagem is None:
                return None, 500

            return nova_viagem, 201

    @module.route('/<int:id>')
    class ViagemOnly(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self, id):
            viagem = get_viagem(id)
            if viagem is None:
                return None, 400

            return json.loads(json.dumps(viagem, cls=Encoder, use_decimal=True)), 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(viagem_model)
        def put(self, id):
            origem = api.payload.get('origem', None)
            destino = api.payload.get('destino', None)
            placa = api.payload.get('placa', None)
            data_viagem = api.payload.get('data_viagem', None)
            valor = api.payload.get('valor', None)
            cpf_motorista = api.payload.get('cpf_motorista', None)
            carga = api.payload.get('carga', None)
            nf = api.payload.get('nf', None)
            despesa = api.payload.get('despesa', None)

            old_viagem = get_viagem(id)
            cpf_usuario = old_viagem['cpf_usuario']

            if origem is None:
                origem = old_viagem['origem']

            if destino is None:
                destino = old_viagem['destino']

            if data_viagem is None:
                data_viagem = old_viagem['data_viagem']

            if valor is None:
                valor = old_viagem['valor']

            if cpf_motorista is None:
                cpf_motorista = old_viagem['cpf_motorista']

            if carga is None:
                carga = old_viagem['carga']

            if nf is None:
                nf = old_viagem['nf']

            if despesa is None:
                despesa = old_viagem['despesa']

            sucesso = update_viagem(id=id, origem=origem, destino=destino, valor=valor, NF=nf, data_viagem=data_viagem,
                                    carga=carga, despesa=despesa, placa=placa, cpf_motorista=cpf_motorista,
                                    cpf_usuario=cpf_usuario)

            if sucesso is False:
                return None, 500

            return {}, 200