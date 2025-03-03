@echo off
setlocal enabledelayedexpansion

rem Count total .doc files
set count=0
for %%f in (*.doc) do set /a count+=1

rem Initialize progress counter
set current=0

rem Loop through all .doc files
for %%f in (*.doc) do (
    set /a current+=1
    echo [!current! / %count%] Converting: %%f
    "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf "%%f" --outdir "%cd%"
)

echo Conversion Completed!
pause
