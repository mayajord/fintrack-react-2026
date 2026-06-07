import React, { useState, useEffect } from 'react'
import api from '../api'

export default function Admin() {
  const [dados, setDados] = useState(null)
  const [erro, setErro] = useState('')

  useEffect(() => {
    api.get('/admin/')
      .then(res => setDados(res.data))
      .catch(err => setErro(err.response?.data?.erro || 'Acesso negado.'))
  }, [])

  if (erro) return (
    <div>
      <h1>Admin</h1>
      <div className="alerta alerta-erro">{erro}</div>
    </div>
  )

  if (!dados) return <div className="carregando">Carregando...</div>

  return (
    <div>
      <h1>Painel Administrativo</h1>
      <p className="subtitulo">Visão geral de todos os dados da plataforma</p>

      <div className="cards">
        <div className="card azul">
          <div className="card-label">Total de usuários</div>
          <div className="card-valor">{dados.total_usuarios}</div>
          <div className="card-nota">{dados.usuarios_ativos} ativos</div>
        </div>
        <div className="card">
          <div className="card-label">Total de boletos</div>
          <div className="card-valor">{dados.total_boletos}</div>
          <div className="card-nota">R$ {Number(dados.volume_boletos).toFixed(2)}</div>
        </div>
        <div className="card">
          <div className="card-label">Total de assinaturas</div>
          <div className="card-valor">{dados.total_assinaturas}</div>
          <div className="card-nota">R$ {Number(dados.volume_assinaturas).toFixed(2)}</div>
        </div>
        <div className="card">
          <div className="card-label">Total de gastos</div>
          <div className="card-valor">{dados.total_gastos}</div>
          <div className="card-nota">R$ {Number(dados.volume_gastos).toFixed(2)}</div>
        </div>
      </div>

      <div className="form-box" style={{ maxWidth: '400px' }}>
        <h2 style={{ fontSize: '16px', marginBottom: '16px' }}>Volume total da plataforma</h2>
        <table>
          <tbody>
            <tr>
              <td>Boletos</td>
              <td><strong>R$ {Number(dados.volume_boletos).toFixed(2)}</strong></td>
            </tr>
            <tr>
              <td>Assinaturas</td>
              <td><strong>R$ {Number(dados.volume_assinaturas).toFixed(2)}</strong></td>
            </tr>
            <tr>
              <td>Gastos</td>
              <td><strong>R$ {Number(dados.volume_gastos).toFixed(2)}</strong></td>
            </tr>
            <tr style={{ borderTop: '2px solid #e2e8f0' }}>
              <td><strong>Total</strong></td>
              <td><strong style={{ color: '#2563eb' }}>R$ {Number(dados.volume_total).toFixed(2)}</strong></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
