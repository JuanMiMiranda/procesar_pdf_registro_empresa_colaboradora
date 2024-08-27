import os

from controlers.registro_empresa_controller import RegistroEmpresaColaboradoraController
from DAL.database import Database

def funcion_escribirLog(mensaje):
    print(mensaje)  # Aquí podrías escribir a un archivo o solo imprimir en consola

# Ruta al archivo de base de datos
# db_path = 'ruta/a/tu/basededatos.accdb'  # Cambia esto por la ruta real del archivo de base de datos
db_path = r'C:\Users\JuanMi\Desktop\BD_UNICO_DATOS.accdb'  # Cambia esto por la ruta real del archivo de base de datos

# Ruta al archivo PDF
# pdf_path = 'ruta/a/tu/documento.pdf'  # Cambia esto por la ruta real del archivo PDF
pdf_path = r'E:\OneDrive\DATOS\99 - SETELECO\TAREAS SETELECO\04_Tarea_UNICODatos_NDA\Tarea_UNICODatos_NDA\ELANTA_Lyntia_Formulario_Registro_Operadora_UNICO_DATOS_v3 firmado 3.pdf'  # Cambia esto por la ruta real del archivo PDF

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