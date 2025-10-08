# JudInfo

**JudInfo** is a command-line interface (CLI) tool developed in Python to query information on Brazilian legal cases directly from the public API [DataJud](https://datajud-wiki.cnj.jus.br/), provided by the National Council of Justice (CNJ) of Brazil.

This tool is designed for lawyers, analysts, and developers who need fast, automated access to case data without having to navigate multiple court websites.

## ✨ Features

- **Case Search**: Look up a case by its unique number in a specific court.  
- **Broad Search**: Search for a case across **all** courts supported by the API at once.  
- **Status Check**: Verify the availability (online/offline) of the DataJud API or specific court endpoints.  
- **List Courts**: Display a complete, organized list of all available court codes for queries.  
- **Output Formats**: Choose how to view the case data:  
  - _resumo:_ A clean and organized summary (default).  
  - _completo:_ The summary plus the last 5 case movements.  
  - _json:_ The raw data output from the API, ideal for integration with other systems.  
- **User-Friendly Interface**: Simple and intuitive commands, with progress bars for time-consuming operations.

## ⚙️ Instllation

You must have Python and Git installed and updated on your machine.

### 1. Clone the repository

```bash
git clone https://github.com/CassioAug/judinfo.git
cd judinfo-cli
```

### Create a virtual environment and install dependencies

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

## 🚀 How to Use

### 1. List all courts

To see a complete list of all the court codes you can use in your searches.

```bash
judinfo --listar-tribunais
```

### 2. Check API and Court Status

Check API status:

```bash
judinfo --verificar api
```

Check a single court:

```bash
judinfo -v tjmg
```

Check multiple courts:

```bash
judinfo -v tjsp,tjrj,trf1
```

Check all courts:

```bash
judinfo -v all
```

### 3. Query a court case

Query in a specific court:

```bash
judinfo --processo "NUMERO_DO_PROCESSO" --tribunal tjmg
```

Search for a case in all courts:

```bash
judinfo -processo "NUMERO_DO_PROCESSO" -tribunal all
```

## 📝 Notes

The functionality and performance of this tool are directly dependent on the availability and speed of the CNJ's DataJud API.