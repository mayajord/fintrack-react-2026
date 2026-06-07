import io
import csv
from repository.gasto_repository import listar_gastos
from repository.boleto_repository import listar_boletos
from repository.assinatura_repository import listar_assinaturas


def gerar_csv_financeiro(usuario_id):   
    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=';')
    escritor.writerow(['Tipo', 'Descrição', 'Valor (R$)', 'Data', 'Categoria', 'Status'])

    for g in listar_gastos(usuario_id):
        escritor.writerow(['Gasto',
            g.descricao or 'Sem descrição',
            f'{g.valor:.2f}',
            g.data.strftime('%d/%m/%Y'),
            g.categoria.nome if g.categoria else '—',
            'Recorrente' if g.recorrente else 'Avulso',
        ])

    for b in listar_boletos(usuario_id):
        escritor.writerow([
            'Boleto',
            b.nome,
            f'{b.valor:.2f}',
            b.vencimento.strftime('%d/%m/%Y'),
            b.categoria.nome if b.categoria else '—',
            b.status.capitalize(),
        ])

    for a in listar_assinaturas(usuario_id):
        escritor.writerow([
            'Assinatura',
            a.nome,
            f'{a.valor:.2f}',
            f'Todo dia {a.dia_vencimento}',
            a.categoria.nome if a.categoria else '—',
            a.status.capitalize(),
        ])

    return saida.getvalue()