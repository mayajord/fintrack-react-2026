from datetime import datetime
import repository.gasto_repository as gasto_repository
from repository.categoria_repository import buscar_por_id as buscar_categoria


def cadastrar_gasto(usuario_id, dados):
    valor = dados.get('valor')
    data_str = dados.get('data')
    descricao = dados.get('descricao', '').strip() or None
    categoria_id = dados.get('categoria_id') or None
    recorrente = dados.get('recorrente') == 'on'

    if not valor or not data_str:
        return None, 'Preencha os campos obrigatórios.'

    try:
        valor_float = float(valor)
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        cat_id = int(categoria_id) if categoria_id else None
    except (TypeError, ValueError):
        return None, 'Valores inválidos informados.'

    if valor_float <= 0:
        return None, 'O valor deve ser maior que zero.'

    if cat_id and not buscar_categoria(cat_id):
        return None, 'Categoria informada não encontrada.'

    gasto = gasto_repository.criar_gasto(
        descricao=descricao, valor=valor_float, data=data,
        recorrente=recorrente, categoria_id=cat_id, usuario_id=usuario_id,
    )
    return gasto, None


def editar_gasto(usuario_id, gasto_id, dados):
    gasto = gasto_repository.buscar_por_id(gasto_id)
    if not gasto or gasto.usuario_id != usuario_id:
        return None, 'Gasto não encontrado.'

    valor = dados.get('valor')
    data_str = dados.get('data')
    categoria_id = dados.get('categoria_id') or None

    if not valor or not data_str:
        return None, 'Preencha os campos obrigatórios.'

    try:
        valor_float = float(valor)
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        cat_id = int(categoria_id) if categoria_id else None
    except (TypeError, ValueError):
        return None, 'Valores inválidos informados.'

    if valor_float <= 0:
        return None, 'O valor deve ser maior que zero.'

    if cat_id and not buscar_categoria(cat_id):
        return None, 'Categoria informada não encontrada.'

    gasto_repository.atualizar_gasto(
        gasto_id=gasto_id, valor=valor_float,
        data=data, categoria_id=cat_id,
    )
    return gasto, None


def excluir_gasto(usuario_id, gasto_id):
    gasto = gasto_repository.buscar_por_id(gasto_id)
    if not gasto or gasto.usuario_id != usuario_id:
        return False, 'Gasto não encontrado.'
    gasto_repository.deletar_gasto(gasto_id)
    return True, None
