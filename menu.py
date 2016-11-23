import pygame
import sys
from pygame.locals import *

pygame.init()

ALTO = 585
ANCHO = 975
Blanco = (255, 255, 255)
sonido = pygame.mixer.Sound('audio/puntero_menu.wav')
fondo = pygame.image.load('Fondo.png')
fuente = pygame.font.Font('Techno.ttf', 90)
creditos_game = fuente.render("Created by: ", 0, Blanco)
nombre = fuente.render("EDISON JAVIER COLORADO", 0, Blanco)

DIMENSION_VENTANA = [975, 585]
pantalla = pygame.display.set_mode(DIMENSION_VENTANA)

class Opcion:
    def __init__(self, fuente, titulo, x, y, paridad, funcion_asignada):
        self.imagen_normal = fuente.render(titulo, 1, Blanco)
        self.imagen_destacada = fuente.render(titulo, 1, Blanco)
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y + 10
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def actualizar(self):
        destino_x = 400
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada
        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:
    def __init__(self, x, y, dy):
        self.image = pygame.image.load('Sprites/proyectil.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x - 20
        self.y_inicial = y + 45  # y inicial del cursor
        self.dy = dy + 25
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)


# Clase que inicializa un menu
class Menu:
    def __init__(self, opciones):
        self.opciones = []
        fuente = pygame.font.Font('Techno.ttf', 72)
        x = 400  # posicion del cursor del menu
        y = 220
        paridad = 1

        self.cursor = Cursor(x - 30, y, 30)

        for titulo, funcion in opciones:
            self.opciones.append(Opcion(fuente, titulo, x, y, paridad, funcion))
            y += 60
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self):
        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.seleccionado -= 1
                sonido.play()
            elif k[K_DOWN]:
                self.seleccionado += 1
                sonido.play()
            elif k[K_RETURN]:
                # Invoca a la funcion asociada a la opcion.
                self.opciones[self.seleccionado].activar()
                sonido.play()

        # procura que el cursor este entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1

        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()

        for o in self.opciones:
            o.actualizar()

    def imprimir(self, screen):
        self.cursor.imprimir(screen)

        for opcion in self.opciones:
            opcion.imprimir(screen)

def creditos():
    salir = False
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == 27:
                    salir = True
            if event.type == QUIT:
                salir = True
        pygame.display.flip()
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(creditos_game, (300, ALTO / 2 - 200))
        pantalla.blit(nombre, (50, ALTO / 2))


def salir_del_programa():
    sys.exit(0)