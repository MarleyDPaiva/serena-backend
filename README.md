# Serena

Sistema web para gerenciamento de consultas de psiquiatria, desenvolvido como projeto acadêmico do curso de Análise e Desenvolvimento de Sistemas.

## Sobre o projeto

O Serena tem como objetivo facilitar o gerenciamento de consultas, pacientes, profissionais e especialidades em uma única aplicação.

O projeto está sendo desenvolvido como atividade acadêmica na disciplina de Programação Web.

## Tecnologias

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended

### Banco de dados

- PostgreSQL

### Frontend

- Em desenvolvimento

## Funcionalidades

Atualmente o projeto está em desenvolvimento.

As principais funcionalidades planejadas são:

- Cadastro e autenticação de usuários
- Cadastro de pacientes
- Cadastro de profissionais
- Cadastro de especialidades
- Agendamento de consultas
- Gerenciamento de consultas
- Autenticação e autorização de usuários

## Estrutura do projeto

```text
Projeto Serena/
│
├── app/
│   ├── models/
│   │   ├── usuario.py
│   │   ├── paciente.py
│   │   ├── profissional.py
│   │   ├── especialidade.py
│   │   └── consulta.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── pacientes.py
│   │   ├── profissionais.py
│   │   └── consultas.py
│   │
│   ├── utils/
│   │   └── decorator.py
│   │
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── seed.py