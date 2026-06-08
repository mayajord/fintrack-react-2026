from datetime import date
from extensao import db
from repository.assinatura_repository import (
    listar_assinaturas, criar_assinatura, buscar_por_id,
    atualizar_assinatura, alterar_status_assinatura, deletar_assinatura
)
from repository.categoria_repository import buscar_por_id as buscar_categoria


def obter_assinaturas_com_total(usuario_id):
    assinaturas = listar_assinaturas(usuario_id)
    total_mensal = sum(s.valor_mensal() for s in assinaturas if s.status == 'ativa')
    return assinaturas, total_mensal


def cadastrar_assinatura(usuario_id, dados):
    nome = dados.get('nome', '').strip()
    valor = dados.get('valor')
    ciclo = dados.get('ciclo', 'mensal')
    dia_vencimento = dados.get('dia_vencimento')
    categoria_id = dados.get('categoria_id') or None
    desde_str = dados.get('desde')
    notas = dados.get('notas', '').strip() or None

    if not nome or not valor or not dia_vencimento:
        return None, 'Preencha os campos obrigatórios.'

    try:
        valor_float = float(valor)
        dia_int = int(dia_vencimento)
        cat_id = int(categoria_id) if categoria_id else None
    except (TypeError, ValueError):
        return None, 'Valores inválidos informados.'

    if dia_int < 1 or dia_int > 31:
        return None, 'Dia de vencimento deve estar entre 1 e 31.'
    if valor_float <= 0:
        return None, 'O valor deve ser maior que zero.'

    if cat_id and not buscar_categoria(cat_id):
        return None, 'Categoria informada não encontrada.'

    assinatura = criar_assinatura(
        nome=nome, valor=valor_float, ciclo=ciclo,
        dia_vencimento=dia_int, usuario_id=usuario_id,
        categoria_id=cat_id,
    )
    assinatura.desde = date.fromisoformat(desde_str) if desde_str else None
    assinatura.notas = notas
    db.session.commit()
    return assinatura, None


def editar_assinatura(usuario_id, assinatura_id, dados):
    assinatura = buscar_por_id(assinatura_id)
    if not assinatura or assinatura.usuario_id != usuario_id:
        return None, 'Assinatura não encontrada.'

    nome = dados.get('nome', '').strip()
    valor = dados.get('valor')
    ciclo = dados.get('ciclo', 'mensal')
    dia_vencimento = dados.get('dia_vencimento')
    categoria_id = dados.get('categoria_id') or None
    desde_str = dados.get('desde')
    notas = dados.get('notas', '').strip() or None

    if not nome or not valor or not dia_vencimento:
        return None, 'Preencha os campos obrigatórios.'

    try:
        valor_float = float(valor)
        dia_int = int(dia_vencimento)
        cat_id = int(categoria_id) if categoria_id else None
    except (TypeError, ValueError):
        return None, 'Valores inválidos informados.'

    if dia_int < 1 or dia_int > 31:
        return None, 'Dia de vencimento deve estar entre 1 e 31.'
    if valor_float <= 0:
        return None, 'O valor deve ser maior que zero.'

    if cat_id and not buscar_categoria(cat_id):
        return None, 'Categoria informada não encontrada.'

    atualizar_assinatura(
        assinatura_id=assinatura_id, nome=nome, valor=valor_float,
        ciclo=ciclo, dia_vencimento=dia_int, categoria_id=cat_id,
    )
    assinatura.desde = date.fromisoformat(desde_str) if desde_str else None
    assinatura.notas = notas
    db.session.commit()
    return assinatura, None


def alternar_status_assinatura(usuario_id, assinatura_id):
    assinatura = buscar_por_id(assinatura_id)
    if not assinatura or assinatura.usuario_id != usuario_id:
        return None, 'Assinatura não encontrada.'
    novo_status = 'pausada' if assinatura.status == 'ativa' else 'ativa'
    alterar_status_assinatura(assinatura_id, novo_status)
    return assinatura, None


def excluir_assinatura(usuario_id, assinatura_id):
    assinatura = buscar_por_id(assinatura_id)
    if not assinatura or assinatura.usuario_id != usuario_id:
        return False, 'Assinatura não encontrada.'
    deletar_assinatura(assinatura_id)
    return True, None
