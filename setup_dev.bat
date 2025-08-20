@echo off
REM Development setup script for Windows

echo Setting up development environment...

REM Create virtual environment
echo Creating virtual environment...
uv venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
uv pip install -e .

echo Development environment setup complete!
echo To activate the environment, run: .venv\Scripts\activate.bat