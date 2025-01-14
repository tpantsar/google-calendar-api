## Download OAuth 2.0 credentials from Google Cloud Platform and place in /src/output directory

https://console.cloud.google.com/apis/credentials?project=unique-acronym-406815

## Install miniconda

curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del miniconda.exe

## Run tests:

```bash
cd backend
pytest
```

## Commands:

```
conda install <package>
conda env create --file environment.yml
conda env update --file environment.yml
conda env update --file environment.yml --prune

pip install -r requirements.txt

(bash) source C:/Users/tomi_/miniconda3/Scripts/activate google-calendar-api
(powershell) C:/Users/tomi_/miniconda3/Scripts/activate.bat google-calendar-api

cd src
python app.py
http://127.0.0.1:5000/
```

## Custom commands:

```
invoke autoflake
invoke isort

# Run both autoflake and isort (format task)
invoke format
```

## Google Calendar API:

https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/metrics?hl=fi&project=unique-acronym-406815

# Docker deployment:

```bash
docker build -t google-calendar-api .
docker run --rm -it -p 5000:5000 google-calendar-api
```
