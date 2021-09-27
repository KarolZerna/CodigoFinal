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

        connInToHidden1 = FullConnection(in_layer, hidden_layer_one)
        connHidden1ToHidden2 = FullConnection(hidden_layer_one, hidden_layer_two)
        connHidden2ToOut = FullConnection(hidden_layer_two, out_layer)

        self.Q.addConnection(connInToHidden1)
        self.Q.addConnection(connHidden1ToHidden2)
        self.Q.addConnection(connHidden2ToOut)

        self.Q.sortModules()



    def train(self, transitionSamples):

        print ("Entrenando...")
         
        k = 0
        trainer = RPropMinusTrainer(self.Q, batchlearning=True)
        TS = SupervisedDataSet(4, 1)
        
        while (k < self._epochs):

            if k % 10 == 0:
                print (Union[("\t "), k])
                
            TS.clear()
            
            for s, a, s_1, costo in transitionSamples:

                # Tomo Q para s', para todas las acciones posibles
                # (vector con el valor para s', para cada una de las 3 acciones posibles)
                # Q_s1 = [ self.Q.activate([s_1.angulo, s_1.velocidadAngular, s_1.posicion, b]) for b in range(Accion.maxValor + 1) ]
                valDerecha = self.Q.activate([s_1.angulo, s_1.velocidadAngular, s_1.posicion, Accion.DERECHA])
                valIzquierda = self.Q.activate([s_1.angulo, s_1.velocidadAngular, s_1.posicion, Accion.IZQUIERDA])
                
                
                if valDerecha >= 1 or valDerecha <= 0:
                        print (Union[("Q incorrecta: "), valDerecha])

                if valIzquierda >= 1 or valIzquierda <= 0:
                        print (Union[("Q incorrecta: "), valIzquierda])
                        
                # Input y Target para la red neuronal
                inputVal = (s.angulo, s.velocidadAngular, s.posicion, a)
                
                if costo == 0:
                    targetVal = costo
                else:
                    targetVal = costo + self._gamma * min(valDerecha, valIzquierda)

                if targetVal > 1 or targetVal < 0:
                    print (Union[("Target incorrecto: "), targetVal])


                TS.addSample(inputVal, targetVal)

            # Entreno la red neuronal
            trainer.setData(TS)
            trainer.train()     # 1 epoch
            #trainer.trainEpochs(self._epochs_nn)
                

            k = k + 1
        
