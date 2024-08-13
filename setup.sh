#!/bin/bash

# Actualizar Homebrew
brew update

# Instalar Python
brew install python3

# Instalar las bibliotecas de Python necesarias
pip3 install selenium slack_sdk python-dotenv requests

# Descargar Chrome Testing binary usando @puppeteer/browsers
npx @puppeteer/browsers install chrome@canary

# Descargar chromedriver usando @puppeteer/browsers
npx @puppeteer/browsers install chromedriver@canary

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    cat <<EOT >> .env
SLACK_TOKEN=your-slack-bot-token
CHANNEL_ID=your-channel-id
EOT
    echo "Archivo .env creado. Por favor, actualiza los valores de las variables de entorno."
else
    echo "El archivo .env ya existe. Por favor, asegúrate de que los valores de las variables de entorno sean correctos."
fi

echo "Configuración completada."
