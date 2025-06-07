# Google Calendar API Backend

## Getting Started

Download OAuth 2.0 credentials from Google Cloud Platform and place `credentials.json` in `creds/` directory

https://console.cloud.google.com/apis/credentials

```sh
cp ~/Downloads/client_secret_*.json ./creds/credentials.json
```

## gcalcli

```bash
# Install from Git Repository:
pip install git+https://github.com/tpantsar/gcalcli.git

# Install from .whl (Wheel) File:
python -m build
pip install dist/package.whl
```

## Create virtual environment

- [uv](https://docs.astral.sh/uv/)

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install project dependencies:

```sh
uv sync
```

Activate the virtual environment:

```sh
source .venv/bin/activate  # On macOS/Linux
source .venv/Scripts/activate  # On Windows
```

- [pip](https://pip.pypa.io/en/stable/installation/)

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
source .venv/Scripts/activate  # On Windows
```

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

```bash
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del miniconda.exe
```

Create conda environment

```bash
conda env create --file environment.yml
conda env update --file environment.yml
conda env update --file environment.yml --prune
conda activate google-calendar-api
conda install <package>
```

Install pyproject.toml dependencies

```bash
# Development
pip install -e .

# Production, this installs only the dependencies listed under [project.dependencies]
pip install .
```

## Run Flask API

```bash
# Run the authorization flow in the browser after starting the app
python app.py
```

## API Endpoints

```sh
# List all calendars
http://127.0.0.1:5000/api/calendars/

# List events from primary calendar
http://127.0.0.1:5000/api/events/primary/?start_date=2025-01-01&end_date=2025-03-31&search_query=Test
```

## Running tests

see [tests/README.md](tests/README.md)

## Invoke commands (tasks.py)

```bash
# Check linting
invoke check

# Remove unused imports, sort imports, format code.
invoke format
```

## Run images in interactive mode:

```bash
docker run --rm -it google-calendar-backend bash
docker run --rm -it google-calendar-frontend bash
```

## Docker deployment:

```bash
docker build -t google-calendar-backend .
```

### Flask API

```bash
docker run --rm -it -p 5000:5000 google-calendar-backend
```

### CLI application

```bash
docker run --rm -it google-calendar-backend bash -c "python terminal.py"
```

---

### CLI application (Legacy)

```bash
docker compose -f docker-compose.cli.yml up --build
docker run --rm -it google-calendar-cli bash -c "python terminal.py"

docker build -f Dockerfile.cli -t google-calendar-cli .
```

## Resources

- [Google Calendar API (Google Cloud)](https://console.cloud.google.com/apis/api/calendar-json.googleapis.com)
