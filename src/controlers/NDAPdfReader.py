import errno

from PyPDF2 import PdfFileReader
import pyodbc

# fichero = r"C:\Cargador_PDF\TELEFONICA_Formulario_Registro_Operadora_UNICO_DATOS_firmado.pdf"
fichero_PDF = r"C:\Cargador_PDF\ASTEO_Formulario_Registro_Operadora_UNICO_DATOS_v3 ASTEO.pdf"

fichero_Access = r"R:\Cobertura_BA\Programa UNICO-Datos\Proyecto_de_datos\01.Contactos\BD_UNICO_DATOS_V2.accdb"

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + fichero_Access + ';')
cursor = conn.cursor()
table_name = "Tabla_Operadores"
cursor.execute('SELECT * FROM ' + table_name)
queryBusquedaEmpresaCIF = 'SELECT * FROM Tabla_Operadores WHERE CIF ='
queryBusquedaUsuarioDNI = 'SELECT * FROM Tabla_Usuarios_Operadores where DNI = '
# for row in cursor.fetchall():
    # print(row)


def PruebaValor(Valor):
    try:
        Valor
    except:
        print(f'Valor {Valor} no localizado')
    finally:
        print(f'Valor {Valor} evaluado')


def ComrpuebaUsuario(DNI, cursor):
    cursor.execute('SELECT * FROM Tabla_Usuarios_Operadores where DNI = ' + DNI )
    if len(cursor.fetchall()) == 0:
        print("Usuario no existe en bbdd")
        return False
    else:
        print("Usuario existe en bbdd")
        return True


def ComrpuebaEmpresa(CIF, cursor):
    cursor.execute('SELECT * FROM Tabla_Operadores where CIF = ' + CIF)
    if len(cursor.fetchall()) == 0:
        print ("Empresa no existe en bbdd")
        return False
    else:
        print ("Empresa existe en bbdd")
        return True


def ComrpuebaFormatoCIF(CIF):
    if len(CIF) == 9:
        if CIF[0].isalpha():
            print("Primer caracter del CIF es una letra")
            return True
        else:
            print("Error en CIF, primer caracter no es una letra")
            return False
    else:
        print("CIF con formato incorrecto")
        CIF = CIF.replace('-', '')
        if ComrpuebaFormatoCIF(CIF):
            return True
        else:
            return False



class Empresa:

    def __init__(self, CIF):
        self.CIF = CIF
        self.Usuarios = []
        self.Nombre_Empresa = ""
        self.Nombre_Comercial = ""
        self.Direccion = ""
        self.Codigo_Postal = ""
        self.Poblacion = ""
        self.Provincia = ""
        self.CorreoElectronico = ""
        self.Telefono = ""
        self.PaginaWeb = ""
        self.SectorEmpresarial = ""
        self.AmbitoActuacion = ""

    def add_Nombre(self, Nombre):
        self.Nombre_Empresa = Nombre

    def add_NombreComercial (self, Nombre):
        self.Nombre_Comercial = Nombre

    def add_Usuario(self, user):
        self.Usuarios.append(user)


class Usuario:
    def __init__(self, DNI):
        self.Nombre = ""
        self.DNI = DNI
        self.Apellido1 = ""
        self.Apellido2 = ""
        self.Cargo = ""
        self.Telefono = ""
        self.Extension = ""
        self.CorreoElectronico = ""

    def add_Nombre(self, Nombre):
        self.Nombre = Nombre

    def add_NombreCompleto(self, Nombre, Apellido1, Apellido2):
        self.Nombre = Nombre
        self.Apellido1 = Apellido1
        self.Apellido2 = Apellido2

    def add_Telefono(self, Telefono):
        self.Telefono = Telefono

    def add_Cargo(self, Cargo):
        self.Cargo = Cargo

    def add_Correo(self, Correo):
        self.CorreoElectronico = Correo


reader = PdfFileReader(fichero_PDF)
numberofpages = len(reader.pages)
print(f"Número de páginas : {numberofpages}")
fields = reader.getFields()
print(f"------------------------DATOS DE LA EMPRESA-----------------------------")
print(f"Nombre de la empresa: {fields['NOMBRE DE LA EMPRESA']['/V']}")
print(f"Nombre comercial de la empresa: {fields['NOMBRE COMERCIAL']['/V']}")
print(f"CIF: {fields['CIF']['/V']}")
print(f"Calle: {fields['Calle']['/V']}")
print(f"Código Postal: {fields['Código Postal']['/V']}")
print(f"Población: {fields['Población']['/V']}")
print(f"Provincia: {fields['Provincia']['/V']}")
print(f"Correo Electrónico: {fields['CORREO ELECTRÓNICO RRHH']['/V']}")
print(f"Telefono: {fields['TELÉFONO CONTACTO RRHH']['/V']}")
print(f"Página Web: {fields['PÁGINA WEB']['/V']}")
# print(f"Ambito Actuación: {fields['ÁMBITO DE ACTUACIÓN']['/V']}")
#todo : Controlar campos nulos
print(f"Sector Empresarial: {fields['SECTOR EMPRESARIAL']['/V']}")
#todo: Controlar limite usuarios
print(f"------------------------DATOS DE USUARIO 1-----------------------------")
print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS']['/V']}")
print(f"DNI : {fields['DNI']['/V']}")
print(f"Cargo : {fields['CARGO']['/V']}")
print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO']['/V']}")
# print(f"Extensión : {fields['Extensión']['/V']}")
print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO']['/V']}")

print(f"------------------------DATOS DE USUARIO 2-----------------------------")
print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS_2']['/V']}")
print(f"DNI : {fields['DNI_2']['/V']}")
print(f"Cargo : {fields['CARGO_2']['/V']}")
print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO_2']['/V']}")
# print(f"Extensión : {fields['Extensión_2']['/V']}")
print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO_2']['/V']}")

print(f"------------------------DATOS DE USUARIO 3-----------------------------")
print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS_3']['/V']}")
print(f"DNI : {fields['DNI_3']['/V']}")
print(f"Cargo : {fields['CARGO_3']['/V']}")
print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO_3']['/V']}")
# print(f"Extensión : {fields['Extensión_3']['/V']}")
print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO_3']['/V']}")

print(f"------------------------DATOS DE USUARIO 4-----------------------------")
print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS_4']['/V']}")
print(f"DNI : {fields['DNI_4']['/V']}")
print(f"Cargo : {fields['CARGO_4']['/V']}")
print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO_4']['/V']}")
# print(f"Extensión : {fields['Extensión_4']['/V']}")
print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO_4']['/V']}")

print(f"------------------------DATOS DE USUARIO 5-----------------------------")
print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS_5']['/V']}")
print(f"DNI : {fields['DNI_5']['/V']}")
print(f"Cargo : {fields['CARGO_5']['/V']}")
print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO_5']['/V']}")
# print(f"Extensión : {fields['Extensión_5']['/V']}")
print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO_5']['/V']}")

print(f"------------------------DATOS DE USUARIO 6-----------------------------")
# print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS_6']['/V']}")
# print(f"DNI : {fields['DNI_6']['/V']}")
# print(f"Cargo : {fields['CARGO_6']['/V']}")
# print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO_6']['/V']}")
# print(f"Extensión : {fields['Extensión_6']['/V']}")
# print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO_6']['/V']}")

print(f"------------------------DATOS DE USUARIO 7-----------------------------")
# print(f"Nombre y Apellidos : {fields['NOMBRE Y APELLIDOS_7']['/V']}")
# print(f"DNI : {fields['DNI_7']['/V']}")
# print(f"Cargo : {fields['CARGO_7']['/V']}")
# print(f"Teléfono de contacto : {fields['TELÉFONO DE CONTACTO_7']['/V']}")
# print(f"Extensión : {fields['Extensión_7']['/V']}")
# print(f"Correo Electrónico : {fields['CORREO ELECTRÓNICO_7']['/V']}")

#todo controlar si usuario existe en bbdd
#todo añadir usuario en bbdd si no existe
#todo añadir operador en bbdd
#todo añadir usuario a operador en bbdd si usuario existia anteriormente
#todo añadir usuario a operador en datos
#todo añadir usuario a operador en bbdd
#todo actualizar tablas bbdd de UNICO Datos

print("END")

