call .venv\Scripts\activate.bat
@REM python server.py
@REM  python manage.py runserver
cd smrp
python -m uvicorn smrp.asgi:application --port 8100 --reload