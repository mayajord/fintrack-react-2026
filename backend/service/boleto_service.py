from datetime import date, datetime
import repository.boleto_repository as boleto_repository
from repository.categoria_repository import buscar_por_id as buscar_categoria


def obter_boletos_com_estatisticas(usuario_id):
    hoje = date.today()
    boletos = boleto_repository.listar_boletos(usuario_id)
    pendentes = [b for b in boletos if b.status == 'pendente']
    pagos = [b for b in boletos if b.status == 'pago']
    vencidos = [b for b in pendentes if b.vencimento < hoje]
    qtd_urgentes = sum(1 for b in pendentes if 0 <= (b.vencimento - hoje).days <= 7)
    total_urgentes = sum(b.valor for b in pendentes if 0 <= (b.vencimento - hoje).days <= 7)
    total_aberto = sum(b.valor for b in pendentes)
    total_pago = sum(b.valor for b in pagos)
    return {
        'boletos': boletos,
        'pendentes': pendentes,
        'pagos': pagos,
        'vencidos': vencidos,
        'hoje': hoje,
        'qtd_pendentes': len(pendentes),
        'qtd_urgentes': qtd_urgentes,
        'total_urgentes': total_urgentes,
        'qtd_vencidos': len(vencidos),
        'qtd_pagos': len(pagos),
        'total_aberto': total_aberto,
        'total_pago': total_pago,
    }


def cadastrar_boleto(usuario_id, dados):
    nome = dados.get('nome', '').strip()
    valor = dados.get('valor')
    vencimento = dados.get('vencimento')
    descricao = dados.get('descricao', '').strip() or None
    codigo_barra = dados.get('codigo_barra', '').strip() or None
    notas = dados.get('notas', '').strip() or None
    categoria_id = dados.get('categoria_id') or None

    if not nome or not valor or not vencimento:
        return None, 'Preencha os campos obrigatórios.'

    try:
        valor_float = float(valor)
        data_vencimento = datetime.strptime(vencimento, '%Y-%m-%d').date()
        cat_id = int(categoria_id) if categoria_id else None
    except (TypeError, ValueError):
        return None, 'Valores inválidos informados.'

    if valor_float <= 0:
        return None, 'O valor deve ser maior que zero.'
    if data_vencimento < date.today():
        return None, 'A data de vencimento não pode ser no passado.'

    if cat_id and not buscar_categoria(cat_id):
        return None, 'Categoria informada não encontrada.'

    boleto = boleto_repository.criar_boleto(
        nome=nome, valor=valor_float, vencimento=data_vencimento,
        usuario_id=usuario_id, categoria_id=cat_id,
        descricao=descricao, codigo_barra=codigo_barra, notas=notas,
    )
    return boleto, None


def editar_boleto(usuario_id, boleto_id, dados):
    boleto = boleto_repository.buscar_por_id(boleto_id)
    if not boleto or boleto.usuario_id != usuario_id:
        return None, 'Boleto não encontrado.'

    nome = dados.get('nome', '').strip()
    valor = dados.get('valor')
    vencimento = dados.get('vencimento')
    descricao = dados.get('descricao', '').strip() or None
    codigo_barra = dados.get('codigo_barra', '').strip() or None
    notas = dados.get('notas', '').strip() or None
    categoria_id = dados.get('categoria_id') or None

    if not nome or not valor or not vencimento:
        return None, 'Preencha os campos obrigatórios.'

    try:
        valor_float = float(valor)
        data_vencimento = datetime.strptime(vencimento, '%Y-%m-%d').date()
        cat_id = int(categoria_id) if categoria_id else None
    except (TypeError, ValueError):
        return None, 'Valores inválidos informados.'

    if valor_float <= 0:
        return None, 'O valor deve ser maior que zero.'

    if cat_id and not buscar_categoria(cat_id):
        return None, 'Categoria informada não encontrada.'

    boleto_repository.atualizar_boleto(
        boleto_id=boleto_id, nome=nome, valor=valor_float,
        vencimento=data_vencimento, categoria_id=cat_id,
        descricao=descricao, codigo_barra=codigo_barra, notas=notas,
    )
    return boleto, None


def pagar_boleto(usuario_id, boleto_id):
    boleto = boleto_repository.buscar_por_id(boleto_id)
    if not boleto or boleto.usuario_id != usuario_id:
        return False, 'Boleto não encontrado.'
    if boleto.status == 'pago':
        return False, 'Este boleto já foi pago.'
    boleto_repository.marcar_como_pago(boleto_id)
    return True, None


def reabrir_boleto(usuario_id, boleto_id):
    boleto = boleto_repository.buscar_por_id(boleto_id)
    if not boleto or boleto.usuario_id != usuario_id:
        return False, 'Boleto não encontrado.'
    if boleto.status == 'pendente':
        return False, 'Este boleto já está pendente.'
    boleto_repository.reabrir(boleto_id)
    return True, None


def excluir_boleto(usuario_id, boleto_id):
    boleto = boleto_repository.buscar_por_id(boleto_id)
    if not boleto or boleto.usuario_id != usuario_id:
        return False, 'Boleto não encontrado.'
    boleto_repository.deletar_boleto(boleto_id)
    return True, None
