
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter.ttk import Notebook, Combobox

from models import GestorUsuarios, GestorTecnicos, GestorTickets
from utils import cadena_no_vacia_tk, validar_email

gestor_usuarios=GestorUsuarios()
gestor_tecnicos=GestorTecnicos()
gestor_usuarios.cargar_usuarios_json()
gestor_tecnicos.cargar_json_tecnicos()
gestor_tickets=GestorTickets(gestor_usuarios, gestor_tecnicos)
gestor_tickets.cargar_json()


def refresh_treeview():
    for fila in tabla_usuarios.get_children():
        tabla_usuarios.delete(fila)
    for usuario in gestor_usuarios.lista_usuarios:
        tabla_usuarios.insert("","end", values=(usuario.id, usuario.nombre, usuario.email))

    for fila in tabla_tecnicos.get_children():
        tabla_tecnicos.delete(fila)
    for tecnico in gestor_tecnicos.lista_tecnicos:
        tabla_tecnicos.insert("", "end", values=(tecnico.id, tecnico.nombre, tecnico.especialidad))

    valores=[f"{u.id}-{u.nombre}" for u in gestor_usuarios.lista_usuarios]
    combobox_ticket["values"]=valores


def refresh_treeview_tickets():
    for fila in tabla_tickets_creacion.get_children():
        tabla_tickets_creacion.delete(fila)
    for t in gestor_tickets.lista_tickets:
        user=gestor_usuarios.buscar_usuario(t.id_usuario)
        nombre_usuario=user.nombre if user else "Usuario no encontrado."
        tec=gestor_tecnicos.buscar_tecnico(t.id_tecnico) if t.id_tecnico is not None else None
        nombre_tecnico=tec.nombre if tec else "Sin asignar."
        tabla_tickets_creacion.insert("", "end", values=(t.id, nombre_usuario, t.prioridad, t.estado, nombre_tecnico, t.descripcion))

def refresh_treeview_tickets_gestion():
    for fila in tabla_tickets_gestion.get_children():
        tabla_tickets_gestion.delete(fila)
    for t in gestor_tickets.lista_tickets:
        user = gestor_usuarios.buscar_usuario(t.id_usuario)
        nombre_usuario = user.nombre if user else "Usuario no encontrado."
        tec = gestor_tecnicos.buscar_tecnico(t.id_tecnico) if t.id_tecnico is not None else None
        nombre_tecnico = tec.nombre if tec else "Sin asignar."
        tabla_tickets_gestion.insert("", "end", values=(t.id, nombre_usuario, t.prioridad, t.estado, nombre_tecnico, t.descripcion))



def crear_usuario_callback():
    nombre=entry_nombre.get().strip()
    email=entry_email.get().strip()

    try:
        cadena_no_vacia_tk(nombre)
        cadena_no_vacia_tk(email)
        validar_email(email)

        for u in gestor_usuarios.lista_usuarios :
            if u.email==email:
                messagebox.showerror("Error", f"Ya fue registrado un usuario con el email: {email}")
                return


        nuevo_usuario=gestor_usuarios.crear_usuario(nombre, email)

        if not nuevo_usuario:
            messagebox.showerror("Error", "No se pudo crear el usuario")
            return

        messagebox.showinfo("Exito", f"Usuario: '{nombre}' fue añadido correctamente.")
        gestor_usuarios.guardar_usuarios_json()

        entry_nombre.delete(0, END)
        entry_email.delete(0, END)
        refresh_treeview()
    except ValueError as e:
        messagebox.showerror("Error de validacion", str(e))

def eliminar_usuario_callback():
    seleccion = tabla_usuarios.selection()
    if not seleccion:
        messagebox.showwarning("Atencion","Debes seleccionar primero a un usuario para eliminar")
        return

    item=seleccion[0]
    valores=tabla_usuarios.item(item, "values")
    id_usuario=valores[0]

    try:
        id_usuario=int(valores[0])
    except (IndexError, ValueError):
        messagebox.showerror("Error", "ID de usuario no valido")


    confirmar=messagebox.askyesno(
        "Confirmar, seleccion",
        f"Estas seguro de eliminar al usuario con ID: '{id_usuario}'?"
    )

    if confirmar:
        eliminar=gestor_usuarios.eliminar_usuario(id_usuario)
        if eliminar:
            messagebox.showinfo("Completado", f"Usuario con ID: '{id_usuario}' fue eliminado correctamente.")
            gestor_usuarios.guardar_usuarios_json()
            refresh_treeview()
        else:
            messagebox.showerror("Error", "No se pudo eliminar este usuario.")

def buscar_usuario_callback():

    filtrados = []
    buscar_nombre=entry_nombre.get()
    buscar_email=entry_email.get()
    if buscar_email or buscar_nombre:

        for u in gestor_usuarios.lista_usuarios:
            if (buscar_nombre and buscar_nombre in u.nombre) or (buscar_email and buscar_email in u.email):
                filtrados.append(u)

        for fila in tabla_usuarios.get_children():
            tabla_usuarios.delete(fila)

        for u in filtrados:
            tabla_usuarios.insert("", "end", values=(u.id, u.nombre, u.email))

    if not filtrados:
        messagebox.showinfo("Sin resultados", "No se encontraron usuarios con ese criterio")

    if not buscar_nombre and not  buscar_email:
        messagebox.showerror("Error", "Debes de llenar al menos un campo (Nombre/Email)")
        refresh_treeview()
        return


def crear_tecnico_callback():
    nombre=entry_nombre_t.get().strip()
    especialidad=entry_especialidad.get().strip()

    try:
        cadena_no_vacia_tk(nombre)
        cadena_no_vacia_tk(especialidad)

        if any(t.nombre==nombre for t in gestor_tecnicos.lista_tecnicos):
            messagebox.showerror("Error", f"Ya fue registrado un tecnico con el nombre: {nombre}")
            return

        nuevo_tecnico=gestor_tecnicos.crear_tecnico(nombre, especialidad)

        if not nuevo_tecnico:
            messagebox.showerror("Error", "No se pudo crear el tecnico")
            return



        messagebox.showinfo("Exito", f"Tecnico: '{nombre}' fue añadido correctamente.")
        gestor_tecnicos.guardar_json_tecnicos()

        entry_nombre_t.delete(0, END)
        entry_especialidad.delete(0, END)
        refresh_treeview()
    except ValueError as e:
        messagebox.showerror("Error de validacion", str(e))

def eliminar_tecnico_callback():
    seleccion = tabla_tecnicos.selection()
    if not seleccion:
        messagebox.showwarning("Atencion","Debes seleccionar primero a un usuario para eliminar")
        return

    item=seleccion[0]
    valores=tabla_tecnicos.item(item, "values")
    id_tecnico=valores[0]

    try:
        id_tecnico=int(valores[0])
    except (IndexError, ValueError):
        messagebox.showerror("Error", "ID de Tecnico no valido")


    confirmar=messagebox.askyesno(
        "Confirmar, seleccion",
        f"Estas seguro de eliminar al tecnico con ID: '{id_tecnico}'?"
    )

    if confirmar:
        eliminar=gestor_tecnicos.eliminar_tecnico(id_tecnico)
        if eliminar:
            messagebox.showinfo("Completado", f"Tecnico con ID: '{id_tecnico}' fue eliminado correctamente.")
            gestor_tecnicos.guardar_json_tecnicos()
            refresh_treeview()
        else:
            messagebox.showerror("Error", "No se pudo eliminar este Tecnico.")

def buscar_tecnico_callback():
    buscar=entry_nombre_t.get()
    filtrados=[]

    for t in gestor_tecnicos.lista_tecnicos:
        if buscar in t.nombre:
            filtrados.append(t)

    if filtrados:
        for fila in tabla_tecnicos.get_children():
            tabla_tecnicos.delete(fila)
        for t in filtrados:
            tabla_tecnicos.insert("", "end", values=(t.id, t.nombre, t.especialidad))
    else:
        messagebox.showinfo("Sin resultados", "No se hallaron coincidencias")

def asignar_tecnico_callback():
    seleccion=tabla_tickets_gestion.selection()
    if not seleccion:
        messagebox.showwarning("Atencion", "Debes seleccionar un ticket.")
        return
    item= seleccion[0]
    valores=tabla_tickets_gestion.item(item, "values")
    id_ticket=int(valores[0])

    ventana_asignar=Toplevel(root)
    ventana_asignar.resizable(False, False)
    ventana_asignar.title("Asignar Tecnico")
    ventana_asignar.geometry("300x200")
    ventana_asignar.grab_set()

    Label(ventana_asignar, text=f"Ticket ID: {id_ticket}", font="bold").pack(pady=10)

    Label(ventana_asignar, text=f"Selecciona un tecnico: ").pack(pady=5)
    tecnicos_disponibles=[f"{t.id} - {t.nombre}" for t in gestor_tecnicos.lista_tecnicos]
    combobox_tecnicos=Combobox(ventana_asignar, values=tecnicos_disponibles, width=25)
    combobox_tecnicos.pack(pady=5)

    def confirmar_asignacion():
        valor=combobox_tecnicos.get()
        if not valor:
            messagebox.showerror("Error", "Debes seleccionar un tecnico.")
            return

        id_tecnico=int(valor.split("-")[0].strip())

        asignado=gestor_tickets.asignar_tecnico(id_ticket, id_tecnico)
        if asignado:
            messagebox.showinfo("Exito", f"Se asigno al tecnico {id_tecnico} al ticket {id_ticket}")
            gestor_tickets.guardar_json()
            refresh_treeview_tickets()
            ventana_asignar.destroy()

        else:
            messagebox.showerror("Error", "No se pudo asignar el tecnico")
    Button(ventana_asignar, text="Aceptar", command=confirmar_asignacion).pack(pady=20)

def cambiar_prioridad_callback():
    ticket_selecionado=tabla_tickets_gestion.selection()
    if not ticket_selecionado:
        messagebox.showwarning("Atencion", "Debes seleccionar un ticket primero.")
        return
    ticket=ticket_selecionado[0]
    valores=tabla_tickets_gestion.item(ticket, "values")
    id_ticket=int(valores[0])
    prioridad_actual=valores[2]

    ventana_prioridades = Toplevel(root)
    ventana_prioridades.resizable(False, False)
    ventana_prioridades.grab_set()
    Label(ventana_prioridades, text="Nueva prioridad del ticket: ", font="bold").grid(row=0, padx=10, pady=30)
    combobox_prioridades = Combobox(ventana_prioridades, values=["alta", "media", "baja"], width=30)
    combobox_prioridades.grid(row=1, padx=20, pady=20)

    def confirmar_prioridad():
        prioridad_seleccionada=combobox_prioridades.get()
        if not prioridad_seleccionada:
            messagebox.showwarning("Atencion", "Debes seleccionar una nueva prioridad.")
            return

        if prioridad_seleccionada==prioridad_actual:
            messagebox.showinfo("Sin cambios", "La prioridad seleccionada es la misma que la actual.")
            return

        confirmado=messagebox.askyesno(
            "Confirmar Cambio",
            f"Deseas cambiar la prioridad del ticket:{id_ticket} a {prioridad_seleccionada}?"
        )

        if not confirmado:
            return

        modificado=gestor_tickets.cambiar_prioridad(id_ticket, prioridad_seleccionada)
        if modificado:
            messagebox.showinfo("Completado", f"Se modifico la prioridad del ticket {id_ticket}")
            gestor_tickets.guardar_json()
            ventana_prioridades.destroy()
        else:
            messagebox.showerror("Error", "No se pudo modificar la prioridad.")
        refresh_treeview()
        refresh_treeview_tickets()
        refresh_treeview_tickets_gestion()

    Button(ventana_prioridades, text="Aceptar", command=confirmar_prioridad).grid(row=3, pady=3)

def cambiar_estado_callback():
    ticket_seleccionado=tabla_tickets_gestion.selection()
    if not ticket_seleccionado:
        messagebox.showwarning("Atencion", "Debes seleccionar un ticket.")
        return

    ticket=ticket_seleccionado[0]
    valores=tabla_tickets_gestion.item(ticket, "values")
    id_ticket=int(valores[0])
    estado_actual=valores[3]

    confirmar=messagebox.askyesno(
        "Confirmar cambio de estado",
        f"Deseas cambiar el estado actual del ticket:{id_ticket}?"
    )

    if not confirmar:
        return

    estado_cambiado = gestor_tickets.cambiar_estado(id_ticket)
    if estado_cambiado:
        messagebox.showinfo("Completado", f"Se modifico el estado del ticket: {id_ticket}")
        gestor_tickets.guardar_json()
        refresh_treeview()
        refresh_treeview_tickets()
        refresh_treeview_tickets_gestion()
    else:
        messagebox.showerror("Error", "No se pudo realizar el cambio de estado.")

def buscar_ticket_callback():
    id_ticket=entry_id_ticket.get()

    if not  id_ticket:
        refresh_treeview_tickets_gestion()
        return

    try:
        valor=int(id_ticket)
    except ValueError:
        messagebox.showerror("Error", "El ID consta unicamente de numeros.")
        return

    id_ticket=int(id_ticket)
    ticket_encontrado=gestor_tickets.buscar_ticket(id_ticket)
    if not ticket_encontrado:
        messagebox.showerror("Error", f"No se encontro ningun ticket con ID: {id_ticket}")
        return

    for fila in tabla_tickets_gestion.get_children():
        tabla_tickets_gestion.delete(fila)
    user=gestor_usuarios.buscar_usuario(ticket_encontrado.id_usuario)
    nombre_usuario=user.nombre if user else "Usuario no encontrado"
    tec=gestor_tecnicos.buscar_tecnico(ticket_encontrado.id_tecnico)
    nombre_tecnico=tec.nombre if tec else "Sin asignar"

    tabla_tickets_gestion.insert(
        "",
        "end",
        values =(
            ticket_encontrado.id,
            nombre_usuario,
            ticket_encontrado.prioridad,
            ticket_encontrado.estado,
            nombre_tecnico,
            ticket_encontrado.descripcion


        )
    )

def crear_ticket_callback():
    id_usuario=combobox_ticket.get().strip()
    descripcion=entry_descripcion.get()
    prioridad=combobox_prioridad.get().lower().strip()

    prioridades=["alta", "baja", "media"]

    if not id_usuario or not descripcion or not prioridad:
        messagebox.showerror("Error", "No se permiten campos vacios.")
        return


    try:
        idusuario=int(id_usuario.split("-")[0].strip())
    except ValueError:
        messagebox.showerror("Error", "Formato de ID incorrecto.")
        return

    if prioridad not in prioridades:
        messagebox.showerror("Error", "Prioridad no valida")
        return

    id_usuario = int(id_usuario.split("-")[0].strip())

    if id_usuario not in gestor_usuarios.lista_usuarios:
        messagebox.showerror("Error" , "No se encontró un usuario con esa ID")
        return


    gestor_tickets.crear_ticket(id_usuario, descripcion, prioridad)
    messagebox.showinfo("Exito", "Ticket generado exitosamente.")

    entry_descripcion.delete(0, END)
    combobox_ticket.set("")
    combobox_prioridad.set("")
    refresh_treeview_tickets()
    refresh_treeview_tickets_gestion()


root=Tk()
root.title("Sistema Tickets")
root.geometry("700x600")
root.resizable(True, True)

notebook=Notebook(root)
notebook.pack(fill="both", expand=True)



pestania_usuarios=Frame(notebook)
pestania_tecnicos=Frame(notebook)
pestania_tickets=Frame(notebook)
operaciones_tickets=Frame(notebook)

notebook.add(pestania_usuarios, text="USUARIOS")
notebook.add(pestania_tecnicos, text="TECNICOS")
notebook.add(pestania_tickets, text="TICKETS")
notebook.add(operaciones_tickets, text="GESTIONAR TICKETS")
###########################   USUARIOS   ###########################################

frame_sup=Frame(pestania_usuarios, pady=15, padx=10)
frame_sup.pack(fill="x")

frame_inf=Frame(pestania_usuarios, pady=15, padx=10)
frame_inf.pack(fill="both", expand=True)

Label(frame_sup, text="Nombre: ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
Label(frame_sup, text="Email: ").grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_nombre=Entry(frame_sup, width=40)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)
entry_nombre.focus_set()

entry_email=Entry(frame_sup, width=40)
entry_email.grid(row=1, column=1, padx=5, pady=5)

btn_crear=Button(frame_sup, text="Crear Usuario", command=crear_usuario_callback)
btn_crear.grid(row=1, column=3, rowspan=1,padx=10, pady=5)

btn_eliminar=Button(frame_sup, text="Eliminar Usuario", command=eliminar_usuario_callback)
btn_eliminar.grid(row=1, column=4, rowspan=1,padx=10, pady=5)


btn_buscar_usuario=Button(frame_sup, text="Buscar Usuario", command=buscar_usuario_callback)
btn_buscar_usuario.grid(row=1, column=5, rowspan=1, padx=10, pady=5)

columnas=("ID", "Nombre", "Email")
tabla_usuarios=ttk.Treeview(frame_inf, columns=columnas, show="headings")

tabla_usuarios.heading("ID", text="ID")
tabla_usuarios.heading("Nombre", text="Nombre")
tabla_usuarios.heading("Email", text="Email")


tabla_usuarios.column("ID", width=50, anchor="center")
tabla_usuarios.column("Nombre", width=150)
tabla_usuarios.column("Email", width=250)

scroll_y=Scrollbar(frame_inf, orient=VERTICAL, command=tabla_usuarios.yview)
tabla_usuarios.configure(yscrollcommand=scroll_y.set)

tabla_usuarios.pack(side=LEFT, fill=BOTH, expand=True)
scroll_y.pack(side=RIGHT, fill=Y)

###########################   TECNICOS   ###########################################
frame_sup_t=Frame(pestania_tecnicos, pady=15, padx=10)
frame_sup_t.pack(fill="x")

frame_inf_t=Frame(pestania_tecnicos, pady=15, padx=10)
frame_inf_t.pack(fill="both", expand=True)

Label(frame_sup_t, text="Nombre: ").grid(row=0, column=0, padx=5, pady=5, sticky="e")
Label(frame_sup_t, text="Especialidad").grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_nombre_t=Entry(frame_sup_t, width=40)
entry_nombre_t.grid(row=0, column=1, padx=5, pady=5)
entry_nombre_t.focus_set()

entry_especialidad=Entry(frame_sup_t, width=40)
entry_especialidad.grid(row=1, column=1, padx=5, pady=5)

btn_crear=Button(frame_sup_t, text="Crear Tecnico", command=crear_tecnico_callback)
btn_crear.grid(row=1, column=3, rowspan=1, padx=10, pady=5)

btn_eliminar_t=Button(frame_sup_t, text="Eliminar Tecnico", command=eliminar_tecnico_callback)
btn_eliminar_t.grid(row=1, column=4, rowspan=1, padx=10, pady=5)

btn_buscar_tecnico=Button(frame_sup_t, text="Buscar Tecnico", command=buscar_tecnico_callback)
btn_buscar_tecnico.grid(row=1, column=5, rowspan=1, padx=10, pady=5)

columnas_t=("ID", "Nombre", "Especialidad")
tabla_tecnicos=ttk.Treeview(frame_inf_t, columns=columnas_t, show="headings")

tabla_tecnicos.heading("ID", text="ID")
tabla_tecnicos.heading("Nombre", text="Nombre")
tabla_tecnicos.heading("Especialidad", text="Especialidad")

tabla_tecnicos.column("ID", width=50, anchor="center")
tabla_tecnicos.column("Nombre", width=150)
tabla_tecnicos.column("Especialidad", width=300)

scroll_y=Scrollbar(frame_inf_t, orient=VERTICAL, command=tabla_tecnicos.yview)
tabla_tecnicos.configure(yscrollcommand=scroll_y.set)

tabla_tecnicos.pack(side=LEFT, fill=BOTH, expand=True)
scroll_y.pack(side=RIGHT, fill=Y)


###########################   TICKETS   ###########################################
frame_sup_ti=Frame(pestania_tickets, pady=15, padx=10)
frame_sup_ti.pack(fill="x")

frame_inf_ti=Frame(pestania_tickets, pady=15, padx=10)
frame_inf_ti.pack(fill="both", expand=True)

valores=[f"{u.id} - {u.nombre}" for u in gestor_usuarios.lista_usuarios]

Label(frame_sup_ti, text="Usuario: ").grid(row=0, column=0, padx=10, pady=10, sticky="w")
combobox_ticket=Combobox(frame_sup_ti, values=valores, width=20)
combobox_ticket.grid(row=1, column=0, padx=10, pady=10, sticky="w")

Label(frame_sup_ti, text="Descripcion: ").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_descripcion=Entry(frame_sup_ti, width=50)
entry_descripcion.grid(row=2, column=2, padx=10, pady=10)

Label(frame_sup_ti, text="Prioridad: ").grid(row=0, column=2, padx=10, pady=10, sticky="w")
combobox_prioridad=Combobox(frame_sup_ti, values=["alta", "media", "baja"], width=20)
combobox_prioridad.grid(row=1, column=2, padx=10, pady=10, sticky="w")

btn_crear_ticket=Button(frame_sup_ti, text="Crear ticket", command=crear_ticket_callback)
btn_crear_ticket.grid(row=2, column=3, sticky="e")

columnas_ticket=("ID", "Usuario", "Prioridad", "Estado", "Tecnico", "Descripcion")
tabla_tickets_creacion=ttk.Treeview(frame_inf_ti, columns=columnas_ticket, show="headings")

tabla_tickets_creacion.heading("ID", text="ID: ")
tabla_tickets_creacion.heading("Usuario", text="Usuario: ")
tabla_tickets_creacion.heading("Prioridad", text="Prioridad: ")
tabla_tickets_creacion.heading("Estado", text="Estado: ")
tabla_tickets_creacion.heading("Tecnico", text="Tecnico: ")
tabla_tickets_creacion.heading("Descripcion", text="Descripcion: ")

tabla_tickets_creacion.column("ID", width=30, anchor="center")
tabla_tickets_creacion.column("Usuario", width=150)
tabla_tickets_creacion.column("Prioridad", width=50)
tabla_tickets_creacion.column("Estado", width=100)
tabla_tickets_creacion.column("Tecnico", width=100)
tabla_tickets_creacion.column("Descripcion", width=150)

scroll_ticket=Scrollbar(frame_inf_ti, orient=VERTICAL, command=tabla_tickets_creacion.yview)
tabla_tickets_creacion.configure(yscrollcommand=scroll_ticket.set)

tabla_tickets_creacion.pack(side=LEFT, fill=BOTH, expand=True)
scroll_ticket.pack(side=RIGHT, fill=Y)


###########################  GESTIONAR TICKETS   ###########################################
frame_sup_gt=Frame(operaciones_tickets, pady=15, padx=10)
frame_sup_gt.pack(fill="x")

frame_inf_gt=Frame(operaciones_tickets, pady=15, padx=10)
frame_inf_gt.pack(fill="both", expand=True)

valores=[f"{u.id} - {u.nombre}" for u in gestor_usuarios.lista_usuarios]

btn_cambiar_prioridad=Button(frame_sup_gt, text="Cambiar prioridad ", command=cambiar_prioridad_callback)
btn_cambiar_prioridad.grid(row=0, column=0, sticky="w", padx=20, pady=15)

bt_asignar_tecnico=Button(frame_sup_gt, text="Asignar tecnico ", command=asignar_tecnico_callback)
bt_asignar_tecnico.grid(row=0, column=2, sticky="w", padx=20, pady=15)

btn_cambiar_estado=Button(frame_sup_gt, text="Cambiar estado ", command=cambiar_estado_callback)
btn_cambiar_estado.grid(row=0, column=4, sticky="e", padx=20, pady=15)


entry_id_ticket=Entry(frame_sup_gt)
entry_id_ticket.grid(row=1, column=0, sticky="w", padx=20, pady=15)

btn_buscar_ticket=Button(frame_sup_gt, text="Buscar Ticket por ID", command=buscar_ticket_callback)
btn_buscar_ticket.grid(row=1, column=2, sticky="e", padx=20, pady=15)


columnas_ticket=("ID", "Usuario", "Prioridad", "Estado", "Tecnico", "Descripcion")
tabla_tickets_gestion=ttk.Treeview(frame_inf_gt, columns=columnas_ticket, show="headings")

tabla_tickets_gestion.heading("ID", text="ID: ")
tabla_tickets_gestion.heading("Usuario", text="Usuario: ")
tabla_tickets_gestion.heading("Prioridad", text="Prioridad: ")
tabla_tickets_gestion.heading("Estado", text="Estado: ")
tabla_tickets_gestion.heading("Tecnico", text="Tecnico: ")
tabla_tickets_gestion.heading("Descripcion", text="Descripcion: ")

tabla_tickets_gestion.column("ID", width=30, anchor="center")
tabla_tickets_gestion.column("Usuario", width=150)
tabla_tickets_gestion.column("Prioridad", width=50)
tabla_tickets_gestion.column("Estado", width=100)
tabla_tickets_gestion.column("Tecnico", width=100)
tabla_tickets_gestion.column("Descripcion", width=150)

tecnicos=[t.nombre for t in gestor_tecnicos.lista_tecnicos]

scroll_ticket=Scrollbar(frame_inf_gt, orient=VERTICAL, command=tabla_tickets_gestion.yview)
tabla_tickets_gestion.configure(yscrollcommand=scroll_ticket.set)


tabla_tickets_gestion.pack(side=LEFT, fill=BOTH, expand=True)
scroll_ticket.pack(side=RIGHT, fill=Y)


refresh_treeview()
refresh_treeview_tickets()
refresh_treeview_tickets_gestion()
root.mainloop()

