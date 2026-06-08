from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from service import gasto_service
from repository.gasto_repository import listar_gastos, total_mes_atual
from werkzeug.datastructures import ImmutableMultiDict

api_gasto = Blueprint('api_gasto', __name__, url_prefix='/api/gastos')


def serial(g):
    return {
        'id': g.id,
        'descricao': g.descricao,
        'valor': float(g.valor),
        'data': g.data.strftime('%Y-%m-%d'),
        'recorrente': g.recorrente,
        'categoria_id': g.categoria_id,
        'categoria_nome': g.categoria.nome if g.categoria else None,
    }


@api_gasto.route('/')
@login_required
def listar():
    gastos = listar_gastos(current_user.id)
    total = total_mes_atual(current_user.id)
    return jsonify({
        'gastos': [serial(g) for g in gastos],
        'total_mes': float(total or 0),
    })


@api_gasto.route('/', methods=['POST'])
@login_required
def cadastrar():
    dados = request.get_json() or {}
    g, erro = gasto_service.cadastrar_gasto(current_user.id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(g)), 201


@api_gasto.route('/<int:gasto_id>', methods=['PUT'])
@login_required
def editar(gasto_id):
    dados = request.get_json() or {}
    g, erro = gasto_service.editar_gasto(current_user.id, gasto_id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(g))


@api_gasto.route('/<int:gasto_id>', methods=['DELETE'])
@login_required
def excluir(gasto_id):
    _, erro = gasto_service.excluir_gasto(current_user.id, gasto_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Gasto excluído.'})
