@echo off
cd /d "CAMINHO\DO\PROJETO"  // Navegar até a pasta do projeto
call venv\Scripts\activate.bat  // Ativar o ambiente virtual
python app.py  // Executar o servidor
start http://127.0.0.1:5000  // Abrir o navegador com a URL padrão
