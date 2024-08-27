# Procesador para extracción de datos Registro empresa colaboradora.


## Generar el ejecutable 

```sh
pyinstaller --onefile --windowed app.py
````



## Utilizar a la funcionalidad sin utilizar el ejecutable. 

```sh 

from controlers.registro_empresa_controller import RegistroEmpresaColaboradoraController
db = Database(db_path)

controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
result = controladoraREC.procesar_pdf(pdf_path, db, escribirLog)
````

def escribirLog(mensaje):
    print(mensaje)