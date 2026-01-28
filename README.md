# Admin Salu - Painel Administrativo

Painel administrativo para o portal de imoveis Salu.

## Funcionalidades

- Dashboard com estatisticas
- Gerenciamento de usuarios
- Gerenciamento de imoveis
- Gerenciamento de contatos/leads
- Gerenciamento de corretores
- Logs de importacao

## Requisitos

- Python 3.10+
- PostgreSQL

## Instalacao

1. Clone o repositorio:
```bash
git clone https://github.com/seu-usuario/admin-salu.git
cd admin-salu
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependencias:
```bash
pip install -r requirements.txt
```

4. Configure as variaveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configuracoes
```

5. Execute o servidor:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Auth
- `POST /api/auth/login` - Login admin
- `GET /api/auth/me` - Dados do admin logado

### Admin
- `GET /api/admin/dashboard` - Estatisticas do painel
- `GET /api/admin/users` - Listar usuarios
- `GET /api/admin/properties` - Listar imoveis
- `GET /api/admin/contacts` - Listar contatos
- `GET /api/admin/brokers` - Listar corretores
- `GET /api/admin/import-logs` - Logs de importacao

## Documentacao da API

Acesse `/docs` para ver a documentacao interativa (Swagger UI).
