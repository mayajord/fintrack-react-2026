from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from service import assinatura_service
from repository.categoria_repository import listar_categorias
from repository.assinatura_repository import buscar_por_id
from utils.decorators import login_required

bp_assinatura = Blueprint('assinatura', __name__, url_prefix='/assinaturas')


@bp_assinatura.route('/')
@login_required
def listar():
    try:
        assinaturas, total_mensal = assinatura_service.obter_assinaturas_com_total(current_user.id)
        return render_template('assinaturas.html',
                               assinaturas=assinaturas, total_mensal=total_mensal)
    except Exception as e:
        print(f'[ERRO] assinatura.listar: {e}')
        flash('Erro ao carregar assinaturas.', 'erro')
        return redirect(url_for('dashboard.painel'))


@bp_assinatura.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'GET':
        categorias = listar_categorias(current_user.id)
        return render_template('cadastrar_assinatura.html',
                               assinatura=None, categorias=categorias)
    try:
        assinatura, erro = assinatura_service.cadastrar_assinatura(current_user.id, request.form)
        if erro:
            flash(erro, 'erro')
            return redirect(url_for('assinatura.cadastrar'))
        flash('Assinatura cadastrada com sucesso.', 'ok')
        return redirect(url_for('assinatura.listar'))
    except Exception as e:
        print(f'[ERRO] assinatura.cadastrar: {e}')
        flash('Erro ao cadastrar assinatura.', 'erro')
        return redirect(url_for('assinatura.cadastrar'))


@bp_assinatura.route('/editar/<int:assinatura_id>', methods=['GET', 'POST'])
@login_required
def editar(assinatura_id):
    try:
        if request.method == 'GET':
            s = buscar_por_id(assinatura_id)
            if not s or s.usuario_id != current_user.id:
                flash('Assinatura não encontrada.', 'erro')
                return redirect(url_for('assinatura.listar'))
            categorias = listar_categorias(current_user.id)
            return render_template('cadastrar_assinatura.html',
                                   assinatura=s, categorias=categorias)
        assinatura, erro = assinatura_service.editar_assinatura(
            current_user.id, assinatura_id, request.form)
        if erro:
            flash(erro, 'erro')
            return redirect(url_for('assinatura.editar', assinatura_id=assinatura_id))
        flash('Assinatura atualizada.', 'ok')
        return redirect(url_for('assinatura.listar'))
    except Exception as e:
        print(f'[ERRO] assinatura.editar: {e}')
        flash('Erro ao editar assinatura.', 'erro')
        return redirect(url_for('assinatura.listar'))


@bp_assinatura.route('/status/<int:assinatura_id>', methods=['POST'])
@login_required
def alternar_status(assinatura_id):
    try:
        _, erro = assinatura_service.alternar_status_assinatura(current_user.id, assinatura_id)
        if erro:
            flash(erro, 'erro')
    except Exception as e:
        print(f'[ERRO] assinatura.alternar_status: {e}')
        flash('Erro ao alterar status.', 'erro')
    return redirect(url_for('assinatura.listar'))


@bp_assinatura.route('/excluir/<int:assinatura_id>', methods=['POST'])
@login_required
def excluir(assinatura_id):
    try:
        _, erro = assinatura_service.excluir_assinatura(current_user.id, assinatura_id)
        if erro:
            flash(erro, 'erro')
        else:
            flash('Assinatura excluída.', 'ok')
    except Exception as e:
        print(f'[ERRO] assinatura.excluir: {e}')
        flash('Erro ao excluir assinatura.', 'erro')
    return redirect(url_for('assinatura.listar'))
