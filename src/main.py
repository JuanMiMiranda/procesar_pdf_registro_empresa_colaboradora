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
from models.enum import PDFProcessingStatus, Status
from models.operador_model import Operador
from models.usuario_operador_model import Usuario_Operador
from view.edit_operadora import editar_operador
import webbrowser



class App:
    # Obtener el directorio actual
    current_directory = os.getcwd()
    version = '1.1.1'

    # Formar la ruta completa
    db_default_path = os.path.join(current_directory, 'BD_UNICO_DATOS.accdb')
    db_path = db_default_path

    # Diccionario que contendra los datos de cada PDF procesado. 
    dic_datos_pdf = {}

    
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

        # Botón para obtener datos del PDF
        self.get_pdf_data_button = tk.Button(
            button_frame,
            text="3. Obtener datos PDF´s",
            command=self.get_pdf_data,
            bg="#5a9bd3",        # Azul más oscuro
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.get_pdf_data_button.pack(side=tk.LEFT, padx=5)
        self.get_pdf_data_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        

        # Botón para Guardar los datos
        self.process_button = tk.Button(
            button_frame,
            text="4. GUARDAR DATOS",
            command=self.process_save_data_of_pdfs,
            bg="#ffa322",        # Naranja
            fg="white",         # Texto blanco
            font=("Helvetica", 12),  # Tamaño de fuente
            padx=15,            # Espacio adicional a los lados del texto
            pady=5              # Espacio adicional arriba y abajo del texto
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        self.process_button.config(state=tk.DISABLED)  # Deshabilitado inicialmente

        # Crear la tabla (Treeview) con una nueva columna para "Nombre Operadora"
        self.tree = ttk.Treeview(root, columns=("PDF_NAME", "PDF_PATH","NOMBRE_OPERADORA", "ESTADO","OBJ_ID"), show="headings")
        self.tree.heading("PDF_NAME", text="Nombre del PDF")
        self.tree.heading("PDF_PATH", text="Ruta del PDF")
        self.tree.heading("NOMBRE_OPERADORA", text="Nombre Operadora")
        self.tree.heading("ESTADO", text="Estado Proceso")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select) # Vincular evento de selección en la tabla
        self.tree.column("OBJ_ID", width=0, stretch=tk.NO) # Ocultar la columna de "OBJ_ID"

        # Vincular el doble clic al evento de abrir PDF
        self.tree.bind("<Double-1>", self.abrir_pdf)

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

    def abrir_pdf(self, event):
        # Obtener el ítem seleccionado
        seleccionado = self.tree.selection()
        if seleccionado:
            # Obtener el identificador del ítem seleccionado
            item = seleccionado[0]
            # Obtener la ruta del PDF desde la columna "PDF_PATH"
            pdf_path = self.tree.item(item, "values")[1]
            if os.path.exists(pdf_path):
                webbrowser.open(pdf_path)  # Abre el PDF en el visor predeterminado
            else:
                print("El archivo no existe:", pdf_path)

   
    def on_tree_select(self, event):
        # Obtener el item seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            # Obtener la información del registro seleccionado
            item_data = self.tree.item(selected_item)
            values = item_data['values']
            print(f"Registro seleccionado: {values}")
            self.edit_button.config(state=tk.NORMAL) # Habilitar boton de edición.
    
    def load_pdfs(self):
        # Abrir diálogo para seleccionar múltiples archivos PDF
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos PDF Formularios Registro Operadora", "*.pdf")])
        if file_paths:
            # Limpiar la tabla actual
            self.tree.delete(*self.tree.get_children())

            self.pdf_paths = file_paths
            iid_pdf = 0 
            for file_path in file_paths:
                pdf_name = os.path.basename(file_path)
                self.tree.insert("", tk.END, iid=iid_pdf, values=(pdf_name, file_path, "", "SIN PROCESAR"))
                iid_pdf += 1
            self.load_bd_access_button.config(state=tk.NORMAL) # Habilitamos el siguiente botón
            self.load_button.config(state=tk.DISABLED)



    def get_pdf_data(self):
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
        id_pdf = -1
        for row in children:
            id_pdf = id_pdf+1
            new_estado = Status.PROCESANDO.value
            pdf_path = self.tree.item(row, "values")[1]
            pdf_name = self.tree.item(row, "values")[0]
            self.log(f"Obteniendo datos del documento {pdf_name}")
            self.tree.item(row, values=(pdf_name, pdf_path,'', new_estado)) # Actualizar estado en la tabla.
            controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
            result: ResultadoProcesamiento = controladoraREC.get_pdf_data(pdf_path, db, self.log)
            if result.pdf_processing_status is PDFProcessingStatus.LOAD_PDF_OK:
                new_estado = Status.LECTURA_PDF_OK.value
            elif result.pdf_processing_status is PDFProcessingStatus.OPERATOR_EXISTS:
                new_estado = Status.LECTURA_PDF_OK_OPERADOR_EXISTE.value
            elif result.pdf_processing_status is PDFProcessingStatus.MISSING_OPERATOR_INFO:
                new_estado = Status.ERROR_PDF_NO_VALIDO.value

            self.tree.item(row, values=(
                pdf_name, 
                pdf_path, 
                result.operador.razon_social if result.operador else " - ",
                new_estado, 
                id_pdf
            ))
            self.dic_datos_pdf[id_pdf] = result # Agregamos al diccionario con el id como clave. 
        # Gestión del estado de los botones.
        self.get_pdf_data_button.config(state=tk.DISABLED)
        self.process_button.config(state=tk.NORMAL)
      
    def edit_selected_record(self):
        selected_item = self.tree.selection()
        if selected_item and len(self.dic_datos_pdf) >0:
            item_data = self.tree.item(selected_item)
            id_pdf_selected = item_data['values'][4]
            operador: Operador = self.dic_datos_pdf[id_pdf_selected].operador
            representante_firma : Usuario_Operador= self.dic_datos_pdf[id_pdf_selected].representante_firma
            representantes : List[Usuario_Operador] = self.dic_datos_pdf[id_pdf_selected].representantes


            if operador is None or len(representantes) == 0:
                messagebox.showinfo("PDF no valido", "El PDF no cumple el formato o no dispone de datos suficientes para ser editado.")
                return


            # Llama a la función editar_operador y pasa el objeto operador
            resultado = editar_operador(self.root, operador,representante_firma, representantes)
            if resultado[0] is not None and resultado[1] is not None:
                operador, representantes = resultado
                self.dic_datos_pdf[id_pdf_selected].operador = operador
                self.dic_datos_pdf[id_pdf_selected].representantes = representantes
                self.dic_datos_pdf[id_pdf_selected].representante_firma = representante_firma
            else:
                # No se hace nada, se canceló la edición
                print("Edición cancelada")

        else:
            if not selected_item:
                messagebox.showinfo("Sin selección", "No se ha seleccionado ningún registro")
                return
            if len(self.dic_datos_pdf) == 0:
                messagebox.showinfo("Sin procesar", "Es necesario obtener los datos del PDF para poder editarlos")


        
    def process_save_data_of_pdfs(self):
        # root = tk.Tk()
        db = Database(self.db_path)

        ###################################
        # 1º Procesar Guardado de datos
        ###################################
        for clave, valor in self.dic_datos_pdf.items():
 
           
            # Obtén los valores actuales de la fila
            item_values = self.tree.item(clave, "values")
            pdf_name = item_values[0]  # Nombre del PDF
            pdf_path = item_values[1]  # Ruta del PDF
            nombre_operadora = item_values[2]  # Nombre de la Operadora
            estado_proceso = item_values[3]  # Estado del Proceso
            # Buscar la palabra "ERROR" en la variable estado_proceso
            if "ERROR" in estado_proceso:
                self.log(f"El {pdf_name} no se procesa por no ser valido.")
                continue

            self.log(f"Procesando {valor.operador.razon_social}")
            controladoraREC = RegistroEmpresaColaboradoraController(pdf_path)
            operador: Operador = self.dic_datos_pdf[clave].operador
            representantes : List[Usuario_Operador] = self.dic_datos_pdf[clave].representantes
            representante_firma : Usuario_Operador = self.dic_datos_pdf[clave].representante_firma
            # Actualización de datos.
            if "OPERADOR YA EXISTE" in estado_proceso:
                self.log("El operador ya existe. ¿Desea continuar con la actualización?")
                #root.withdraw()  # Oculta la ventana principal
                mensaje = (
                f"El operador con CIF {nombre_operadora} ya está registrado en la base de datos. "
                "Si decides continuar, actualizaremos los datos del operador con los nuevos datos. "
                "Si prefieres cancelar, no se procesará el PDF y los datos actuales del operador permanecerán sin cambios. "
                "¿Deseas proceder con la actualización?"
                )
                respuesta = messagebox.askyesno("Confirmar Actualización", mensaje)
                if respuesta:
                    respuesta_actualizacion = controladoraREC.actualizar_datos_operador(operador, representantes, representante_firma, db, self.log)
                    if respuesta_actualizacion:
                        new_estado = Status.DATOS_ACTUALIZADOS.value
                    else:
                        new_estado = Status.ERROR_ACTUALIZAR.value
                else:
                    print(f"Proceso cancelado. Los datos del operador {nombre_operadora} permanecerán sin cambios.")
                    new_estado = "SIN MODIFICAR"
            # Alta de nuevo operador.
            else:
                result = controladoraREC.guardar_datos_registros_pdf(db, operador, representante_firma, representantes, self.log)
                if result.pdf_processing_status == PDFProcessingStatus.SUCCESS:
                    new_estado = Status.OK_GUARDADO.value
                elif result.pdf_processing_status == PDFProcessingStatus.MISSING_OPERATOR_INFO:
                    self.log("No se pudo procesar el PDF porque falta información del operador.")
                    new_estado = Status.ERROR_INSERCION_BD.value
                elif result.pdf_processing_status == PDFProcessingStatus.INSERTION_ERROR:
                    self.log("Ocurrió un error al intentar insertar el operador en la base de datos.")
                    new_estado = Status.ERROR_INSERCION_BD.value
                elif result.pdf_processing_status == PDFProcessingStatus.REPRESENTATIVE_PROCESSING_ERROR:
                    self.log("Ocurrió un error al procesar uno de los representantes.")
                    new_estado = Status.ERROR_PROCESADO_REPRESENTANTES.value
                
            # Actualizar la fila en la tabla
            self.tree.item(clave, values=(pdf_name, pdf_path, nombre_operadora, new_estado, clave))
        # DISABLED Botón para que no se pueda hacer nada mas (proceso finalizado). 
        self.process_button.config(state=tk.DISABLED)
        self.edit_button.config(state=tk.DISABLED)

        
    
    def change_db_access(self):
        # Abrir diálogo para seleccionar archivo BD Access
        self.db_path = filedialog.askopenfilename(filetypes=[("BD Access incorporación de datos", "*.accdb")])
        if self.db_path:  # Si se selecciona un archivo
            # Actualizar el texto del Label con la ruta de la base de datos
            self.db_access_label.config(text=f"BD Access: {self.db_path}")
            self.get_pdf_data_button.config(state=tk.NORMAL) # Habilitamos el siguiente botón
            self.load_bd_access_button.config(state=tk.DISABLED)

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




