## Add credentials.json file to the root of the project

## Install miniconda

curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del miniconda.exe

## Commands:

```
conda env create --file environment.yml
conda env update --file environment.yml
conda env update --file environment.yml --prune
```
