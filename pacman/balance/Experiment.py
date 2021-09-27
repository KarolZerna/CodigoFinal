from RLObjects import Posicion, Accion, Estado
from Simulator import Simulator


_simulador = Simulator(True, True)


def inicializar(imprimir_angulo, imprimir_tiempo):
    global _simulador
    _simulador = Simulator(imprimir_angulo, imprimir_tiempo)
 


def set_angulo_inicial(angulo):
    _simulador.cartPole_angulo = angulo


def ejecutar_accion(accion):
    if (accion == Accion.DERECHA):
        acc_sim = 1
    elif (accion == Accion.IZQUIERDA):
        acc_sim = -1
    else:
        acc_sim = 0

    # Corro las veces necesarias para mostrar el resultado
    for _ in range(_simulador.vueltasPorMovimiento):
        _simulador.run(acc_sim)


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



