import math

class Accion:
    DERECHA = 1
    IZQUIERDA = 0
    max_valor = 1


class Posicion:
    BORDE_IZQUIERDO = 1
    BORDE_DERECHO = 2
    CENTRO = 3


class Estado:
    angulo = 0
    velocidad_angular = 0
    posicion = Posicion.CENTRO


    def __init__(self):
        self.angulo = math.pi
        self.velocidad_angular = 0

    def __repr__(self):
        return "Angulo: {}, Velocidad Angular: {}, Posicion: {})".format(
            self.angulo,
            self.velocidad_angular,
            self.posicion)
        
