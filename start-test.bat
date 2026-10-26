@echo off
chcp 65001 >nul
title Karaoke Kenz - Windows Test Launcher
cls

echo =========================================================================
echo       KHOI DONG KIEM THU WEB KARAOKE KENZ TREN WINDOWS
echo =========================================================================
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Tim thay Python tren may! Dang khoi chay Web Server cong 80...
    start http://localhost
    python server.py
    goto end
)

where node >nul 2>nul
if %errorlevel% equ 0 (
    echo [*] Tim thay Node.js tren may! Dang khoi chay Web Server cong 80...
    start http://localhost
    node server.js
    goto end
)

echo [*] May cua ban khong can cai them bat ky phan mem nao!
echo [*] Dang mo truc tiep index.html tren trinh duyet mac dinh cua ban...
start "" "%~dp0index.html"

:end
echo.
pause
