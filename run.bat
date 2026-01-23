@echo off
echo Starting Cable Design Validation System (Streamlit)...
echo.

if not exist .venv (
    echo Virtual environment not found. Creating one...
    uv venv
    uv pip install -r requirements.txt
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Running Streamlit app...
streamlit run app.py
pause
