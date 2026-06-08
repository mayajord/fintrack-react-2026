from werkzeug.security import generate_password_hash, check_password_hash
from repository import usuario_repository
from utils.decorators import ADMIN_EMAIL


def autenticar_usuario(email, senha):
    if not email or not senha:
        return None, 'E-mail e senha são obrigatórios.'
    usuario = usuario_repository.buscar_por_email(email)
    if not usuario or not check_password_hash(usuario.senha, senha):
        return None, 'E-mail ou senha incorretos.'
    return usuario, None


def registrar_usuario(nome, email, senha, confirmar):
    if not nome or not email or not senha or not confirmar:
        return None, 'Preencha todos os campos.'
    if email.lower() == ADMIN_EMAIL:
        return None, 'Este e-mail não pode ser usado para cadastro.'
    if senha != confirmar:
        return None, 'As senhas não coincidem.'
    if len(senha) < 6:
        return None, 'A senha deve ter pelo menos 6 caracteres.'
    if usuario_repository.buscar_por_email(email):
        return None, 'Este e-mail já está cadastrado.'
    senha_hash = generate_password_hash(senha)
    usuario = usuario_repository.criar_usuario(nome, email, senha_hash)
    if not usuario:
        return None, 'Erro ao cadastrar usuário. Tente novamente.'
    return usuario, None
