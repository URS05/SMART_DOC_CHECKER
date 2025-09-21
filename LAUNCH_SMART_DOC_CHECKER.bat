@echo off
setlocal EnableDelayedExpansion

:: ============================================================================
:: 🚀 SMART DOC CHECKER AGENT - MASTER LAUNCHER
:: ============================================================================
:: This single file will:
:: 1. Check Python installation
:: 2. Install all dependencies
:: 3. Download required AI models
:: 4. Launch the application
:: Perfect for GitHub users - just run this one file!
:: ============================================================================

title Smart Doc Checker Agent - Master Launcher

echo.
echo  ████████████████████████████████████████████████████████████████████
echo  █                                                                  █
echo  █              🚀 SMART DOC CHECKER AGENT 🚀                      █
echo  █                                                                  █
echo  █     AI-Powered Document Contradiction Detection System           █
echo  █                                                                  █
echo  ████████████████████████████████████████████████████████████████████
echo.

:: Set colors
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo %BLUE%Starting Smart Doc Checker Agent Setup and Launch...%RESET%
echo.

:: ============================================================================
:: STEP 1: Check Python Installation
:: ============================================================================
echo %YELLOW%[1/6] Checking Python installation...%RESET%

python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Python is not installed or not in PATH!%RESET%
    echo.
    echo %YELLOW%Please install Python 3.8+ from https://python.org%RESET%
    echo %YELLOW%Make sure to check "Add Python to PATH" during installation%RESET%
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo %GREEN%✅ Python !PYTHON_VERSION! is installed%RESET%
)
echo.

:: ============================================================================
:: STEP 2: Check if this is first run (check for virtual environment)
:: ============================================================================
echo %YELLOW%[2/6] Checking project environment...%RESET%

if not exist "venv" (
    echo %BLUE%🔧 First run detected - setting up virtual environment...%RESET%
    python -m venv venv
    if errorlevel 1 (
        echo %RED%❌ Failed to create virtual environment%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%✅ Virtual environment created%RESET%
) else (
    echo %GREEN%✅ Virtual environment already exists%RESET%
)
echo.

:: ============================================================================
:: STEP 3: Activate virtual environment and install dependencies
:: ============================================================================
echo %YELLOW%[3/6] Installing dependencies...%RESET%

call venv\Scripts\activate.bat

:: Check if requirements are already installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo %BLUE%📦 Installing Python packages...%RESET%
    echo %YELLOW%This may take a few minutes on first run...%RESET%
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo %RED%❌ Failed to install dependencies%RESET%
        echo %YELLOW%Trying alternative installation...%RESET%
        
        :: Try installing core packages individually
        pip install streamlit pandas numpy plotly
        pip install pdfminer.six python-docx beautifulsoup4 lxml
        pip install spacy transformers torch scikit-learn
        pip install jinja2 chardet tqdm
        
        if errorlevel 1 (
            echo %RED%❌ Critical error: Could not install required packages%RESET%
            pause
            exit /b 1
        )
    )
    echo %GREEN%✅ Dependencies installed successfully%RESET%
) else (
    echo %GREEN%✅ Dependencies already installed%RESET%
)
echo.

:: ============================================================================
:: STEP 4: Download spaCy language model
:: ============================================================================
echo %YELLOW%[4/6] Setting up AI language model...%RESET%

python -c "import spacy; spacy.load('en_core_web_sm')" >nul 2>&1
if errorlevel 1 (
    echo %BLUE%🧠 Downloading spaCy English model (this may take a moment)...%RESET%
    python -m spacy download en_core_web_sm
    if errorlevel 1 (
        echo %RED%❌ Failed to download spaCy model%RESET%
        echo %YELLOW%Trying alternative download method...%RESET%
        pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
    )
    echo %GREEN%✅ Language model downloaded%RESET%
) else (
    echo %GREEN%✅ Language model already available%RESET%
)
echo.

:: ============================================================================
:: STEP 5: Verify installation and create templates
:: ============================================================================
echo %YELLOW%[5/6] Verifying installation...%RESET%

python -c "from reports.generator import ReportGenerator; rg = ReportGenerator(); print('Templates initialized')" >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Installation verification failed%RESET%
    pause
    exit /b 1
) else (
    echo %GREEN%✅ Installation verified successfully%RESET%
)

:: Check if reports directory exists, create if not
if not exist "reports" mkdir reports

echo %GREEN%✅ All systems ready!%RESET%
echo.

:: ============================================================================
:: STEP 6: Launch Application Menu
:: ============================================================================
echo %YELLOW%[6/6] Launching Smart Doc Checker Agent...%RESET%
echo.

:MENU
echo %BLUE%════════════════════════════════════════════════════════════════════%RESET%
echo %BLUE%                    🚀 SMART DOC CHECKER MENU                        %RESET%
echo %BLUE%════════════════════════════════════════════════════════════════════%RESET%
echo.
echo  %GREEN%1%RESET% - 🌐 Start Web Interface (Recommended)
echo  %GREEN%2%RESET% - 🎯 Run Demo (See it in action)
echo  %GREEN%3%RESET% - 📊 Verify Installation
echo  %GREEN%4%RESET% - 📖 View Documentation
echo  %GREEN%5%RESET% - ❌ Exit
echo.
set /p choice=%YELLOW%Enter your choice (1-5): %RESET%

if "%choice%"=="1" goto WEB_INTERFACE
if "%choice%"=="2" goto RUN_DEMO
if "%choice%"=="3" goto VERIFY
if "%choice%"=="4" goto DOCS
if "%choice%"=="5" goto EXIT
goto INVALID_CHOICE

:WEB_INTERFACE
echo.
echo %GREEN%🌐 Starting Web Interface...%RESET%
echo %BLUE%The application will open in your browser at: http://localhost:8501%RESET%
echo %YELLOW%Press Ctrl+C to stop the server when you're done%RESET%
echo.
echo %YELLOW%Starting in 3 seconds...%RESET%
timeout /t 3 /nobreak >nul
python main.py
goto MENU

:RUN_DEMO
echo.
echo %GREEN%🎯 Running Demo Analysis...%RESET%
echo %BLUE%This will analyze sample documents and show you what the system can do%RESET%
echo.
python demo.py
echo.
echo %GREEN%✅ Demo completed! Check the 'reports' folder for generated reports.%RESET%
echo.
pause
goto MENU

:VERIFY
echo.
echo %GREEN%📊 Verifying Installation...%RESET%
python verify_structure.py
echo.
pause
goto MENU

:DOCS
echo.
echo %GREEN%📖 Opening Documentation...%RESET%
if exist "README.md" (
    start README.md
) else (
    echo %RED%README.md not found%RESET%
)
if exist "FIXED_QUICK_START.md" (
    start FIXED_QUICK_START.md
) else (
    echo %RED%Quick start guide not found%RESET%
)
echo.
pause
goto MENU

:INVALID_CHOICE
echo %RED%❌ Invalid choice. Please enter 1-5.%RESET%
echo.
timeout /t 2 /nobreak >nul
goto MENU

:EXIT
echo.
echo %BLUE%Thanks for using Smart Doc Checker Agent! 🚀%RESET%
echo %YELLOW%Star us on GitHub if this helped you! ⭐%RESET%
echo.

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat 2>nul

pause
exit /b 0

:: ============================================================================
:: ERROR HANDLING
:: ============================================================================
:ERROR
echo %RED%❌ An error occurred during setup.%RESET%
echo %YELLOW%Please check the following:%RESET%
echo - Python 3.8+ is installed and in PATH
echo - You have internet connection for downloads
echo - You have sufficient disk space (at least 2GB free)
echo - Antivirus is not blocking the installation
echo.
pause
exit /b 1
