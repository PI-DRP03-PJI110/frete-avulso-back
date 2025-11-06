from flask_restx import Api, Resource
from flask_jwt_extended import jwt_required

def use_auth_controller(api: Api):
    auth_schema = {'jwt': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    module = api.namespace('auth', authorizations=auth_schema, path='/auth')

    @module.route('/validate')
    class Validate(Resource):
        @jwt_required(locations=['headers'])
        @module.doc(security='jwt')
        def get(self):
            return {'ok': True}, 200