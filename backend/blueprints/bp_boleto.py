from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from utils.decorators import login_required
from service import boleto_service
from repository.boleto_repository import buscar_por_id
from repository.categoria_repository import listar_categorias
from datetime import date

bp_boleto = Blueprint('boleto', __name__, url_prefix='/boletos')


@bp_boleto.route('/')
@login_required
def listar():
    try:
        dados = boleto_service.obter_boletos_com_estatisticas(current_user.id)
        return render_template('boletos.html',
            boletos=dados['boletos'], pendentes=dados['pendentes'],
            pagos=dados['pagos'], vencidos=dados['vencidos'],
            today=dados['hoje'], qtd_pendentes=dados['qtd_pendentes'],
            qtd_urgentes=dados['qtd_urgentes'], total_urgentes=dados['total_urgentes'],
            qtd_vencidos=dados['qtd_vencidos'], qtd_pagos=dados['qtd_pagos'],
            total_aberto=dados['total_aberto'], total_pago=dados['total_pago'])
    except Exception as e:
        print(f'[ERRO] boleto.listar: {e}')
        flash('Erro ao carregar boletos.', 'erro')
        return redirect(url_for('dashboard.painel'))


@bp_boleto.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    try:
        categorias = listar_categorias(current_user.id)
        if request.method == 'GET':
            return render_template('cadastrar_boleto.html',
                                   boleto=None, categorias=categorias,
                                   today=date.today().isoformat())
        _, erro = boleto_service.cadastrar_boleto(current_user.id, request.form)
        if erro:
            flash(erro, 'erro')
            return render_template('cadastrar_boleto.html',
                                   boleto=None, categorias=categorias,
                                   today=date.today().isoformat())
        flash('Boleto cadastrado!', 'ok')
        return redirect(url_for('boleto.listar'))
    except Exception as e:
        print(f'[ERRO] boleto.cadastrar: {e}')
        flash('Erro ao cadastrar boleto.', 'erro')
        return redirect(url_for('boleto.listar'))


@bp_boleto.route('/editar/<int:boleto_id>', methods=['GET', 'POST'])
@login_required
def editar(boleto_id):
    try:
        categorias = listar_categorias(current_user.id)
        if request.method == 'GET':
            b = buscar_por_id(boleto_id)
            if not b or b.usuario_id != current_user.id:
                flash('Boleto não encontrado.', 'erro')
                return redirect(url_for('boleto.listar'))
            return render_template('cadastrar_boleto.html',
                                   boleto=b, categorias=categorias,
                                   today=date.today().isoformat())
        _, erro = boleto_service.editar_boleto(current_user.id, boleto_id, request.form)
        if erro:
            flash(erro, 'erro')
            return redirect(url_for('boleto.editar', boleto_id=boleto_id))
        flash('Boleto atualizado!', 'ok')
        return redirect(url_for('boleto.listar'))
    except Exception as e:
        print(f'[ERRO] boleto.editar: {e}')
        flash('Erro ao editar boleto.', 'erro')
        return redirect(url_for('boleto.listar'))


@bp_boleto.route('/pagar/<int:boleto_id>', methods=['POST'])
@login_required
def pagar(boleto_id):
    try:
        _, erro = boleto_service.pagar_boleto(current_user.id, boleto_id)
        if erro:
            flash(erro, 'erro')
        else:
            flash('Boleto marcado como pago!', 'ok')
    except Exception as e:
        print(f'[ERRO] boleto.pagar: {e}')
        flash('Erro ao marcar boleto como pago.', 'erro')
    return redirect(url_for('boleto.listar'))


@bp_boleto.route('/reabrir/<int:boleto_id>', methods=['POST'])
@login_required
def reabrir(boleto_id):
    try:
        _, erro = boleto_service.reabrir_boleto(current_user.id, boleto_id)
        if erro:
            flash(erro, 'erro')
        else:
            flash('Boleto reaberto.', 'ok')
    except Exception as e:
        print(f'[ERRO] boleto.reabrir: {e}')
        flash('Erro ao reabrir boleto.', 'erro')
    return redirect(url_for('boleto.listar'))


@bp_boleto.route('/excluir/<int:boleto_id>', methods=['POST'])
@login_required
def excluir(boleto_id):
    try:
        _, erro = boleto_service.excluir_boleto(current_user.id, boleto_id)
        if erro:
            flash(erro, 'erro')
        else:
            flash('Boleto excluído.', 'ok')
    except Exception as e:
        print(f'[ERRO] boleto.excluir: {e}')
        flash('Erro ao excluir boleto.', 'erro')
    return redirect(url_for('boleto.listar'))
