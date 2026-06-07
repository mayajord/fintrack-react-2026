from flask import Blueprint, jsonify, Response
from flask_login import current_user, login_required
from service.relatorio_service import gerar_csv_financeiro
from datetime import date

api_relatorio = Blueprint('api_relatorio', __name__, url_prefix='/api/relatorio')


@api_relatorio.route('/csv')
@login_required
def exportar_csv():
    try:
        conteudo = gerar_csv_financeiro(current_user.id)
        nome = f'fintrack_{date.today().isoformat()}.csv'
        return Response(
            conteudo.encode('utf-8-sig'),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{nome}"'}
        )
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
