# Sistema de autenticacion con Fprint y escaner QR con camaras IP

## Tecnologias usadas
- MongoDB
- Node
- Python 3.7
- Fprint
- OpenCV
- ZBar

## Requisitos
- Instalar e iniciar `MongoDB`
- Instalar las librerias `zbar` y `libfprint`
- Instalar `NodeJS` y `NPM` 
- Instalar `python 3` y `pip`

## Instalacion
1. Ejecutar el comando `pip install --user requests opencv-python pyzbar`
2. En la carpeta `pyfprint-cffi-master` ejecutar el comando `pip install --user .`
3. En la carpeta `api` ejecutar el comando `npm install`
4. En la carpeta `api` ejecutar el comando `npm start` para iniciar la API
5. En la raiz del proyecto ejecutar el comando `python fpEnroller.py` y seguir los pasos para registrar un usuario
6. En la raiz del proyecto ejecutar el comando `python login.py` y seguir las instrucciones para iniciar sesion
