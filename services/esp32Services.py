import serial
from fastapi import HTTPException

"""
Aqui es donde se hará la logica de la conexión de la esp32

"""


class Conexion:
    def __init__(self, puerto='COM4', baudrate=115200, timeout=10):
        self.puerto = puerto
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def open_connection(self):
        try:
            self.serial = serial.Serial(
                self.puerto, self.baudrate, timeout=self.timeout)
            return self.serial
        except serial.SerialException as e:
            raise HTTPException(
                status_code=500, detail="Error al abrir la conexión serial")

    def enviar_mensaje(self, mensaje):
        if self.serial and self.serial.is_open:
            self.serial.write(mensaje.encode('utf-8'))
            print(f"Mensaje enviado: {mensaje}")
        else:
            print("Error: El puerto no esta abierto")

    def recibir_mensaje(self):
        mensaje = self.serial.readline().decode('utf-8').rstrip()
        print(f'mensaje recibido{mensaje}')
        return mensaje

    def esp32_status(self):
        return self.serial.is_open

    def cerrar(self):
        if self.serial:
            self.serial.close()
