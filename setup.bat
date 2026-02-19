@echo off
echo ============================================
echo   MahiraClipper - Setup
echo   Whisper (lokal) + Groq (gratis)
echo ============================================
echo.

:: Cek Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js tidak ditemukan!
    echo Download dari: https://nodejs.org
    pause & exit /b 1
)
echo [OK] Node.js: ditemukan

:: Cek Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Download dari: https://python.org
    pause & exit /b 1
)
echo [OK] Python: ditemukan

:: Cek FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] FFmpeg tidak ditemukan - diperlukan untuk crop dan subtitle
    echo Download dari: https://ffmpeg.org/download.html
    echo Tambahkan ke PATH setelah install
    echo.
)

:: Install Node dependencies
echo.
echo [1/3] Install Node.js dependencies...
call npm install
if %errorlevel% neq 0 ( echo [ERROR] npm install gagal & pause & exit /b 1 )

:: Install Python - Whisper
echo.
echo [2/3] Install faster-whisper (transkripsi lokal ~50MB)...
echo      Model Whisper akan didownload otomatis saat pertama kali dipakai (~500MB untuk small)
pip install faster-whisper --break-system-packages 2>nul || pip install faster-whisper
if %errorlevel% neq 0 ( echo [ERROR] faster-whisper gagal diinstall & pause & exit /b 1 )
echo [OK] faster-whisper terinstall

:: Install Python - downloader
echo.
echo [3/3] Install yt-dlp (download video)...
pip install yt-dlp --break-system-packages 2>nul || pip install yt-dlp

echo.
echo ============================================
echo   Setup SELESAI!
echo ============================================
echo.
echo Langkah selanjutnya:
echo   1. Jalankan: jalankan.bat
echo   2. Buka Settings
echo   3. Isi Groq API Key (gratis di console.groq.com)
echo   4. Pilih model Whisper (default: small)
echo   5. Paste link ceramah - Mulai Proses!
echo.
echo CATATAN: Pertama kali proses video, Whisper akan
echo download model ~500MB. Selanjutnya offline selamanya.
echo.
pause
