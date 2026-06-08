from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from utils.decorators import login_required
from service import gasto_service
from repository.gasto_repository import buscar_por_id, listar_gastos, total_mes_atual
from repository.categoria_repository import listar_categorias
from datetime import date

bp_gasto = Blueprint('gasto', __name__, url_prefix='/gastos')


@bp_gasto.route('/')
@login_required
def listar():
    try:
        gastos = listar_gastos(current_user.id)
        total_mes = total_mes_atual(current_user.id)
        return render_template('gastos.html', gastos=gastos, total_mes=total_mes)
    except Exception as e:
        print(f'[ERRO] gasto.listar: {e}')
        flash('Erro ao carregar gastos.', 'erro')
        return redirect(url_for('dashboard.painel'))


@bp_gasto.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    try:
        categorias = listar_categorias(current_user.id)
        if request.method == 'GET':
            return render_template('cadastrar_gasto.html',
                                   gasto=None, categorias=categorias,
                                   today=date.today().isoformat())
        _, erro = gasto_service.cadastrar_gasto(current_user.id, request.form)
        if erro:
            flash(erro, 'erro')
            return render_template('cadastrar_gasto.html',
                                   gasto=None, categorias=categorias,
                                   today=date.today().isoformat())
        flash('Gasto cadastrado!', 'ok')
        return redirect(url_for('gasto.listar'))
    except Exception as e:
        print(f'[ERRO] gasto.cadastrar: {e}')
        flash('Erro ao cadastrar gasto.', 'erro')
        return redirect(url_for('gasto.listar'))


@bp_gasto.route('/editar/<int:gasto_id>', methods=['GET', 'POST'])
@login_required
def editar(gasto_id):
    try:
        categorias = listar_categorias(current_user.id)
        if request.method == 'GET':
            g = buscar_por_id(gasto_id)
            if not g or g.usuario_id != current_user.id:
                flash('Gasto não encontrado.', 'erro')
                return redirect(url_for('gasto.listar'))
            return render_template('cadastrar_gasto.html',
                                   gasto=g, categorias=categorias,
                                   today=date.today().isoformat())
        _, erro = gasto_service.editar_gasto(current_user.id, gasto_id, request.form)
        if erro:
            flash(erro, 'erro')
            return redirect(url_for('gasto.editar', gasto_id=gasto_id))
        flash('Gasto atualizado!', 'ok')
        return redirect(url_for('gasto.listar'))
    except Exception as e:
        print(f'[ERRO] gasto.editar: {e}')
        flash('Erro ao editar gasto.', 'erro')
        return redirect(url_for('gasto.listar'))


@bp_gasto.route('/excluir/<int:gasto_id>', methods=['POST'])
@login_required
def excluir(gasto_id):
    try:
        _, erro = gasto_service.excluir_gasto(current_user.id, gasto_id)
        if erro:
            flash(erro, 'erro')
        else:
            flash('Gasto excluído.', 'ok')
    except Exception as e:
        print(f'[ERRO] gasto.excluir: {e}')
        flash('Erro ao excluir gasto.', 'erro')
    return redirect(url_for('gasto.listar'))
