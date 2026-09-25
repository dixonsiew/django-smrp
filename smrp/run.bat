call ..\.venv\Scripts\activate.bat
@REM python server.py
@REM  python manage.py runserver
python -m uvicorn smrp.asgi:application --reload