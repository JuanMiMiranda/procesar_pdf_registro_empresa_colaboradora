import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
from typing import List
import pandas as pd
from controlers.registro_empresa_controller import RegistroEmpresaColaboradoraController
from DAL.database import Database
from tkinter import messagebox
import os




class App:
    # Obtener el directorio actual
    current_directory = os.getcwd()
    version = '1.0.1'

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

        # Botón para seleccionar DB Access
        self.load_bd_access_button = tk.Button(
            button_frame,
            text="2. Seleccionar DB Access",
            command=self.change_db_access,
            bg="#abebe4",        # Azul
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.load_bd_access_button.pack(side=tk.LEFT, padx=5)
        self.load_bd_access_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        # Botón para procesar los archivos PDF
        self.process_button = tk.Button(
            button_frame,
            text="3. Procesar PDFs",
            command=self.process_pdfs,
            bg="#ffa322",        # Naranja
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        self.process_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        # Crear la tabla (Treeview)
        self.tree = ttk.Treeview(root, columns=("PDF_NAME", "PDF_PATH", "ESTADO"), show="headings")
        self.tree.heading("PDF_NAME", text="Nombre del PDF")
        self.tree.heading("PDF_PATH", text="Ruta del PDF")
        self.tree.heading("ESTADO", text="Estado Proceso")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

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
            self.load_bd_access_button.config(state=tk.NORMAL) # Habilitamos el siguiente botón
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
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal
            messagebox.showwarning("Archivos PDF no encontrado", f"No hay elementos PDF en la lista para procesar.")
            root.destroy()  # Cerrar la ventana emergente
            return
        
        ###################################
        # 1º Procesar PDF. 
        ###################################

        for row in children:
            pdf_path = self.tree.item(row, "values")[1]
            pdf_name = self.tree.item(row, "values")[0]
            self.log(f"Procesado {pdf_name}")
            controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
            result = controladoraREC.procesar_pdf(pdf_path, db, self.log)
             # Actualizar el campo "ESTADO" basado en `result`
            new_estado = "OK" if result else "ERROR"
            self.tree.item(row, values=(pdf_name, pdf_path, new_estado))


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




