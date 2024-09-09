#!/bin/bash

# Actualizar Homebrew
brew update

# Instalar Python
brew install python3

# Instalar las bibliotecas de Python necesarias
pip3 install selenium slack_sdk python-dotenv requests schedule

# Descargar Chrome Testing binary usando @puppeteer/browsers
npx @puppeteer/browsers install chrome@canary

# Descargar chromedriver usando @puppeteer/browsers
npx @puppeteer/browsers install chromedriver@canary

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    cat <<EOT >> .env
SLACK_TOKEN=token-de-slack
CHANNEL_ID=id-canal-de-slack
SCHEDULED_TIME="09:50"
ID=tu-cedula-aca
NAME=tu-nombre
LAST_NAME="tus-apellidos"
EOT
    echo "Archivo .env creado. Por favor, actualiza los valores de las variables de entorno."
else
    echo "El archivo .env ya existe. Por favor, asegúrate de que los valores de las variables de entorno sean correctos."
fi

echo "Configuración completada."
