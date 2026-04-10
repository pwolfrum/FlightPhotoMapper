@echo off
setlocal

echo [1/3] Syncing dependencies...
call uv sync --group dev
if errorlevel 1 goto :fail

echo [2/3] Building standalone executable (one-folder)...
call uv run --group dev pyinstaller --clean --noconfirm flightphotomapper.spec
if errorlevel 1 goto :fail

echo [3/3] Cleaning up one-file artifacts...
if exist dist\flightphotomapper.exe del dist\flightphotomapper.exe
if exist dist\smoke_export rmdir /s /q dist\smoke_export
if exist dist\smoke_export_after_fix rmdir /s /q dist\smoke_export_after_fix
if exist dist\smoke_export_viewer_control rmdir /s /q dist\smoke_export_viewer_control

echo Build completed.
echo Output: dist\flightphotomapper\flightphotomapper.exe
goto :eof

:fail
echo Build failed.
exit /b 1
