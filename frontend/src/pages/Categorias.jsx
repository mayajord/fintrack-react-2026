import React, { useState, useEffect } from 'react'
import api from '../api'

const FORM_VAZIO = { nome: '', icone: '📌', cor: '#2563eb' }
const CORES = ['#2563eb', '#16a34a', '#dc2626', '#d97706', '#7c3aed', '#0891b2', '#db2777', '#059669', '#ea580c', '#4f46e5']

export default function Categorias() {
  const [categorias, setCategorias] = useState([])
  const [form, setForm] = useState(FORM_VAZIO)
  const [editandoId, setEditandoId] = useState(null)
  const [mostrarForm, setMostrarForm] = useState(false)
  const [erro, setErro] = useState('')

  async function carregar() {
    const res = await api.get('/categorias/')
    setCategorias(res.data)
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

  function editarForm(c) {
    setForm({ nome: c.nome, icone: c.icone || '📌', cor: c.cor || '#2563eb' })
    setEditandoId(c.id)
    setMostrarForm(true)
    setErro('')
  }

  async function salvar(e) {
    e.preventDefault()
    setErro('')
    try {
      if (editandoId) {
        await api.put(`/categorias/${editandoId}`, form)
      } else {
        await api.post('/categorias/', form)
      }
      setMostrarForm(false)
      carregar()
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao salvar.')
    }
  }

  async function excluir(id) {
    if (!confirm('Excluir esta categoria?')) return
    try {
      await api.delete(`/categorias/${id}`)
      carregar()
    } catch (err) {
      alert(err.response?.data?.erro || 'Erro ao excluir.')
    }
  }

  return (
    <div>
      <h1>Categorias</h1>
      <p className="subtitulo">Organize seus gastos e assinaturas</p>

      <div className="toolbar">
        <p>{categorias.length} categorias</p>
        <button className="btn btn-primario" onClick={novoForm}>+ Nova categoria</button>
      </div>

      {mostrarForm && (
        <div className="form-box">
          <h2 style={{ fontSize: '16px', marginBottom: '16px' }}>
            {editandoId ? 'Editar categoria' : 'Nova categoria'}
          </h2>
          {erro && <div className="alerta alerta-erro">{erro}</div>}
          <form onSubmit={salvar}>
            <div className="campo">
              <label>Nome *</label>
              <input name="nome" value={form.nome} onChange={atualizar} placeholder="Alimentação, Casa..." required />
            </div>
            <div className="grid2">
              <div className="campo">
                <label>Ícone (emoji)</label>
                <input name="icone" value={form.icone} onChange={atualizar} placeholder="📌" maxLength={4} style={{ fontSize: '20px', textAlign: 'center' }} />
              </div>
              <div className="campo">
                <label>Cor</label>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <input type="color" name="cor" value={form.cor}
                    onChange={atualizar}
                    style={{ width: '50px', height: '40px', padding: '2px', cursor: 'pointer', border: '1px solid #d1d5db', borderRadius: '6px' }} />
                  <input name="cor" value={form.cor} onChange={atualizar}
                    placeholder="#2563eb" style={{ fontFamily: 'monospace', flex: 1, padding: '9px 12px', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '14px' }} />
                </div>
              </div>
            </div>

            {/* Paleta rápida */}
            <div className="campo">
              <label>Paleta rápida</label>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '4px' }}>
                {CORES.map(cor => (
                  <div key={cor}
                    onClick={() => setForm({ ...form, cor })}
                    style={{
                      width: '28px', height: '28px', borderRadius: '6px',
                      background: cor, cursor: 'pointer',
                      border: form.cor === cor ? '3px solid #1e293b' : '2px solid transparent'
                    }}
                  />
                ))}
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
              <th>Categoria</th>
              <th>Ícone</th>
              <th>Cor</th>
              <th>Assinaturas</th>
              <th>Gastos</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {categorias.length === 0 ? (
              <tr><td colSpan="6" className="vazio">Nenhuma categoria cadastrada.</td></tr>
            ) : categorias.map(c => (
              <tr key={c.id}>
                <td>
                  <span className="cor-dot" style={{ background: c.cor }} />
                  <strong>{c.nome}</strong>
                </td>
                <td style={{ fontSize: '20px' }}>{c.icone}</td>
                <td><code style={{ fontSize: '12px', color: '#64748b' }}>{c.cor}</code></td>
                <td>{c.qtd_assinaturas}</td>
                <td>{c.qtd_gastos}</td>
                <td style={{ display: 'flex', gap: '6px' }}>
                  <button className="btn btn-cinza" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => editarForm(c)}>Editar</button>
                  <button className="btn btn-vermelho" style={{ fontSize: '12px', padding: '4px 10px' }} onClick={() => excluir(c.id)}>Excluir</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
