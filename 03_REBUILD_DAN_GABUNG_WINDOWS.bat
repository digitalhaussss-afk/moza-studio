@echo off
setlocal
cd /d "%~dp0"
echo.
echo =============================================
echo  MOZA STUDIO - BUILD FIGCRAFT DAN GABUNG
echo =============================================
echo.
echo Masukkan lokasi folder source FigCraft (yang berisi Cargo.toml).
echo Contoh: C:\Users\ASUS\Downloads\Petal_Studio_FigCraft_Web_Mod_Kit\figcraft
set /p SOURCE=Path FigCraft: 
set "SOURCE=%SOURCE:"=%"
if not exist "%SOURCE%\Cargo.toml" (
 echo ERROR: Cargo.toml tidak ditemukan pada folder itu.
 pause & exit /b 1
)
where py >nul 2>nul
if not errorlevel 1 (set "PY=py -3") else (set "PY=python")
%PY% "tools\retint_figcraft.py" "%SOURCE%"
if errorlevel 1 goto :fail
where rustup >nul 2>nul
if errorlevel 1 (echo ERROR: Rust belum terpasang & goto :fail)
where trunk >nul 2>nul
if errorlevel 1 (echo ERROR: Trunk belum terpasang & goto :fail)
rustup target add wasm32-unknown-unknown
if errorlevel 1 goto :fail
pushd "%SOURCE%\apps\figcraft-web"
trunk build --release
if errorlevel 1 (popd & goto :fail)
popd
%PY% "tools\merge_figcraft.py" "%SOURCE%\dist\web"
if errorlevel 1 goto :fail
echo.
echo SELESAI! Cari Moza_Studio_Complete_Deploy.zip di folder induk.
pause
exit /b 0
:fail
echo GAGAL: lihat pesan di atas. File asli tidak dibuang.
pause
exit /b 1
