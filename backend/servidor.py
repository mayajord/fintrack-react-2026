import os
from flask import Flask, render_template
from blueprints import bp_relatorio
from extensao import db, login_manager
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///fintrack.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'home_page'

import modelos

from blueprints.bp_auth import bp_auth
from blueprints.bp_dashboard import bp_dashboard
from blueprints.bp_boleto import bp_boleto
from blueprints.bp_assinatura import bp_assinatura
from blueprints.bp_categoria import bp_categoria
from blueprints.bp_gasto import bp_gasto
from blueprints.bp_admin import bp_admin
from blueprints.bp_relatorio import bp_relatorio

app.register_blueprint(bp_auth)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_boleto)
app.register_blueprint(bp_assinatura)
app.register_blueprint(bp_categoria)
app.register_blueprint(bp_gasto)
app.register_blueprint(bp_admin)
app.register_blueprint(bp_relatorio)

@app.context_processor
def inject_now():
    from datetime import datetime
    from flask_login import current_user
    from service.dashboard_service import montar_dashboard
    dados = {'now': datetime.now()}
    if current_user.is_authenticated:
        try:
            dash = montar_dashboard(current_user.id)
            dados['qtd_alertas'] = dash['qtd_alertas']
        except:
            dados['qtd_alertas'] = 0
    return dados

@app.template_filter('data_ptbr')
def data_ptbr(valor):
    dias = ['Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo']
    meses = ['','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    return f"{dias[valor.weekday()]}, {valor.day:02d} de {meses[valor.month]} de {valor.year}"

@app.route('/')
def home_page():
    return render_template('login.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
