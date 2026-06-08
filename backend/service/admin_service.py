from extensao import db
from modelos.usuario import Usuario
from modelos.boleto import Boleto
from modelos.assinatura import Assinatura
from modelos.gasto import Gasto


def obter_estatisticas_admin():
    total_usuarios    = Usuario.query.count()
    total_boletos     = Boleto.query.count()
    total_assinaturas = Assinatura.query.count()
    total_gastos      = Gasto.query.count()

    volume_boletos     = db.session.query(db.func.sum(Boleto.valor)).scalar()     or 0
    volume_assinaturas = db.session.query(db.func.sum(Assinatura.valor)).scalar() or 0
    volume_gastos      = db.session.query(db.func.sum(Gasto.valor)).scalar()      or 0
    volume_total       = volume_boletos + volume_assinaturas + volume_gastos
    usuarios_ativos    = db.session.query(Gasto.usuario_id).distinct().count()

    return {
        'total_usuarios': total_usuarios,
        'total_boletos': total_boletos,
        'total_assinaturas': total_assinaturas,
        'total_gastos': total_gastos,
        'volume_boletos': volume_boletos,
        'volume_assinaturas': volume_assinaturas,
        'volume_gastos': volume_gastos,
        'volume_total': volume_total,
        'usuarios_ativos': usuarios_ativos,
    }
