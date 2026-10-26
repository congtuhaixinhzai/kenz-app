@echo off
chcp 65001 >nul
title Karaoke Kenz - Dang Nhap Zalo
cls

echo =========================================================================
echo       DANG NHAP ZALO PHU DE LAY MA QUET QR
echo =========================================================================
echo.
echo [*] Dang mo cua so Zalo Web chuyen dung de ban quet ma QR bang dien thoai...
echo.

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "https://chat.zalo.me"
    goto opened
)

if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "https://chat.zalo.me"
    goto opened
)

if exist "C:\Program Files\CocCoc\Browser\Application\browser.exe" (
    start "" "C:\Program Files\CocCoc\Browser\Application\browser.exe" "https://chat.zalo.me"
    goto opened
)

if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "https://chat.zalo.me"
    goto opened
)

explorer.exe "https://chat.zalo.me"

:opened
echo [OK] Da mo trang Zalo Web: https://chat.zalo.me tren Google Chrome!
echo.
echo =========================================================================
echo HUONG DAN TUNG BUOC:
echo 1. Tren man hinh Chrome vua mo, ban se thay MA QR cua Zalo.
echo 2. Lay dien thoai (dang dang nhap nick Zalo phu):
echo    - Mo ung dung Zalo -> Bam vao bieu tuong Quet Ma QR (goc tren ben phai).
echo    - Huong camera vao ma QR tren man hinh may tinh -> Bam "Dang nhap".
echo.
echo 3. Sau khi Zalo Web tren may tinh da dang nhap thanh cong:
echo    - Nhan phim F12 tren ban phim (hoac bam chuot phai vao trang web -> chon "Kiem tra" / Inspect).
echo    - Bam vao tab "Console" o phia tren.
echo    - Copy dong chu sau, dan vao tab Console roi an Enter:
echo.
echo         copy(document.cookie)
echo.
echo    - Mo file "zalo_config.json" bang Notepad.
echo    - Dan (Ctrl+V) ma cookie vua copy vao muc "cookie".
echo =========================================================================
echo.
pause

