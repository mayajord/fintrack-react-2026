from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from service import assinatura_service
from werkzeug.datastructures import ImmutableMultiDict

api_assinatura = Blueprint('api_assinatura', __name__, url_prefix='/api/assinaturas')


def serial(s):
    return {
        'id': s.id,
        'nome': s.nome,
        'valor': float(s.valor),
        'ciclo': s.ciclo,
        'dia_vencimento': s.dia_vencimento,
        'status': s.status,
        'notas': s.notas,
        'categoria_id': s.categoria_id,
        'categoria_nome': s.categoria.nome if s.categoria else None,
        'desde': s.desde.strftime('%Y-%m-%d') if s.desde else None,
        'valor_mensal': float(s.valor_mensal()),
    }


@api_assinatura.route('/')
@login_required
def listar():
    assinaturas, total = assinatura_service.obter_assinaturas_com_total(current_user.id)
    return jsonify({
        'assinaturas': [serial(s) for s in assinaturas],
        'total_mensal': float(total),
    })


@api_assinatura.route('/', methods=['POST'])
@login_required
def cadastrar():
    dados = request.get_json() or {}
    s, erro = assinatura_service.cadastrar_assinatura(current_user.id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(s)), 201


@api_assinatura.route('/<int:assinatura_id>', methods=['PUT'])
@login_required
def editar(assinatura_id):
    dados = request.get_json() or {}
    s, erro = assinatura_service.editar_assinatura(current_user.id, assinatura_id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(s))


@api_assinatura.route('/<int:assinatura_id>', methods=['DELETE'])
@login_required
def excluir(assinatura_id):
    _, erro = assinatura_service.excluir_assinatura(current_user.id, assinatura_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Assinatura excluída.'})


@api_assinatura.route('/<int:assinatura_id>/status', methods=['POST'])
@login_required
def alternar_status(assinatura_id):
    _, erro = assinatura_service.alternar_status_assinatura(current_user.id, assinatura_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Status alterado.'})
