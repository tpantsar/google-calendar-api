## Download and add credentials.json file to the root of the project

https://console.cloud.google.com/apis/credentials?project=unique-acronym-406815

## Install miniconda

curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del miniconda.exe

## Commands:

```
conda env create --file environment.yml
conda env update --file environment.yml
conda env update --file environment.yml --prune

(bash) source C:/Users/tomi_/miniconda3/Scripts/activate google-calendar-year
(powershell) C:/Users/tomi_/miniconda3/Scripts/activate.bat google-calendar-year

cd src
python app.py
http://127.0.0.1:5000/

## This will run the autoflake and isort commands to remove unused imports and sort the remaining ones in all Python files in your project.
make format

# Remove unused imports
autoflake --remove-all-unused-imports --in-place --recursive .

# Sort imports
isort .
```

## Google Calendar API:

https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/metrics?hl=fi&project=unique-acronym-406815
