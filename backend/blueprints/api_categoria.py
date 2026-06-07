from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from service import categoria_service
from repository.categoria_repository import listar_categorias
from werkzeug.datastructures import ImmutableMultiDict

api_categoria = Blueprint('api_categoria', __name__, url_prefix='/api/categorias')


def serial(c):
    return {
        'id': c.id,
        'nome': c.nome,
        'icone': c.icone,
        'cor': c.cor,
        'qtd_assinaturas': len(c.assinaturas) if hasattr(c, 'assinaturas') else 0,
        'qtd_gastos': len(c.gastos) if hasattr(c, 'gastos') else 0,
    }


@api_categoria.route('/')
@login_required
def listar():
    return jsonify([serial(c) for c in listar_categorias(current_user.id)])


@api_categoria.route('/', methods=['POST'])
@login_required
def cadastrar():
    dados = request.get_json() or {}
    c, erro = categoria_service.cadastrar_categoria(current_user.id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(c)), 201


@api_categoria.route('/<int:categoria_id>', methods=['PUT'])
@login_required
def editar(categoria_id):
    dados = request.get_json() or {}
    c, erro = categoria_service.editar_categoria(current_user.id, categoria_id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(c))


@api_categoria.route('/<int:categoria_id>', methods=['DELETE'])
@login_required
def excluir(categoria_id):
    _, erro = categoria_service.excluir_categoria(current_user.id, categoria_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Categoria excluída.'})
