import datetime
import decimal
import simplejson as json
from typing import Any
from flask import request
from flask_restx import Api, Resource
from flask_jwt_extended import jwt_required

from modules.dashboards.dao import (
    get_viagens_mensal,
    get_resumo_financeiro,
    get_analise_despesas,
    get_analise_rotas,
    get_kpis,
    get_top_motoristas,
    get_top_veiculos,
    get_ultimas_viagens,
)


class Encoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return super().default(o)


def _ok_or_500(data):
    if data is None:
        return {"message": "Falha ao consultar as views."}, 500
    return json.loads(json.dumps(data, cls=Encoder, use_decimal=True)), 200


def use_dashboard_controller(api: Api):
    auth_schema = {"jwt": {"type": "apiKey", "in": "header", "name": "Authorization"}}
    module = api.namespace(
        "dash",
        authorizations=auth_schema,
        path="/dash",
        description="Dashboards a partir das views do banco",
    )

    @module.route("/fretes-por-periodo")
    class FretesPorPeriodo(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_viagens_mensal()
            return _ok_or_500(data)

    @module.route("/viagens-mensal")
    class ViagensMensal(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_viagens_mensal()
            return _ok_or_500(data)

    @module.route("/custos-receita")
    class CustosReceita(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_resumo_financeiro()
            return _ok_or_500(data)

    @module.route("/resumo-financeiro")
    class ResumoFinanceiro(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_resumo_financeiro()
            return _ok_or_500(data)

    @module.route("/top-clientes")
    class TopClientes(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            limit = request.args.get("limit", type=int)
            data = get_top_motoristas(limit)
            return _ok_or_500(data)

    @module.route("/top-motoristas")
    class TopMotoristas(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            limit = request.args.get("limit", type=int)
            data = get_top_motoristas(limit)
            return _ok_or_500(data)

    @module.route("/top-veiculos")
    class TopVeiculos(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            limit = request.args.get("limit", type=int)
            data = get_top_veiculos(limit)
            return _ok_or_500(data)

    @module.route("/analise-despesas")
    class AnaliseDespesas(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_analise_despesas()
            return _ok_or_500(data)

    @module.route("/analise-rotas")
    class AnaliseRotas(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_analise_rotas()
            return _ok_or_500(data)

    @module.route("/kpis")
    class KPIs(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            data = get_kpis()
            return _ok_or_500(data)

    @module.route("/ultimas-viagens")
    class UltimasViagens(Resource):
        @jwt_required(locations=["headers"])
        @module.doc(security="jwt")
        def get(self):
            limit = request.args.get("limit", default=50, type=int)
            data = get_ultimas_viagens(limit)
            return _ok_or_500(data)