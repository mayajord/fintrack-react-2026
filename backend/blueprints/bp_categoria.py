from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from utils.decorators import login_required
from service import categoria_service
from repository.categoria_repository import listar_categorias, buscar_por_id

bp_categoria = Blueprint('categoria', __name__, url_prefix='/categorias')


@bp_categoria.route('/')
@login_required
def listar():
    try:
        categorias = listar_categorias(current_user.id)
        return render_template('categorias.html', categorias=categorias)
    except Exception as e:
        print(f'[ERRO] categoria.listar: {e}')
        flash('Erro ao carregar categorias.', 'erro')
        return redirect(url_for('dashboard.painel'))


@bp_categoria.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar():
    if request.method == 'GET':
        return render_template('cadastrar_categoria.html', categoria=None)
    try:
        _, erro = categoria_service.cadastrar_categoria(current_user.id, request.form)
        if erro:
            flash(erro, 'erro')
            return render_template('cadastrar_categoria.html', categoria=None)
        flash('Categoria criada!', 'ok')
        return redirect(url_for('categoria.listar'))
    except Exception as e:
        print(f'[ERRO] categoria.cadastrar: {e}')
        flash('Erro ao criar categoria.', 'erro')
        return render_template('cadastrar_categoria.html', categoria=None)


@bp_categoria.route('/editar/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
def editar(categoria_id):
    try:
        if request.method == 'GET':
            categoria = buscar_por_id(categoria_id)
            if not categoria or categoria.usuario_id != current_user.id:
                flash('Categoria não encontrada.', 'erro')
                return redirect(url_for('categoria.listar'))
            return render_template('cadastrar_categoria.html', categoria=categoria)
        _, erro = categoria_service.editar_categoria(current_user.id, categoria_id, request.form)
        if erro:
            flash(erro, 'erro')
            return redirect(url_for('categoria.editar', categoria_id=categoria_id))
        flash('Categoria atualizada!', 'ok')
        return redirect(url_for('categoria.listar'))
    except Exception as e:
        print(f'[ERRO] categoria.editar: {e}')
        flash('Erro ao editar categoria.', 'erro')
        return redirect(url_for('categoria.listar'))


@bp_categoria.route('/excluir/<int:categoria_id>', methods=['POST'])
@login_required
def excluir(categoria_id):
    try:
        _, erro = categoria_service.excluir_categoria(current_user.id, categoria_id)
        if erro:
            flash(erro, 'erro')
        else:
            flash('Categoria excluída.', 'ok')
    except Exception as e:
        print(f'[ERRO] categoria.excluir: {e}')
        flash('Erro ao excluir categoria.', 'erro')
    return redirect(url_for('categoria.listar'))
