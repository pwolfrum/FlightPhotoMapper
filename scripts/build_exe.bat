@echo off
setlocal

echo [1/4] Syncing dependencies...
call uv sync --group dev
if errorlevel 1 goto :fail

echo [2/4] Building standalone executable (one-folder)...
call uv run --group dev python -m PyInstaller --clean --noconfirm flightphotomapper.spec
if errorlevel 1 goto :fail

echo [3/4] Cleaning up one-file artifacts...
if exist dist\flightphotomapper.exe del dist\flightphotomapper.exe
if exist dist\smoke_export rmdir /s /q dist\smoke_export
if exist dist\smoke_export_after_fix rmdir /s /q dist\smoke_export_after_fix
if exist dist\smoke_export_viewer_control rmdir /s /q dist\smoke_export_viewer_control

echo [4/4] Adding end-user how-to...
if not exist howto.txt (
	echo Missing howto.txt in repository root.
	goto :fail
)
copy /Y howto.txt dist\flightphotomapper\howto.txt >nul
if errorlevel 1 goto :fail

echo Build completed.
echo Output: dist\flightphotomapper\flightphotomapper.exe
echo Included: dist\flightphotomapper\howto.txt
goto :eof

:fail
echo Build failed.
exit /b 1
