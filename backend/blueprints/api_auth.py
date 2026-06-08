from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from service.auth_service import autenticar_usuario, registrar_usuario

api_auth = Blueprint('api_auth', __name__, url_prefix='/api/auth')


@api_auth.route('/login', methods=['POST'])
def login():
    dados = request.get_json() or {}
    email = dados.get('email', '')
    senha = dados.get('senha', '')
    usuario, erro = autenticar_usuario(email, senha)
    if erro:
        return jsonify({'erro': erro}), 401
    login_user(usuario)
    return jsonify({'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email, 'role': usuario.role})


@api_auth.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json() or {}
    usuario, erro = registrar_usuario(dados.get('nome',''), dados.get('email',''), dados.get('senha',''), dados.get('confirmar',''))
    if erro:
        return jsonify({'erro': erro}), 400
    login_user(usuario)
    return jsonify({'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email, 'role': usuario.role}), 201


@api_auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'mensagem': 'Deslogado.'})


@api_auth.route('/me')
@login_required
def me():
    return jsonify({'id': current_user.id, 'nome': current_user.nome, 'email': current_user.email, 'role': current_user.role})
