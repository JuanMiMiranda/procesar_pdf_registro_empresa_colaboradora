import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
from typing import List
import pandas as pd
from controlers.registro_empresa_controller import RegistroEmpresaColaboradoraController
from DAL.database import Database
from tkinter import messagebox
import os

from models.ResultadoProcesamiento import ResultadoProcesamiento
from models.enum import PDFProcessingStatus




class App:
    # Obtener el directorio actual
    current_directory = os.getcwd()
    version = '1.0.2'

    # Formar la ruta completa
    db_default_path = os.path.join(current_directory, 'BD_UNICO_DATOS.accdb')
    # db_default_path = r'E:\OneDrive\DATOS\99 - SETELECO\TAREAS SETELECO\04_Tarea_UNICODatos_NDA\Tarea_UNICODatos_NDA\BD_UNICO_DATOS.accdb'
    db_path = db_default_path
    
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"Herramienta interna para Importar datos de archivos de Registro de empresas colaboradoras - SETELECO - V."+ self.version)
        self.root.geometry("1200x600")

        # Frame para los botones en la parte superior
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X, pady=10)

        # Botón para cargar los archivos PDF
        self.load_button = tk.Button(
            button_frame,
            text="1. Cargar PDFs",
            command=self.load_pdfs,
            bg="#4CAF50",        # Verde
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.load_button.pack(side=tk.LEFT, padx=5)


        # Botón para obtener datos del PDF
        self.get_pdf_data_button = tk.Button(
            button_frame,
            text="2. Obtener datos PDF´s",
            command=self.get_pdf_data,
            bg="#5a9bd3",        # Azul más oscuro
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.get_pdf_data_button.pack(side=tk.LEFT, padx=5)
        self.get_pdf_data_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        
        # Botón para seleccionar DB Access
        self.load_bd_access_button = tk.Button(
            button_frame,
            text="3. Seleccionar DB Access",
            command=self.change_db_access,
            bg="#abebe4",        # Azul
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.load_bd_access_button.pack(side=tk.LEFT, padx=5)
        self.load_bd_access_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente
       
        # Botón para Guardar los datos
        self.process_button = tk.Button(
            button_frame,
            text="4. GUARDAR DATOS",
            command=self.process_pdfs,
            bg="#ffa322",        # Naranja
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        self.process_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        # Crear la tabla (Treeview) con una nueva columna para "Nombre Operadora"
        self.tree = ttk.Treeview(root, columns=("PDF_NAME", "PDF_PATH", "ESTADO", "NOMBRE_OPERADORA"), show="headings")
        self.tree.heading("PDF_NAME", text="Nombre del PDF")
        self.tree.heading("PDF_PATH", text="Ruta del PDF")
        self.tree.heading("NOMBRE_OPERADORA", text="Nombre Operadora")
        self.tree.heading("ESTADO", text="Estado Proceso")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        # Vincular evento de selección en la tabla
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Crear el label para los logs
        self.log_label = tk.Label(root, text="Log:")
        self.log_label.pack(pady=5, anchor='w')

        # Crear el campo de texto para mostrar logs
        self.log_text = tk.Text(root, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame para los controles de base de datos en la parte inferior
        db_frame = tk.Frame(root)
        db_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM)

        # Crear el label para la base de datos
        self.db_access_label = tk.Label(db_frame, text="BD Access: No seleccionada")
        self.db_access_label.pack(side=tk.LEFT, padx=5)

        # Botón para editar el registro seleccionado
        self.edit_button = tk.Button(
            root,
            text="Editar registro seleccionado",
            command=self.edit_selected_record,
            bg="#ff6347",        # Rojo
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.edit_button.pack(pady=5, anchor='e')  # Alineado a la derecha
        self.edit_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

    def on_tree_select(self, event):
        # Obtener el item seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            # Obtener la información del registro seleccionado
            item_data = self.tree.item(selected_item)
            values = item_data['values']
            print(f"Registro seleccionado: {values}")
            self.edit_button.config(state=tk.NORMAL) # Habilitar boton de edición.
    
    def get_pdf_data(self):
      
    

    def edit_selected_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Obtén la información del registro seleccionado
            item_data = self.tree.item(selected_item)
            print(f"Editar: {item_data}")
            # Implementa la lógica para editar el registro
        else:
            print("No se ha seleccionado ningún registro.")

    def load_pdfs(self):

        # Abrir diálogo para seleccionar múltiples archivos PDF
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos PDF Formularios Registro Operadora", "*.pdf")])
        if file_paths:
            # Limpiar la tabla actual
            self.tree.delete(*self.tree.get_children())

            self.pdf_paths = file_paths
            for file_path in file_paths:
                pdf_name = os.path.basename(file_path)
                self.tree.insert("", tk.END, values=(pdf_name, file_path, "SIN PROCESAR"))

            self.log("Archivos PDF cargados y mostrados en la tabla.")
            self.get_pdf_data_button.config(state=tk.NORMAL) # Habilitamos el siguiente botón
            self.load_button.config(state=tk.DISABLED)


    def change_db_access(self):
        # Abrir diálogo para seleccionar archivo BD Access
        self.db_path = filedialog.askopenfilename(filetypes=[("BD Access incorporación de datos", "*.accdb")])
        if self.db_path:  # Si se selecciona un archivo
            # Actualizar el texto del Label con la ruta de la base de datos
            self.db_access_label.config(text=f"BD Access: {self.db_path}")
            self.process_button.config(state=tk.NORMAL) # Habilitamos el siguiente botón
            self.load_bd_access_button.config(state=tk.DISABLED)
           
 

    def process_pdfs(self):
        root = tk.Tk()
        ###################################
        # 0º Validaciones e Instanciación DB. 
        ###################################
        if not  self.check_db_file(self.db_path):
            return

        db = Database(self.db_path)

        # Obtener los elementos de self.tree
        children = self.tree.get_children()

        # Verificar si no hay elementos
        if not children:
            self.log("No hay elementos en la lista para procesar.")
            root.withdraw()  # Ocultar la ventana principal
            messagebox.showwarning("Archivos PDF no encontrado", f"No hay elementos PDF en la lista para procesar.")
            root.destroy()  # Cerrar la ventana emergente
            return
        
        ###################################
        # 1º Procesar PDF. 
        ###################################

        for row in children:
            new_estado = "Procesando..."
            pdf_path = self.tree.item(row, "values")[1]
            pdf_name = self.tree.item(row, "values")[0]
            self.log(f"Procesando {pdf_name}")
            self.tree.item(row, values=(pdf_name, pdf_path, new_estado)) # Actualizar estado en la tabla.
            controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
            result: ResultadoProcesamiento = controladoraREC.procesar_pdf(pdf_path, db, self.log)
            if result.pdf_processing_status is PDFProcessingStatus.SUCCESS:
                new_estado = "OK"
            elif result.pdf_processing_status == PDFProcessingStatus.OPERATOR_EXISTS:
                self.log("El operador ya existe. ¿Desea continuar con la actualización?")
                root.withdraw()  # Oculta la ventana principal
                cif = result.operador.nif_operador
                mensaje = (
                f"El operador con CIF {cif} ya está registrado en la base de datos. "
                "Si decides continuar, actualizaremos los datos del operador con la información del PDF. "
                "Si prefieres cancelar, no se procesará el PDF y los datos actuales del operador permanecerán sin cambios. "
                "¿Deseas proceder con la actualización?"
                )
                respuesta = messagebox.askyesno("Confirmar Actualización", mensaje)
                if respuesta:
                    respuesta_actualizacion = controladoraREC.actualizar_datos_operador(result.operador, result.representantes, result.representante_firma, db, self.log)
                    if respuesta_actualizacion:
                        new_estado = "DATOS ACTUALIZADOS"
                    else:
                        new_estado = "ERROR AL ACTUALIZAR"
                else:
                    print("Proceso cancelado. Los datos del operador permanecerán sin cambios.")
                    new_estado = "YA EXISTE. SIN CAMBIOS"
            elif result.pdf_processing_status == PDFProcessingStatus.MISSING_OPERATOR_INFO:
                self.log("No se pudo procesar el PDF porque falta información del operador.")
                new_estado = "ERROR. FALTA INFO. OPERADOR"
            elif result.pdf_processing_status == PDFProcessingStatus.INSERTION_ERROR:
                self.log("Ocurrió un error al intentar insertar el operador en la base de datos.")
                new_estado = "ERROR. INSERCIÓN EN BD"
            elif result.pdf_processing_status == PDFProcessingStatus.REPRESENTATIVE_PROCESSING_ERROR:
                self.log("Ocurrió un error al procesar uno de los representantes.")
                new_estado = "ERROR. EN PROCESADO DE REPRESENTANTES"
            
            self.tree.item(row, values=(pdf_name, pdf_path, new_estado)) # Actualizar estado en la tabla.


    def log(self, message):
        # Agregar mensaje al campo de texto de logs
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)  # Desplazar hacia abajo para mostrar el nuevo mensaje

    def check_db_file(self, db_path):

        # Comprobar si el archivo existe
        if not os.path.isfile(db_path):
            # Crear una ventana emergente si el archivo no existe
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal
            messagebox.showwarning("Archivo no encontrado", f"El archivo '{db_path}' no se encuentra. Selecciona un archivo de BD")
            self.log("Archivo no encontrado", f"El archivo '{db_path}' no se encuentra. Selecciona un archivo de BD")
            root.destroy()  # Cerrar la ventana emergente
            return False
        else:
            return True



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()




