from RLObjects import Posicion, Accion, Estado
import random


_epsilon = 0.1


def get_siguiente_accion_greedy(estado, Q):
    Q_estado = [(b, Q.activate([estado.angulo, estado.velocidadAngular, estado.posicion, b])) for b in range(Accion.maxValor + 1) ]
    accionMin, valorMin = Q_estado[0]
    
    for (acc, valor) in Q_estado:
        if (valor < valorMin):
            accionMin = acc
            valorMin = valor
    return accionMin
    

def get_siguiente_accion_epsilon_greedy(estado, Q):
    rndNumber = random.random()

    if rndNumber <= _epsilon:
        accion = random.randint(0, Accion.maxValor)
    else:
        accion = get_siguiente_accion_greedy(estado, Q)

    return accion



def get_siguiente_accion_random(estado):

    accion = random.randint(0, Accion.maxValor)
    return accion




