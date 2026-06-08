import React, { useState, useEffect } from 'react'
import api from '../api'

const hoje = new Date().toISOString().split('T')[0]
const FORM_VAZIO = { descricao: '', valor: '', data: hoje, recorrente: 'false', categoria_id: '' }

export default function Gastos() {
  const [dados, setDados] = useState(null)
  const [categorias, setCategorias] = useState([])
  const [form, setForm] = useState(FORM_VAZIO)
  const [editandoId, setEditandoId] = useState(null)
  const [mostrarForm, setMostrarForm] = useState(false)
  const [erro, setErro] = useState('')

  async function carregar() {
    const [r1, r2] = await Promise.all([
      api.get('/gastos/'),
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

  function editarForm(g) {
    setForm({
      descricao: g.descricao || '',
      valor: g.valor,
      data: g.data,
      recorrente: g.recorrente ? 'true' : 'false',
      categoria_id: g.categoria_id || ''
    })
    setEditandoId(g.id)
    setMostrarForm(true)
    setErro('')
  }

  async function salvar(e) {
    e.preventDefault()
    setErro('')
    try {
      if (editandoId) {
        await api.put(`/gastos/${editandoId}`, form)
      } else {
        await api.post('/gastos/', form)
      }
      setMostrarForm(false)
      carregar()
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao salvar.')
    }
  }

  async function excluir(id) {
    if (!confirm('Excluir este gasto?')) return
    await api.delete(`/gastos/${id}`)
    carregar()
  }

  if (!dados) return <div className="carregando">Carregando...</div>

  return (
    <div>
      <h1>Gastos</h1>
      <p className="subtitulo">Despesas fixas e variáveis</p>

      <div className="toolbar">
        <p>{dados.gastos.length} registros — R$ {Number(dados.total_mes).toFixed(2)} este mês</p>
        <button className="btn btn-primario" onClick={novoForm}>+ Novo gasto</button>
      </div>

      {mostrarForm && (
        <div className="form-box">
          <h2 style={{ fontSize: '16px', marginBottom: '16px' }}>
            {editandoId ? 'Editar gasto' : 'Novo gasto'}
          </h2>
          {erro && <div className="alerta alerta-erro">{erro}</div>}
          <form onSubmit={salvar}>
            <div className="campo">
              <label>Descrição *</label>
              <input name="descricao" value={form.descricao} onChange={atualizar} placeholder="Conta de luz, aluguel..." required />
            </div>
            <div className="grid2">
              <div className="campo">
                <label>Valor (R$) *</label>
                <input name="valor" type="number" step="0.01" value={form.valor} onChange={atualizar} placeholder="150.00" required />
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
                <label>Data *</label>
                <input name="data" type="date" value={form.data} onChange={atualizar} required />
              </div>
              <div className="campo">
                <label>Tipo *</label>
                <select name="recorrente" value={form.recorrente} onChange={atualizar}>
                  <option value="false">Variável</option>
                  <option value="true">Fixo / Recorrente</option>
                </select>
              </div>
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
              <th>Descrição</th>
              <th>Categoria</th>
              <th>Data</th>
              <th>Tipo</th>
              <th>Valor</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {dados.gastos.length === 0 ? (
              <tr><td colSpan="6" className="vazio">Nenhum gasto cadastrado.</td></tr>
            ) : dados.gastos.map(g => (
              <tr key={g.id}>
                <td><strong>{g.descricao}</strong></td>
                <td>
                  {g.categoria_nome ? (
                    <span>{g.categoria_nome}</span>
                  ) : '—'}
                </td>
                <td>{g.data}</td>
                <td>
                  <span className={`badge ${g.recorrente ? 'badge-ativa' : 'badge-pendente'}`}>
                    {g.recorrente ? 'Fixo' : 'Variável'}
                  </span>
                </td>
                <td><strong>R$ {Number(g.valor).toFixed(2)}</strong></td>
                <td style={{ display: 'flex', gap: '6px' }}>
                  <button className="btn btn-cinza" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => editarForm(g)}>Editar</button>
                  <button className="btn btn-vermelho" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => excluir(g.id)}>Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
