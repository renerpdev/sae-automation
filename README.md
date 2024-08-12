
# Script de Monitoreo para citas del SAE

Este script monitorea la página web del Sistema de Agenda Electrónica (SAE), notificando via Slack cuando hay cupos nuevos. El script se ejecuta cada 5 segundos, brindando así una actualización constante.

> NOTE: Currently it only supports macOS

## Requisitos

- Python 3
- pip (Python package installer)
- Google Chrome
- ChromeDriver

## Instalación

1. **Clonar el repositorio o descargar los archivos necesarios**:

   ```sh
   git clone git@github.com:renerpdev/sae-automation.git
   cd sae-automation
   ```

2. **Ejecutar el script de configuración**:

   ```sh
   chmod +x setup.sh
   ./setup.sh
   ```

   Este script hará lo siguiente:
   - Instalará Python y pip.
   - Instalará las bibliotecas de Python necesarias (`selenium`, `slack_sdk`, `python-dotenv`).
   - Descargar y configurar ChromeDriver.
   - Crear un archivo `.env` para las variables de entorno.

3. **Actualizar el archivo `.env` con tus valores**:

   Abre el archivo `.env` y actualiza los valores:

   ```plaintext
   SLACK_TOKEN=your-slack-bot-token
   CHANNEL_ID=your-channel-id
   SESSION_ID=session-id-here
   ```
   
> **Note**: El valor de `SESSION_ID` se encuentra al final de la url de la página del SAE 

## Uso

1. **Ejecutar el script de monitoreo**:

   ```sh
   python main.py
   ```

   Este script:
   - Accederá a la URL especificada.
   - Intentará encontrar y hacer clic en el botón con ID `form:botonElegirHora`.
   - Verificará si se ha cargado una nueva página.
   - Enviará una notificación a Slack si se carga una nueva página.

## Notas

- Asegúrate de tener configurado correctamente tu token de Slack y el ID del canal.
- Puedes personalizar el intervalo de tiempo de monitoreo modificando el valor de `time.sleep(5)` en el script.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.
