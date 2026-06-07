import os
from flask import Flask, jsonify
from flask_cors import CORS
from extensao import db, login_manager
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-secreta-dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///fintrack.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Permite o frontend React acessar o backend
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:3000'])

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = None

@login_manager.unauthorized_handler
def nao_autorizado():
    return jsonify({'erro': 'Faça login primeiro.'}), 401

import modelos

# Blueprints da API
from blueprints.api_auth import api_auth
from blueprints.api_dashboard import api_dashboard
from blueprints.api_boleto import api_boleto
from blueprints.api_assinatura import api_assinatura
from blueprints.api_categoria import api_categoria
from blueprints.api_gasto import api_gasto
from blueprints.api_admin import api_admin
from blueprints.api_relatorio import api_relatorio

app.register_blueprint(api_auth)
app.register_blueprint(api_dashboard)
app.register_blueprint(api_boleto)
app.register_blueprint(api_assinatura)
app.register_blueprint(api_categoria)
app.register_blueprint(api_gasto)
app.register_blueprint(api_admin)
app.register_blueprint(api_relatorio)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
