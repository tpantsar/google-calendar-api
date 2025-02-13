## Download OAuth 2.0 credentials from Google Cloud Platform and place credentials.json in /creds directory

https://console.cloud.google.com/apis/credentials

## Install miniconda

```bash
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del miniconda.exe
```

## gcalcli

```bash
# Install from Git Repository:
pip install git+https://github.com/tpantsar/gcalcli.git

# Install from .whl (Wheel) File:
python -m build
pip install dist/package.whl
```

## Run tests:

```bash
cd backend
pytest
```

## Commands:

```bash
conda env create --file environment.yml
conda env update --file environment.yml
conda env update --file environment.yml --prune
conda activate google-calendar-api
conda install <package>

python -m venv .venv
source .venv/bin/activate
source .venv/Scripts/activate
pip install -r requirements.txt

python app.py
http://127.0.0.1:5000/
```

## Custom commands:

```bash
# Check linting
invoke check

# Remove unused imports, sort imports, format code.
invoke format
```

## Google Calendar API:

https://console.cloud.google.com/apis/api/calendar-json.googleapis.com

## Docker deployment:

### Flask API

```bash
docker build -t google-calendar-api .
docker run --rm -it -p 5000:5000 google-calendar-api
```

---

### CLI application (Legacy)

```bash
docker compose -f docker-compose.cli.yml up --build
docker run --rm -it google-calendar-cli bash -c "python terminal.py"

docker build -f Dockerfile.cli -t google-calendar-cli .
```
