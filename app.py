from flask import Flask
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
from flask_restx import Api
from flask_cors import CORS
from jwt import ExpiredSignatureError, PyJWTError
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_jwt_extended import JWTManager

from modules.login.moduloUsuario import use_user_controller
from modules.login.moduloLogin import use_login_controller
from modules.motorista.moduloMotorista import use_motorista_controller
from modules.veiculo.moduloVeiculo import use_veiculo_controller
from modules.viagem.moduloViagem import use_viagem_controller
from modules.despesa.moduloDespesa import use_Despesas_controller
from modules.auth.moduloAuth import use_auth_controller
from modules.dashboards.moduloDashboard import use_dashboard_controller

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'PI-DRP03-PJI110'
app.wsgi_app = ProxyFix(app.wsgi_app)

CORS(app)

api = Api(app, doc="/", title='Api frete avulso', description='Api para o projeto PI da univesp')
jwt = JWTManager(app)


@api.errorhandler(ExpiredSignatureError)
def handle_expire_token_exception(error):
    return {'message': 'Token expirado'}, 401


@api.errorhandler(NoAuthorizationError)
def handle_missing_token_exception(error):
    return {'message': 'Token não enviado', 'trace': error.args[0]}, 401


@api.errorhandler(JWTExtendedException)
def handle_token_error_exception(error):
    return {'message': 'Erro no token', 'trace': error.args[0]}, 401


@api.errorhandler(PyJWTError)
def handle_decode_error_exception(error):
    return {'message': 'Erro no token', 'trace': error.args[0]}, 401


@api.errorhandler(Exception)
def handle_general_error_exception(error):
    return {'message': 'Não foi possivel atender a solicitação. Erro interno', 'trace': error.args[0]}, 500


use_login_controller(api)
use_user_controller(api)
use_motorista_controller(api)
use_veiculo_controller(api)
use_viagem_controller(api)
use_Despesas_controller(api)
use_auth_controller(api)
use_dashboard_controller(api)

def run():
    from waitress import serve
    serve(app)


if __name__ == '__main__':
    app.run(debug=False)
