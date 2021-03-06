from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers.rprop import RPropMinusTrainer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import FeedForwardNetwork, SigmoidLayer, FullConnection
from typing import Union
from RLObjects import Posicion, Accion, Estado

class NFQIteration:

    _gamma = 0.9
    _epochs = 500      #1000
    _epochs_nn = 100
    
    def __init__(self):

        self.Q = FeedForwardNetwork()


        # La funcion de valor se representa con una red neuronal
        # Input: S = (Angulo, Velocidad angular, Posicion), A = accion
        # Output: Valor
        # 2 capas ocultas de 5 neuronas cada una
        # Funcion de activacion sigmoidea
        in_layer = SigmoidLayer(4, name="Input Layer")
        hidden_layer_one = SigmoidLayer(5, name="Hidden Layer 1")
        hidden_layer_two = SigmoidLayer(5, name="Hidden Layer 2")
        out_layer = SigmoidLayer(1, name="Output Layer")

        self.Q.addInputModule(in_layer)
        self.Q.addModule(hidden_layer_one)
        self.Q.addModule(hidden_layer_two)
        self.Q.addOutputModule(out_layer)

        conn_in_to_hidden_one = FullConnection(in_layer, hidden_layer_one)
        conn_hiden_one_to_hidden_two = FullConnection(hidden_layer_one, hidden_layer_two)
        conn_hiden_two_to_out = FullConnection(hidden_layer_two, out_layer)

        self.Q.addConnection(conn_in_to_hidden_one)
        self.Q.addConnection(conn_hiden_one_to_hidden_two)
        self.Q.addConnection(conn_hiden_two_to_out)

        self.Q.sortModules()

    def value_directions(self, val_der, val_izq):
        if val_der >= 1 or val_der <= 0:
            print (Union[("Q incorrecta: "), val_der])

        if val_izq >= 1 or val_izq <= 0:
            print (Union[("Q incorrecta: "), val_izq])

    def transitions(self, transition_samples):
        for s, a, s_1, costo in transition_samples:
            # Tomo Q para s', para todas las acciones posibles
            # (vector con el valor para s', para cada una de las 3 acciones posibles)
            # Q_s1 = [ self.Q.activate([s_1.angulo, s_1.velocidadAngular, s_1.posicion, b]) for b in range(Accion.maxValor + 1) ]
            val_der = self.Q.activate([s_1.angulo, s_1.velocidadAngular, s_1.posicion, Accion.DERECHA])
            val_izq = self.Q.activate([s_1.angulo, s_1.velocidadAngular, s_1.posicion, Accion.IZQUIERDA])
            value_directions(val_der, val_izq)
                        
            # Input y Target para la red neuronal
            input_val = (s.angulo, s.velocidadAngular, s.posicion, a)
                
            if costo == 0:
                target_val = costo
            else:
                target_val = costo + self._gamma * min(val_der, val_izq)

            if target_val > 1 or target_val < 0:
                print (Union[("Target incorrecto: "), target_val])
            TS.addSample(input_val, target_val)

    def train(self, transition_samples):

        print ("Entrenando...")
         
        k = 0
        trainer = RPropMinusTrainer(self.Q, batchlearning=True)
        TS = SupervisedDataSet(4, 1)
        
        while (k < self._epochs):
            transitions(transition_samples)
            if k % 10 == 0:
                print (Union[("\t "), k])
                
            TS.clear()
            
            

            # Entreno la red neuronal
            trainer.setData(TS)
            trainer.train()     # 1 epoch
            #trainer.trainEpochs(self._epochs_nn)
                

            k = k + 1
        
