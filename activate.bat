:: run with `activate.bat` to activate the virtual environment

@echo off
IF NOT EXIST .venv (
    py -m venv .venv
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) ELSE (
    call .venv\Scripts\activate
    where python
)