@echo off
title Otomobil Danismanı Chatbot
echo.
echo ======================================================
echo           OTOMOBİL DANIŞMANI CHATBOT SUNUCUSU
echo ======================================================
echo.
echo Sunucu yukleniyor...
echo Lutfen tarayicinizda http://localhost:8000 adresini acin.
echo.
cd /d "%~dp0"
start "" cmd /c "timeout /t 2 >nul && start http://localhost:8000"
python main.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo Sunucu baslatilamadı! Lutfen Python'in yuklu oldugundan ve requirements.txt
    echo bağımlılıklarının yuklendiginden emin olun.
)
pause
