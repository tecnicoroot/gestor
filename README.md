# No meu computador com Ubuntu Linux.

## cria a pasta onde o projeto sera criado.
```bash
# cria a pasta
mkdir nome-do-projeto 
# acessa a pasta
cd nome-do-projeto 
# cria o ambiente virtual onde o s pacotes serão instalados
python3 -m venv .venv 
# ativa o ambiente virtual no Ubuntu
source /home/david/Projetos/python/gestor/.venv/bin/activate
```

# Estrutura do projeto
```
meu_app/
│
├── main.py
├── app.py                  # inicialização da aplicação
│
├── core/                  # configurações centrais
│   ├── config.py
│   ├── theme.py
│   └── router.py          # troca de telas
│
├── models/                # regras de negócio e dados
│   └── user_model.py
│
├── services/              # lógica mais complexa (regras, APIs, DB)
│   └── auth_service.py
│
├── controllers/           # conecta view ↔ service
│   └── login_controller.py
│
├── views/                 # interface (CustomTkinter)
│   ├── screens/
│   │   ├── login_view.py
│   │   └── dashboard_view.py
│   │
│   └── components/        # componentes reutilizáveis
│       ├── button.py
│       └── input.py
│
├── utils/                 # helpers
│   └── helpers.py
│
└── assets/                # imagens, ícones
```