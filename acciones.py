from Dispositivo import Dispositivo
from dispositivos_disponibles.dispositivos_controller import leer_archivo
from tkinter import Toplevel, Entry, StringVar, Label, Button
from tkinter.messagebox import askyesno
from functools import partial

dispositivos = leer_archivo()


def ventana_basica(ventana, titulo):
    x = ventana.winfo_x()
    y = ventana.winfo_y()

    addDispositivoVentana = Toplevel(ventana)
    addDispositivoVentana.title(titulo)
    addDispositivoVentana.geometry("400x250")
    addDispositivoVentana.geometry("+%d+%d" % (x + 100, y + 200))
    return addDispositivoVentana


def add_dispositivo(ventana, index=None):
    texto_boton = "Guardar"
    addDispositivoVentana = ventana_basica(ventana, "Agregar dispositivo")
    comunidad_string = StringVar()
    puerto_string = StringVar()
    ip_string = StringVar()

    if index is not None:
        comunidad_string.set(dispositivos[index].comunidad)
        puerto_string.set(dispositivos[index].puerto)
        ip_string.set(dispositivos[index].ip)
        texto_boton = "Actualizar"

    Label(addDispositivoVentana, text="IP/hostname:").grid(row=3, padx=20, pady=20)
    Entry(
        addDispositivoVentana,
        textvariable=ip_string
    ).grid(row=3, column=1)

    Label(addDispositivoVentana, text="Puerto:").grid(row=2, padx=20, pady=20)
    Entry(
        addDispositivoVentana,
        textvariable=puerto_string
    ).grid(row=2, column=1)

    Label(
        addDispositivoVentana,
        text="Comunidad:"
    ).grid(
        row=0,
        padx=20,
        pady=20
    )

    Entry(
        addDispositivoVentana,
        textvariable=comunidad_string
    ).grid(row=0, column=1)

    def guardar_dispositivo():
        if index is not None:
            dispositivos[index].comunidad = comunidad_string.get()
            dispositivos[index].ip = ip_string.get()
            dispositivos[index].puerto = puerto_string.get()
        else:
            dispositivos.append(
                Dispositivo(
                    comunidad_string.get(),
                    puerto_string.get(),
                    ip_string.get()
                )
            )
        addDispositivoVentana.destroy()
        addDispositivoVentana.update()

    Button(
        addDispositivoVentana,
        text=texto_boton,
        command=guardar_dispositivo
    ).grid(row=4, pady=5)


def update_dispositivos(ventana):
    menu_update = ventana_basica(ventana, "Seleccionar dispositivo")
    Label(
        menu_update,
        text="Selecciona el dispositivo a actualizar:"
    ).grid(
        row=0,
        padx=20,
        pady=20
    )

    def update(index):
        add_dispositivo(ventana, index)
        menu_update.destroy()
        menu_update.update()

    for index in range(len(dispositivos)):
        Button(
            menu_update,
            text=dispositivos[index].ip,
            command=partial(update, index)
        ).grid(row=index + 1, pady=5)


def delete_dispositivo(ventana):
    menu_delete = ventana_basica(ventana, "Eliminar dispositivo")
    Label(
        menu_delete,
        text="Selecciona el dispositivo a eliminar:"
    ).grid(
        row=0,
        padx=20,
        pady=20
    )

    def delete(index):
        confirmado = askyesno(
            title="Confirmación", message="¿Estás seguro que deseas eliminar el dispositivo: \n" + dispositivos[index].ip + "?")
        if confirmado:
            del dispositivos[index]
            menu_delete.destroy()
            menu_delete.update()

    for index in range(len(dispositivos)):
        Button(
            menu_delete,
            text=dispositivos[index].ip,
            command=partial(delete, index)
        ).grid(row=index + 1, pady=5)


def trackear_dispositivo(ventana):
    menu_PDF = ventana_basica(ventana, "Trackear dispositivo")
    Label(
        menu_PDF,
        text="Selecciona el dispositivo para trackear su actividad"
    ).grid(
        row=0,
        padx=20,
        pady=20
    )

    def generarPDF(index):
        inventarioDispositivo = dispositivos[index].getPDFInfo()
        rendimientoCPUS = dispositivos[index].getUsoCPU()
        print(rendimientoCPUS)

        #confirmado = askyesno(
        #    title="Confirmación", message="¿Estás seguro que deseas eliminar el dispositivo: \n" + dispositivos[index].ip + "?")
        #if confirmado:
        #    del dispositivos[index]
        #    menu_delete.destroy()
        #    menu_delete.update()

    for index in range(len(dispositivos)):
        Button(
            menu_PDF,
            text=dispositivos[index].ip,
            command=partial(generarPDF, index)
        ).grid(row=index + 1, pady=5)
