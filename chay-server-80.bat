@echo off
chcp 65001 >nul
title Karaoke Kenz - Máy Chủ Cổng 80 & Zalo Bot Bridge
cls

echo =========================================================================
echo       🚀 KHỞI ĐỘNG MÁY CHỦ KARAOKE KENZ CỔNG 80 (HTTP)
echo =========================================================================
echo [*] Đang kiểm tra môi trường Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Khong tim thay Python. Vui long cai dat Python 3 de tiep tuc.
    pause
    exit /b 1
)

echo [*] Đang mở trình duyệt: http://localhost
start http://localhost

echo [*] Khởi chạy máy chủ cổng 80 và kết nối Zalo Bot (3000)...
python "%~dp0server.py"

pause
