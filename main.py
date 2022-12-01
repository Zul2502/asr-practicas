from tkinter import Tk, Label, Button
from acciones import add_dispositivo, update_dispositivos, delete_dispositivo, trackear_dispositivo
from functools import partial

ventana = Tk()

ventana.geometry("600x350")
ventana.title("Práctica 2")
ventana.eval('tk::PlaceWindow . center')

Label(
    ventana,
    text="Sistema de Administración de Red \n\nPráctica 2 - Sistema de administración de Contabilidad\n\n Cruz Acosta Margarita de la luz   4CM13   2016630078",
    font=("Arial", 16)
).pack()

Label(
    ventana,
    text="Elige una opción:",
    font=("Arial", 15)
).pack(
    pady=20,
    padx=15,
    anchor="w"
)

Button(
    ventana,
    text="Agregar dispositivo",
    command=partial(add_dispositivo, ventana),
    width=30
).pack(pady=5)

Button(
    ventana,
    text="Cambiar información de dispositivo",
    command=partial(update_dispositivos, ventana),
    width=30
).pack(pady=5)

Button(
    ventana,
    text="Eliminar dispositivo",
    command=partial(delete_dispositivo, ventana),
    width=30
).pack(pady=5)

Button(
    ventana,
    text="Trackear dispositivo",
    command=partial(trackear_dispositivo, ventana),
    width=30
).pack(pady=5)

ventana.mainloop()
