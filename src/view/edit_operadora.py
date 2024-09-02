import tkinter as tk
from tkinter import ttk
from models.operador_model import Operador  
from models.usuario_operador_model import Usuario_Operador

def editar_operador(root, operador, representante_firma, representantes):
    """
    Función para abrir una ventana de edición para un objeto Operador y sus Representantes.

    :param root: La ventana principal de la aplicación (o el padre de la nueva ventana).
    :param operador: El objeto Operador a editar.
    :param representantes: Una lista de objetos Representante a editar.
    """
    # Crear la nueva ventana
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Operador")
    edit_window.geometry("1200x600")

    # Crear el Notebook (con tabs)
    notebook = ttk.Notebook(edit_window)
    notebook.pack(expand=True, fill="both")

    # Tab 1: Datos del Operador
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Datos Operador")

    # Crear un frame interno para alinear todo a la izquierda
    frame_tab1 = tk.Frame(tab1)
    frame_tab1.pack(fill="both", expand=True, padx=10, pady=10)

    # Campos de entrada para los datos del operador en Tab 1
    tk.Label(frame_tab1, text="NIF Operador:").grid(row=0, column=0, sticky="w", pady=5)
    nif_entry = tk.Entry(frame_tab1)
    nif_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    nif_entry.insert(0, operador.nif_operador)

    tk.Label(frame_tab1, text="Razón Social:").grid(row=1, column=0, sticky="w", pady=5)
    razon_entry = tk.Entry(frame_tab1)
    razon_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    razon_entry.insert(0, operador.razon_social)

    # Campo "Cobertura Fija"
    tk.Label(frame_tab1, text="Cobertura Fija:").grid(row=2, column=0, sticky="w", pady=5)
    cob_fija_var = tk.BooleanVar(value=operador.cob_fija if operador.cob_fija is not None else False)
    cob_fija_checkbutton = tk.Checkbutton(frame_tab1, variable=cob_fija_var)
    cob_fija_checkbutton.grid(row=2, column=1, sticky="w", pady=5, padx=5)

    # Campo "Cobertura FWA"
    tk.Label(frame_tab1, text="Cobertura FWA:").grid(row=3, column=0, sticky="w", pady=5)
    cob_fwa_var = tk.BooleanVar(value=operador.cob_fwa if operador.cob_fwa is not None else False)
    cob_fwa_checkbutton = tk.Checkbutton(frame_tab1, variable=cob_fwa_var)
    cob_fwa_checkbutton.grid(row=3, column=1, sticky="w", pady=5, padx=5)

    # Campo "Cobertura Móvil"
    tk.Label(frame_tab1, text="Cobertura Móvil:").grid(row=4, column=0, sticky="w", pady=5)
    cob_movil_var = tk.BooleanVar(value=operador.cob_movil if operador.cob_movil is not None else False)
    cob_movil_checkbutton = tk.Checkbutton(frame_tab1, variable=cob_movil_var)
    cob_movil_checkbutton.grid(row=4, column=1, sticky="w", pady=5, padx=5)

    # Campo "Grupo Operador"
    tk.Label(frame_tab1, text="Grupo Operador:").grid(row=5, column=0, sticky="w", pady=5)
    grupo_operador_entry = tk.Entry(frame_tab1)
    grupo_operador_entry.grid(row=5, column=1, sticky="ew", pady=5, padx=5)
    grupo_operador_value = operador.grupo_operador if operador.grupo_operador is not None else ""
    grupo_operador_entry.insert(0, grupo_operador_value)

    # Campo "Email"
    tk.Label(frame_tab1, text="Email:").grid(row=6, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(frame_tab1)
    email_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
    email_value = operador.email_notificacion if operador.email_notificacion is not None else ""
    email_entry.insert(0, email_value)

    # Línea divisoria
    separator = ttk.Separator(frame_tab1, orient="horizontal")
    separator.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

    # Etiqueta "Datos del firmante (Representante legal)"
    tk.Label(frame_tab1, text="Datos del firmante (Representante Legal):").grid(row=8, column=0, sticky="w", pady=5, columnspan=2)

    # Campos de entrada para los datos del firmante
    tk.Label(frame_tab1, text="Nombre:").grid(row=9, column=0, sticky="w", pady=5)
    nombre_firmante_entry = tk.Entry(frame_tab1)
    nombre_firmante_entry.grid(row=9, column=1, sticky="ew", pady=5, padx=5)
    nombre_firmante_entry.insert(0, representante_firma.nombre)

    tk.Label(frame_tab1, text="Apellido 1:").grid(row=10, column=0, sticky="w", pady=5)
    apellido1_firmante_entry = tk.Entry(frame_tab1)
    apellido1_firmante_entry.grid(row=10, column=1, sticky="ew", pady=5, padx=5)
    apellido1_firmante_entry.insert(0, representante_firma.apellido1)

    tk.Label(frame_tab1, text="Apellido 2:").grid(row=11, column=0, sticky="w", pady=5)
    apellido2_firmante_entry = tk.Entry(frame_tab1)
    apellido2_firmante_entry.grid(row=11, column=1, sticky="ew", pady=5, padx=5)
    apellido2_firmante_entry.insert(0, representante_firma.apellido2)

    tk.Label(frame_tab1, text="NIF:").grid(row=12, column=0, sticky="w", pady=5)
    nif_firmante_entry = tk.Entry(frame_tab1)
    nif_firmante_entry.grid(row=12, column=1, sticky="ew", pady=5, padx=5)
    nif_firmante_entry.insert(0, representante_firma.nif)

    tk.Label(frame_tab1, text="Email:").grid(row=13, column=0, sticky="w", pady=5)
    email_firmante_entry = tk.Entry(frame_tab1)
    email_firmante_entry.grid(row=13, column=1, sticky="ew", pady=5, padx=5)
    email_firmante_entry.insert(0, representante_firma.email)

    tk.Label(frame_tab1, text="Teléfono:").grid(row=14, column=0, sticky="w", pady=5)
    telefono_firmante_entry = tk.Entry(frame_tab1)
    telefono_firmante_entry.grid(row=14, column=1, sticky="ew", pady=5, padx=5)
    telefono_firmante_entry.insert(0, representante_firma.telefono)

    # Expande los campos de entrada cuando se redimensione la ventana
    frame_tab1.columnconfigure(1, weight=1)



    # Crear la segunda pestaña para los representantes
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Representantes")

    # Crear la tabla (Treeview) en Tab 2 para los representantes
    representantes_tree = ttk.Treeview(tab2, columns=("NOMBRE", "APELLIDO_1", "APELLIDO_2", "NIF", "EMAIL", "TELEFONO"), show="headings")
    representantes_tree.heading("NOMBRE", text="Nombre")
    representantes_tree.heading("APELLIDO_1", text="Apellido 1")
    representantes_tree.heading("APELLIDO_2", text="Apellido 2")
    representantes_tree.heading("NIF", text="NIF")
    representantes_tree.heading("EMAIL", text="Email")
    representantes_tree.heading("TELEFONO", text="Teléfono")
    representantes_tree.pack(expand=True, fill="both", pady=5)

    # Llenar la tabla con los representantes actuales
    for rep in representantes:
        representantes_tree.insert("", "end", values=(rep.nombre, rep.apellido1, rep.apellido2, rep.nif, rep.email, rep.telefono))

    # Crear un frame debajo de la tabla para los inputs de edición
    edit_frame = tk.Frame(tab2)
    edit_frame.pack(fill="x", pady=10)

    # Labels y Entries para editar el representante seleccionado
    tk.Label(edit_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    nombre_entry = tk.Entry(edit_frame)
    nombre_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(edit_frame, text="Apellido 1:").grid(row=0, column=2, padx=5, pady=5)
    apellido1_entry = tk.Entry(edit_frame)
    apellido1_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(edit_frame, text="Apellido 2:").grid(row=0, column=4, padx=5, pady=5)
    apellido2_entry = tk.Entry(edit_frame)
    apellido2_entry.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(edit_frame, text="NIF:").grid(row=1, column=0, padx=5, pady=5)
    nif_entry_rep = tk.Entry(edit_frame)
    nif_entry_rep.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(edit_frame, text="Email:").grid(row=1, column=2, padx=5, pady=5)
    email_entry_rep = tk.Entry(edit_frame)
    email_entry_rep.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(edit_frame, text="Teléfono:").grid(row=1, column=4, padx=5, pady=5)
    telefono_entry_rep = tk.Entry(edit_frame)
    telefono_entry_rep.grid(row=1, column=5, padx=5, pady=5)

    # Función para manejar la selección en la tabla y cargar los datos en los inputs
    def on_tree_select(event):
        selected_item = representantes_tree.selection()
        if selected_item:
            item_values = representantes_tree.item(selected_item[0], "values")
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(0, item_values[0])
            apellido1_entry.delete(0, tk.END)
            apellido1_entry.insert(0, item_values[1])
            apellido2_entry.delete(0, tk.END)
            apellido2_entry.insert(0, item_values[2])
            nif_entry_rep.delete(0, tk.END)
            nif_entry_rep.insert(0, item_values[3])
            email_entry_rep.delete(0, tk.END)
            email_entry_rep.insert(0, item_values[4])
            telefono_entry_rep.delete(0, tk.END)
            telefono_entry_rep.insert(0, item_values[5])

        # Vincula la función al evento KeyRelease de cada Entry:
        nombre_entry.bind("<KeyRelease>", lambda event: update_table())
        apellido1_entry.bind("<KeyRelease>", lambda event: update_table())
        apellido2_entry.bind("<KeyRelease>", lambda event: update_table())
        nif_entry_rep.bind("<KeyRelease>", lambda event: update_table())
        email_entry_rep.bind("<KeyRelease>", lambda event: update_table())
        telefono_entry_rep.bind("<KeyRelease>", lambda event: update_table())

    # Vincular la función a la selección de la tabla
    representantes_tree.bind("<<TreeviewSelect>>", on_tree_select)

    

    # Función para manejar la aceptación de los cambios
    def aceptar():
        # Actualizar los datos del operador
        operador.nif_operador = nif_entry.get()
        operador.razon_social = razon_entry.get()
        operador.cob_fija = cob_fija_var.get()
        operador.cob_fwa = cob_fwa_var.get()
        operador.cob_movil = cob_movil_var.get()
        operador.grupo_operador = grupo_operador_entry.get()
        operador.email_notificacion = email_entry.get()

        representante_firma.nombre = nombre_firmante_entry.get()
        representante_firma.apellido1 = apellido1_firmante_entry.get()
        representante_firma.apellido2 = apellido2_firmante_entry.get()
        representante_firma.nif = nif_firmante_entry.get()
        representante_firma.email = email_firmante_entry.get()
        representante_firma.telefono = telefono_firmante_entry.get()

        # Limpiar la lista de representantes actuales y llenar con los nuevos datos
        representantes.clear()
        for item in representantes_tree.get_children():
            item_values = representantes_tree.item(item, "values")
            nuevo_representante = Usuario_Operador(
                id=0, # Valor desconocido
                nombre=item_values[0],
                apellido1=item_values[1],
                apellido2=item_values[2],
                nif=item_values[3],
                email=item_values[4],
                telefono=item_values[5]
            )
            representantes.append(nuevo_representante)
        
        edit_window.result = True  # Indicamos que se ha aceptado
        edit_window.destroy()

    def update_table():
        selected_item = representantes_tree.selection()
        if selected_item:
            representantes_tree.item(selected_item[0], values=(
                nombre_entry.get(),
                apellido1_entry.get(),
                apellido2_entry.get(),
                nif_entry_rep.get(),
                email_entry_rep.get(),
                telefono_entry_rep.get()
            ))


      

    def cancelar():
        edit_window.result = False  # Indicamos que se ha cancelado
        edit_window.destroy()

   # Botones Aceptar y Cancelar
    button_frame = tk.Frame(edit_window)
    button_frame.pack(pady=20, anchor="e")  # Alinear a la derecha (east)

    aceptar_button = tk.Button(button_frame, text="Aceptar", command=aceptar, bg="#4CAF50", fg="white", padx=20, pady=10)
    aceptar_button.pack(side=tk.LEFT, padx=10)

    cancelar_button = tk.Button(button_frame, text="Cancelar", command=edit_window.destroy, bg="#f44336", fg="white", padx=20, pady=10)
    cancelar_button.pack(side=tk.LEFT, padx=10)

    edit_window.result = None  # Valor inicial
    root.wait_window(edit_window)  # Espera a que la ventana se cierre

    if edit_window.result:
        return operador, representantes
    else:
        return None, None
