from flask import Blueprint, render_template, flash, redirect, url_for
from utils.decorators import login_required, admin_required
from service import admin_service

bp_admin = Blueprint('admin', __name__, url_prefix='/admin')


@bp_admin.route('/')
@login_required
@admin_required
def painel():
    try:
        dados = admin_service.obter_estatisticas_admin()
        return render_template('admin/painel.html', **dados)
    except Exception as e:
        print(f'[ERRO] admin.painel: {e}')
        flash('Erro ao carregar painel admin.', 'erro')
        return redirect(url_for('dashboard.painel'));
