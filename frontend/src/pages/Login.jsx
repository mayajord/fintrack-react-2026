import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api'
import { useAuth } from '../App'

export default function Login() {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const { setUsuario } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setErro('')
    try {
      const res = await api.post('/auth/login', { email, senha })
      setUsuario(res.data)
      navigate('/')
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao fazer login.')
    }
  }

  return (
    <div className="auth-pagina">
      <div className="auth-caixa">
        <div className="auth-logo">FinTrack</div>
        <div className="auth-titulo">Entrar</div>
        <div className="auth-sub">Faça login para continuar</div>

        {erro && <div className="alerta alerta-erro">{erro}</div>}

        <form onSubmit={handleSubmit}>
          <div className="campo">
            <label>E-mail</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="seu@email.com"
              required
            />
          </div>
          <div className="campo">
            <label>Senha</label>
            <input
              type="password"
              value={senha}
              onChange={e => setSenha(e.target.value)}
              placeholder="Sua senha"
              required
            />
          </div>
          <button type="submit" className="btn btn-primario" style={{ width: '100%', padding: '10px' }}>
            Entrar
          </button>
        </form>

        <p style={{ marginTop: '16px', fontSize: '13px', color: '#64748b', textAlign: 'center' }}>
          Não tem conta? <Link to="/cadastrar" style={{ color: '#2563eb' }}>Criar conta</Link>
        </p>
      </div>
    </div>
  )
}
