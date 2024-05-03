from flask_restx import Api, Resource, fields
from flask_jwt_extended import create_access_token

from modules.login.dao import get_user_login, hash_password


def use_login_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('login', authorizations=auth_schema)
    login_model = api.model('Login', {
        'cpf': fields.String(required=True, description='Login com o documento'),
        'senha': fields.String(required=True, description='A senha para login')
    })

    # Endpoint para login e geração de token
    @module.route('')
    class UserLogin(Resource):

        @module.expect(login_model)
        def post(self):
            cpf = api.payload.get('cpf', None)
            senha = api.payload.get('senha', None)

            if not cpf or not senha:
                return {'message': 'Favor fornecer nome de usuário e senha'}, 400

            stored_user = get_user_login(cpf)
            if stored_user is None:
                return {'message': 'Usuário inválido'}, 401

            if stored_user['senha'] != hash_password(senha):
                return {'message': 'Credenciais inválidas'}, 401

            # Se as credenciais estiverem corretas, criar e retornar o token de acesso
            access_token = create_access_token(identity=cpf)
            return {'access_token': access_token}, 200
