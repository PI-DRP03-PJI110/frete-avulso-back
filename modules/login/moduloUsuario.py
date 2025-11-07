from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required

from modules.login.dao import get_user, add_user, update_user, get_all_users, hash_password


def use_user_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('usuario', authorizations=auth_schema)
    user_model = api.model('Usuario', {
        'cpf': fields.String(required=True),
        'nome': fields.String(required=True),
        'email': fields.String(required=True),
        'funcao': fields.String(required=False),
        'endereco': fields.String(required=False),
        'senha': fields.String(required=True)
    })

    @module.route('')
    class User(Resource):

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            users = get_all_users()
            if users is None:
                return None, 500

            return users, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(user_model)
        def post(self):
            cpf = api.payload.get('cpf', None)
            email = api.payload.get('email', None)
            nome = api.payload.get('nome', None)
            endereco = api.payload.get('endereco', None)
            funcao = api.payload.get('funcao', None)
            senha = api.payload.get('senha', None)

            if not nome or not cpf or not senha:
                return {'message': 'O cpf, nome de usuário e senha são obrigatórios'}, 400

            senha = hash_password(senha)

            novo_usuario = add_user(cpf=cpf, nome=nome, funcao=funcao, endereco=endereco, senha=senha, email=email)

            if novo_usuario is None:
                return None, 500

            return novo_usuario, 201

    @module.route('/<string:cpf>')
    class UserOnly(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self, cpf):
            usuario = get_user(cpf)
            if usuario is None:
                return None, 500

            return usuario, 200

        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        @module.expect(user_model)
        def put(self, cpf):
            nome = api.payload.get('nome', None)
            email = api.payload.get('email', None)
            funcao = api.payload.get('funcao', None)
            endereco = api.payload.get('endereco', None)
            senha = api.payload.get('senha', None)

            old_user = get_user(cpf)
            if not nome:
                nome = old_user['nome']

            if not email:
                email = old_user['email']

            if not funcao:
                funcao = old_user['funcao']

            if not endereco:
                endereco = old_user['endereco']

            if not senha:
                senha = hash_password(senha)
            else:
                senha = old_user['senha']

            sucesso = update_user(cpf=cpf, nome=nome, funcao=funcao, endereco=endereco, senha=senha, email=email)

            if sucesso is False:
                return None, 500

            return {}, 200
