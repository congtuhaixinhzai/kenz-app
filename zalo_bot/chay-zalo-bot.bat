@echo off
chcp 65001 >nul
title Karaoke Kenz - Zalo Bot Service
cls

echo =========================================================================
echo       KHOI DONG DICH VU ZALO BOT TU DONG BAO DON KARAOKE KENZ
echo =========================================================================
echo.
cd /d "%~dp0"
python zalo_service.py
pause
