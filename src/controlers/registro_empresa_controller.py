import fitz  # PyMuPDF
import os
from models.usuario_operador_model import Usuario_Operador
from models.operador_model import Operador
from helpers.NombreApellidosParser import NombreApellidosParser
from DAL.operador_dal import OperadorDAL
from DAL.usuario_operador_dal import Usuario_OperadorDAL



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
                        if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                            field_name = widget.field_name
                            field_value = widget.field_value if hasattr(widget, 'field_value') else ''
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
        cob_fwa = None  # Valor no proporcionado en los datos
        cob_movil = None  # Valor no proporcionado en los datos
        nif_grupo_operador = None  # Valor no proporcionado en los datos
        grupo_operador = None # Valor no proporcionado en los datos
        nif_replegal = None  # Valor no proporcionado en los datos
        nombre_replegal = None  # Valor no proporcionado en los datos
        nif_notificacion = None  # Valor no proporcionado en los datos
        representante_notificacion = None  # Valor no proporcionado en los datos
        email_notificacion = datos.get('CORREO ELECTRÓNICO RRHH')


        # Crear el objeto Operador solo si 'nif_operador' y 'razon_social' están presentes
        if not (nif_operador and razon_social):
            return None

        operador = Operador(
            nif_operador=nif_operador,
            razon_social=razon_social,
            cob_fwa=cob_fwa,
            cob_movil=cob_movil,
            nif_grupo_operador=nif_grupo_operador,
            grupo_operador=grupo_operador,
            nif_replegal=nif_replegal,
            nombre_replegal=nombre_replegal,
            nif_notificacion=nif_notificacion,
            representante_notificacion=representante_notificacion,
            email_notificacion=email_notificacion
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


    def procesar_pdf(self, pdf_path, db, log_function):
        """
        Procesa un único PDF, inserta el operador y los representantes en la base de datos.
        """
        # Obtener los campos del PDF
        dic_campos_completados_pdf = self.get_dict_from_PDF(pdf_path)
        operador = self.crear_operador_from_dict(dic_campos_completados_pdf)
        representantes = self.crear_representantes_from_dict(dic_campos_completados_pdf)
        representate_firma = self.crear_representante_firma_from_dict(dic_campos_completados_pdf)
        representate_firma = self.completar_datos_representante_firma(representantes, representate_firma)

        if operador is None:
            log_function("PDF no procesado, el campo operador no contiene información")
            return False

        operador_dal = OperadorDAL(db)
        r_operador = operador_dal.get_record_by_nif(operador.nif_operador)
        if r_operador:
            log_function(f"El Operador {r_operador.nif_operador} - {r_operador.razon_social} ya existe en la BD. No se continuará con el proceso de importación de datos del PDF.")
            return False

        try:
            operador_dal.insert(operador, representate_firma)
            log_function("Operador insertado exitosamente.")
        except Exception as e:
            log_function(f"Error al insertar el operador: {str(e)}")
            return False

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
                    log_function(f"El usuario {representante_con_info_operadoras.nombre_completo} ya esta dado de alta como representante de la Operadora")
                else:
                    log_function(f"El usuario {representante_con_info_operadoras.nombre_completo} No se encontró como representante de la Operadora. Generamos la relación.")
                    usuario_operador_dal.add_usuario_relacion_con_operadora(representante, operador)

            except Exception as e:
                log_function(f"Error al procesar el representante {representante.nif}: {str(e)}")
        return True

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


    

          