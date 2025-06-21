@echo off
rem Mover para a pasta do projeto
cd /d "CAMINHO\DO\PROJETO"

rem Ativar o ambiente virtual
call "CAMINHO\DO\PROJETO\venv\Scripts\activate.bat"

rem Abrir o navegador
start http://127.0.0.1:5000

rem Executar o servidor
python app.py
