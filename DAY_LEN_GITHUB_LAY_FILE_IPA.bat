@echo off
chcp 65001 >nul
title Karaoke Kenz - Đẩy Code Lên GitHub Để Lấy File .IPA Ký Chứng Chỉ
cls

echo =========================================================================
echo       TỰ ĐỘNG ĐẨY CODE LÊN GITHUB ĐỂ LẤY FILE .IPA (SẴN SÀNG KÝ)
echo =========================================================================
echo.
echo Bạn muốn có file .IPA chuẩn 100%% ARM64 để đem đi thuê ký chứng chỉ?
echo Máy ảo macOS 14 của GitHub sẽ tự động compile và xuất file .IPA cho bạn!
echo.
echo -------------------------------------------------------------------------
echo BƯỚC 1: Truy cập https://github.com/new và tạo 1 kho lưu trữ mới.
echo BƯỚC 2: Copy link kho lưu trữ của bạn (dạng: https://github.com/user/kenz.git)
echo -------------------------------------------------------------------------
echo.

set /p REPO_URL="Dán link GitHub Repository của bạn vào đây và ấn Enter: "

if "%REPO_URL%"=="" (
    echo [!] Bạn chưa nhập link GitHub. Vui lòng chạy lại file.
    pause
    exit /b
)

echo.
echo [*] Đang thiết lập kết nối tới GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
echo [*] Đang đồng bộ và đẩy mã nguồn lên GitHub...
git add -A
git commit -m "Auto Build Unsigned IPA for Signing Service" 2>nul
git push -u origin main --force

if %errorlevel% equ 0 (
    echo.
    echo =========================================================================
    echo [THÀNH CÔNG] Đã đẩy mã nguồn lên GitHub!
    echo.
    echo Bây giờ bạn chỉ cần:
    echo 1. Vào lại trang GitHub của bạn, bấm vào thẻ "Actions".
    echo 2. Chọn workflow "Build Unsigned iOS IPA (San Sang Ky Chung Chi)".
    echo 3. Sau khoảng 2 phút, bấm tải file "Karaoke-Kenz-VIP-IPA.zip" về.
    echo 4. Giải nén ra là có ngay file "Karaoke-Kenz-VIP.ipa" chuẩn 100%% để gửi đi ký!
    echo =========================================================================
) else (
    echo.
    echo [!] Có lỗi xảy ra khi push. Vui lòng kiểm tra lại quyền đăng nhập GitHub.
)

echo.
pause
