@echo off
set "FLASK_APP=app:app"
waitress-serve --port=8000 %FLASK_APP%
