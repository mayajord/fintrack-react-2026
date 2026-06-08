import React from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../App'
import api from '../api'

export default function Layout() {
  const { usuario, setUsuario } = useAuth()
  const navigate = useNavigate()

  async function sair() {
    await api.post('/auth/logout')
    setUsuario(null)
    navigate('/login')
  }

  const isAdmin = usuario?.email === 'fintrack@admin.com' || usuario?.role === 'admin'

  return (
    <div className="layout">
      <div className="sidebar">
        <div className="sidebar-logo">
          FinTrack
          <span>Controle financeiro</span>
        </div>

        <nav>
          <NavLink to="/" end className={({ isActive }) => isActive ? 'ativo' : ''}>
            Dashboard
          </NavLink>
          <NavLink to="/boletos" className={({ isActive }) => isActive ? 'ativo' : ''}>
            Boletos
          </NavLink>
          <NavLink to="/assinaturas" className={({ isActive }) => isActive ? 'ativo' : ''}>
            Assinaturas
          </NavLink>
          <NavLink to="/gastos" className={({ isActive }) => isActive ? 'ativo' : ''}>
            Gastos
          </NavLink>
          <NavLink to="/categorias" className={({ isActive }) => isActive ? 'ativo' : ''}>
            Categorias
          </NavLink>
          {isAdmin && (
            <NavLink to="/admin" className={({ isActive }) => isActive ? 'ativo' : ''}>
              Admin
            </NavLink>
          )}
        </nav>

        <div className="sidebar-user">
          <p>Logado como:</p>
          <strong>{usuario?.nome}</strong>
          <br />
          <button onClick={sair}>Sair</button>
        </div>
      </div>

      <div className="conteudo">
        <Outlet />
      </div>
    </div>
  )
}
