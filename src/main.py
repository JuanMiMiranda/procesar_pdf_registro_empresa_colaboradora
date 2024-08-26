import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
from typing import List
import pandas as pd
from controlers.registro_empresa_controller import RegistroEmpresaColaboradoraController
from DAL.database import Database
from DAL.operador_dal import OperadorDAL
from DAL.usuario_operador_dal import Usuario_OperadorDAL
from models.operador_model import Operador
import pyodbc

from models.usuario_operador_model import Usuario_Operador


class App:
    # TODO CAMBIAR BD POR DEFECTO.
    db_default_path = r'E:\OneDrive\DATOS\99 - SETELECO\TAREAS SETELECO\04_Tarea_UNICODatos_NDA\Tarea_UNICODatos_NDA\BD_UNICO_DATOS.accdb'
    db_path = db_default_path
    
    
    def __init__(self, root):
        self.root = root
        self.root.title("Importar datos de archivos para acuerdos de confidencialidad")
        self.root.geometry("800x600")
        # Frame para los botones
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X, pady=10)

        # Botón para cargar los archivos PDF
        self.load_button = tk.Button(button_frame, text="1. Cargar PDFs", command=self.load_pdfs)
        self.load_button.pack(side=tk.LEFT, padx=5)

          # Botón para seleccionar DB Access
        self.load_bd_access_button = tk.Button(button_frame, text="2. Seleccionar DB Access.", command=self.change_db_access)
        self.load_bd_access_button.pack(side=tk.LEFT, padx=5)

        # Botón para procesar los archivos PDF
        self.process_button = tk.Button(button_frame, text="3. Procesar PDFs", command=self.process_pdfs)
        self.process_button.pack(side=tk.LEFT, padx=5)

        # Botón para exportar el contenido de la tabla a CSV
        self.export_button = tk.Button(button_frame, text="4. Exportar a CSV", command=self.export_to_csv)
        self.export_button.pack(side=tk.LEFT, padx=5)

        # Crear la tabla (Treeview)
        self.tree = ttk.Treeview(root, columns=("PDF_NAME", "PDF_PATH", "EMPRESA"), show="headings", selectmode="extended")
        self.tree.heading("PDF_NAME", text="Nombre del PDF")
        self.tree.heading("PDF_PATH", text="Ruta del PDF")
        self.tree.heading("EMPRESA", text="Nombre de la Empresa")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Crear el label para los logs
        self.log_label = tk.Label(root, text="Log:")
        self.log_label.pack(pady=5, anchor='w')

    
        # Crear el campo de texto para mostrar logs
        self.log_text = tk.Text(root, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)

        self.pdf_paths = []  # Lista para almacenar las rutas de los archivos PDF

        # Crear un label para el preloader (invisible inicialmente)
        self.preloader = tk.Label(root, text="Cargando...", font=('Helvetica', 16))
        self.preloader.pack(pady=10)
        self.preloader.place_forget()  # Ocultar el preloader inicialmente

        # Crear el label para los logs
        self.db_access_label = tk.Label(root, text=f"BD Access: {self.db_path}")
        self.db_access_label.pack(pady=5, anchor='w')

    def load_pdfs(self):
        # Abrir diálogo para seleccionar múltiples archivos PDF
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos PDF Formularios Registro Operadora", "*.pdf")])
        if file_paths:
            # Limpiar la tabla actual
            self.tree.delete(*self.tree.get_children())

            self.pdf_paths = file_paths
            for file_path in file_paths:
                pdf_name = os.path.basename(file_path)
                self.tree.insert("", tk.END, values=(pdf_name, file_path, ""))

            self.log("Archivos PDF cargados y mostrados en la tabla.")

    def change_db_access(self):
        # Abrir diálogo para seleccionar archivo BD Access
        self.db_path = filedialog.askopenfilename(filetypes=[("BD Access incorporación de datos", "*.accdb")])
        if self.db_path:  # Si se selecciona un archivo
            # Actualizar el texto del Label con la ruta de la base de datos
            self.db_access_label.config(text=f"BD Access: {self.db_path}")
 

    def process_pdfs(self):
        # Mostrar preloader
        self.preloader.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.root.update()  # Actualizar la interfaz gráfica para mostrar el preloader

        ###################################
        # 0º Instanciación DB. 
        ###################################
        db = Database(self.db_path)

        # Obtener los elementos de self.tree
        children = self.tree.get_children()

        # Verificar si no hay elementos
        if not children:
            self.log("No hay elementos en la lista para procesar.")
            return
        
        for row in children:
            pdf_path = self.tree.item(row, "values")[1]
            pdf_name = self.tree.item(row, "values")[0]
            self.log(f"Procesado {pdf_name}")
            controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
            controladoraREC.procesar_pdf(pdf_path, db, self.log)

            """
            ###################################
            # 1º Obtener los campos del PDF. 
            #    - Generar la instancia con los datos del operador.
            #    - Generar la instancia de la lista de representantes del operador. 
            ###################################
            controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
            dic_campos_completados_pdf = controladoraREC.get_dict_from_PDF()
            print(dic_campos_completados_pdf)
            operador = controladoraREC.crear_operador_from_dict(dic_campos_completados_pdf)
            representantes = controladoraREC.crear_representantes_from_dict(dic_campos_completados_pdf)

            if operador is None:
                self.log("PDF no procesado, el campo operador no contiene información")
                continue  # Continuar con el siguiente PDF

            ###################################
            # 2º Gestionar representantes.
            #    A. Comprobar si existe el operador en BD. En caso de no estar damos de alta el operador en la BD.
            #    B. Comprobar si los representantes ya están en BD. En caso de no estar, damos de alta el representante en la BD.
            ###################################
            # 2º-A. Alta de operador.
            operador_dal = OperadorDAL(db)
            r_operador = operador_dal.get_record_by_nif(operador.nif_operador)
            if r_operador:
                self.log(f"El Operador {r_operador.nif_operador} - {r_operador.razon_social} ya existe en la BD. No se continuará con el proceso de importación de datos del PDF.")
                continue  # Continuar con el siguiente PDF

            try:
                operador_dal.insert(operador)
                self.log("Operador insertado exitosamente.")
            except Exception as e:
                self.log(f"Error al insertar el operador: {str(e)}")
                continue  # Continuar con el siguiente PDF

            # 2º-B. Alta de representante en BD.
            usuario_operador_dal = Usuario_OperadorDAL(db)
            for representante in representantes:
                self.log(f"Procesando representante con NIF {representante.nif}")

                try:
                    representante = usuario_operador_dal.get_record_by_nif(representante.nif)
                    if representante.id is None:
                        self.log(f"El representante {representante.nif} - {representante.nombre_completo} NO existe en la BD. Se procederá a su inserción.")
                        usuario_operador_dal.insert(representante)
                        self.log(f"Representante {representante.nif} insertado exitosamente.")
                    else:
                        self.log(f"El representante {representante.nif} - {representante.nombre_completo} ya existe en la BD. Comprobando si es representante de la empresa {operador.razon_social}.")

                    # Alta de relación representante empresa.
                    representante_con_info_operadoras: Usuario_Operador = usuario_operador_dal.get_usuario_con_relacion_de_operadoras(representante)
                    operadora_encontrada = [o for o in representante_con_info_operadoras.operadoras if o.nif_operador == operador.nif_operador]
                    if operadora_encontrada:
                        self.log(f"Operadora encontrada: {operadora_encontrada[0].razon_social} para el representante {representante_con_info_operadoras.nombre_completo}")
                    else:
                        self.log("No se encontró una operadora con ese CIF para el representante. Generamos la relación.")
                        usuario_operador_dal.add_usuario_relacion_con_operadora(representante, operador)   
                  

                except Exception as e:
                    self.log(f"Error al procesar el representante {representante.nif}: {str(e)}")
            """

            
        # Ocultar preloader
        self.preloader.place_forget()
        self.root.update()  # Actualizar la interfaz gráfica para ocultar el preloader

        """
        operador_dal = OperadorDAL(db)
        
        # Recuperar todos los registros de la tabla de operadores
        operadores = operador_dal.get_all_records()
        # Imprimir los objetos Operador
        for operador in operadores:
            print(operador.nif_operador + ' - ' + operador.razon_social)


        usuario_operador_dal = Usuario_OperadorDAL(db)
        usuarios_operadores = usuario_operador_dal.get_all_records()
         # Imprimir los objetos usuarios_operadores
        for u_operador in usuarios_operadores:
            print(u_operador.nif + " - " + u_operador.nombre_completo)

       
    
        # Cerrar la conexión a la base de datos
        db.close()
        self.preloader.place_forget()  # Ocultar preloader
        self.root.update()  # Actualizar la interfaz gráfica para ocultar el preloader
        """


        #todo controlar si usuario existe en bbdd
        #todo añadir usuario en bbdd si no existe
        #todo añadir operador en bbdd
        #todo añadir usuario a operador en bbdd si usuario existia anteriormente
        #todo añadir usuario a operador en datos
        #todo añadir usuario a operador en bbdd
        #todo actualizar tablas bbdd de UNICO Datos

    def export_to_csv(self):

        # Crear una instancia de la base de datos
        db = Database(self.db_path)

        # Crear una instancia de Usuario_OperadorDAL con la conexión a la base de datos
        usuario_operador_dal = Usuario_OperadorDAL(db)

        # Crear una instancia de Usuario_Operador
        representante = Usuario_Operador(
            id=400,         # ID del representante
            nombre='Juan',  # Nombre
            apellido1='',   # Primer apellido (vacío)
            apellido2='',   # Segundo apellido (vacío)
            nif='1234',     # NIF 
            email='',       # Correo electrónico (vacío)
            telefono=''     # Teléfono (vacío)
        )

        # Insertar el representante en la base de datos
        usuario_operador_dal.insert(representante)

        # Cierra la conexión para asegurar que los cambios se guardan
        db.close()  # Asegúrate de que hay un método `close` que cierra la conexión correctamente

        # Reabrir la conexión para consultar
        db = Database(self.db_path)
        usuario_operador_dal = Usuario_OperadorDAL(db)

        # Consulta para verificar si el registro se insertó
        record = usuario_operador_dal.get_record_by_nif('1234')

        if record:
             self.log("El registro existe y tiene un ID asignado:", record)
        else:
             self.log("El registro no se encontró.")
            
        # Cierra la conexión nuevamente
        db.close()



        # Obtener el nombre del archivo para guardar el contenido de la tabla
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Obtener los datos de la tabla
            rows = [self.tree.item(row)["values"] for row in self.tree.get_children()]

            # Crear un DataFrame y guardarlo como CSV
            df = pd.DataFrame(rows, columns=["Nombre del PDF", "Ruta del PDF", "Nombre de la Empresa"])
            df.to_csv(file_path, index=False)
            self.log(f"Contenido de la tabla exportado a {file_path}")

    def log(self, message):
        # Agregar mensaje al campo de texto de logs
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)  # Desplazar hacia abajo para mostrar el nuevo mensaje

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()