from RLObjects import Posicion, Accion, Estado
from Simulator import Simulator
#from ODESim import ODESim

_simulador = Simulator(True, True)


def inicializar(imprimirAngulo, imprimirTiempo):
    global _simulador
    _simulador = Simulator(imprimirAngulo, imprimirTiempo)
    #_simulador = ODESim()


def set_angulo_inicial(angulo):
    _simulador.cartPole_angulo = angulo


def ejecutar_accion(accion):
    if (accion == Accion.DERECHA):
        accSim = 1
    elif (accion == Accion.IZQUIERDA):
        accSim = -1
    else:
        accSim = 0

    # Corro las veces necesarias para mostrar el resultado
    for i in range(_simulador.vueltasPorMovimiento):
        _simulador.run(accSim)


def get_estado():
    result = Estado()

    result.angulo = _simulador.cartPole_angulo
    result.velocidadAngular = int(_simulador.cartPole_velocidadAngular)


    # Posicion
    if _simulador.cartPole_x <= _simulador.xMin:
        result.posicion = Posicion.BORDE_IZQUIERDO

    elif _simulador.cartPole_x >= _simulador.xMax:
        result.posicion = Posicion.BORDE_DERECHO

    else:
        result.posicion = Posicion.CENTRO

    return result


def get_key_pressed():
    return _simulador.get_key_pressed()


def finalizar():
    _simulador.finalizar()



