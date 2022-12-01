from  .send_email import send_alert_attached
import sys
import rrdtool
import time
import datetime
import time
import os

rrdpath = '/Users/zul/Documents/escuela/Admin Servicios en Red/practicas/practica2/grafica_correo/rrd/'
imgpath = '/Users/zul/Documents/escuela/Admin Servicios en Red/practicas/practica2/grafica_correo/img/'

def generarGrafica(ultima_lectura, elemento_trackeado, tipo_informacion, path):
    tiempo_final = int(ultima_lectura)
    tiempo_inicial = tiempo_final - 1800
    ret = rrdtool.graphv( imgpath+"deteccion-"+ elemento_trackeado + ".png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label="+ tipo_informacion,
                    '--lower-limit', '0',
                    '--upper-limit', '100',
                    "--title=Carga del " + elemento_trackeado + " del agente Usando SNMP y RRDtools \n Detección de umbrales",
                    "DEF:cargaCPU="+ path + ":" + tipo_informacion + ":AVERAGE",
                     "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                     "VDEF:cargaMIN=cargaCPU,MINIMUM",
                     "VDEF:cargaSTDEV=cargaCPU,STDEV",
                     "VDEF:cargaLAST=cargaCPU,LAST",
                     "CDEF:umbral50=cargaCPU,50,LT,0,cargaCPU,IF",
                     "AREA:cargaCPU#00FF00:Carga del" + elemento_trackeado,
                     "AREA:umbral50#FF9F00:Carga" + elemento_trackeado +" mayor de 60",
                     "HRULE:8#FF0000:Umbral  60%",
                     "PRINT:cargaLAST:%6.2lf",
                     "GPRINT:cargaMIN:%6.2lf %SMIN",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST" )
    print (ret)

def verifica_estado(ip):
    path_ip = rrdpath + ip
    files = os.listdir(path_ip)
    while (1):
        for f in files:
            if f.__contains__("trend"):
                tipo_informacion = "CPUload"
                elemento_trackeado = "CPU"
            elif f.__contains__("ram"):
                tipo_informacion = "RAMload"
                elemento_trackeado = "RAM"
            else:
                tipo_informacion = "HDDload"
                elemento_trackeado = "HDD"

            ultima_actualizacion = rrdtool.lastupdate(path_ip + "/" + f)
            timestamp=ultima_actualizacion['date'].timestamp()
            dato=ultima_actualizacion['ds'][tipo_informacion]
            print(dato)

            if dato:
                if dato > 44 and dato < 50:
                    print("Estamos en fase ready en el " + elemento_trackeado)
                if dato >= 50 and dato < 60:
                    print("Estamos en fase set en el" + elemento_trackeado)
                if dato > 60:
                    generarGrafica(int(timestamp), elemento_trackeado, tipo_informacion, path_ip + "/" + f)
                    send_alert_attached(elemento_trackeado + " sobrepasa el umbral", elemento_trackeado)
                    print(elemento_trackeado + " sobrepasa el umbral")
        time.sleep(20)