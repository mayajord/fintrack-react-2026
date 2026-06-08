import React, { useState, useEffect } from 'react'
import api from '../api'

const FORM_VAZIO = { nome: '', valor: '', ciclo: 'mensal', dia_vencimento: '1', categoria_id: '', desde: '', notas: '' }

export default function Assinaturas() {
  const [dados, setDados] = useState(null)
  const [categorias, setCategorias] = useState([])
  const [form, setForm] = useState(FORM_VAZIO)
  const [editandoId, setEditandoId] = useState(null)
  const [mostrarForm, setMostrarForm] = useState(false)
  const [erro, setErro] = useState('')

  async function carregar() {
    const [r1, r2] = await Promise.all([
      api.get('/assinaturas/'),
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

  function editarForm(s) {
    setForm({
      nome: s.nome,
      valor: s.valor,
      ciclo: s.ciclo || 'mensal',
      dia_vencimento: s.dia_vencimento || '1',
      categoria_id: s.categoria_id || '',
      desde: s.desde || '',
      notas: s.notas || ''
    })
    setEditandoId(s.id)
    setMostrarForm(true)
    setErro('')
  }

  async function salvar(e) {
    e.preventDefault()
    setErro('')
    try {
      if (editandoId) {
        await api.put(`/assinaturas/${editandoId}`, form)
      } else {
        await api.post('/assinaturas/', form)
      }
      setMostrarForm(false)
      carregar()
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao salvar.')
    }
  }

  async function alternarStatus(id) {
    await api.post(`/assinaturas/${id}/status`)
    carregar()
  }

  async function excluir(id) {
    if (!confirm('Excluir esta assinatura?')) return
    await api.delete(`/assinaturas/${id}`)
    carregar()
  }

  if (!dados) return <div className="carregando">Carregando...</div>

  const ativas = dados.assinaturas.filter(s => s.status === 'ativa')

  return (
    <div>
      <h1>Assinaturas</h1>
      <p className="subtitulo">Serviços e cobranças recorrentes</p>

      <div className="toolbar">
        <p>{ativas.length} ativas — R$ {Number(dados.total_mensal).toFixed(2)}/mês</p>
        <button className="btn btn-primario" onClick={novoForm}>+ Nova assinatura</button>
      </div>

      {mostrarForm && (
        <div className="form-box">
          <h2 style={{ fontSize: '16px', marginBottom: '16px' }}>
            {editandoId ? 'Editar assinatura' : 'Nova assinatura'}
          </h2>
          {erro && <div className="alerta alerta-erro">{erro}</div>}
          <form onSubmit={salvar}>
            <div className="grid2">
              <div className="campo">
                <label>Nome *</label>
                <input name="nome" value={form.nome} onChange={atualizar} placeholder="Netflix, Spotify..." required />
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
                <input name="valor" type="number" step="0.01" value={form.valor} onChange={atualizar} placeholder="39.90" required />
              </div>
              <div className="campo">
                <label>Ciclo *</label>
                <select name="ciclo" value={form.ciclo} onChange={atualizar}>
                  <option value="mensal">Mensal</option>
                  <option value="anual">Anual</option>
                  <option value="semanal">Semanal</option>
                  <option value="bimestral">Bimestral</option>
                  <option value="trimestral">Trimestral</option>
                  <option value="semestral">Semestral</option>
                </select>
              </div>
            </div>
            <div className="grid2">
              <div className="campo">
                <label>Dia do vencimento *</label>
                <input name="dia_vencimento" type="number" min="1" max="31" value={form.dia_vencimento} onChange={atualizar} required />
              </div>
              <div className="campo">
                <label>Desde</label>
                <input name="desde" type="date" value={form.desde} onChange={atualizar} />
              </div>
            </div>
            <div className="campo">
              <label>Notas</label>
              <input name="notas" value={form.notas} onChange={atualizar} placeholder="Plano, detalhes..." />
            </div>
            <div className="form-acoes">
              <button type="submit" className="btn btn-primario">Salvar</button>
              <button type="button" className="btn btn-cinza" onClick={() => setMostrarForm(false)}>Cancelar</button>
            </div>
          </form>
        </div>
      )}

      <div className="tabela-box">
        <table>
          <thead>
            <tr>
              <th>Serviço</th>
              <th>Categoria</th>
              <th>Ciclo</th>
              <th>Dia venc.</th>
              <th>Status</th>
              <th>Valor/mês</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {dados.assinaturas.length === 0 ? (
              <tr><td colSpan="7" className="vazio">Nenhuma assinatura cadastrada.</td></tr>
            ) : dados.assinaturas.map(s => (
              <tr key={s.id} style={{ opacity: s.status === 'pausada' ? 0.55 : 1 }}>
                <td><strong>{s.nome}</strong></td>
                <td>{s.categoria_nome || '—'}</td>
                <td>{s.ciclo}</td>
                <td>{s.dia_vencimento}</td>
                <td>
                  <span className={`badge badge-${s.status}`}>
                    {s.status === 'ativa' ? 'Ativa' : 'Pausada'}
                  </span>
                </td>
                <td><strong>R$ {Number(s.valor_mensal).toFixed(2)}</strong></td>
                <td style={{ display: 'flex', gap: '6px' }}>
                  <button className="btn btn-cinza" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => alternarStatus(s.id)}>
                    {s.status === 'ativa' ? 'Pausar' : 'Ativar'}
                  </button>
                  <button className="btn btn-cinza" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => editarForm(s)}>Editar</button>
                  <button className="btn btn-vermelho" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => excluir(s.id)}>Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
