from getSNMP import consultaSNMP
from grafica_correo.grafica import create_grafica, update_grafica
from grafica_correo.trendGraphDetection import verifica_estado
import datetime
import rrdtool
import threading

class Dispositivo:
    def __init__(self, comunidad, puerto, ip):
        self.comunidad = comunidad
        self.puerto = puerto
        self.ip = ip

    def getPDFInfo(self):
        sistema_operativo = consultaSNMP(
            self.comunidad, self.ip, "1.3.6.1.2.1.1.1.0")
        nombre = consultaSNMP(self.comunidad, self.ip,
                              "1.3.6.1.2.1.1.1.0", index_resultado=3)
        tiempo_actividad = datetime.timedelta(seconds=int(
            consultaSNMP(self.comunidad, self.ip, "1.3.6.1.2.1.1.3.0")) / 100)
        fecha_hora = str(consultaSNMP(self.comunidad, self.ip,
                         "1.3.6.1.4.1.2021.100.4.0", True)).split(" = ")[1]

        return {
            "sistema_operativo": sistema_operativo,
            "nombre": nombre,
            "tiempo_actividad": str(tiempo_actividad),
            "fecha_hora": fecha_hora,
            "comunidad": self.comunidad,
        }

    def getUsoCPU(self):
        nucleo_seleccionado = 8
        nucleos_disponibles = []
        thread = threading.Thread(target = verifica_estado, args=(self.ip, ))

        while True:
            oid = "1.3.6.1.2.1.25.3.3.1.2.1966" + str("0" + str(nucleo_seleccionado) if nucleo_seleccionado < 10 else nucleo_seleccionado)
            resultado = consultaSNMP(self.comunidad, self.ip, oid)
            if resultado == "No":
                break
            create_grafica(self.ip, str(nucleo_seleccionado - 7))
            nucleos_disponibles.append(nucleo_seleccionado)
            nucleo_seleccionado += 1
        create_grafica(self.ip, ram = True)
        create_grafica(self.ip, disk = True)
        thread.start()
        update_grafica(nucleos_disponibles, self.ip, self.comunidad)