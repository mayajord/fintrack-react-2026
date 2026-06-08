import React, { useState, useEffect } from 'react'
import api from '../api'

const FORM_VAZIO = { nome: '', valor: '', vencimento: '', descricao: '', codigo_barra: '', notas: '', categoria_id: '' }

export default function Boletos() {
  const [dados, setDados] = useState(null)
  const [categorias, setCategorias] = useState([])
  const [form, setForm] = useState(FORM_VAZIO)
  const [editandoId, setEditandoId] = useState(null)
  const [mostrarForm, setMostrarForm] = useState(false)
  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState('')

  async function carregar() {
    const [r1, r2] = await Promise.all([
      api.get('/boletos/'),
      api.get('/categorias/')
    ])
    setDados(r1.data)
    setCategorias(r2.data)
  }

  useEffect(() => { carregar() }, [])

  function atualizar(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function novoForm() {
    setForm(FORM_VAZIO)
    setEditandoId(null)
    setMostrarForm(true)
    setErro('')
  }

  function editarForm(b) {
    setForm({
      nome: b.nome,
      valor: b.valor,
      vencimento: b.vencimento,
      descricao: b.descricao || '',
      codigo_barra: b.codigo_barra || '',
      notas: b.notas || '',
      categoria_id: b.categoria_id || ''
    })
    setEditandoId(b.id)
    setMostrarForm(true)
    setErro('')
  }

  async function salvar(e) {
    e.preventDefault()
    setErro('')
    try {
      if (editandoId) {
        await api.put(`/boletos/${editandoId}`, form)
      } else {
        await api.post('/boletos/', form)
      }
      setSucesso('Boleto salvo com sucesso!')
      setMostrarForm(false)
      carregar()
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao salvar boleto.')
    }
  }

  async function pagar(id) {
    if (!confirm('Marcar como pago?')) return
    await api.post(`/boletos/${id}/pagar`)
    carregar()
  }

  async function reabrir(id) {
    await api.post(`/boletos/${id}/reabrir`)
    carregar()
  }

  async function excluir(id) {
    if (!confirm('Excluir este boleto?')) return
    await api.delete(`/boletos/${id}`)
    carregar()
  }

  function statusBadge(b) {
    if (b.status === 'pago') return <span className="badge badge-pago">Pago</span>
    if (b.dias_para_vencer < 0) return <span className="badge badge-vencido">Vencido</span>
    if (b.dias_para_vencer <= 7) return <span className="badge badge-pendente">⚠ {b.dias_para_vencer} dias</span>
    return <span className="badge badge-pendente">Pendente</span>
  }

  if (!dados) return <div className="carregando">Carregando...</div>

  return (
    <div>
      <h1>Boletos</h1>
      <p className="subtitulo">Gerencie seus boletos e vencimentos</p>

      {/* Cards */}
      <div className="cards">
        <div className="card vermelho">
          <div className="card-label">Em aberto</div>
          <div className="card-valor">R$ {Number(dados.total_aberto).toFixed(2)}</div>
          <div className="card-nota">{dados.qtd_pendentes} pendentes</div>
        </div>
        <div className="card">
          <div className="card-label">Urgentes (≤7 dias)</div>
          <div className="card-valor">{dados.qtd_urgentes}</div>
        </div>
        <div className="card vermelho">
          <div className="card-label">Vencidos</div>
          <div className="card-valor">{dados.qtd_vencidos}</div>
        </div>
        <div className="card verde">
          <div className="card-label">Pagos</div>
          <div className="card-valor">{dados.qtd_pagos}</div>
          <div className="card-nota">R$ {Number(dados.total_pago).toFixed(2)}</div>
        </div>
      </div>

      {sucesso && <div className="alerta alerta-ok">{sucesso}</div>}

      <div className="toolbar">
        <p>{dados.boletos.length} boletos</p>
        <button className="btn btn-primario" onClick={novoForm}>+ Novo boleto</button>
      </div>

      {/* Formulário */}
      {mostrarForm && (
        <div className="form-box">
          <h2 style={{ fontSize: '16px', marginBottom: '16px' }}>
            {editandoId ? 'Editar boleto' : 'Novo boleto'}
          </h2>
          {erro && <div className="alerta alerta-erro">{erro}</div>}
          <form onSubmit={salvar}>
            <div className="grid2">
              <div className="campo">
                <label>Nome *</label>
                <input name="nome" value={form.nome} onChange={atualizar} placeholder="IPTU, Água..." required />
              </div>
              <div className="campo">
                <label>Categoria</label>
                <select name="categoria_id" value={form.categoria_id} onChange={atualizar}>
                  <option value="">Sem categoria</option>
                  {categorias.map(c => <option key={c.id} value={c.id}>{c.icone} {c.nome}</option>)}
                </select>
              </div>
            </div>
            <div className="grid2">
              <div className="campo">
                <label>Valor (R$) *</label>
                <input name="valor" type="number" step="0.01" value={form.valor} onChange={atualizar} placeholder="150.00" required />
              </div>
              <div className="campo">
                <label>Vencimento *</label>
                <input name="vencimento" type="date" value={form.vencimento} onChange={atualizar} required />
              </div>
            </div>
            <div className="campo">
              <label>Descrição</label>
              <input name="descricao" value={form.descricao} onChange={atualizar} placeholder="Referência, parcela..." />
            </div>
            <div className="campo">
              <label>Código de barras</label>
              <input name="codigo_barra" value={form.codigo_barra} onChange={atualizar} placeholder="Opcional" />
            </div>
            <div className="campo">
              <label>Notas</label>
              <input name="notas" value={form.notas} onChange={atualizar} placeholder="Observações..." />
            </div>
            <div className="form-acoes">
              <button type="submit" className="btn btn-primario">Salvar</button>
              <button type="button" className="btn btn-cinza" onClick={() => setMostrarForm(false)}>Cancelar</button>
            </div>
          </form>
        </div>
      )}

      {/* Tabela */}
      <div className="tabela-box">
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>Vencimento</th>
              <th>Categoria</th>
              <th>Status</th>
              <th>Valor</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {dados.boletos.length === 0 ? (
              <tr><td colSpan="6" className="vazio">Nenhum boleto cadastrado.</td></tr>
            ) : dados.boletos.map(b => (
              <tr key={b.id} style={{ opacity: b.status === 'pago' ? 0.6 : 1 }}>
                <td><strong>{b.nome}</strong></td>
                <td>{b.vencimento}</td>
                <td>{b.categoria_nome || '—'}</td>
                <td>{statusBadge(b)}</td>
                <td><strong>R$ {Number(b.valor).toFixed(2)}</strong></td>
                <td style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                  {b.status === 'pendente' && (
                    <button className="btn btn-verde" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => pagar(b.id)}>Pagar</button>
                  )}
                  {b.status === 'pago' && (
                    <button className="btn btn-cinza" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => reabrir(b.id)}>Reabrir</button>
                  )}
                  <button className="btn btn-cinza" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => editarForm(b)}>Editar</button>
                  <button className="btn btn-vermelho" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => excluir(b.id)}>Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
