import repository.categoria_repository as categoria_repository


def cadastrar_categoria(usuario_id, dados):
    nome = dados.get('nome', '').strip()
    icone = dados.get('icone', '📌').strip()
    cor = dados.get('cor', '#2dd4bf').strip()

    if not nome:
        return None, 'Nome é obrigatório.'
    if len(nome) > 100:
        return None, 'Nome deve ter no máximo 100 caracteres.'

    categorias_existentes = categoria_repository.listar_categorias(usuario_id)
    nomes_existentes = [c.nome.lower() for c in categorias_existentes]
    if nome.lower() in nomes_existentes:
        return None, 'Você já possui uma categoria com esse nome.'

    categoria = categoria_repository.criar_categoria(nome, usuario_id, icone, cor)
    return categoria, None


def editar_categoria(usuario_id, categoria_id, dados):
    categoria = categoria_repository.buscar_por_id(categoria_id)
    if not categoria or categoria.usuario_id != usuario_id:
        return None, 'Categoria não encontrada.'

    nome = dados.get('nome', '').strip()
    icone = dados.get('icone', '📌').strip()
    cor = dados.get('cor', '#2dd4bf').strip()

    if not nome:
        return None, 'Nome é obrigatório.'
    if len(nome) > 100:
        return None, 'Nome deve ter no máximo 100 caracteres.'

    categorias_existentes = categoria_repository.listar_categorias(usuario_id)
    nomes_existentes = [c.nome.lower() for c in categorias_existentes if c.id != categoria_id]
    if nome.lower() in nomes_existentes:
        return None, 'Você já possui uma categoria com esse nome.'

    categoria_repository.atualizar_categoria(categoria_id, nome, icone, cor)
    return categoria, None


def excluir_categoria(usuario_id, categoria_id):
    categoria = categoria_repository.buscar_por_id(categoria_id)
    if not categoria or categoria.usuario_id != usuario_id:
        return False, 'Categoria não encontrada.'
    categoria_repository.deletar_categoria(categoria_id)
    return True, None
