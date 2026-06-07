from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user
from service import auth_service

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/login', methods=['POST'])
def fazer_login():
    try:
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario, erro = auth_service.autenticar_usuario(email, senha)
        if erro:
            flash(erro, 'erro')
            return redirect(url_for('home_page'))
        login_user(usuario)
        session['usuario_nome'] = usuario.nome
        session['usuario_role'] = usuario.role
        return redirect(url_for('dashboard.painel'))
    except Exception as e:
        print(f'[ERRO] fazer_login: {e}')
        flash('Erro ao fazer login. Tente novamente.', 'erro')
        return redirect(url_for('home_page'))


@bp_auth.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        return render_template('cadastrar.html')
    try:
        nome      = request.form.get('nome')
        email     = request.form.get('email')
        senha     = request.form.get('senha')
        confirmar = request.form.get('confirmar')
        usuario, erro = auth_service.registrar_usuario(nome, email, senha, confirmar)
        if erro:
            flash(erro, 'erro')
            return render_template('cadastrar.html')
        login_user(usuario)
        session['usuario_nome'] = usuario.nome
        session['usuario_role'] = usuario.role
        return redirect(url_for('dashboard.painel'))
    except Exception as e:
        print(f'[ERRO] cadastrar_usuario: {e}')
        flash('Erro inesperado ao cadastrar. Tente novamente.', 'erro')
        return render_template('cadastrar.html')


@bp_auth.route('/logout')
def logout():
    try:
        logout_user()
        session.clear()
    except Exception as e:
        print(f'[ERRO] logout: {e}')
    return redirect(url_for('home_page'))
