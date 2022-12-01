import os
import sys
from Dispositivo import Dispositivo
sys.path.append('..')


def leer_archivo():
    path = os.path.dirname(os.path.realpath(__file__))
    file_path = path + "/dispositivos.txt"
    if os.path.isfile(file_path) is False:
        open(file_path, "x")
        return []
    db_dispositivos = open(file_path, "r")
    dispositivos_disponibles = db_dispositivos.read().splitlines()
    dispositivos = []

    for device in dispositivos_disponibles:
        info_dispositivo = device.split(",")
        dispositivos.append(Dispositivo(
            info_dispositivo[0], info_dispositivo[1], info_dispositivo[2]))
    db_dispositivos.close()
    return dispositivos
