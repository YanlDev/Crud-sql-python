from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import sqlite3
import tkinter
from webbrowser import get

#---------------------------------Ventana principal-------------------
root = Tk()
root.title('App BBDD')

#--------------------------------VENTANA CENTRADA
ancho_ventana = 360
alto_ventana = 280

x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2 - 100

posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.resizable(0,0)
#------------Mensajes box--------------------------------
#Funcion Salir
def salir_app():
    # messagebox.askyesno(message="¿Desea salir?", title= "Salir")
    salir =messagebox.askyesno(message="¿Desea salir?", title= "Salir")
    if salir :
        root.destroy()

#=========================BASE DE DATOS CREACION++++++++++++++++++++++
# miConexion = sqlite3.connect("Usuarios")
# miCursor = miConexion.cursor()
def crear_BD():
    miConexion = sqlite3.connect("Usuarios") 
    miCursor = miConexion.cursor() 
    try:
        miCursor.execute('''CREATE TABLE DATOS_USUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR (50),
            APELLIDO VARCHAR (50),
            PASSWORD VARCHAR (50),
            DIRECCION VARCHAR (50),
            COMENTARIOS VARCHAR (100))''')
        miConexion.commit()
        miConexion.close() 
        messagebox.showinfo("App BBDD","Base de datos creada 'Correctamente'")
    except sqlite3.OperationalError: 
        messagebox.showwarning("Error", "La BBDD ya existe ")
# CREAR USUARIO EN LA BBDD        
def crear_user():
    miConexion = sqlite3.connect("Usuarios") 
    miCursor = miConexion.cursor() 
    
    miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL,'"+entry_name.get()+"','"+entry_lname.get()+"','"+entry_pass.get()+"','"+entry_direc.get()+"','"+texto_comentario.get("1.0",tkinter.END)+"')")
    miConexion.commit()
    miConexion.close()    
    messagebox.showinfo("App BBDD","Registro existoso")
    borrar_todo()
#LEER USER MEDIANTE ID
def leer_usuarios():
    miConexion = sqlite3.connect("Usuarios") 
    miCursor = miConexion.cursor()     
    
    miCursor.execute("SELECT * FROM DATOS_USUARIOS WHERE ID ='"+entry_id.get()+"'")
    lista_de_datos = miCursor.fetchall()
    
    for i in lista_de_datos:
        entry_id.delete(0,END)
        entry_id.insert(0,i[0])
        entry_name.insert(0,i[1])
        entry_lname.insert(0,i[2])
        entry_pass.insert(0,i[3])
        entry_direc.insert(0,i[4])
        texto_comentario.insert(1.0,i[5])
        
    miConexion.commit()
    miConexion.close()    

#UPDATE USERS
def modifica_users():
    miConexion = sqlite3.connect("Usuarios") 
    miCursor = miConexion.cursor() 
    miCursor.execute("UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO = '"+entry_name.get()+"', APELLIDO = '"+entry_lname.get()+"', PASSWORD = '"+entry_pass.get()+"', DIRECCION = '"+entry_direc.get()+"', COMENTARIOS = '"+texto_comentario.get("1.0",tkinter.END)+"'  WHERE ID = '"+entry_id.get()+"'")     
    miConexion.commit()
    miConexion.close() 
    messagebox.showinfo("App BBDD","Se cambiaron los datos de manera existosa")
    borrar_todo()
 
 #DELETE USERS
def borrar_users():
    miConexion = sqlite3.connect("Usuarios") 
    miCursor = miConexion.cursor()     
    miCursor.execute("DELETE FROM DATOS_USUARIOS WHERE ID = '"+entry_id.get()+"'")
    miConexion.commit()
    miConexion.close() 
    messagebox.showinfo("App BBDD","Se borro el ID: '"+entry_id.get()+"' de manera  existosa")
    borrar_todo()
    
#BORRAR CAMPOS
def borrar_todo():
    entry_id.delete(0,END)
    entry_name.delete(0,END)
    entry_lname.delete(0,END)
    entry_pass.delete(0,END)
    entry_direc.delete(0,END)
    texto_comentario.delete("1.0",tkinter.END)
    
#----------------------------------MENU-------------------

barraMenu = Menu(root) #iniciando el menu
root.config(menu=barraMenu) #menu construido

menu_bbdd=Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="BBDD", menu= menu_bbdd)
menu_bbdd.add_command(  #Pestañas
    label='Conectar',
    command= crear_BD
)
menu_bbdd.add_command(
    label='Salir',
    command= salir_app
)

menu_borrar=Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="Borrar", menu= menu_borrar)
menu_borrar.add_command(
    label='Borrar Campos' , command= borrar_todo
)

menu_crud=Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="CRUD", menu= menu_crud)
menu_crud.add_command(
    label='Create', command= crear_user)
menu_crud.add_command(
    label='Read', command= leer_usuarios)
menu_crud.add_command(
    label='Update', command= modifica_users)
menu_crud.add_command(
    label='Delete', command= borrar_users)

menu_ayuda=Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="Ayuda", menu= menu_ayuda)
menu_ayuda.add_command(
    label='Licencia')
menu_ayuda.add_command(
    label='Acerca de...')

#=----------- STILOS PARA LOS TTK-----------------------
estilo_boton = ttk.Style()
estilo_boton.configure('boton_style.TButton', font = 'Helveltica 10 bold')

estilo_label = ttk.Style()
estilo_label.configure('label_style.TLabel',font = 'Helveltica 10 bold')

estilo_entry = ttk.Style()
estilo_entry.configure('entry.style.TEntry', foreground="#212F6F")

#-------------------FRAME INTERNO-----------------------
miframe = ttk.Frame(root)
miframe.grid(row=0,column=0)

#-------------------LABELS-----------------------------
label_id = ttk.Label(miframe, text=" ID:", style='label_style.TLabel')
label_id.grid(row=0, column= 0)

label_name = ttk.Label(miframe, text=" Nombre:",style='label_style.TLabel')
label_name.grid(row=1, column= 0)

label_lname = ttk.Label(miframe, text=" Apellido:",style='label_style.TLabel')
label_lname.grid(row=2, column= 0)

label_pass = ttk.Label(miframe, text=" Password:",style='label_style.TLabel')
label_pass.grid(row=3, column= 0)

label_direc = ttk.Label(miframe, text=" Dirección:",style='label_style.TLabel')
label_direc.grid(row=4, column= 0)

label_comment = ttk.Label(miframe, text=" Comentarios:",style='label_style.TLabel')
label_comment.grid(row=5, column= 0)

#Valores Entrys
id_var = StringVar()
name_var = StringVar()
lname_var = StringVar()
pass_var = StringVar()
direc_var = StringVar()

#-----------------ENTRYS------------------------------
entry_id = ttk.Entry(miframe, style= 'entry.style.TEntry',textvariable= id_var)
entry_id.grid(row=0,column=2, columnspan=3,padx= 5, pady = 5)


entry_name = ttk.Entry(miframe, style= 'entry.style.TEntry',textvariable= name_var)
entry_name.grid(row=1,column=2, columnspan=3,padx= 5, pady = 5)

entry_lname = ttk.Entry(miframe, style= 'entry.style.TEntry',textvariable= lname_var)
entry_lname.grid(row=2,column=2, columnspan=3,padx= 5, pady = 5)

entry_pass = ttk.Entry(miframe, style= 'entry.style.TEntry',textvariable= pass_var)
entry_pass.grid(row=3,column=2, columnspan=3,padx= 5, pady = 5)

entry_direc = ttk.Entry(miframe, style= 'entry.style.TEntry',textvariable= direc_var)
entry_direc.grid(row=4,column=2, columnspan=3,padx= 5, pady = 5)

#----------ENTRY GRANDE CON SCROLLBAR------------------
texto_comentario = scrolledtext.ScrolledText(miframe,height=5,width=20)
texto_comentario.grid(row=5, column=2, columnspan=2,padx= 5, pady = 5)


#------------------BOTONES------------------------------
boton_create= ttk.Button(miframe, text="Create", command= crear_user)
boton_create.grid(row=6, column=0, padx= 2, pady = 2)
boton_read= ttk.Button(miframe, text="Read", command= leer_usuarios)
boton_read.grid(row=6, column=1, padx= 2, pady = 2)
boton_update= ttk.Button(miframe, text="Update", command= modifica_users)
boton_update.grid(row=6, column=2, padx= 2, pady = 2)
boton_delete= ttk.Button(miframe, text="Delete", command= borrar_users)
boton_delete.grid(row=6, column=3, padx= 2, pady = 2)







root.mainloop()