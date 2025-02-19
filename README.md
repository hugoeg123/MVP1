# Health MVP 🏥

Aplicação full-stack para gestão de saúde com **backend Python (FastAPI)** e **frontend React (TypeScript)**, desenvolvida para alta performance e fácil escalabilidade.

## Tech Stack 🛠️
| Camada       | Tecnologias                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **Backend**  | FastAPI, PostgreSQL, Redis, SQLAlchemy Async, Celery, Pydantic, Poetry      |
| **Frontend** | React 18, TypeScript, Vite, React Query, Tailwind CSS, Shadcn/ui, Zustand   |
| **Infra**    | Docker, NGINX, GitHub Actions, Sentry, Prometheus                           |

## Features Chave ✨
- Autenticação OAuth2 com refresh tokens
- Cache distribuído com Redis
- Operações assíncronas com Celery (ex: integração Google Calendar)
- Monitoramento de performance integrado
- Design System consistente com Tailwind

## Setup Rápido 🚀
```bash
# 1. Clone o repositório
git clone https://github.com/hugoeg123/MVP1.git
cd MVP1

# 2. Inicie os containers e construa as imagens
docker-compose up --build

# 3. Em outro terminal, execute as migrações do banco
docker-compose exec backend alembic upgrade head

# 4. Se necessário, instale as dependências do frontend
cd client && npm install

# 5. Para executar os testes do backend
docker-compose exec backend pytest -v

# 6. Acesse:
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:3000