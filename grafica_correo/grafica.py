
import time
import rrdtool
import os
from getSNMP import consultaSNMP

RRD_FOLDER_PATH = "/Users/zul/Documents/escuela/Admin Servicios en Red/practicas/practica2/grafica_correo/rrd/"


def create_grafica(ip, cpu="0", ram=False, disk=False):
    current_ip_folder = RRD_FOLDER_PATH + ip

    if not os.path.exists(current_ip_folder):
        os.makedirs(current_ip_folder)

    path = current_ip_folder + "/trend-" + cpu + ".rrd"
    nombre_grafica = "CPUload"
    texto = "CPU"

    if ram:
        path = current_ip_folder + "/ram.rrd"
        nombre_grafica = "RAMload"
        texto = "RAM"
    if disk:
        path = current_ip_folder + "/disk.rrd"
        nombre_grafica = "HDDload"
        texto = "HDD"

    ret = rrdtool.create(path,
                         "--start", 'N',
                         "--step", '60',
                         "DS:" + nombre_grafica + ":GAUGE:60:0:100",
                         "RRA:AVERAGE:0.5:1:24")

    if ret:
        print(rrdtool.error())

    print("Archivo " + texto + " creado!")


def update_grafica(nucleos_disponibles, ip, comunidad):
    current_ip_folder = RRD_FOLDER_PATH + ip

    while 1:
        for nucleo in nucleos_disponibles:
            numero_nucleo = str(nucleo - 7)
            oid = "1.3.6.1.2.1.25.3.3.1.2.1966" + \
                str("0" + str(nucleo) if nucleo < 10 else nucleo)
            carga_CPU = int(consultaSNMP(comunidad, ip, oid))
            valor = "N:" + str(carga_CPU)
            print("Carga core " + numero_nucleo + ":" + str(carga_CPU))
            rrdtool.update(current_ip_folder + "/trend-" +
                           numero_nucleo + ".rrd", valor)
        #   RAM                           
        RAM_TOTAL = int(consultaSNMP(comunidad, ip, "1.3.6.1.4.1.2021.4.5.0"))
        RAM_USADA = int(consultaSNMP(comunidad, ip, "1.3.6.1.4.1.2021.4.6.0"))
        PORCENTAJE_RAM_USADA = int((RAM_USADA* 100) / RAM_TOTAL)
        valor_RAM = "N:" + str(PORCENTAJE_RAM_USADA)
        rrdtool.update(current_ip_folder + "/ram.rrd", valor_RAM)
        print("Carga RAM: " + str(PORCENTAJE_RAM_USADA))
        #   HDD                           
        #carga_HDD = consultaSNMP(comunidad, ip, "1.3.6.1.4.1.2021.9.1.9.1")
        #valor_HDD = "N:" + str(carga_HDD)
        #rrdtool.update(current_ip_folder + "/disk.rrd", valor_HDD)
        #print("Carga HDD: " + str(carga_HDD))
        time.sleep(5)

    if ret:
        print(rrdtool.error())
        time.sleep(300)
