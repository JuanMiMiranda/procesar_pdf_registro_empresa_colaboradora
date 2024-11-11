from typing import List
import fitz  # PyMuPDF
import os
from models.ResultadoProcesamiento import ResultadoProcesamiento
from models.enum import PDFProcessingStatus
from models.usuario_operador_model import Usuario_Operador
from models.operador_model import Operador
from helpers.NombreApellidosParser import NombreApellidosParser
from DAL.operador_dal import OperadorDAL
from DAL.usuario_operador_dal import Usuario_OperadorDAL

from pyhanko.sign.validation import validate_pdf_signature
from pyhanko.sign.fields import enumerate_sig_fields
from pyhanko.pdf_utils.reader import PdfFileReader


class RegistroEmpresaColaboradoraController:
    """
    Controlador para la gestión de formularios PDF de registro de empresas colaboradoras.

    Este controlador permite abrir un archivo PDF, extraer los campos rellenados y devolverlos en forma de diccionario.
    """

    def __init__(self, pdf_path):
        """
        Inicializa una instancia del controlador con la ruta del archivo PDF.

        :param pdf_path: Ruta al archivo PDF.
        """
        self.pdf_path = pdf_path

    def get_dict_from_PDF(self, pdf_path):
        """
        Extrae los campos rellenados del formulario PDF y los devuelve en un diccionario.

        :return: Un diccionario con los nombres de los campos como claves y los valores rellenados como valores.
        :rtype: dict
        """
        doc = fitz.open(pdf_path)
        all_fields = {}

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            widgets = page.widgets()

            if widgets:
                for widget in widgets:
                    try:
                        field_name = widget.field_name
                        if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                            field_value = widget.field_value if hasattr(widget, 'field_value') else ''
                        elif widget.field_type == fitz.PDF_WIDGET_TYPE_CHECKBOX:
                            field_value = True if widget.field_value not in [0, ''] else False # Valor 0 o una cadena vacía ('') indica que la casilla no está marcada, y otros valores indican que sí lo está
                        else:
                            field_value = ''

                        if field_name:
                            all_fields[field_name] = field_value
                    except Exception as e:
                        print(f"Error en el widget en {pdf_path}, página {page_num + 1}: {str(e)}")

        print(f"Campos rellenados en {os.path.basename(pdf_path)}:")
        for field_name, field_value in all_fields.items():
            print(f"{field_name}: {field_value}")
        
        return all_fields
    
    
    def crear_operador_from_dict(self, datos):
      
        nif_operador = datos.get('CIF')
        razon_social = datos.get('NOMBRE DE LA EMPRESA')
        cob_fija = datos.get('InfraestructuraFija', None)
        cob_fwa = datos.get('InfraestructuraFWA', None)
        cob_movil = datos.get('InfraestructuraMovil', None)
        nif_grupo_operador = None  # Valor no proporcionado en los datos
        grupo_operador = None # Valor no proporcionado en los datos
        nif_replegal = None  # Valor no proporcionado en los datos
        nombre_replegal = None  # Valor no proporcionado en los datos
        nif_notificacion = None  # Valor no proporcionado en los datos
        representante_notificacion = None  # Valor no proporcionado en los datos
        email_notificacion = datos.get('CORREO ELECTRÓNICO RRHH')
        servicio_fija= datos.get('ServicioFijo', None)
        servicio_movil= datos.get('ServicioMovil', None)
        servicio_fwa= datos.get('ServicioFWA', None)
        servicio_movil_virtual= datos.get('ServicioMovilVirtual', None)
        servicio_otros= datos.get('Indicar Otros_2', None)
    
        # Crear el objeto Operador solo si 'nif_operador' y 'razon_social' están presentes
        if not (nif_operador and razon_social):
            return None

        operador = Operador(
            nif_operador=nif_operador,
            razon_social=razon_social,
            cob_fija=cob_fija,
            cob_fwa=cob_fwa,
            cob_movil=cob_movil,
            nif_grupo_operador=nif_grupo_operador,
            grupo_operador=grupo_operador,
            nif_replegal=nif_replegal,
            nombre_replegal=nombre_replegal,
            nif_notificacion=nif_notificacion,
            representante_notificacion=representante_notificacion,
            email_notificacion=email_notificacion,
            servicio_fija=servicio_fija,
            servicio_movil= servicio_movil,
            servicio_fwa= servicio_fwa,
            servicio_movil_virtual= servicio_movil_virtual,
            servicio_otros=servicio_otros
        )

        return operador
    


    def crear_representantes_from_dict(self, datos):
        """
        Crea una lista de objetos Representante a partir de un diccionario de datos.
        
        :param datos: Diccionario que contiene la información de los representantes.
        :return: Lista de objetos Representante con datos válidos.
        """
        representantes = []
        for i in range(1, 9):  # Asumimos que hay hasta 9 representantes
            representante = self.crear_representante_desde_dict(datos, i)
            if representante:
                representantes.append(representante)
        
        return representantes
    
    @staticmethod
    def crear_representante_desde_dict(datos, posicion):
        """
        Crea un objeto Representante a partir de un diccionario de datos y una posición específica.
        
        :param datos: Diccionario que contiene la información de los representantes.
        :param posicion: Posición del representante (por ejemplo, 1, 2, 9, etc.).
        :return: Objeto Representante con datos válidos o None si no se encuentran los datos necesarios.
        """
        # Definir las claves basadas en la posición
        nombre_key = f"NOMBRE Y APELLIDOS_{posicion}" if posicion > 1 else "NOMBRE Y APELLIDOS"
        dni_key = f"DNI_{posicion}" if posicion > 1 else "DNI"
        cargo_key = f"CARGO_{posicion}" if posicion > 1 else "CARGO"
        telefono_key = f"TELÉFONO DE CONTACTO_{posicion}" if posicion > 1 else "TELÉFONO DE CONTACTO"
        correo_key = f"CORREO ELECTRÓNICO_{posicion}" if posicion > 1 else "CORREO ELECTRÓNICO"
        extension_key = f"Extensión_{posicion}" if posicion > 1 else "Extensión"

        # Obtener los valores del diccionario
        nombre_y_apellidos = datos.get(nombre_key)
        dni = datos.get(dni_key)
        cargo = datos.get(cargo_key)
        telefono = datos.get(telefono_key)
        correo_electronico = datos.get(correo_key)
        extension = datos.get(extension_key)  # TODO: Considerar cómo tratar la extensión si es relevante

        # Crear el objeto Representante solo si 'nombre' y 'dni' están presentes
        if nombre_y_apellidos and dni:
            nombre, apellido1, apellido2 = NombreApellidosParser(nombre_y_apellidos).parse()
            representante = Usuario_Operador(
                id=None,  # Asumimos que el ID se asignará posteriormente
                nombre=nombre,
                apellido1=apellido1,
                apellido2=apellido2,
                nif=dni,
                email=correo_electronico or '',
                telefono=telefono or ''
            )
            return representante

        return None  # Retorna None si no se encuentran los datos necesarios
    

    def crear_representante_firma_from_dict(self, datos):
        """
        Crea un objeto Representante a partir de un diccionario de datos, tomando solo el representante firmante (posición 9).
        
        :param datos: Diccionario que contiene la información de los representantes.
        :return: Objeto Representante con datos válidos o None si no se encuentra.
        """
        return self.crear_representante_desde_dict(datos, 9)


    def get_pdf_data(self, pdf_path, db, log_function):
        """
        Procesa un único PDF para obtener los datos almacenados en el mismo. Este método no realiza inserción en BD.
        # :return: Una instancia de ResultadoProcesamiento que contiene:
        #          - operador: Instancia del operador procesado del PDF o None si falta la información.
        #          - representantes: Lista de representantes procesados del PDF o None si falla.
        #          - representante_firma: Instancia del representante que firma, extraída del PDF o None si falla.
        #          - pdf_processing_status: Un valor de PDFProcessingStatus que indica el estado final del procesamiento.
        """
        # Obtener los campos del PDF
        dic_campos_completados_pdf = self.get_dict_from_PDF(pdf_path)
        operador = self.crear_operador_from_dict(dic_campos_completados_pdf)
        representantes = self.crear_representantes_from_dict(dic_campos_completados_pdf)
        representante_firma = self.crear_representante_firma_from_dict(dic_campos_completados_pdf)
        representante_firma = self.completar_datos_representante_firma(representantes, representante_firma)
        aceptacion_condiciones_uso = dic_campos_completados_pdf.get('Aceptación Condiciones', dic_campos_completados_pdf.get('Casilla de verificación1', False)) # En la versión 2 de los PDF la casilla de aceptación se llama de esta forma.
        documento_firmado = self.verificar_firma_pdf(pdf_path)
       

        if operador is None:
            log_function(PDFProcessingStatus.MISSING_OPERATOR_INFO.value)
            return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.MISSING_OPERATOR_INFO, aceptacion_condiciones_uso, documento_firmado)
        
        if documento_firmado is False:
            return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.MISSING_SIGNATURE, aceptacion_condiciones_uso, documento_firmado)

        operador_dal = OperadorDAL(db)
        r_operador = operador_dal.get_record_by_nif(operador.nif_operador)
        if r_operador:
            log_function(f"{PDFProcessingStatus.OPERATOR_EXISTS.value}: {r_operador.nif_operador} - {r_operador.razon_social}. Si continua se actualizaran los datos del operador.")
            return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.OPERATOR_EXISTS, aceptacion_condiciones_uso, documento_firmado)
        
        return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.LOAD_PDF_OK, aceptacion_condiciones_uso, documento_firmado)


    def guardar_datos_registros_pdf(self, db, operador, representante_firma, representantes, log_function):

        """
        Guarda los datos de operador y rerpresentante en la BD indicada.
        """


        operador_dal = OperadorDAL(db)
        try:
            operador_dal.insert(operador, representante_firma)
            log_function(PDFProcessingStatus.SUCCESS.value)
        except Exception as e:
            log_function(f"{PDFProcessingStatus.INSERTION_ERROR.value}: {str(e)}")
            return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.INSERTION_ERROR)

        usuario_operador_dal = Usuario_OperadorDAL(db)
        for representante in representantes:
            log_function(f"Procesando representante con NIF {representante.nif}")

            try:
                usuario = usuario_operador_dal.get_record_by_nif(representante.nif)
                if usuario is None:
                    log_function(f"El representante {representante.nif} - {representante.nombre_completo} NO existe en la tabla de usuarios. Se procederá a su inserción.")
                    representante = usuario_operador_dal.insert(representante)
                    log_function(f"Representante {representante.nif} insertado exitosamente.")
                else:
                    log_function(f"El representante {usuario.nif} - {usuario.nombre_completo} ya existe en la tabla de usuarios.")
                    representante = usuario

                representante_con_info_operadoras = usuario_operador_dal.get_usuario_con_relacion_de_operadoras(representante)
                operadora_encontrada = [o for o in representante_con_info_operadoras.operadoras if o.nif_operador == operador.nif_operador]
                if operadora_encontrada:
                    log_function(f"El usuario {representante_con_info_operadoras.nombre_completo} ya está dado de alta como representante de la Operadora")
                else:
                    log_function(f"El usuario {representante_con_info_operadoras.nombre_completo} no se encontró como representante de la Operadora. Generamos la relación.")
                    usuario_operador_dal.add_usuario_relacion_con_operadora(representante, operador)

            except Exception as e:
                log_function(f"{PDFProcessingStatus.REPRESENTATIVE_PROCESSING_ERROR.value} {representante.nif}: {str(e)}")
                return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.REPRESENTATIVE_PROCESSING_ERROR)
            
        return ResultadoProcesamiento(operador, representantes, representante_firma, PDFProcessingStatus.SUCCESS)


    def completar_datos_representante_firma(self, representantes, representante_firma):
        """
        Completa el campo email del representante firmante utilizando el dato del representante que comparte el mismo CIF.

        :param representantes: Lista de objetos Representante.
        :param representante_firma: Objeto Representante firmante.
        :return: Objeto Representante firmante con el campo email completado si se encuentra coincidencia.
        """
        if not representante_firma or not representante_firma.nif:
            return representante_firma  # Si no hay representante firmante o no tiene CIF, no hacemos nada

        # Buscar en la lista de representantes
        for representante in representantes:
            if representante.nif == representante_firma.nif:
                # Si encontramos un representante con el mismo CIF, completamos el email
                representante_firma.email = representante.email
                break  # Una vez encontrado, no necesitamos seguir buscando

        return representante_firma
    

    def actualizar_datos_operador(self, 
                                  operador: Operador, 
                                  representantes: List[Usuario_Operador], 
                                  representante_legal: Usuario_Operador,
                                  db, 
                                  log) -> bool:
        """
       Actualiza los datos del operador, representantes y representante legal en la base de datos.

        Parámetros:
        - operador: Instancia del operador cuyos datos se actualizarán.
        - representantes: Lista de representantes cuyos datos se actualizarán.
        - representante_legal: Representante legal que firma, cuyos datos se actualizarán.
        - db: Conexión a la base de datos.
        - log: Logger para registrar la actividad.

        Retorna:
        - bool: True si la actualización fue exitosa, False si ocurrió un error.
        """
        try:
            operador_dal = OperadorDAL(db)
            operador_dal.update_operador(operador, representante_legal)
            log("Datos del operador actualizados correctamente.")

            usuario_operador_dal = Usuario_OperadorDAL(db)

            for representante in representantes:
                usuario = usuario_operador_dal.get_record_by_nif(representante.nif)

                if usuario is None:
                    r_representante = usuario_operador_dal.insert(representante)
                    log(f"Representante {representante.nif} insertado exitosamente.")
                else:
                    r_representante = usuario_operador_dal.update_usuario(representante)
                    log(f"Representante {usuario.nif} - {usuario.nombre_completo} ya existe. Se han actualizado sus datos.")

                if not r_representante:
                    log(f"No se pudo actualizar los datos del representante {representante.nombre_completo}.")
                    continue

                

                representante_info = usuario_operador_dal.get_usuario_con_relacion_de_operadoras(representante)
                if any(o.nif_operador == operador.nif_operador for o in representante_info.operadoras):
                    log(f"El representante {representante_info.nombre_completo} ya está vinculado a la operadora {operador.nif_operador}.")
                else:
                    usuario_operador_dal.add_usuario_relacion_con_operadora(representante, operador)
                    log(f"Vinculación del representante {representante_info.nombre_completo} a la operadora {operador.nif_operador} realizada con éxito.")

            return True
        except Exception as e:
            log(f"Error al actualizar los datos: {str(e)}")
            return False
        

    def verificar_firma_pdf(self, pdf_path):
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_reader = PdfFileReader(pdf_file, strict=False)

                # Verificar la existencia de AcroForm y Fields
                acro_form = pdf_reader.root.get("/AcroForm")
                if acro_form is not None:
                    acro_form = acro_form.get_object()  # Resolver IndirectObject
                    fields = acro_form.get("/Fields")
                    if fields:
                        for field in fields:
                            field = field.get_object()  # Resolver cada campo
                            if field.get("/FT") == "/Sig":  # Verificar si es campo de firma
                                print(f"Firma encontrada en el archivo {os.path.basename(pdf_path)}. No se comprueba la validez de la firma. ")
                                return True
                                
                                """
                                sig_field_name = field.get("/T")
                                
                                signature_status = validate_pdf_signature(pdf_reader, field_name=sig_field_name)
                                if signature_status is not None and signature_status.is_valid:
                                    print(f"Firma válida encontrada en el archivo {os.path.basename(pdf_path)}.")
                                    return True
                                else:
                                    print(f"Firma no válida en el archivo {os.path.basename(pdf_path)}.")
                        print("No se detectaron firmas válidas en los campos del formulario PDF.")
                        """
                        print(f"No se detectaron firmas en el archivo {os.path.basename(pdf_path)}.")
                        return False

        except Exception as e:
            print(f"Error al abrir o procesar el archivo PDF: {e}")
            return False
                        


    

          