from tkinter import messagebox,ttk
from ping3 import ping, verbose_ping
import time
import threading
import tkinter
from tkinter import *
import sqlite3

# AUTOR: PABLO LARA
# EDAD: 20 years old

variable_util = 1

if 1 == variable_util:
    print("Variable util es 1")

def ventana1():
    global v

    v = tkinter.Tk()
    v.geometry("750x500")
    v.state('zoomed')
    v.title("Principal")
    icono=tkinter.PhotoImage(file="flujo-de-senal.png")
    v.iconphoto(True,icono)
    text_label = tkinter.Label(v, text="Pausado",fg="white",font="helvetica 10",bg="red",anchor="w")
    text_label.place(relx=0,rely=0.96,relwidth=0.22,relheight=0.04)

    firma = tkinter.Label(v,text="@PabloLara",font="helvetica 8", anchor="e").place(relx=0.9,rely=0.95,relwidth=0.1,relheight=0.05)

    list_label = []
    def leer_host():
        global list_nombre
        global lista_ip
        try:
            list_nombre = []
            lista_ip = []
            conectada = sqlite3.connect("setting.db")
            c = conectada.cursor()
            c.execute(f""" 
            SELECT 
                * 
            FROM 
                HOST""")
            for i1 in c.fetchall():
                    list_nombre.append(i1[0]) 
                    lista_ip.append(i1[1]) 
    
        except Exception as err:
            messagebox.showinfo(message=f"{err}", title = "NOT FOUND BD")

    def leer_config():
            global cantidad_columna, tiempo_refresco
            try:
                conectada = sqlite3.connect("setting.db")
                c = conectada.cursor()
                c.execute(f""" 
                SELECT 
                    * 
                FROM 
                    CONFIG""")
                for i2 in c.fetchall():
                    tiempo_refresco = i2[0]
                max_cant_cada_cuanto.set(tiempo_refresco)
            except NameError:
                return
            except Exception as err:
                messagebox.showinfo(message=f"{err}", title = "NOT FOUND BD")
        
    #_____________________________________________________________________ Limite de caracteres
    def limitador(max_cant, limit):
        if len(max_cant.get()) > 0:
            #donde esta el :limit la cantidad d caracteres
            max_cant.set(max_cant.get()[:limit])


    v.attributes("-fullscreen", False) 
    v.bind("<F11>", lambda event: v.attributes("-fullscreen", not v.attributes("-fullscreen"))) 
    v.bind("<Escape>", lambda event: v.attributes("-fullscreen", False)) 


    leer_host()
    leer_config()
    def ejecutar_label():    
        global var_label

        contador = 0
        columna = 2
        fila = len(lista_ip) + 1
        c = 0
        posicion_x = 0
        posicion_y = 0.06
        try:
            
                for i2 in range(1,fila):                
                    cont = contador + c
                    var_nombre = list_nombre[cont]
                    var_ip = lista_ip[cont]
                    var_label = var_nombre
                    var_label = tkinter.Label(v, text=f"{var_nombre}\n{var_ip}", bg="white", fg="black", width=20, font="helvetica 10", relief="groove")
                    list_label.append(var_label)
                    var_label.place(relx=posicion_x, rely=posicion_y,relwidth=0.1667,relheight=0.1)
                    c = c+1
                
                    posicion_x = posicion_x + 0.1667
                    if posicion_x == 1.0002:
                        posicion_x = posicion_x - 1.0002
                        posicion_y = posicion_y + 0.1
        except Exception as e:
            return


    

    def define_bucle(n):
        global rompe_bucle
        estado_bucle = n
        if estado_bucle == 1:
            rompe_bucle = 0
        else:
            rompe_bucle = 1
    def ejecutar_ping():
        global timer_runs_on
        
        list_label.clear()
        ejecutar_label()
        leer_config()

        try:
            def timer_on(running_timer):
                cont = 0
                define_bucle(0)
                text_label.config(bg="green")
                text_label.config(text="Preparando...")
                while running_timer.is_set():
                        text_label.config(bg="green")
                        if rompe_bucle == 0:
                            break
                        for i in range(len(lista_ip)):
                            
                            
                            contador = cont + i
                            var_nombre = list_nombre[contador]
                            labels = list_label[contador]
                            var_ip = lista_ip[contador]
                            d = ping(var_ip) 
                            if rompe_bucle == 0:
                                break
                            if d == False:
                                labels.config(bg='red')
                                labels.config(fg="white")
                            elif d == None:
                                labels.config(bg='red')
                                labels.config(fg="white")
                            else:
                                labels.config(bg='green')
                                labels.config(fg="black")
                            text_label.config(text=f"En ejecución... {i+1}")
                        text_label.config(bg="green")
                        text_label.config(text=f"Tiempo de espera {tiempo_refresco} seg.") 
                        time.sleep(int(tiempo_refresco))
                        
            
            timer_runs_on = threading.Event()
            timer_runs_on.set()
            t = threading.Thread(target=timer_on, args=(timer_runs_on,))
            t.start()
        except Exception as err:
            text_label.config(bg="red")
            text_label.config(text="Pausado")
            messagebox.showinfo(message=err, title = "NO TIENES INTERNET")

    def detener_ping():
        try:
            timer_runs_on.clear()
            define_bucle(1)
            cont = 0
            for i in range(len(list_nombre)):
                contador = cont + i
                labels = list_label[contador]
                labels.config(bg='gray')
                labels.config(fg="black")
            text_label.config(bg="red")
            text_label.config(text="Pausado")
        except:
            return

    def pagina_config():
        global max_cant_cada_cuanto, visual_config
        detener_ping()
        list_label.clear()
        visual_config = tkinter.Toplevel(v)
        visual_config.geometry("400x300")
        visual_config.title("Parámetros Principal")
        

        text_seg = tkinter.Label(visual_config, text="segundos", font="helvetica 10", anchor="w")
        text_seg.place(relx=0.59, rely=0.05, relwidth=0.45, relheight=0.08)
        text_cada_cuanto = tkinter.Label(visual_config, text="Time Refresh", font="helvetica 10")
        text_cada_cuanto.place(relx=0.08, rely=0.05, relwidth=0.45, relheight=0.08)
        max_cant_cada_cuanto = StringVar()
        caja_cada_cuanto = tkinter.Entry(visual_config, textvariable=max_cant_cada_cuanto, font = "helvetica 10")
        caja_cada_cuanto.place(relx=0.5, rely=0.05, relwidth=0.08, relheight=0.08)
        max_cant_cada_cuanto.trace("w", lambda *args: limitador(max_cant_cada_cuanto, 3))

        text_nombre_pc = tkinter.Label(visual_config, text="Nombre PC", font="helvetica 10")
        text_nombre_pc.place(relx=0.08, rely=0.15, relwidth=0.45, relheight=0.08)
        max_cant_nombre = StringVar()
        caja_nombre_pc = tkinter.Entry(visual_config, textvariable=max_cant_nombre, font = "helvetica 10")
        caja_nombre_pc.place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.08)
        max_cant_nombre.trace("w", lambda *args: limitador(max_cant_nombre, 40))
        caja_nombre_pc.focus()

        text_ip = tkinter.Label(visual_config, text="IP", font="helvetica 10")
        text_ip.place(relx=0.08, rely=0.25, relwidth=0.45, relheight=0.08)
        max_cant_ip = StringVar()
        caja_ip = tkinter.Entry(visual_config, textvariable=max_cant_ip, font = "helvetica 10")
        caja_ip.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.08)
        max_cant_ip.trace("w", lambda *args: limitador(max_cant_ip, 40))

        leer_config()
        #_______ TABLA USUARIOS
        def tabla_tbj():
            global ver_tbj
            #__________________TABLA DE DEVOLUCION
            ver_tbj = ttk.Treeview(visual_config, columns = ("col1"))
            #__________________CREACION COLUMNAS
            ver_tbj.column("#0", width = 50, anchor = CENTER)
            ver_tbj.column("col1", width = 50, anchor = CENTER)
            
            #__________________NOMBRE COLUMNAS
            ver_tbj.heading("#0", text = "NOMBRE PC", anchor = CENTER)
            ver_tbj.heading("col1", text = "IP/NOMBRE PC", anchor = CENTER)
            ver_tbj.place(relx = 0.04, rely = 0.6, relwidth = 0.93, relheight = 0.37)
            scroll = tkinter.Scrollbar(ver_tbj)
            scroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)
            scroll.config(command = ver_tbj.yview)
            ver_tbj.config(yscrollcommand = scroll.set)
            ver_tbj.bind('<Double-Button-1>', selecciona_nombre) 

        #__________________FUNCION MUESTRA USUARIOS REGISTRADOS

        def actualiza_tabla():
            tabla_tbj()
            try:
                #______MUESTRA LOS DATOS EN TABLA TRABAJADOR
                for row_nombre,row_ip in zip(list_nombre,lista_ip):
                
                    ver_tbj.insert("", END, text = row_nombre, values =
                                    (row_ip))
                    
            except Exception as e:
                messagebox.showinfo(message=f"{e}", title="Exception") 
        
        
        def selecciona_nombre(event):
            global seleccionar, guarda_nombre, guardar_pass1, valida_host, valida_ip
            item = ver_tbj.focus()
            seleccionar = ver_tbj.item(item)
            try:
                guarda_nombre = seleccionar.get("text").upper()
                guardar_pass0 = seleccionar.get("values")
                guardar_pass1 = guardar_pass0[0].upper()
                valida_host = guarda_nombre.upper() in list_nombre
                valida_ip = guardar_pass1 in lista_ip

                conectada = sqlite3.connect("setting.db")
                c = conectada.cursor()
                c.execute(f"""
                SELECT
                    *
                FROM 
                    HOST
                WHERE
                    nombre_pc = '{seleccionar.get("text")}' """)
                for i in c.fetchall():            
                    max_cant_nombre.set(i[0])
                    max_cant_ip.set(i[1])
            except:
                messagebox.showinfo(message=f"""
                Interrumpido, lista posibles casos.
                1. Ingresar solo numeros en nombre pc o ip.
                2. Dejar vacio un campo de nombre pc o ip.
                3. Repetir nombre o ip.\n
                Revisar que cumpla los requisitos.
                De lo contrario hablar con el desarrollador
                @PabloLara""", title = "Proceso Interrumpido.")
                caja_nombre_pc.delete(0,END)
                caja_ip.delete(0,END)
                caja_nombre_pc.focus()


        def elimina_nombre():
            item = ver_tbj.focus()
            seleccionar = ver_tbj.item(item)
            valida_eliminar = messagebox.askyesno(message=f"{seleccionar.get('text')}\n¿Desea eliminar?", title="Confirmar Proceso.")
            if valida_eliminar == True:
                conectada = sqlite3.connect("setting.db")
                c = conectada.cursor()
                c.execute(f"""
                DELETE
                FROM 
                    HOST
                WHERE
                    nombre_pc = '{seleccionar.get("text")}' """)
                conectada.commit()
                leer_host()
                actualiza_tabla()
                messagebox.showinfo(message=f"{seleccionar.get('text')}\nha sido eliminado.", title = "Proceso Completado.")
                caja_nombre_pc.focus()
            else:
                messagebox.showinfo(message=f"Operación Cancelada.", title = "Proceso Cancelado.")
                caja_nombre_pc.focus()
            

        actualiza_tabla()

        def actualizar_fila():
            try:
                conectada = sqlite3.connect("setting.db")
                c_fila = conectada.cursor()

                all_items = ver_tbj.get_children()
                c_fila.execute(f"DELETE FROM HOST")
                for item in all_items:
                    text = ver_tbj.item(item, 'text')
                    values = ver_tbj.item(item, 'values')
                    c_fila.execute(f"INSERT INTO HOST VALUES('{text}', '{values[0]}');")
                conectada.commit()
                leer_host()
                actualiza_tabla()
            except Exception as e:
                messagebox.showinfo(message=e, title = "Error carga filas")
                caja_nombre_pc.focus()




        def move_up():
            try:
                selected_item = ver_tbj.selection()[0]
                if selected_item:
                    index = ver_tbj.index(selected_item)
                    if index > 0:
                        ver_tbj.move(selected_item, '', index - 1)
            except IndexError:
                messagebox.showinfo(message="Debe seleccionar una fila.", title = "Error mover filas")
                caja_nombre_pc.focus()
            except Exception as e:
                messagebox.showinfo(message=e, title = "Error mover filas")
                caja_nombre_pc.focus()
            

        def move_down():
            try:
                selected_item = ver_tbj.selection()[0]
                if selected_item:
                    index = ver_tbj.index(selected_item)
                    if index < len(list_nombre):
                        ver_tbj.move(selected_item, '', index + 1)
            except IndexError:
                messagebox.showinfo(message="Debe seleccionar una fila.", title = "Error mover filas")
                caja_nombre_pc.focus()
            except Exception as e:
                messagebox.showinfo(message=e, title = "Error mover filas")
                caja_nombre_pc.focus()

      
        
        def agregar_datos(event):
            global cantidad_columna, tiempo_refresco
            list_label.clear()
            conectada = sqlite3.connect("setting.db")
            if len(caja_cada_cuanto.get()):
        
                valida_num_ccuanto = caja_cada_cuanto.get().isnumeric()
                if valida_num_ccuanto == True:
                    num_config = conectada.cursor()
                    num_config.execute(f"UPDATE CONFIG SET tiempo_refresco ='{caja_cada_cuanto.get()}'")
                    conectada.commit()
                    messagebox.showinfo(message=f"Cada {caja_cada_cuanto.get()} segundos se realizará el ping general.", title = "Proceso Completado.")
                    caja_nombre_pc.focus()
                else:
                    messagebox.showinfo(message="Solo se aceptan números.", title = "Advertencia.")
                    caja_cada_cuanto.focus()
            try:
                
                no_repetido_host = caja_nombre_pc.get().upper() in list_nombre
                no_repetida_ip = caja_ip.get().upper() in lista_ip
                if no_repetido_host == False and len(caja_nombre_pc.get()) != 0 and len(caja_ip.get().upper()) != 0 and no_repetida_ip  == False and len(list_nombre) < 54:
                        c = conectada.cursor()
                        c.execute(f"INSERT INTO HOST VALUES('{caja_nombre_pc.get().upper()}','{caja_ip.get().upper()}')")
                        conectada.commit()
                        leer_host()
                        tabla_tbj()
                        actualiza_tabla()
                        messagebox.showinfo(message=f"{caja_nombre_pc.get().upper()}\nCreado con exito", title = "Datos.")
                        caja_ip.delete(0,END)
                        caja_nombre_pc.delete(0,END)
                        caja_nombre_pc.focus()                
                    
                elif len(caja_nombre_pc.get()) != 0 and len(caja_ip.get().upper()) != 0:
                    if valida_host == True and valida_ip == True:
                        modifica_pc = conectada.cursor()
                        print(valida_host, valida_ip)
                        modifica_pc.execute(f"UPDATE HOST SET nombre_pc = '{caja_nombre_pc.get().upper()}', ip = '{caja_ip.get().upper()}' WHERE nombre_pc = '{guarda_nombre.upper()}'")
                        conectada.commit()
                        leer_host()

                        tabla_tbj()
                        actualiza_tabla()
                        caja_ip.delete(0,END)
                        caja_nombre_pc.delete(0,END)
                        caja_nombre_pc.focus()
                else:
                    messagebox.showinfo(message=f"""
                    No fué guardado, lista posibles casos.
                    1. Ingresar solo numeros en nombre pc o ip.
                    2. Dejar vacio un campo de nombre pc o ip.
                    3. Repetir nombre o ip.
                    4. Alcanzó el máximo de datos en pantalla(54).\n
                    Revisar que cumpla los requisitos.
                    De lo contrario hablar con el desarrollador
                    @PabloLara""", title = "Proceso Interrumpido.")
                    caja_nombre_pc.focus()
                
            except Exception as err:
                return

            time.sleep(1)
            
        

        caja_cada_cuanto.bind("<Return>",agregar_datos)
        caja_ip.bind('<Return>', agregar_datos) 
        btn_guardar = tkinter.Button(visual_config, text="Guardar", font="arial 10", command = lambda : agregar_datos('<Return>'))
        btn_guardar.place(relx=0.24, rely = 0.35, relwidth= 0.25, relheight= 0.1)

        btn_eliminar = tkinter.Button(visual_config, text="Eliminar", font="arial 10", command = elimina_nombre)
        btn_eliminar.place(relx=0.50, rely = 0.35, relwidth= 0.25, relheight= 0.1)


        btn_up = tkinter.Button(visual_config, text="Arriba", font="arial 10", command = move_up)
        btn_up.place(relx=0.42, rely = 0.5, relwidth= 0.15, relheight= 0.09)

        btn_down = tkinter.Button(visual_config, text="Abajo", font="arial 10", command = move_down)
        btn_down.place(relx=0.58, rely = 0.5, relwidth= 0.15, relheight= 0.09)

        btn_ok = tkinter.Button(visual_config, text="OK", font="arial 10", command = actualizar_fila)
        btn_ok.place(relx=0.26, rely = 0.5, relwidth= 0.15, relheight= 0.09)

        visual_config.mainloop()

    def abre_config():
        if config_string01.get() == 1:
            pagina_config()
        else:
            visual_config.destroy()

    def abre_page_2():
            if config_string.get() == 1:
                ventana2()
            else:
                v2.destroy()

    btn_iniciar = tkinter.Button(v, text="Iniciar", command=lambda:[ejecutar_ping()]).place(relx=0, rely=0, relwidth=0.25, relheight=0.05)
    btn_detener = tkinter.Button(v, text="Detener", command=lambda:[detener_ping()]).place(relx=0.25, rely=0, relwidth=0.25, relheight=0.05)
    config_string01 = BooleanVar()
    check_config01 = Checkbutton(v,text="Parámetros", command=abre_config, variable= config_string01,onvalue=1,offvalue=0, relief=RAISED).place(relx=0.5, rely=0, relwidth=0.25, relheight=0.05)
    config_string = BooleanVar()
    check_pag = Checkbutton(v,text="Ventana 2", command=abre_page_2, variable= config_string,onvalue=1,offvalue=0, relief=RAISED).place(relx=0.75, rely=0, relwidth=0.25, relheight=0.05)

    v.mainloop()


def ventana2():
    global v2
    v2 = tkinter.Toplevel(v)
    v2.geometry("750x500")
    v2.state('zoomed')
    v2.title("Ventana 2")
    list_label2 = []
    text_label2 = tkinter.Label(v2, text="Pausado",fg="white",font="helvetica 10",bg="red",anchor="w")
    text_label2.place(relx=0,rely=0.96,relwidth=0.22,relheight=0.04)
    def leer_host2():
        global list_nombre2
        global lista_ip2
        try:
            list_nombre2 = []
            lista_ip2 = []
            conectada = sqlite3.connect("setting.db")
            c = conectada.cursor()
            c.execute(f""" 
            SELECT 
                * 
            FROM 
                HOST2""")
            for i1 in c.fetchall():
                    list_nombre2.append(i1[0]) 
                    lista_ip2.append(i1[1]) 
    
        except Exception as err:
            messagebox.showinfo(message=f"{err}", title = "NOT FOUND BD")

    def leer_config2():
            global cantidad_columna2, tiempo_refresco2
            try:
                conectada = sqlite3.connect("setting.db")
                c = conectada.cursor()
                c.execute(f""" 
                SELECT 
                    * 
                FROM
                    CONFIG2""")
                for i2 in c.fetchall():
                    tiempo_refresco2 = i2[0]
                max_cant_cada_cuanto2.set(tiempo_refresco2)
            except NameError:
                return
            except Exception as err:
                messagebox.showinfo(message=f"{err}", title = "NOT FOUND BD")
        
    #_____________________________________________________________________ Limite de caracteres
    def limitador(max_cant, limit):
        if len(max_cant.get()) > 0:
            #donde esta el :limit la cantidad d caracteres
            max_cant.set(max_cant.get()[:limit])

    v2.attributes("-fullscreen", False) 
    v2.bind("<F11>", lambda event: v2.attributes("-fullscreen", not v2.attributes("-fullscreen"))) 
    v2.bind("<Escape>", lambda event: v2.attributes("-fullscreen", False)) 


    leer_host2()
    leer_config2()
    def ejecutar_label2():    
        global var_label2

        contador = 0
        columna = 2
        fila = len(lista_ip2) + 1
        c = 0
        posicion_x = 0
        posicion_y = 0.06
        try:
            for i2 in range(1,fila):        
                cont = contador + c
                var_nombre2 = list_nombre2[cont]
                var_ip2 = lista_ip2[cont]
                var_label2 = var_nombre2
                var_label2 = tkinter.Label(v2, text=f"{var_nombre2}\n{var_ip2}", bg="white", fg="black", width=20, font="helvetica 10", relief="groove")
                list_label2.append(var_label2)
                var_label2.place(relx=posicion_x, rely=posicion_y,relwidth=0.1667,relheight=0.1)
                c = c+1
            
                posicion_x = posicion_x + 0.1667
                if posicion_x == 1.0002:
                    posicion_x = posicion_x - 1.0002
                    posicion_y = posicion_y + 0.1
        except:
            return


    def define_bucle2(n):
        global rompe_bucle2
        estado_bucle2 = n
        if estado_bucle2 == 1:
            rompe_bucle2 = 0
        else:
            rompe_bucle2 = 1
    
    def ejecutar_ping2():
        global timer_runs_on2
        leer_config2()
        list_label2.clear()
        ejecutar_label2()
        try:
            def timer_on2(running_timer2):
                cont = 0
                text_label2.config(bg="green")
                text_label2.config(text="Preparando...")
                define_bucle2(0)
                while running_timer2.is_set():
                        if rompe_bucle2 == 0:
                            break
                        for i in range(len(lista_ip2)):
                            contador = cont + i
                            labels2 = list_label2[contador]
                            var_ip2 = lista_ip2[contador]
                            d = ping(var_ip2) 
                            if rompe_bucle2 == 0:
                                break
                            if d == False:
                                labels2.config(bg='red')
                                labels2.config(fg="white")
                            elif d == None:
                                labels2.config(bg='red')
                                labels2.config(fg="white")
                            else:
                                labels2.config(bg='green')
                                labels2.config(fg="black")
                            text_label2.config(bg="green")
                            text_label2.config(text=f"En ejecución... {i+1}")        
                        text_label2.config(bg="green")
                        text_label2.config(text=f"Tiempo de espera {tiempo_refresco2} seg.") 
                        time.sleep(int(tiempo_refresco2))
            
            timer_runs_on2 = threading.Event()
            timer_runs_on2.set()
            t2 = threading.Thread(target=timer_on2, args=(timer_runs_on2,))
            t2.start()
        except Exception as e:
            messagebox.showinfo(message=e, title = "NO TIENES INTERNET")
            text_label2.config(bg="red")
            text_label2.config(text="Pausado")

    def detener_ping2():
        try:
            timer_runs_on2.clear()
            define_bucle2(1)
            cont = 0
            for i in range(len(list_nombre2)):
                contador = cont + i
                labels2 = list_label2[contador]
                labels2.config(bg='gray')
                labels2.config(fg="black")
                text_label2.config(bg="red")
                text_label2.config(text="Pausado")
        except:
            return

    def pagina_config2():
        global max_cant_cada_cuanto2, visual_config2

        detener_ping2()
        list_label2.clear()
        visual_config2 = tkinter.Toplevel(v2)
        visual_config2.geometry("400x300")
        visual_config2.title("Parámetros Ventana 2")

        
        text_seg2 = tkinter.Label(visual_config2, text="segundos", font="helvetica 10", anchor="w")
        text_seg2.place(relx=0.59, rely=0.05, relwidth=0.45, relheight=0.08)
        text_cada_cuanto2 = tkinter.Label(visual_config2, text="Time Refresh", font="helvetica 10")
        text_cada_cuanto2.place(relx=0.08, rely=0.05, relwidth=0.45, relheight=0.08)
        max_cant_cada_cuanto2 = StringVar()
        caja_cada_cuanto2 = tkinter.Entry(visual_config2, textvariable=max_cant_cada_cuanto2, font = "helvetica 10")
        caja_cada_cuanto2.place(relx=0.5, rely=0.05, relwidth=0.08, relheight=0.08)
        max_cant_cada_cuanto2.trace("w", lambda *args: limitador(max_cant_cada_cuanto2, 3))

        text_nombre_pc2 = tkinter.Label(visual_config2, text="Nombre PC", font="helvetica 10")
        text_nombre_pc2.place(relx=0.08, rely=0.15, relwidth=0.45, relheight=0.08)
        max_cant_nombre2 = StringVar()
        caja_nombre_pc2 = tkinter.Entry(visual_config2, textvariable=max_cant_nombre2, font = "helvetica 10")
        caja_nombre_pc2.place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.08)
        max_cant_nombre2.trace("w", lambda *args: limitador(max_cant_nombre2, 40))
        caja_nombre_pc2.focus()

        text_ip2 = tkinter.Label(visual_config2, text="IP", font="helvetica 10")
        text_ip2.place(relx=0.08, rely=0.25, relwidth=0.45, relheight=0.08)
        max_cant_ip2 = StringVar()
        caja_ip2 = tkinter.Entry(visual_config2, textvariable=max_cant_ip2, font = "helvetica 10")
        caja_ip2.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.08)
        max_cant_ip2.trace("w", lambda *args: limitador(max_cant_ip2, 40))

        leer_config2()
        #_______ TABLA USUARIOS
        def tabla_host2():
            global ver_host2
            #__________________TABLA DE DEVOLUCION
            ver_host2 = ttk.Treeview(visual_config2, columns = ("col1"))
            #__________________CREACION COLUMNAS
            ver_host2.column("#0", width = 50, anchor = CENTER)
            ver_host2.column("col1", width = 50, anchor = CENTER)
            
            #__________________NOMBRE COLUMNAS
            ver_host2.heading("#0", text = "NOMBRE HOST", anchor = CENTER)
            ver_host2.heading("col1", text = "IP", anchor = CENTER)
            ver_host2.place(relx = 0.04, rely = 0.6, relwidth = 0.93, relheight = 0.37)
            scroll = tkinter.Scrollbar(ver_host2)
            scroll.pack(side = tkinter.RIGHT, fill = tkinter.Y)
            scroll.config(command = ver_host2.yview)
            ver_host2.config(yscrollcommand = scroll.set)
            ver_host2.bind('<Double-Button-1>', selecciona_nombre2) 

        #__________________FUNCION MUESTRA USUARIOS REGISTRADOS

        def actualiza_tabla2():
            tabla_host2()
            try:
                #______MUESTRA LOS DATOS EN TABLA TRABAJADOR
                for row_nombre,row_ip in zip(list_nombre2,lista_ip2):
                    ver_host2.insert("", END, text = row_nombre, values =
                                    (row_ip))
            except Exception as e:
                messagebox.showinfo(message=f"{e}", title="Exception") 


        def selecciona_nombre2(event):
            global seleccionar2, guarda_nombre2, guardar_pass2, valida_host2, valida_ip2
            item = ver_host2.focus()
            seleccionar2 = ver_host2.item(item)
            try:
                guarda_nombre2 = seleccionar2.get("text").upper()
                guardar_pass0 = seleccionar2.get("values")
                guardar_pass2 = guardar_pass0[0].upper()
                valida_host2 = guarda_nombre2.upper() in list_nombre2
                valida_ip2 = guardar_pass2 in lista_ip2

                conectada = sqlite3.connect("setting.db")
                c = conectada.cursor()
                c.execute(f"""
                SELECT
                    *
                FROM 
                    HOST2
                WHERE
                    nombre_pc = '{seleccionar2.get("text")}' """)
                for i in c.fetchall():            
                    max_cant_nombre2.set(i[0])
                    max_cant_ip2.set(i[1])
            except:
                messagebox.showinfo(message=f"""
                Interrumpido, lista posibles casos.
                1. Ingresar solo numeros en nombre host o ip.
                2. Dejar vacio un campo de nombre host o ip.
                3. Repetir nombre o ip.\n
                Revisar que cumpla los requisitos.
                De lo contrario hablar con el desarrollador
                @PabloLara""", title = "Proceso Interrumpido.")
                caja_nombre_pc2.delete(0,END)
                caja_ip2.delete(0,END)
                caja_nombre_pc2.focus()

        def elimina_nombre2():
            item = ver_host2.focus()
            seleccionar = ver_host2.item(item)
            valida_eliminar2 = messagebox.askyesno(message=f"{seleccionar.get('text')}\n¿Desea eliminar?", title="Confirmar Proceso.")
            if valida_eliminar2 == True:
                conectada = sqlite3.connect("setting.db")
                c = conectada.cursor()
                c.execute(f"""
                DELETE
                FROM 
                    HOST2
                WHERE
                    nombre_pc = '{seleccionar.get("text")}' """)
                conectada.commit()
                leer_host2()
                actualiza_tabla2()
                messagebox.showinfo(message=f"{seleccionar.get('text')}\nha sido eliminado.", title = "Proceso Completado.")
                caja_nombre_pc2.focus()
            else:
                messagebox.showinfo(message=f"Operación Cancelada.", title = "Proceso Cancelado.")
                caja_nombre_pc2.focus()
            

        actualiza_tabla2()

        def actualizar_fila2():
            try:
                conectada = sqlite3.connect("setting.db")
                c_fila = conectada.cursor()

                all_items = ver_host2.get_children()
                c_fila.execute(f"DELETE FROM HOST2")
                for item in all_items:
                    text = ver_host2.item(item, 'text')
                    values = ver_host2.item(item, 'values')
                    c_fila.execute(f"INSERT INTO HOST2 VALUES('{text}', '{values[0]}');")
                conectada.commit()
                leer_host2()
                actualiza_tabla2()
            except Exception as e:
                messagebox.showinfo(message=e, title = "Error carga filas")
                caja_nombre_pc2.focus()




        def move_up2():
            try:
                selected_item = ver_host2.selection()[0]
                if selected_item:
                    index = ver_host2.index(selected_item)
                    if index > 0:
                        ver_host2.move(selected_item, '', index - 1)
            except IndexError:
                messagebox.showinfo(message="Debe seleccionar una fila.", title = "Error mover filas")
                caja_nombre_pc2.focus()
            except Exception as e:
                messagebox.showinfo(message=e, title = "Error mover filas")
                caja_nombre_pc2.focus()
            

        def move_down2():
            try:
                selected_item = ver_host2.selection()[0]
                if selected_item:
                    index = ver_host2.index(selected_item)
                    if index < len(list_nombre2):
                        ver_host2.move(selected_item, '', index + 1)
            except IndexError:
                messagebox.showinfo(message="Debe seleccionar una fila.", title = "Error mover filas")
                caja_nombre_pc2.focus()
            except Exception as e:
                messagebox.showinfo(message=e, title = "Error mover filas")
                caja_nombre_pc2.focus()


        def agregar_datos2(event):
            global cantidad_columna2, tiempo_refresco2
            
            conectada = sqlite3.connect("setting.db")
            if len(caja_cada_cuanto2.get()):
        
                valida_num_ccuanto2 = caja_cada_cuanto2.get().isnumeric()
                if valida_num_ccuanto2 == True:
                    num_config = conectada.cursor()
                    num_config.execute(f"UPDATE CONFIG2 SET tiempo_refresco ='{caja_cada_cuanto2.get()}'")
                    conectada.commit()
                    messagebox.showinfo(message=f"Cada {caja_cada_cuanto2.get()} segundos se realizará el ping general.", title = "Proceso Completado.")
                    caja_nombre_pc2.focus()
                else:
                    messagebox.showinfo(message="Solo se aceptan números.", title = "Advertencia.")
            try:
                no_repetido_host2 = caja_nombre_pc2.get().upper() in list_nombre2
                no_repetida_ip2 = caja_ip2.get().upper() in lista_ip2
                if no_repetido_host2 == False and len(caja_nombre_pc2.get()) != 0 and len(caja_ip2.get().upper()) != 0 and no_repetida_ip2  == False and len(list_nombre2) < 54:  
                    c = conectada.cursor()
                    c.execute(f"INSERT INTO HOST2 VALUES('{caja_nombre_pc2.get().upper()}','{caja_ip2.get().upper()}')")
                    conectada.commit()
                    leer_host2()
                    actualiza_tabla2()
                    messagebox.showinfo(message=f"{caja_nombre_pc2.get().upper()}\nCreado con exito", title = "Datos.")
                    caja_ip2.delete(0,END)
                    caja_nombre_pc2.delete(0,END)
                    caja_nombre_pc2.focus()
            
                elif len(caja_nombre_pc2.get()) != 0 and len(caja_ip2.get()) != 0:
                    if valida_host2 == True and valida_ip2 == True:                   
                        modifica_pc = conectada.cursor()
                        modifica_pc.execute(f"UPDATE HOST2 SET nombre_pc = '{caja_nombre_pc2.get().upper()}', ip = '{caja_ip2.get().upper()}' WHERE nombre_pc = '{guarda_nombre2.upper()}'")
                        conectada.commit()
                        leer_host2()
                        tabla_host2()
                        actualiza_tabla2()
                        caja_ip2.delete(0,END)
                        caja_nombre_pc2.delete(0,END)
                        caja_nombre_pc2.focus()
                   
                else:
                    messagebox.showinfo(message=f"""
                    No fué guardado, lista posibles casos.
                    1. Ingresar solo numeros en nombre host o ip.
                    2. Dejar vacio un campo de nombre host o ip.
                    3. Repetir nombre o ip.
                    4. Alcanzó el máximo de datos en pantalla(54).\n
                    Revisar que cumpla los requisitos.
                    De lo contrario hablar con el desarrollador
                    @PabloLara""", title = "Proceso Interrumpido.")
                    caja_nombre_pc2.focus()
                
                    
            except Exception as err:
                return
            time.sleep(1)
            
            
            

        caja_cada_cuanto2.bind('<Return>',agregar_datos2)
        caja_ip2.bind('<Return>',agregar_datos2)
        btn_guardar2 = tkinter.Button(visual_config2, text="Guardar", font="arial 10", command = lambda : agregar_datos2('<Return>'))
        btn_guardar2.place(relx=0.24, rely = 0.35, relwidth= 0.25, relheight= 0.1)

        btn_eliminar2 = tkinter.Button(visual_config2, text="Eliminar", font="arial 10", command = elimina_nombre2)
        btn_eliminar2.place(relx=0.50, rely = 0.35, relwidth= 0.25, relheight= 0.1)

        
        btn_up2 = tkinter.Button(visual_config2, text="Arriba", font="arial 10", command = move_up2)
        btn_up2.place(relx=0.42, rely = 0.5, relwidth= 0.15, relheight= 0.09)

        btn_down2 = tkinter.Button(visual_config2, text="Abajo", font="arial 10", command = move_down2)
        btn_down2.place(relx=0.58, rely = 0.5, relwidth= 0.15, relheight= 0.09)

        btn_ok2 = tkinter.Button(visual_config2, text="OK", font="arial 10", command = actualizar_fila2)
        btn_ok2.place(relx=0.26, rely = 0.5, relwidth= 0.15, relheight= 0.09)

        visual_config2.mainloop()

    def abre_config2():
        if config_string2.get() == 1:
            pagina_config2()
        else:
            visual_config2.destroy()

    btn_iniciar2 = tkinter.Button(v2, text="Iniciar", command=lambda:[ejecutar_ping2()]).place(relx=0, rely=0, relwidth=0.33, relheight=0.05)
    btn_detener2 = tkinter.Button(v2, text="Detener", command=lambda:[detener_ping2()]).place(relx=0.34, rely=0, relwidth=0.32, relheight=0.05)
    config_string2 = BooleanVar()
    check_config2 = Checkbutton(v2,text="Parámetros", command=abre_config2, variable= config_string2,onvalue=1,offvalue=0, relief=RAISED).place(relx=0.68, rely=0, relwidth=0.32, relheight=0.05)
    
    
    firma2 = tkinter.Label(v2,text="@PabloLara",font="helvetica 8", anchor="e").place(relx=0.9,rely=0.95,relwidth=0.1,relheight=0.05)
    v2.mainloop()

    #FUE UN GUSTO TRABAJAR EN ESTE PROYECTO, AUN QUE HACE TIEMPO LO INTENTE
    # HACE DOS DÍAS UN COMPRAÑERO DE TRABAJO ME COMENTO QUE QUERÍA ALGO QUE SE PARECIERA A SERVICIOS DE PRTG
    # O DE LOS QUE HICIERAN PING YA QUE ERAN LICENCIADOS, DECIDÍ CREAR UNO PROPIO PARA 108 EQUIPOS EN DOS VENTANAS DIFERENTES
    # DE FORMA AJUSTABLE A PANTALLA.

ventana1()
