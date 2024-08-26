import pyodbc
import os

# Verifica que pyodbc esté instalado y configurado correctamente
db_path = r'E:\Temp\BD_UNICO_DATOS.accdb'
if os.path.exists(db_path):
    print("El archivo existe.")
else:
    print("El archivo no existe.")
connection_string = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=" + db_path + ";"
)
try:
    conn = pyodbc.connect(connection_string)
    print("Connected to the database successfully!")
    conn.close()
except pyodbc.Error as e:
    print("Error: ", e)