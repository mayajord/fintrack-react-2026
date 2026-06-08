from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from service import boleto_service
from werkzeug.datastructures import ImmutableMultiDict
from datetime import date

api_boleto = Blueprint('api_boleto', __name__, url_prefix='/api/boletos')


def serial(b):
    hoje = date.today()
    dias = (b.vencimento - hoje).days if b.status == 'pendente' else None
    return {
        'id': b.id,
        'nome': b.nome,
        'valor': float(b.valor),
        'vencimento': b.vencimento.strftime('%Y-%m-%d'),
        'descricao': b.descricao,
        'codigo_barra': b.codigo_barra,
        'notas': b.notas,
        'status': b.status,
        'categoria_id': b.categoria_id,
        'categoria_nome': b.categoria.nome if b.categoria else None,
        'dias_para_vencer': dias,
    }


@api_boleto.route('/')
@login_required
def listar():
    dados = boleto_service.obter_boletos_com_estatisticas(current_user.id)
    return jsonify({
        'boletos': [serial(b) for b in dados['boletos']],
        'total_aberto': float(dados['total_aberto']),
        'total_pago': float(dados['total_pago']),
        'qtd_pendentes': dados['qtd_pendentes'],
        'qtd_urgentes': dados['qtd_urgentes'],
        'qtd_vencidos': dados['qtd_vencidos'],
        'qtd_pagos': dados['qtd_pagos'],
    })


@api_boleto.route('/', methods=['POST'])
@login_required
def cadastrar():
    dados = request.get_json() or {}
    b, erro = boleto_service.cadastrar_boleto(current_user.id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(b)), 201


@api_boleto.route('/<int:boleto_id>', methods=['PUT'])
@login_required
def editar(boleto_id):
    dados = request.get_json() or {}
    b, erro = boleto_service.editar_boleto(current_user.id, boleto_id, ImmutableMultiDict(dados.items()))
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify(serial(b))


@api_boleto.route('/<int:boleto_id>', methods=['DELETE'])
@login_required
def excluir(boleto_id):
    _, erro = boleto_service.excluir_boleto(current_user.id, boleto_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Boleto excluído.'})


@api_boleto.route('/<int:boleto_id>/pagar', methods=['POST'])
@login_required
def pagar(boleto_id):
    _, erro = boleto_service.pagar_boleto(current_user.id, boleto_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Boleto marcado como pago.'})


@api_boleto.route('/<int:boleto_id>/reabrir', methods=['POST'])
@login_required
def reabrir(boleto_id):
    _, erro = boleto_service.reabrir_boleto(current_user.id, boleto_id)
    if erro:
        return jsonify({'erro': erro}), 400
    return jsonify({'mensagem': 'Boleto reaberto.'})
