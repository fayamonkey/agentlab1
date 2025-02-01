@echo off
echo Setting up Dirk's Agent Laboratory Research Lab (Streamlit Version)...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    echo You can download it from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements_streamlit.txt

REM Create .streamlit directory and secrets.toml if they don't exist
echo Setting up Streamlit configuration...
if not exist ".streamlit" mkdir .streamlit
if exist ".env" (
    echo Creating secrets.toml from .env file...
    for /f "tokens=1,2 delims==" %%a in (.env) do (
        set key=%%a
        set val=%%b
        setlocal enabledelayedexpansion
        echo !key! = "!val!" > .streamlit\secrets.toml
        endlocal
    )
)

REM Create a runner script that activates venv and runs streamlit
echo @echo off > run_streamlit.bat
echo call "%~dp0venv\Scripts\activate.bat" >> run_streamlit.bat
echo streamlit run "%~dp0streamlit_app.py" >> run_streamlit.bat

REM Create desktop shortcut
echo Creating desktop shortcut...
set SCRIPT="%TEMP%\CreateShortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = oWS.ExpandEnvironmentStrings("%%USERPROFILE%%\Desktop\Dirk's Research Lab.lnk") >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0run_streamlit.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.IconLocation = "%~dp0agentlabsmall.png" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo Setup completed successfully!
echo A shortcut has been created on your desktop: "Dirk's Research Lab"
echo.
echo You can now run the application by:
echo 1. Double-clicking the desktop shortcut
echo 2. Or running 'run_streamlit.bat' directly from this folder
echo.
pause 