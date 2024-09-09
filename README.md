
# Script de Monitoreo para citas del SAE

Este script monitorea la página web del Sistema de Agenda Electrónica (SAE), notificando via Slack cuando hay cupos nuevos. El script se ejecuta cada 5 segundos, brindando así una actualización constante.

> NOTE: Currently it only supports macOS

## Requisitos

- Laptop running MacOS
- Python3
- pip3 (Python package installer)
- Google Chrome for testing
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
   SLACK_TOKEN=token-de-slack
   CHANNEL_ID=id-canal-de-slack
   SCHEDULED_TIME="09:50"
   ID=tu-cedula-aca
   NAME=tu-nombre
   LAST_NAME="tus-apellidos"
   ```
   
## Uso

1. **Ejecutar el script de monitoreo**:

   ```sh
   python main.py
   ```

   Este script:
   - Creará una tarea programada para Lunes a las 9:50am _(modifica el código para cambiar este comportamiento)_
   - Accederá a la URL del SA usando una instancia de Chrome. 
   - Para cada uno de los pasos (un total de 3) hará lo siguiente:
     1. Completerá los datos necesarios para el paso actual.
     2. Hará clic en el botón submit del formulario actual.
     3. Verificará si se ha cargado una nueva página. De lo contrario, ejecuta nuevamente el paso **a)**
     4. Enviará una notificación a Slack si se carga una nueva página.

## Notas

- Asegúrate de tener configurado correctamente tu token de Slack y el ID del canal.
- Puedes personalizar el intervalo de tiempo de monitoreo de cada página modificando el valor de `time.sleep(0)` en el script.
- Puedes modificar la hora de inicio, cambiando el valor de `SCHEDULED_TIME` (el día es fijo para "lunes").
- Puedes eliminar el valor de la variable de entorno `SCHEDULED_TIME` para hacer que la tarea se ejecute inmediatamente.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.
