# Procesador para extracción de datos Registro empresa colaboradora

## Flujo de Trabajo

1. **Extracción de Datos:**
   - Se extraen los datos del PDF y se genera un diccionario con la información contenida en el documento.
   - A partir de este diccionario, se crean objetos `Operador` y `Representantes`.
   - Se considera representante legal como el firmante. Dado que falta información sobre el firmante, se completa la información de contacto de la empresa utilizando la información introducida al inicio por los representantes (relacionando por DNI).
   - Si el operador extraído no es correcto (es decir, si falta información crítica en el PDF), se registra un mensaje de error y el proceso se detiene.

2. **Validación e Inserción del Operador:**
   - El método verifica si el operador ya existe en la base de datos a través de su NIF.
   - Si el operador no está en la base de datos, se inserta en la tabla `Tabla_Operadores` junto con la información del representante legal.
   - Si el operador ya existe en la base de datos, se muestra un mensaje informando al usuario de que ya existe un operador con el CIF indicado. El usuario tiene la opción de continuar o cancelar. Si el usuario opta por continuar, se actualizarán los datos del operador en la base de datos si alguno de ellos difiere de la información actual. Si el usuario elige cancelar, la importación de datos se detiene y el proceso finaliza.

3. **Validación e Inserción de los Representantes:**
   - Cada representante en la lista se procesa individualmente:
     - Se verifica si ya existe en la `Tabla_Usuarios_UNICODatos`.
     - Si no existe, se inserta.
     - Si ya existe, se verifica si está relacionado con el operador.
     - Si la relación entre el representante y el operador no existe, se genera esta relación en la tabla `Tabla_Usuarios_Operadores`.

**Consideraciones:**

- Los nombres y apellidos de los representantes en el PDF se proporcionan en un único campo. La separación de estos en nombre y apellidos se realiza aplicando cierta lógica. Sin embargo, este método puede no ser completamente preciso, ya que identificar si un nombre o apellido es compuesto resulta complicado de automatizar mediante programación. Por este motivo es recomendable siempre revisar estos campos tras el procesado.

- Para los datos del representante legal, se utilizan los del firmante del documento. Sin embargo, no se disponen de datos como el correo electrónico o el teléfono de contacto. En esos casos, si estos datos están presentes en la información de alguno de los 8 representantes posibles en el documento, se toman de ahí para completar la información faltante del operador.

- Los campos `Estado`, `Cob_Fija`, `Cob_FWA`, `Cob_Movil`, y los datos del grupo operador no se proporcionan en el formulario PDF, por lo que actualmente no se completan.

- Para los campos `telefono`, `DNI` y `CIF` se realiza una normalización para quitar cualquier carácter como puntos, guiones, etc.

## Utilizar a la funcionalidad sin utilizar el ejecutable

Es posible utilizar este proyecto desde un script python. En el fichero test_script dentro del directorio src se detalla un ejemplo. Los pasos basicos serian los siguientes:

```sh
import os

from controlers.registro_empresa_controller import RegistroEmpresaColaboradoraController
from DAL.database import Database

def funcion_escribirLog(mensaje):
    print(mensaje)  # Aquí podrías escribir a un archivo o solo imprimir en consola

# Ruta al archivo de base de datos
db_path = 'ruta/a/tu/basededatos.accdb'  # Cambia esto por la ruta real del archivo de base de datos


# Ruta al archivo PDF
pdf_path = 'ruta/a/tu/documento.pdf'  # Cambia esto por la ruta real del archivo PDF

# Verificar que las rutas existan antes de proceder
if not os.path.exists(db_path):
    print(f"Error: El archivo de base de datos no existe en la ruta especificada: {db_path}")
    exit()

if not os.path.exists(pdf_path):
    print(f"Error: El archivo PDF no existe en la ruta especificada: {pdf_path}")
    exit()

# Crear instancia de la base de datos
db = Database(db_path)

# Crear instancia de la controladora para registro de empresa colaboradora
controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)

# Procesar el PDF y obtener el resultado
result = controladoraREC.procesar_pdf(pdf_path, db, funcion_escribirLog)

# Verificar el resultado y mostrar un mensaje apropiado
if result:
    print("El proceso del PDF fue exitoso.")
else:
    print("El proceso del PDF falló.")

````

## Generar el ejecutable

```sh
pyinstaller --onefile --windowed main.py
````
