import re

"""
Este modelo representa la estructura de la tabla 'Tabla_Usuarios_UNICODatos' en la base de datos 'BD_UNICO_DATOS'. 
La clase 'Usuario_Operador' encapsula la información básica de un usuario, incluyendo su nombre, apellidos, 
NIF, correo electrónico y teléfono. 

Además, este modelo establece una relación con la tabla 'Tabla_Usuarios_Operadores', que registra la vinculación 
de un usuario con una o varias operadoras. Esta relación se refleja en la propiedad 'operadoras', la cual 
almacena una lista de operadoras asociadas a cada usuario.
"""

class Usuario_Operador:
  def __init__(self,id, nombre, apellido1, apellido2, nif, email, telefono):
        self.id = id
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.nif = self.normalizar_dni(nif)
        self.email = email
        self.telefono = self.normalizar_telefono(telefono)
        self.operadoras = []

  @property
  def nombre_completo(self):
        """Retorna el nombre completo del usuario concatenando nombre, apellido1 y apellido2."""
        # Aquí concatenamos los valores para formar el nombre completo.
        # Si apellido2 no está presente, simplemente se omitirá.
        return f"{self.nombre} {self.apellido1} {self.apellido2}".strip()




  @staticmethod
  def normalizar_dni(dni):
        """
        Normaliza un valor de DNI al formato estándar '12345678K'.
        
        :param dni: El DNI a normalizar.
        :return: El DNI normalizado.
        """
        # Eliminar cualquier carácter no numérico o letra (como puntos, espacios, etc.)
        dni = re.sub(r'\s|\.|-', '', dni)
        # Asegurarse de que la letra esté en mayúscula
        dni = dni.upper()
        # Verificar y ajustar la longitud
        if len(dni) > 9:
            dni = dni[:9]  # Tomar solo los primeros 9 caracteres (en caso de que haya más)
        return dni
  

  @staticmethod
  def normalizar_telefono(telefono):
        """
        Normaliza un número de teléfono eliminando espacios, puntos, guiones y cualquier carácter no numérico.
        
        :param telefono: El número de teléfono en su formato original.
        :return: El número de teléfono normalizado.
        """
        # Usar una expresión regular para eliminar cualquier carácter que no sea un dígito
        telefono_normalizado = re.sub(r'\D', '', telefono)
        return telefono_normalizado