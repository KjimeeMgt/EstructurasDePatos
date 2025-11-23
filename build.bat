@echo off
echo =====================================
echo      Limpiando carpetas antiguas
echo =====================================

IF EXIST dist (
    echo Eliminando carpeta dist...
    rmdir /s /q dist
)

IF EXIST build (
    echo Eliminando carpeta build...
    rmdir /s /q build
)

echo =====================================
echo           Compilando la app
echo =====================================

pyinstaller --onefile --windowed ^
 --add-data "src/frontend/dist;frontend/dist" ^
 --icon "src/assets/app.ico" ^
 --name "MiTodoApp" ^
 main.py

echo =====================================
echo            Limpiando cache
echo =====================================

IF EXIST src\**\__pycache__ (
    echo Eliminando __pycache__...
    for /d /r %%i in (__pycache__) do (
        rmdir /s /q "%%i"
    )
)

cls

echo =====================================
echo      App compilada exitosamente!
echo =====================================

pause
