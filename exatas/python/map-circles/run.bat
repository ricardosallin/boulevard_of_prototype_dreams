@echo off

:: Navegar até a pasta do projeto (mude para a sua pasta)
cd /d "C:\Users\projects\map_circles"

:: Ativar o ambiente virtual
call venv\Scripts\activate.bat

:: Abrir o navegador com a URL padrão
start http://127.0.0.1:5000 

:: Executar o servidor
python app.py
