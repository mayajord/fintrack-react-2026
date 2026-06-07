import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../App'

export default function Cadastrar() {
  const [form, setForm] = useState({ nome: '', email: '', senha: '', confirmar: '' })
  const [erro, setErro] = useState('')
  const { setUsuario } = useAuth()
  const navigate = useNavigate()

  function atualizar(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setErro('')
    if (form.senha !== form.confirmar) {
      setErro('As senhas não coincidem.')
      return
    }
    try {
      const res = await api.post('/auth/cadastrar', form)
      setUsuario(res.data)
      navigate('/')
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao criar conta.')
    }
  }

  return (
    <div className="auth-pagina">
      <div className="auth-caixa">
        <div className="auth-logo">FinTrack</div>
        <div className="auth-titulo">Criar conta</div>
        <div className="auth-sub">Preencha os dados abaixo</div>

        {erro && <div className="alerta alerta-erro">{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div className="campo">
            <label>Nome</label>
            <input name="nome" value={form.nome} onChange={atualizar} placeholder="Seu nome" required />
          </div>
          <div className="campo">
            <label>E-mail</label>
            <input name="email" type="email" value={form.email} onChange={atualizar} placeholder="seu@email.com" required />
          </div>
          <div className="campo">
            <label>Senha</label>
            <input name="senha" type="password" value={form.senha} onChange={atualizar} placeholder="Mínimo 6 caracteres" required />
          </div>
          <div className="campo">
            <label>Confirmar senha</label>
            <input name="confirmar" type="password" value={form.confirmar} onChange={atualizar} placeholder="Repita a senha" required />
          </div>
          <button type="submit" className="btn btn-primario" style={{ width: '100%', padding: '10px' }}>
            Criar conta
          </button>
        </form>

        <p style={{ marginTop: '16px', fontSize: '13px', color: '#64748b', textAlign: 'center' }}>
          Já tem conta? <Link to="/login" style={{ color: '#2563eb' }}>Entrar</Link>
        </p>
      </div>
    </div>
  )
}
