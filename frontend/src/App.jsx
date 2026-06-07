import React, { useState, useEffect, createContext, useContext } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import api from './api'

import Login from './pages/Login'
import Cadastrar from './pages/Cadastrar'
import Dashboard from './pages/Dashboard'
import Boletos from './pages/Boletos'
import Assinaturas from './pages/Assinaturas'
import Gastos from './pages/Gastos'
import Categorias from './pages/Categorias'
import Admin from './pages/Admin'
import Layout from './components/Layout'

export const AuthContext = createContext(null)

export function useAuth() {
  return useContext(AuthContext)
}

function RotaPrivada({ children }) {
  const { usuario, carregando } = useAuth()
  if (carregando) return <div className="carregando">Carregando...</div>
  if (!usuario) return <Navigate to="/login" />
  return children
}

export default function App() {
  const [usuario, setUsuario] = useState(null)
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    api.get('/auth/me')
      .then(res => setUsuario(res.data))
      .catch(() => setUsuario(null))
      .finally(() => setCarregando(false))
  }, [])

  return (
    <AuthContext.Provider value={{ usuario, setUsuario, carregando }}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/cadastrar" element={<Cadastrar />} />

          <Route path="/" element={
            <RotaPrivada>
              <Layout />
            </RotaPrivada>
          }>
            <Route index element={<Dashboard />} />
            <Route path="boletos" element={<Boletos />} />
            <Route path="assinaturas" element={<Assinaturas />} />
            <Route path="gastos" element={<Gastos />} />
            <Route path="categorias" element={<Categorias />} />
            <Route path="admin" element={<Admin />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  )
}
