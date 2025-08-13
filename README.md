# Projeto Mercado de Troca

## Dependências python

- black 25.1.0
- blinker 1.9.0
- click 8.2.1
- colorama 0.4.6
- flake8 7.3.0
- Flask 3.1.1
- Flask-Login 0.6.3
- itsdangerous 2.2.0
- Jinja2 3.1.6
- MarkupSafe 3.0.2
- mccabe 0.7.0
- mypy_extension 1.1.0
- packaging 25.0
- pathspec 0.12.1
- platformdirs 4.3.8
- pycodestyle 2.14.0
- pyflakes 3.4.0
- Werkzeug 3.1.3


## Como rodar

1. Clone esse repositório `git clone https://github.com/Joyuv/projeto2romero`
2. Crie um virtual environment python (venv) `python3` ou `py` no windows `{seu comando python} -m venv env`
3. Ative o venv `source env/bin/activate` no linux e `env\Scripts\activate` no windows cmd ou `source env/Scripts/activate` num terminal bash no windows
4. Instale as dependências `pip install -r requirements.txt`
5. Rode o código `python3 app.py` ou `py app.py`

## Requisitos funcionais

- O usuário deve poder logar no sistema
- O usuário após login deve ser capaz de cadastrar um produto
- O usuário deve ser capaz de olhar outros produtos cadastrados por outros usuários
- O usuário deve ser capaz de adicionar, checar, editar e remover produtos em uma aba específica dentro da área de usuário
- O sistema deve notificar o usuário quando outro usuário se interessar pelo seu produto
- O usuário deve ser capaz de se interessar por produtos postados, fazendo uma oferta
- O usuário deve ser capaz de analisar interesses de outros usuários e negar ou conceder
- O sistema deve notificar o usuário quando seu pedido for negado ou aceito, e, se aceito gerar um qrcode e um id aleatório para pagamento via pix

## [Como contribuir](https://github.com/Joyuv/projeto2romero/blob/main/CONTRIBUTING.md)
