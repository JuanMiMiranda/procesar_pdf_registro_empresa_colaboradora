from typing import List

from models.enum import PDFProcessingStatus
from models.operador_model import Operador
from models.usuario_operador_model import Usuario_Operador

class ResultadoProcesamiento:
    def __init__(self, 
                 operador: Operador, 
                 representantes: List[Usuario_Operador], 
                 representante_firma: Usuario_Operador, 
                 pdf_processing_status: PDFProcessingStatus):
        """
        Inicializa una instancia de ResultadoProcesamiento.
        
        Parámetros:
        - operador: La instancia del operador procesado del PDF.
        - representantes: La lista de representantes procesados del PDF.
        - representante_firma: La instancia del representante que firma, extraída del PDF.
        - pdf_processing_status: El estado final del procesamiento del PDF (por ejemplo, 'SUCCESS' o 'FAILED').
        """
        self.operador = operador
        self.representantes = representantes
        self.representante_firma = representante_firma
        self.pdf_processing_status = pdf_processing_status
    