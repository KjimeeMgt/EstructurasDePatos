# Estructura de Patos

Este es el proyecto final de Estructuras de Datos, en el cual tenemos que hacer una app con Python y usando algunas estructuras de datos, en las cuales usamos Arboles Binarios y Listas Enlazadas.
El proyecto fue creado con Flask para el backend y React para el frontend, y se compila todo en un solo ejecutable usando PyInstaller, usando SQLite como base de datos.

## 1. Clonar el respositorio
```bash
git clone https://github.com/MrMikeDevTech/EstructurasDePatos.git
```

## 2. Entramos a la carpeta
``` bash
cd EstructurasDePatos
```

## 3. Crear entorno virtual

Esto es para crearlo

``` bash
python -m venv venv
```

## 4. Activar entorno virtual

``` bash
venv\Scripts\activate
```

## 5. Instalar dependencias del backend

``` bash
pip install -r requirements.txt
```

## 6. Instalar dependencias del frontend

Dentro de `src/frontend`:

``` bash
npm install
```

## 7. Compilar frontend

``` bash
npm run build
```

Esto genera la carpeta `dist` usada por PyInstaller.

## 8. Compilar el proyecto con PyInstaller

El proyecto incluye un script `.bat` que ejecuta:

``` bash
./build.bat
```

## 9. Ejecutar el programa
El ejecutable se encuentra en la carpeta `dist` generada por PyInstaller.

``` bash
./dist/MiTodoApp.exe
```

## 10. Ejecutar el proyecto en modo desarrollo (opcional)
Puedes ejecutar el backend y frontend por separado para desarrollo.

``` bash
# Para el backend
python main.py

# Para el frontend
cd src/frontend
npm run dev
```