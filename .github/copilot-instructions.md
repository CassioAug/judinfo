<!-- Copilot / AI agent instructions for quick onboarding in the JudInfo repo -->

# Quick instructions for AI coding assistants

Keep this short and specific to this project so an AI can be immediately productive.

- Project shape: Python CLI + small Flask web UI. Key files:

  - `judinfo_cli.py` — the click-based CLI and core client `DataJudSimple`.
  - `judinfo_web.py` — tiny Flask app that exposes `/courts`, `/search` and `/status`.
  - `config.py` — contains `API_KEY` used by `DataJudSimple` (replace with secret management for production).
  - `templates/index.html`, `static/script.js`, `static/style.css` — web UI assets.

- Big picture / data flow:
  1. CLI or web UI calls `DataJudSimple` methods.

2.  `DataJudSimple` issues synchronous HTTP POSTs to DataJud endpoints (base `https://api-publica.datajud.cnj.jus.br`).
3.  CLI formats the first hit and prints a `resumo` or `completo` view; the web UI aggregates results as JSON.

- Important behavioral details (use these when changing code):

  - `DataJudSimple.consultar_processo(numero, tribunal)` returns the first `_source` hit or `None` when no results.
  - `buscar_em_todos_tribunais(...)` iterates all codes from `get_all_courts()` and stops on the first found result.
  - Timeouts: requests use 30s for searches, 10s for status checks — preserve these unless you intentionally change reliability semantics.

- Web API conventions:

  - `GET /courts` -> returns `get_all_courts_categorized()` JSON.
  - `POST /search` -> expects JSON {"numero": "<case>", "tribunais": ["tjmg","tjsp"]} and returns an array of found results.
  - `POST /status` -> expects JSON {"tribunais": [...] } and returns a mapping of tribunal->status object.

- Developer workflows (documented and reproducible):

  - Install in editable mode after creating a venv: `pip install -r requirements.txt` then `pip install --editable .` (see `README.md`).
  - CLI: once installed the console-script `judinfo` is the intended entry in the README; you can also run `python judinfo_cli.py` for quick dev.
  - Web: `python judinfo_web.py` runs the Flask app directly (suitable for local dev).

- Coding conventions & quick checks for PRs:

  - Keep changes small and focused; the repo has no tests—run the related script locally to validate behavior.
  - When touching networking code, preserve existing status codes and error-handling style (return dicts with `success`/`error` for status checks).
  - Use the tribunal codes exactly as listed by `get_all_courts()` (lowercase short codes: `tjmg`, `tjsp`, `trf1`, etc.).

- Examples to reference in edits:

  - To add a new CLI option, follow the `click` pattern in `judinfo_cli.py` (see `main()` and `@click.option` usage).
  - To extend the web UI, add endpoints in `judinfo_web.py` and update `templates/index.html` + `static/script.js` to consume them.

- Security note:
  - `config.py` currently contains a literal `API_KEY`. For production or PRs that will be published, replace with environment-based secret loading and avoid leaking keys in commits.

If anything below is unclear or you want extra examples (unit tests, CI steps, or deployment notes), say which area to expand.

- Additional notes for maintainers:
  - Recommended Python version: 3.8+.
  - `setup.py` now includes `Flask` in `install_requires` so `pip install .` pulls web dependencies.
  - A `requirements-prod.txt` file was added with optional production extras (`gunicorn`, `python-dotenv`) — install it only for deployments.
  - A `requirements-dev.txt` file exists with recommended developer tooling: `pytest`, `black`, `isort`, `flake8`, `mypy` and `pre-commit`.
  - Local developer steps: create a venv, install `requirements.txt` and `requirements-dev.txt`, then `pip install --editable .` (see README.md developer section).
