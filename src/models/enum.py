from enum import Enum

class PDFProcessingStatus(Enum):
    LOAD_PDF_OK = "Lectura OK"
    SUCCESS = "Operador insertado exitosamente"
    OPERATOR_EXISTS = "El operador ya existe en la base de datos"
    MISSING_OPERATOR_INFO = "Falta información del operador en el PDF"
    MISSING_SIGNATURE = "Falta Firma en el PDF"
    INSERTION_ERROR = "Error al insertar el operador"
    REPRESENTATIVE_PROCESSING_ERROR = "Error al procesar un representante"

# Enumerado utilizado para mostrar los datos en la tabla. 
class Status(Enum):
    SIN_PROCESAR = "SIN PROCESAR"
    LECTURA_PDF_OK = "LECTURA PDF OK"
    SIN_FIRMA = "PDF SIN FIRMAR"
    LECTURA_PDF_OK_OPERADOR_EXISTE = "LECTURA PDF OK. OPERADOR YA EXISTE"
    PROCESANDO = "PROCESANDO...."
    DATOS_ACTUALIZADOS = "OK. DATOS ACTUALIZADOS"
    ERROR_ACTUALIZAR = "ERROR. AL ACTUALIZAR"
    ERROR_PDF_NO_VALIDO = "ERROR. DATOS PDF NO VALIDO"
    ERROR_INSERCION_BD = "ERROR. INSERCIÓN EN BD"
    ERROR_PROCESADO_REPRESENTANTES = "ERROR. EN PROCESADO DE REPRESENTANTES"
    OK_GUARDADO = "OK. DATOS GUARDADOS"