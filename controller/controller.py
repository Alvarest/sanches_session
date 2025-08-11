import serial
import struct
import mido
import time
import sys

class Boton():
    def __init__(self, control, channel, msg_type = "note_on"):
        self.control_value = control
        self.channel = channel
        self.msg_type = msg_type

class Slider():
    def __init__(self, min_val, max_val, control, channel, msg_type = "control_change"):
        self.min_val = min_val
        self.max_val = max_val
        self.control_value = control
        self.channel = channel
        self.msg_type = msg_type

# Mi idea es hacer una matriz de 16 x 3 con todos los controles de la mesa
# y entonces con el valor de selector y entrada elegir el control correspondiente
# y enviar el mensaje con el valor que tenga
def enviar_msg(shift, selector, entrada, valor):
    control = controles[selector][entrada]
    if control.msg_type == "note_on":
        # Estoy asumiendo que el valor sera o 0 o 1, pero si lo leemos con una entrada analogica habrá que 
        # cambiar este codigo y seguramente la clase Boton
        msg = mido.Message(control.msg_type, note = control.control_value, velocity = valor*127, 
                           channel = control.channel)
    elif control.msg_type == "control_change":
        msg = mido.Message(control.msg_type, control = control.control_value, value = value, 
                           channel = control.channel)
    else:
        print("Tipo de mensaje no valido")
        return 1

    outport.send(msg)
    return 0

def conectar_arduino(puerto, baudrate):
    puntos = 0
    while True:
        try:
            ser = serial.Serial(puerto, baudrate, timeout = 1)
            print("Arduino conectado")
            return ser
        except serial.SerialException:
            if puntos == 0:
                print("                                            ", end="\r")
            print("Esperando a que el arduino este conectado", end = "."*puntos + "\r")
            puntos = (puntos+1)%4
            time.sleep(2)

def main():
    puerto = "dev/ttyACM0"
    baudrate = 115200
    ser = conectar_arduino(puerto, baudrate)
    tamaño = 4*4

    try:
        while True:
            data = ser.read(packet_size)
            if len(data) == packet_size:
                valores = struct.unpack("<iiii", data) # < significa little-endian
                enviar_msg(*valores)
    except serial.SerialException:
        print("Se ha desconectado el arduino.")
        ser.close()
        main()
    except KeyboardInterrupt:
        print("Terminado")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
