import math, sys, time, random
from pygame import draw

class Simulator:
    
    def __init__(self, imprimir_angulo, imprimir_tiempo):

        self.imprimir_angulo = imprimir_angulo        # Imprime angulo y velocidad angular en pantalla
        self.imprimir_tiempo = imprimir_tiempo        # Imprime cantidad de tiempo que mantiene seguido en la region target
        self.target_value = 0.5
        

        # Inicializo variables
        self.GRAVITY = 9.8
        self.MASSCART = 10.0
        self.MASSPOLE = 0.3
        self.TOTAL_MASS = (self.MASSPOLE + self.MASSCART)
        self.LENGTH = 0.5 # actually half the pole's length
        self.POLEMASS_LENGTH = (self.MASSPOLE * self.LENGTH)
        self.FORCE_MAG = 10.0
        self.TAU = 0.02 # dt
        self.FOURTHIRDS = 1.3333333333333
        
        self.vueltas = 0
        self.movimiento_seleccionado = 0
        self.vueltas_por_movimiento = 5  #cada cuantas vueltas del TAU va a durar una desicion
        self.acumulador_vueltas_por_movimiento = self.vueltas_por_movimiento
        self.mov_totales = 1
        self.movimiento_temporario = 0
        self.aplicacion_fuerza = 0
        
        self.screen_width = 1000
        self.cart_width = 80
        self.altura = 150

        self.cart_pole_x = 0.5
        self.cart_pole_velocidad_x = 0.0
        self.cart_pole_angulo = math.pi
        self.cart_pole_velocidad_angular = 0.0

        self.en_objetivo = False         # Indica si el pendulo esta dentro del angulo objetivo - para contador de tiempo
        self.en_objetivo_tiempo_de_inicio = 0
        self.en_objetivo_tiempo_maximo = 0
        self.en_objetivo_ultimo_tiempo = 0
        self.color_carro = (150, 0, 0)
        self.colorPendulo = (0, 100, 0)
        self.colorPelota = (92, 51, 23)

        
        self.xMin = 0
        self.xMax = 1

        
        self.fastMotion = False


    
        pygame.init()
        pygame.display.set_caption('Cart Pole Balancing')


        self.background = pygame.image.load("imgs/bg2.jpg")
        self.backgroundRect = self.background.get_rect()

        self.x_size, self.y_size = 1000, 480
        self.screen = pygame.display.set_mode((self.x_size, self.y_size))
        self.clock = pygame.time.Clock()
        self.position = self.x_size/2, self.y_size - 100
        self.height = -100
        self.top_position = self.position[0], self.position[1] + self.height
        self.clock.tick(1/self.TAU)

        
    
    def calcPhysics(self):
        
        force = (self.movimiento_seleccionado*250) * (1 + random.random()/10 - 0.05)

        if self.movimiento_seleccionado != 0:
            self.movimiento_seleccionado = 0
            self.aplicacion_fuerza = self.vueltas_por_movimiento
            self.cart_pole_velocidad_x = 0

        self.aplicacion_fuerza = self.aplicacion_fuerza-1
        
        

        costheta = math.cos(self.cart_pole_angulo)
        sintheta = math.sin(self.cart_pole_angulo)

        temp = ((force + self.POLEMASS_LENGTH * self.cart_pole_velocidad_angular * \
                 self.cart_pole_velocidad_angular * sintheta)
                             / self.TOTAL_MASS)

        gravedadModificada = self.GRAVITY

        # Intento de rozamiento
        if self.cart_pole_angulo > 0:
            if self.cart_pole_velocidad_angular > 0:
                gravedadModificada = gravedadModificada * 0.8
            else:
                gravedadModificada = gravedadModificada * 1.2
        else:
            if self.cart_pole_velocidad_angular > 0:
                gravedadModificada = gravedadModificada * 1.2
            else:
                gravedadModificada = gravedadModificada * 0.8

            
        thetaacc = ((gravedadModificada * sintheta - costheta* temp)
                   / (self.LENGTH * (self.FOURTHIRDS - self.MASSPOLE * costheta * costheta
                                                  / self.TOTAL_MASS)))

        xacc  = temp - self.POLEMASS_LENGTH * thetaacc* costheta / self.TOTAL_MASS

        # Update the four state variables, using Euler's method.

        self.cart_pole_x  += self.TAU * self.cart_pole_velocidad_x
        self.cart_pole_velocidad_x += self.TAU * xacc
        
        if (self.aplicacion_fuerza <= 0):
            self.aplicacion_fuerza = 0
            self.cart_pole_velocidad_x = 0
            
        self.cart_pole_angulo += self.TAU * self.cart_pole_velocidad_angular
        self.cart_pole_velocidad_angular += self.TAU * thetaacc

        while self.cart_pole_angulo > math.pi:
            self.cart_pole_angulo -= 2.0 * math.pi

        while self.cart_pole_angulo < -math.pi:
            self.cart_pole_angulo += 2.0 * math.pi

    def rendering(self):
        # RENDERING
        self.calcPhysics()

        tetha = self.cart_pole_angulo
        length = 150
        
        self.position = self.cart_pole_x*(self.screen_width/self.mov_totales), self.y_size - self.altura - 25
        self.top_position = int(self.position[0] + math.sin(tetha)*length), \
                    int(self.position[1] - math.cos(tetha)*length)

        self.fastMotion = False
        
        if self.fastMotion:
            self.clock.tick(200)
            self.screen.fill((200,200,255))
        else:
            self.screen.fill((255,255,255))                    
            self.clock.tick(1/self.TAU)


        self.screen.blit(self.background, self.backgroundRect)
        
        base = pygame.Rect(0,0,75,50)
        base.center = self.position

        floor = pygame.Rect(0, 0, self.x_size, self.altura)
        floor.bottom = self.y_size
        draw.rect(self.screen, (20,20,20), floor)

    def car_and_text(self):
        # Carro
        draw.rect(self.screen, self.color_carro , base)
        #self.screen.blit(self.texturaCarro, base, pygame.Rect(0,0,75,50))
        draw.line(self.screen, self.colorPendulo, self.position, self.top_position, 4)
        draw.circle(self.screen, self.colorPelota, self.top_position, 10)

        # Texto
        font = pygame.font.SysFont("Arial", 18, bold = True)
        textAngulo = font.render("Vel Angular: {0:.1f}   Angulo: {1:.1f} ".format(self.cart_pole_velocidad_angular, self.cart_pole_angulo) \
                    , 1, (0,0,0))

    def printing(self):
        if self.imprimir_angulo:
            self.screen.blit(textAngulo, (50, 30))

        if self.imprimir_tiempo:
            # Chequeo si llego a la zona objetivo,
            # y si es la primera vez que entra
            if abs(self.cart_pole_angulo) <= self.target_value:

                if not self.en_objetivo:
                    # Primera vez que llega
                    self.en_objetivo = True;
                    self.en_objetivo_tiempo_de_inicio = time.time()
                    tiempoTranscurrido = 0

                else:
                    tiempoTranscurrido = time.time() - self.en_objetivo_tiempo_de_inicio
    
                self.en_objetivo_ultimo_tiempo = tiempoTranscurrido
                
            else:    
                self.en_objetivo = False
                tiempoTranscurrido = 0


            if (tiempoTranscurrido > self.en_objetivo_tiempo_maximo):
                self.en_objetivo_tiempo_maximo = tiempoTranscurrido
                
            textTiempo = font.render("Tiempo Arriba: {0:.2f}".format(self.en_objetivo_ultimo_tiempo), 1, (0, 0, 0))
            textTiempoMaximo = font.render("Maximo: {0:.2f} segundos".format(self.en_objetivo_tiempo_maximo), 1, (0, 0, 0))

            self.screen.blit(textTiempo, (750, 30))
            #self.screen.blit(textUltimoTiempo, (750, 50))
            self.screen.blit(textTiempoMaximo, (750, 50))    

    def run(self, accion):

        if(self.acumulador_vueltas_por_movimiento == self.vueltas_por_movimiento):
            self.acumulador_vueltas_por_movimiento = 0

            self.movimiento_seleccionado = accion

            # Bordes
            if self.cart_pole_x >= 1 and self.movimiento_seleccionado == 1:
                self.cart_pole_x = 1
                self.movimiento_seleccionado = 0

            if self.cart_pole_x <= 0 and self.movimiento_seleccionado == -1:
                self.cart_pole_x = 0
                self.movimiento_seleccionado = 0
            
        self.acumulador_vueltas_por_movimiento = self.acumulador_vueltas_por_movimiento + 1
        rendering()
        car_and_text()
        printing()
        pygame.display.flip()


    def Finalizar(self):
        pygame.quit()


    def GetKeyPressed(self):
        return pygame.key.get_pressed()
        
        
