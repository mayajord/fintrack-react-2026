# FinTrack — React + Flask

Projeto de controle financeiro pessoal com frontend em React e backend em Flask.

## Como rodar

### Backend

```bash
cd backend
pip install -r requirements.txt
python servidor_api.py
# Roda em http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Abre em http://localhost:5173
```

## Estrutura

```
backend/
  servidor_api.py        ← novo servidor que serve JSON
  servidor.py            ← servidor original (Jinja2) — não modificado
  blueprints/
    api_auth.py          ← POST /api/auth/login, /logout, /cadastrar
    api_dashboard.py     ← GET  /api/dashboard/
    api_boleto.py        ← CRUD /api/boletos/
    api_assinatura.py    ← CRUD /api/assinaturas/
    api_categoria.py     ← CRUD /api/categorias/
    api_gasto.py         ← CRUD /api/gastos/
    api_admin.py         ← GET  /api/admin/
    api_relatorio.py     ← GET  /api/relatorio/csv
  modelos/, repository/, service/, utils/  ← originais, não modificados

frontend/
  src/
    App.jsx              ← rotas e autenticação
    api.js               ← axios configurado
    style.css            ← estilo simples
    components/
      Layout.jsx         ← sidebar + conteúdo
    pages/
      Login.jsx
      Cadastrar.jsx
      Dashboard.jsx
      Boletos.jsx
      Assinaturas.jsx
      Gastos.jsx
      Categorias.jsx
      Admin.jsx
```

## O que mudou

- `servidor_api.py` criado ao lado do `servidor.py` original
- Novos blueprints `api_*.py` criados (os `bp_*.py` originais continuam intactos)
- Todo o frontend em React (a pasta `templates/` não é mais usada)
- `Flask-Cors` adicionado ao requirements.txt
