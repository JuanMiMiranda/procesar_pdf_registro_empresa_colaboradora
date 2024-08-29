from enum import Enum

class PDFProcessingStatus(Enum):
    SUCCESS = "Operador insertado exitosamente"
    OPERATOR_EXISTS = "El operador ya existe en la base de datos"
    MISSING_OPERATOR_INFO = "Falta información del operador en el PDF"
    INSERTION_ERROR = "Error al insertar el operador"
    REPRESENTATIVE_PROCESSING_ERROR = "Error al procesar un representante"

# Enumerado utilizado para mostrar los datos en la tabla. 
class PDFProcessingStatusShow(Enum):
    SIN_PROCESAR = "SIN PROCESAR"
    PROCESANDO = "PROCESANDO...."
    DATOS_ACTUALIZADOS = "OK. DATOS ACTUALIZADOS"
    ERROR_ACTUALIZAR = "ERROR AL ACTUALIZAR"
    ERROR_FALTA_INFO_OPERADOR = "ERROR. FALTA INFO. OPERADOR"
    ERROR_INSERCION_BD = "ERROR. INSERCIÓN EN BD"
    ERROR_PROCESADO_REPRESENTANTES = "ERROR. EN PROCESADO DE REPRESENTANTES"
    OK_GUARDADO = "OK. DATOS GUARDADOS"