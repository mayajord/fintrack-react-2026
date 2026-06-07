from flask import Blueprint, Response, flash, redirect, url_for
from flask_login import current_user
from utils.decorators import login_required
from service.relatorio_service import gerar_csv_financeiro
from datetime import date

bp_relatorio = Blueprint('relatorio', __name__, url_prefix='/relatorio')


@bp_relatorio.route('/csv')
@login_required
def exportar_csv():
    try:
        conteudo = gerar_csv_financeiro(current_user.id)
        nome_arquivo = f'fintrack_{date.today().isoformat()}.csv'
        return Response(
            conteudo.encode('utf-8-sig'),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{nome_arquivo}"'}
        )
    except Exception as e:
        print(f'[ERRO] relatorio.exportar_csv: {e}')
        flash('Erro ao gerar relatório.', 'erro')
        return redirect(url_for('dashboard.painel'))