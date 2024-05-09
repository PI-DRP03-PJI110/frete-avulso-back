from flask import Flask
from flask_restx import Api
from jwt import ExpiredSignatureError
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_jwt_extended import JWTManager

from modules.login.moduloUsuario import use_user_controller
from modules.login.moduloLogin import use_login_controller
from modules.motorista.moduloMotorista import use_motorista_controller
from modules.veiculo.moduloVeiculo import use_veiculo_controller
from modules.viagem.moduloViagem import use_viagem_controller

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'PI-DRP03-PJI110'  # Mantenha isso seguro na produção
app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, doc="/", title='Api frete avulso', description='Api para o projeto PI da univesp')
jwt = JWTManager(app)


@api.errorhandler(ExpiredSignatureError)
def handle_custom_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'Token expirado'}, 401


use_login_controller(api)
use_user_controller(api)
use_motorista_controller(api)
use_veiculo_controller(api)
use_viagem_controller(api)


def run():
    from waitress import serve
    serve(app)


if __name__ == '__main__':
    app.run(debug=False)
