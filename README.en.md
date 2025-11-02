# JudInfo

**JudInfo** is a small command-line (CLI) Python tool to query Brazilian court case information using the public DataJud API from the National Council of Justice (CNJ).

This README contains instructions in English. The Portuguese version is available at `README.md`.

## Features

- Case search by number on a specific court.
- Broad search across all supported courts.
- Status checks for API and court endpoints.
- List available court codes.
- Output formats: `resumo` (default), `completo`, `json`.

## Installation

1. Clone the repository and enter the project folder:

```bash
git clone https://github.com/CassioAug/judinfo.git
cd judinfo
```

2. Create a virtual environment and install dependencies.

- Windows (Command Prompt):

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

## How to Use

You can use the installed `judinfo` command (when installed) or run the scripts directly with Python.

- List courts:

```bash
judinfo --listar-tribunais
# or
python judinfo_cli.py --listar-tribunais
```

- Check API / court status:

```bash
judinfo --verificar api
judinfo -v tjmg
judinfo -v tjsp,tjrj,trf1
judinfo -v all
```

- Query a case in a specific court:

```bash
judinfo --processo "CASE_NUMBER" --tribunal tjmg
```

- Query across all courts:

```bash
judinfo --processo "CASE_NUMBER" --tribunal all
```

- Run the web interface locally:

## Examples

Quick examples using fake case numbers (for demonstration only):

- Query a case on TJMG:

```bash
judinfo --processo "0000000-00.0000.0.00.0000" --tribunal tjmg
# or
python judinfo_cli.py --processo "0000000-00.0000.0.00.0000" --tribunal tjmg
```

- Broad search across all courts:

```bash
judinfo --processo "0000000-00.0000.0.00.0000" --tribunal all
```

<!-- end examples -->

- Run the web interface locally:

```bash
python judinfo_web.py
# open http://127.0.0.1:5000 in your browser
```

## Development & Tests

Install development dependencies and run tests:

```bash
python -m venv .venv
source .venv/bin/activate  # or use the appropriate Windows activation
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install --editable .

pytest -q
```

## Production

For production deployments use a WSGI server such as `gunicorn` (Linux):

```bash
pip install -r requirements-prod.txt
gunicorn -w 4 -b 0.0.0.0:8000 judinfo_web:app
```

Note: on Windows use `python judinfo_web.py` for local development.

## Notes

This project depends on the availability and responsiveness of the CNJ DataJud API.

The web UI references CDNs (Bootstrap, Font Awesome); in restricted networks ensure CDN access or self-host the assets.
