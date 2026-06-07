import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../api'

export default function Dashboard() {
  const [dados, setDados] = useState(null)
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    api.get('/dashboard/')
      .then(res => setDados(res.data))
      .finally(() => setCarregando(false))
  }, [])

  if (carregando) return <div className="carregando">Carregando dashboard...</div>
  if (!dados) return <div className="carregando">Erro ao carregar dados.</div>

  function formatarValor(v) {
    return 'R$ ' + Number(v).toFixed(2).replace('.', ',')
  }

  function corDias(dias) {
    if (dias < 0) return '#dc2626'
    if (dias === 0) return '#dc2626'
    if (dias <= 3) return '#d97706'
    return '#2563eb'
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p className="subtitulo">Resumo das suas finanças</p>

      {dados.qtd_alertas > 0 && (
        <div className="alerta alerta-erro" style={{ marginBottom: '20px' }}>
          ⚠ Você tem {dados.qtd_alertas} vencimento(s) nos próximos 7 dias!
        </div>
      )}

      {/* Cards */}
      <div className="cards">
        <div className="card vermelho">
          <div className="card-label">Boletos em aberto</div>
          <div className="card-valor">{formatarValor(dados.total_boletos)}</div>
          <div className="card-nota">{dados.qtd_boletos_pendentes} pendentes</div>
        </div>
        <div className="card azul">
          <div className="card-label">Assinaturas / mês</div>
          <div className="card-valor">{formatarValor(dados.total_assinaturas)}</div>
          <div className="card-nota">{dados.qtd_assinaturas_ativas} ativas</div>
        </div>
        <div className="card">
          <div className="card-label">Gastos este mês</div>
          <div className="card-valor">{formatarValor(dados.total_gastos_mes)}</div>
          <div className="card-nota">Total do mês atual</div>
        </div>
        <div className="card">
          <div className="card-label">Total de saídas</div>
          <div className="card-valor">{formatarValor(dados.total_mensal)}</div>
          <div className="card-nota">Assinaturas + Gastos</div>
        </div>
      </div>

      <div className="secoes">
        {/* Boletos urgentes */}
        <div className="secao">
          <div className="secao-titulo">
            Boletos urgentes
            <Link to="/boletos">Ver todos →</Link>
          </div>
          <table>
            <tbody>
              {dados.boletos_urgentes.length === 0 ? (
                <tr><td className="vazio">Nenhum boleto urgente.</td></tr>
              ) : dados.boletos_urgentes.map(b => (
                <tr key={b.id}>
                  <td>{b.nome}</td>
                  <td>{b.vencimento}</td>
                  <td style={{ fontWeight: 'bold' }}>{formatarValor(b.valor)}</td>
                  <td style={{ color: corDias(b.dias), fontWeight: 'bold', fontSize: '12px' }}>
                    {b.dias < 0 ? 'Vencido' : b.dias === 0 ? 'Hoje!' : `${b.dias} dias`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Últimos gastos */}
        <div className="secao">
          <div className="secao-titulo">
            Últimos gastos
            <Link to="/gastos">Ver todos →</Link>
          </div>
          <table>
            <thead>
              <tr>
                <th>Descrição</th>
                <th>Categoria</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {dados.gastos_recentes.length === 0 ? (
                <tr><td colSpan="3" className="vazio">Nenhum gasto registrado.</td></tr>
              ) : dados.gastos_recentes.map((g, i) => (
                <tr key={i}>
                  <td>{g.descricao || '—'}</td>
                  <td>{g.categoria || '—'}</td>
                  <td style={{ color: '#dc2626', fontWeight: 'bold' }}>{formatarValor(g.valor)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{ marginTop: '8px' }}>
        <a href="/api/relatorio/csv" className="btn btn-cinza" style={{ fontSize: '13px' }}>
          ⬇ Exportar CSV
        </a>
      </div>
    </div>
  )
}
