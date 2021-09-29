from RLObjects import Posicion, Accion, Estado
import random
from random import SystemRandom


_epsilon = 0.1


def get_siguiente_accion_greedy(estado, q_state):
    q_estado = [(b, Q.activate([estado.angulo, estado.velocidadAngular, estado.posicion, b])) for b in range(Accion.maxValor + 1) ]
    accion_min, valor_min = q_estado[0]
    
    for (acc, valor) in q_estado:
        if (valor < valor_min):
            accion_min = acc
            valor_min = valor
    return accion_min
    

def get_siguiente_accion_epsilon_greedy(estado, q_estado):
    cryptogen = SystemRandom()
    random_num = cryptogen.random()

    if random_num <= _epsilon:
        accion = cryptogen.randrange(0, Accion.maxValor)
    else:
        accion = get_siguiente_accion_greedy(estado, Q)

    return accion



def get_siguiente_accion_random(estado):

    accion = cryptogen.randrange(0, Accion.maxValor)
    return accion




