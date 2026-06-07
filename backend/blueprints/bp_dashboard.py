from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from service import dashboard_service
from utils.decorators import login_required

bp_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp_dashboard.route('/')
@login_required
def painel():
    try:
        dados = dashboard_service.montar_dashboard(current_user.id)
        return render_template('dashboard.html', **dados)
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash('Erro ao carregar dashboard.', 'erro')
        return redirect(url_for('home_page'))
