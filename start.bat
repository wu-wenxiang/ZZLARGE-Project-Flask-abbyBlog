@echo off
echo Starting up project...

pushd "%~dp0" > NUL
set BASE_DIR=%~dp0
popd > NUL

echo.BASE_DIR : %BASE_DIR%

::--------------------------------------------------------
:: Config
::--------------------------------------------------------

set APP_CONFIG_FILE=%BASE_DIR%config\development.py
echo.APP_CONFIG_FILE : %APP_CONFIG_FILE%

::--------------------------------------------------------
:: Main
::--------------------------------------------------------

call cd %BASE_DIR%
set OPT_ENV_FORCE=%1
echo.OPT_ENV_FORCE : %OPT_ENV_FORCE%
if "%OPT_ENV_FORCE%x" == "-fx" (
  python "%BASE_DIR%manage.py" "clean"
)

python "%BASE_DIR%manage.py" "prepare"

call :build_venv
call :launch_webapp

echo.&pause&goto:eof


::--------------------------------------------------------
::-- Function definition starts below here
::--------------------------------------------------------

:logging
echo "[INFO] %*"
goto :eof


:build_venv
if not exist env (
  virtualenv env
)
call env\Scripts\activate
call pip install -r requirements.txt
exit /b

:launch_webapp
echo.BASE_DIR : %BASE_DIR%
call python "%BASE_DIR%run.py" "%APP_CONFIG_FILE%"
exit /b

PAUSE
