# JudInfo

**JudInfo** é uma ferramenta de linha de comando (CLI) escrita em Python para consultar informações de processos judiciais brasileiros por meio da API pública DataJud (CNJ).

> Este arquivo contém instruções em Português (Brasil). A versão em inglês está em `README.en.md`.

## Funcionalidades principais

- Consultar um processo por número em um tribunal específico.
- Buscar um processo em todos os tribunais suportados (busca ampla).
- Verificar status da API/tribunais (online/offline).
- Listar códigos de tribunais disponíveis.
- Saídas em `resumo` (padrão), `completo` e `json`.

## Requisitos

- Python 3.8+ (recomendado)
- Git

## Instalação

1. Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/CassioAug/judinfo.git
cd judinfo
```

2. Crie um ambiente virtual e instale dependências.

- Windows (Prompt de Comando):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

- Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

- macOS / Linux / Git Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

> Observação: em PowerShell a política de execução pode impedir a execução de scripts; se necessário, ajuste `Set-ExecutionPolicy` com cautela.

## Uso

Você pode usar a CLI instalada (`judinfo`) ou executar o script diretamente com Python.

- Listar tribunais:

```bash
judinfo --listar-tribunais
# ou
python judinfo_cli.py --listar-tribunais
```

- Verificar status (API / tribunais):

```bash
judinfo --verificar api
judinfo -v tjmg
judinfo -v tjsp,tjrj,trf1
judinfo -v all
```

- Consultar um processo (tribunal específico):

```bash
judinfo --processo "NUMERO_DO_PROCESSO" --tribunal tjmg
```

- Buscar em todos os tribunais:

```bash
judinfo --processo "NUMERO_DO_PROCESSO" --tribunal all
```

- Executar a interface web localmente:

## Exemplos

Exemplos rápidos com números fictícios (apenas para demonstração):

- Consultar um processo no Tribunal de Justiça de Minas Gerais (TJMG):

```bash
judinfo --processo "0000000-00.0000.0.00.0000" --tribunal tjmg
# ou
python judinfo_cli.py --processo "0000000-00.0000.0.00.0000" --tribunal tjmg
```

- Buscar em todos os tribunais (busca ampla):

```bash
judinfo --processo "0000000-00.0000.0.00.0000" --tribunal all
```

<!-- fim dos exemplos -->

- Executar a interface web localmente:

```powershell
python judinfo_web.py
# abra http://127.0.0.1:5000 no navegador
```

## Desenvolvimento e testes

Instale dependências de desenvolvimento e rode testes:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install --editable .

# rodar testes
pytest -q

# formatar (opcional)
black .

# checagem de tipos (opcional)
mypy judinfo_cli.py judinfo_web.py
```

## Produção

- Para produção, use um servidor WSGI (por exemplo `gunicorn` no Linux):

```bash
pip install -r requirements-prod.txt
gunicorn -w 4 -b 0.0.0.0:8000 judinfo_web:app
```

- No Windows, para desenvolvimento local, use `python judinfo_web.py`.

## Observações

O funcionamento depende da disponibilidade da API DataJud do CNJ.

A interface web utiliza CDNs (Bootstrap, Font Awesome). Se estiver em rede restrita, verifique o acesso às CDNs.
