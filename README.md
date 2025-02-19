# Health MVP 🏥

Aplicação monolítica de gestão de saúde desenvolvida com Django, oferecendo uma solução completa e de fácil implantação.

## Tech Stack 🛠️
- **Framework:** Django 5.0.1
- **Frontend:** Django Templates, Crispy Forms, Bootstrap 5
- **Database:** PostgreSQL
- **Autenticação:** Django AllAuth
- **Estilo:** Django Widget Tweaks

## Features ✨
- Sistema completo de autenticação (login/registro)
- Gestão de perfil de usuário
- Agendamento de consultas
- Histórico médico
- Interface administrativa
- Formulários responsivos

## Setup Rápido 🚀

```bash
# 1. Clone o repositório
git clone https://github.com/hugoeg123/MVP1.git
cd MVP1

# 2. Crie e ative um ambiente virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações
python manage.py migrate

# 5. Crie um superusuário
python manage.py createsuperuser

# 6. Inicie o servidor
python manage.py runserver

# 7. Acesse:
# Aplicação: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## Estrutura do Projeto 📁
```
health_mvp/
├── manage.py
├── health_mvp/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   └── (autenticação e perfis)
├── appointments/
│   └── (agendamentos)
├── medical_records/
│   └── (prontuários)
└── templates/
    └── (templates HTML)
```