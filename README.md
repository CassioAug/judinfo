# JudInfo

**JudInfo** é uma ferramenta de linha de comando (CLI) desenvolvida em Python para consultar informações de processos judiciais brasileiros diretamente da API pública [DataJud](https://datajud-wiki.cnj.jus.br/) do Conselho Nacional de Justiça (CNJ).

Esta ferramenta foi pensada para advogados, analistas e desenvolvedores que precisam de acesso rápido e automatizado a dados processuais sem a necessidade de navegar por múltiplos sites de tribunais.

## ✨ Funcionalidades

- **Consulta de Processos**: Busque um processo por seu número em um tribunal específico.
- **Busca Ampla**: Procure um processo em **todos** os tribunais suportados pela API de uma só vez.
- **Verificação de Status**: Verifique a disponibilidade (online/offline) da API do DataJud ou de tribunais específicos.
- **Listagem de Tribunais**: Exiba uma lista completa e organizada de todos os códigos de tribunais disponíveis para consulta.
- **Formatos de Saída**: Escolha como visualizar os dados do processo:
  - _resumo:_ Um resumo limpo e organizado (padrão).
  - _completo:_ Resumo mais os últimos 5 movimentos processuais.
  - _json:_ A saída de dados brutos da API, ideal para integração com outros sistemas.
- **Interface Amigável**: Comandos simples e intuitivos, com barras de progresso para operações demoradas.

## ⚙️ Instalação

Tenha o Python instalado e atualizado em sua máquina.

### 1. Clone o repositório

```bash
git clone https://github.com/CassioAug/judinfo.git
cd judinfo-cli
```

### 2. Crie um ambiente virtual e instale as dependências

#### WINDOWS (CMD)

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

#### WINDOWS (GIT BASH / POWERSHELL)

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

#### LINUX (DEBIAN / UBUNTU)

```bash
sudo apt update
sudo apt install python3-venv python3-pip git -y
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

## 🚀 Como Usar

## 🧰 Python version & production notes

- Recommended Python version: 3.8+ (code uses `fromisoformat` and f-strings; 3.7+ works but 3.8+ is preferred).
- For production deployments consider using a WSGI server (example using `gunicorn` on Linux):

```bash
# install production extras
pip install -r requirements-prod.txt

# run with gunicorn (Linux/WSGI environment):
gunicorn -w 4 -b 0.0.0.0:8000 judinfo_web:app
```

Note: `gunicorn` is not supported on Windows the same way; for local development on Windows use `python judinfo_web.py`.

## 🧰 Developer setup (local)

If you're contributing or running tests locally, create a venv and install development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install --editable .
```

Run tests and linters:

```powershell
# run tests
pytest -q

# format with black
black .

# static type check
mypy judinfo_cli.py judinfo_web.py
```


### 1. Listar todos os tribunais

Para ver uma lista completa de todos os códigos de tribunais que você pode usar nas buscas.

```bash
judinfo --listar-tribunais
```

### 2. Verificar o status da API e dos tribunais

Verificar o status da API:

```bash
judinfo --verificar api
```

Verificar um único tribunal:

```bash
judinfo -v tjmg
```

Verificar múltiplos tribunais:

```bash
judinfo -v tjsp,tjrj,trf1
```

Verificar todos os tribunais:

```bash
judinfo -v all
```

### 3. Consultar um processo

Consultar em tribunal específico:

```bash
judinfo --processo "NUMERO_DO_PROCESSO" --tribunal tjmg
```

Buscar processo em todos os tribunais:

```bash
judinfo -processo "NUMERO_DO_PROCESSO" -tribunal all
```

## 📝 Observações

O funcionamento e performance desta ferramenta depende diretamente da disponibilidade e velocidade da API DataJud do CNJ.
