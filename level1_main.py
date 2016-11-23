import pygame
import menu
import random
import level2
from pygame.locals import *

pygame.init()

#Constantes
NEGRO = (0, 0, 0)
Blanco = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
reloj = pygame.time.Clock()
DIMENSION_VENTANA = [975, 585]
pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
pygame.display.set_caption("Galaxy War")


################# IMAGENES  ########################
fondo = pygame.image.load('Fondo.png')
kame = pygame.image.load('Sprites/proyectil.png')
muerte = pygame.image.load('perdiste.png')

#################### SONIDOS #######################
pygame.mixer.music.load('audio/space.wav')
muerto = pygame.mixer.Sound('audio/Muerto.wav')
win = pygame.mixer.Sound('audio/win.wav')
juego = pygame.mixer.Sound('audio/through space.wav')
sonido = pygame.mixer.Sound('audio/disparo_nave.wav')
explosion = pygame.mixer.Sound('audio/explosion.wav')
explosion2 = pygame.mixer.Sound('audio/explosion2.wav')
seleccion_nave = pygame.mixer.Sound('audio/seleccion_nave.wav')
desaparece = pygame.mixer.Sound('audio/dead.wav')
to_level_2 = pygame.mixer.Sound('audio/space laser.wav')
to_level_2.set_volume(0.5)
sonido.set_volume(0.8)
muerto.set_volume(1.0)
explosion.set_volume(1.0)
explosion2.set_volume(0.3)

####################### TEXTO   #######################
fuente = pygame.font.Font('Techno.ttf', 90)
fuente3 = pygame.font.Font('computerized.ttf', 40)
fuente2 = pygame.font.Font('computerized.ttf', 20)
texto = fuente.render("NIVEL SUPERADO", 0, Blanco)
texto3 = fuente.render("ACABASTE CON ELLOS!!!", 0, Blanco)
texto4 = fuente.render("SIGUIENTE NIVEL:", 0, Blanco)
texto5 = fuente3.render("LIFE: ", 0, Blanco)
texto6 = fuente3.render("POINTS: ", 0, Blanco)
texto7 = fuente.render("HAS GANADO!!! ", 0, Blanco)
texto8 = fuente3.render("BOSS LIFE: ", 0, Blanco)
texto9 = fuente2.render("- 2 P", 0, Blanco)
texto10 = fuente2.render("- 3 P", 0, Blanco)
texto11 = fuente2.render("- 5 P", 0, Blanco)
Titulo = fuente.render("GALAXY WAR", 0, Blanco)
creditos_game = fuente.render("Created by: ", 0, Blanco)
nombre = fuente.render("EDISON JAVIER COLORADO", 0, Blanco)

'''
grid = []
for fila in range(9):
    grid.append([])
    for columna in range(15):
        grid[fila].append(0)  # Anade una celda
'''
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)

    def update(self):
        self.left,self.top = pygame.mouse.get_pos()



class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x = 200,y = 200):
        self.imagen_normal = imagen1
        self.imagen_seleccion = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left,self.rect.top = (x,y)

    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else:
            self.imagen_actual = self.imagen_normal
        pantalla.blit(self.imagen_actual,self.rect)


class Jugador(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.disparar = random.randrange(200)
        self.vida = 5

    def update(self):
        self.disparar -= 1
        if self.disparar < 0:
            self.disparar = random.randrange(200)

# Clase que inicializa Enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.disparar =  random.randrange(280) #100
        self.direccion = 0

    def update(self):
        if self.rect.y >= (DIMENSION_VENTANA[1] - 100):
            self.direccion = 1
        if self.rect.y <= 10:
            self.direccion = 0

        if self.direccion == 0:
            self.rect.y += 5
        else:
            self.rect.y -= 5
        self.disparar -= 10 #frecuencia de tiro (+ --> +)
        if self.disparar < 0:
            self.disparar = random.randrange(280) #100

class Boss(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.disparar = random.randrange(100)
        self.direccion = 0
        self.vida = 500

    def update(self):
        if self.rect.y >= (DIMENSION_VENTANA[1] - 230):
            self.direccion = 1
        if self.rect.y <= 10:
            self.direccion = 0
        if self.direccion == 0:
            self.rect.y += random.randrange(20)
            # self.rect.x += random.randrange(5)
        else:
            self.rect.y -= random.randrange(20)
            self.disparar -= 4  # frecuencia de disparos
        if self.disparar < 0:
            self.disparar = random.randrange(100)

########## Clases que inicializan los proyectiles de las naves ("jugadores") #######

#Horizontal
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 1

    def update(self):
        if self.jugador == 1:
            self.rect.x += 10
        else:
            self.rect.x -= 10
#Diagonal hacia arriba
class Proyectil_1(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0

    def update(self):
        if (self.jugador == 0):
            self.rect.x += 10
            self.rect.y -= 2
#Curvo hacia arriba
class Proyectil_2(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0
        self.x = 0
        self.r = 15
        self.y = self.r
        self.p = (5 / 4) - self.r

    def update(self):
        if (self.jugador == 0):
            self.x += 1
            if (self.p < 0):
                 self.p = self.p + 2 * self.x + 1
            else:
                 self.y = self.y - 1
                 self.p = self.p + 2 * (self.x - self.y) + 1
            self.rect.x += self.x
            self.rect.y += self.y
#Curvo hacia abajo
class Proyectil_3(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0
        self.x = 0
        self.r = 15
        self.y = self.r
        self.p = (5 / 4) - self.r

    def update(self):
        if (self.jugador == 0):
            self.x += 1
            if (self.p < 0):
                self.p = self.p + 2 * self.x + 1
            else:
                self.y = self.y - 1
                self.p = self.p + 2 * (self.x - self.y) + 1
                self.rect.x += self.x
                self.rect.y -= self.y


######### Clases que inicializan los proyectiles de los enemigos #######

#Clase de proyectil 1
class Laser1(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0

    def update(self):
        if (self.jugador == 0):
            self.rect.x -= 5
            self.rect.y -= 2

# Clase de proyectil 2
class Laser2(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0

    def update(self):
        if (self.jugador == 0):
            self.rect.x -= 5

# Clase de proyectil 3
class Laser3(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0

    def update(self):
        if (self.jugador == 0):
            self.rect.x -= 5
            self.rect.y += 2

# Clase de proyectil 4 (Proyectil curvo hacia arriba)
class Laser4(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0
        self.x = 0
        self.r = 20
        self.y = self.r
        self.p = (5 / 4) - self.r

    def update(self):
        if (self.jugador == 0):
            self.x += 1
            if (self.p < 0):
                self.p = self.p + 2 * self.x + 1
            else:
                self.y = self.y - 1
                self.p = self.p + 2 * (self.x - self.y) + 1
            self.rect.x -= self.x
            self.rect.y -= self.y

# Clase de proyectil 5 (Proyectil curvo hacia abajo)
class Laser5(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.jugador = 0
        self.x = 0
        self.r = 20
        self.y = self.r
        self.p = (5 / 4) - self.r

    def update(self):
        if (self.jugador == 0):
            self.x += 1
            if (self.p < 0):
                self.p = self.p + 2 * self.x + 1
            else:
                self.y = self.y - 1
                self.p = self.p + 2 * (self.x - self.y) + 1
                self.rect.x -= self.x
                self.rect.y += self.y


################### SPRITES NAVES ###################
nave1 = pygame.image.load('bottoms/nave2.png')
nave2 = pygame.image.load('bottoms/nave2_boton.png')
nave3 =  pygame.image.load('bottoms/nave.png')
nave4 =  pygame.image.load('bottoms/nave_boton.png')
nave5 =  pygame.image.load('bottoms/nave3.png')
nave6 =  pygame.image.load('bottoms/nave3_boton.png')

##################### BOTONES###############################
botton_start_1 = pygame.image.load('bottoms/start_button.png')
botton_start_2 = pygame.image.load('bottoms/start_button2.png')
botton_reset_1 = pygame.image.load('bottoms/reset_button.png')
botton_reset_2 = pygame.image.load('bottoms/reset_button2.png')
boton = Boton(nave1,nave2,x = 10,y = 10)
boton1 = Boton(nave3,nave4,x =  90, y = 20)
boton2 = Boton(nave5,nave6,x = 160,y = 10)
boton_inicio = Boton(botton_start_1,botton_start_2,x = 220,y = 10)
boton_reset = Boton(botton_reset_1,botton_reset_2,x= 290,y = 7)


def Nivel_1():
    puntos_influencia = 10
    contador = 0
    contador_inicio = 0
    num_enemigos = 16
    num_jugadores = 0
    pag = 0
    level_2 = 0
    bool_pag = False
    bool_level2 = False
    bool_lose = False
    bandera = True
    cursor = Cursor()
    hecho = False
    jugador_aux = Jugador('Sprites/nave2.png')
    jugador_aux_3 = Jugador('Sprites/nave2.png')
    jugador_aux_2 = Jugador('Sprites/nave.png')
    jugador_aux_4 = Jugador('Sprites/nave3.png')

    ####################### LISTAS #######################
    lista_todos = pygame.sprite.Group()
    lista_jugadores1 = pygame.sprite.Group()
    lista_jugadores2 = pygame.sprite.Group()
    lista_jugadores3 = pygame.sprite.Group()
    lista_enemigos1 = pygame.sprite.Group()
    lista_enemigos2 = pygame.sprite.Group()
    lista_enemigos3 = pygame.sprite.Group()
    lista_enemigos4 = pygame.sprite.Group()
    lista_balas_jugadores = pygame.sprite.Group()
    lista_balas_enemigo = pygame.sprite.Group()

    while not hecho and bandera:
        pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(boton.rect): # nave 1 en pantalla
                    seleccion_nave.play()
                    jugador_aux = jugador_aux_3
                    contador += 1
                    lista_todos.add(jugador_aux)
                if cursor.colliderect(boton1.rect): # nave 2 en pantalla
                    seleccion_nave.play()
                    jugador_aux = jugador_aux_2
                    contador += 1
                    lista_todos.add(jugador_aux)
                if cursor.colliderect(boton2.rect): #nave 3 en pantalla
                    seleccion_nave.play()
                    jugador_aux = jugador_aux_4
                    contador += 1
                    lista_todos.add(jugador_aux)
                if cursor.colliderect(boton_inicio.rect) and contador_inicio == 0:
                    contador_inicio += 1
                    pygame.mixer.music.stop()
                    juego.play()
                    #####  Ciclos de llenado de las listas de enemigos
                    for x in range(4):
                        x += 1
                        enemigo = Enemigo('Sprites/nave_enemiga_2.png')
                        enemigo.rect.x = random.randrange(DIMENSION_VENTANA[0] / 2, DIMENSION_VENTANA[0] - 95)
                        enemigo.rect.y = random.randrange(0, DIMENSION_VENTANA[1] - 100)
                        enemigo.disparar = random.randrange(30, 100)
                        lista_todos.add(enemigo)
                        lista_enemigos1.add(enemigo)
                    for y in range(4):
                        y += 1
                        enemigo = Enemigo('Sprites/nave_enemiga_3.png')
                        enemigo.rect.x = random.randrange(DIMENSION_VENTANA[0] / 2, DIMENSION_VENTANA[0] - 95)
                        enemigo.rect.y = random.randrange(0, DIMENSION_VENTANA[1] - 100)
                        enemigo.disparar = random.randrange(30, 100)
                        lista_todos.add(enemigo)
                        lista_enemigos2.add(enemigo)
                    for w in range(4):
                        w += 1
                        enemigo = Enemigo('Sprites/nave_enemiga_4.png')
                        enemigo.rect.x = random.randrange(DIMENSION_VENTANA[0] / 2, DIMENSION_VENTANA[0] - 95)
                        enemigo.rect.y = random.randrange(0, DIMENSION_VENTANA[1] - 100)
                        enemigo.disparar = random.randrange(30, 100)
                        lista_todos.add(enemigo)
                        lista_enemigos3.add(enemigo)
                    for z in range(4):
                        z += 1
                        enemigo = Enemigo('Sprites/nave_enemiga_5.png')
                        enemigo.rect.x = random.randrange(DIMENSION_VENTANA[0] / 2, DIMENSION_VENTANA[0] - 95)
                        enemigo.rect.y = random.randrange(0, DIMENSION_VENTANA[1] - 100)
                        enemigo.disparar = random.randrange(30, 100)
                        lista_todos.add(enemigo)
                        lista_enemigos4.add(enemigo)

            if evento.type == pygame.MOUSEBUTTONUP and contador > 0:
                contador -= 1
                if puntos_influencia > 0:
                    if jugador_aux == jugador_aux_2:
                        if puntos_influencia >= 3:
                            nave = Jugador('Sprites/nave.png')
                            nave.vida += 1
                            lista_jugadores1.add(nave)
                            lista_todos.add(nave)
                            num_jugadores += 1
                            puntos_influencia -= 3
                            bool_lose = True
                    if jugador_aux == jugador_aux_3:
                        if puntos_influencia >= 2:
                            nave = Jugador('Sprites/nave2.png')
                            lista_jugadores2.add(nave)
                            lista_todos.add(nave)
                            num_jugadores += 1
                            puntos_influencia -= 2
                            bool_lose = True
                    if jugador_aux == jugador_aux_4:
                        if puntos_influencia >= 5:
                            nave = Jugador('Sprites/nave3.png')
                            nave.vida += 2
                            lista_jugadores3.add(nave)
                            lista_todos.add(nave)
                            num_jugadores += 1
                            puntos_influencia -= 5
                            bool_lose = True

                    if pos[1] > 135:
                        nave.rect.x = pos[0] - 40
                        nave.rect.y = pos[1] - 40
                    else:
                        nave.rect.x = pos[0] - 40 + 90
                        nave.rect.y = pos[1] - 40 + 135

                lista_todos.remove(jugador_aux)

        if contador_inicio == 1:
            ##### Ciclos de llenado de balas de enemigos
            for a in lista_enemigos1:
                if a.disparar == 0:
                    balae = Laser1('Sprites/BlueLaser.png')
                    balae.rect.x = a.rect.x - 30
                    balae.rect.y = a.rect.y
                    balae.jugador = 0
                    lista_balas_enemigo.add(balae)
                    lista_todos.add(balae)
            for b in lista_enemigos2:
                if b.disparar == 0:
                    balae = Laser2('Sprites/RedLaser.png')
                    balae.rect.x = b.rect.x - 30
                    balae.rect.y = b.rect.y
                    balae.jugador = 0
                    lista_balas_enemigo.add(balae)
                    lista_todos.add(balae)
            for c in lista_enemigos3:
                if c.disparar == 0:
                    balae = Laser3('Sprites/GreenLaser.png')
                    balae.rect.x = c.rect.x - 30
                    balae.rect.y = c.rect.y
                    balae.jugador = 0
                    lista_balas_enemigo.add(balae)
                    lista_todos.add(balae)
            for d in lista_enemigos4:
                if d.disparar == 0:
                    balae = Laser4('Sprites/BlueLaser.png')
                    balae.rect.x = d.rect.x - 30
                    balae.rect.y = d.rect.y
                    balae.jugador = 0
                    lista_balas_enemigo.add(balae)
                    lista_todos.add(balae)

            #### llenado de proyectiles de las naves ("jugadores")
            for e in lista_jugadores1:
               if e.disparar == 0:
                   balaj = Proyectil_1('Sprites/proyectil.png')
                   balaj.rect.x = e.rect.x + 40
                   balaj.rect.y = e.rect.y + 10
                   lista_balas_jugadores.add(balaj)
                   lista_todos.add(balaj)
                   sonido.play()
            for f in lista_jugadores2:
               if f.disparar == 0:
                   balaj = Proyectil('Sprites/proyectil.png')
                   balaj.rect.x = f.rect.x + 40
                   balaj.rect.y = f.rect.y + 10
                   lista_balas_jugadores.add(balaj)
                   lista_todos.add(balaj)
                   sonido.play()
            for g in lista_jugadores3:
               if g.disparar == 0:
                   balaj = Proyectil_2('Sprites/proyectil.png')
                   balaj2 = Proyectil_3('Sprites/proyectil.png')
                   balaj2.rect.x = g.rect.x + 40
                   balaj.rect.x = g.rect.x + 40
                   balaj2.rect.y = g.rect.y + 10
                   balaj.rect.y = g.rect.y + 10
                   lista_balas_jugadores.add(balaj)
                   lista_balas_jugadores.add(balaj2)
                   lista_todos.add(balaj)
                   lista_todos.add(balaj2)
                   sonido.play()

############################# COLISIONES ########################################

        ##### Colision de un jugador con la bala de un enemigo ###########
        for h1 in lista_jugadores1:
            ls_impactoe = pygame.sprite.spritecollide(h1, lista_balas_enemigo, True)
            for imp1 in ls_impactoe:
                print (h1.vida)
                h1.vida -= 1
                if h1.vida == 0:
                    lista_jugadores1.remove(h1)
                    lista_todos.remove(h1)
                    num_jugadores -= 1
                    desaparece.play()

        for h2 in lista_jugadores2:
            ls_impactoe = pygame.sprite.spritecollide(h2, lista_balas_enemigo, True)
            for imp2 in ls_impactoe:
                print (h2.vida)
                h2.vida -= 1
                if h2.vida == 1:
                    lista_jugadores2.remove(h2)
                    lista_todos.remove(h2)
                    num_jugadores -= 1
                    desaparece.play()

        for h3 in lista_jugadores3:
            ls_impactoe = pygame.sprite.spritecollide(h3, lista_balas_enemigo, True)
            for imp3 in ls_impactoe:
                print (h3.vida)
                h3.vida -= 1
                if h3.vida == 1:
                    lista_jugadores3.remove(h3)
                    lista_todos.remove(h3)
                    num_jugadores -= 1
                    desaparece.play()
        ##################################################################

        ######## Colision de una bala del jugador con un enemigo
        for k in lista_balas_jugadores:
            ls_impacto1 = pygame.sprite.spritecollide(k, lista_enemigos1, True)
            for impacto1 in ls_impacto1:
                lista_balas_jugadores.remove(k)
                lista_todos.remove(k)
                num_enemigos -= 1
                explosion.play()

        for l in lista_balas_jugadores:
            ls_impacto2 = pygame.sprite.spritecollide(l, lista_enemigos2, True)
            for impacto2 in ls_impacto2:
                lista_balas_jugadores.remove(l)
                lista_todos.remove(l)
                num_enemigos -= 1
                explosion.play()

        for m in lista_balas_jugadores:
            ls_impacto3 = pygame.sprite.spritecollide(m, lista_enemigos3, True)
            for impacto3 in ls_impacto3:
                lista_balas_jugadores.remove(m)
                lista_todos.remove(m)
                num_enemigos -= 1
                explosion.play()

        for n in lista_balas_jugadores:
            ls_impacto4 = pygame.sprite.spritecollide(n, lista_enemigos4, True)
            for impacto3 in ls_impacto4:
                lista_balas_jugadores.remove(n)
                lista_todos.remove(n)
                num_enemigos -= 1
                explosion.play()


########################################################################################

        jugador_aux.rect.x = pos[0] - 30
        jugador_aux.rect.y = pos[1] - 30

        if num_enemigos == 0:
            level_2 = 1
            bandera = False
            bool_level2 = True
            juego.stop()

        if num_jugadores == 0 and bool_lose:
            pag += 1
            bandera = False
            bool_pag = True
            juego.stop()
            pygame.mixer.music.stop()
            explosion2.play()
            muerto.play()


        pantalla.blit(fondo, [0, 0])

        while (not bandera):
            pos = pygame.mouse.get_pos()
            xg = pos[0]
            yg = pos[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP and bool_pag:
                    pag += 1
                if event.type == pygame.KEYUP and bool_level2:
                    level_2 += 1
            if pag == 1:
                pantalla.blit(muerte, [0, 0])
            if pag == 2:
                pygame.mixer.music.stop()
                while not bandera:
                    for e in pygame.event.get():
                        if e.type == QUIT:
                            bandera = True
                            quit()
                    pantalla.blit(fondo, (0, 0))
                    menu.actualizar()
                    menu.imprimir(pantalla)
                    pantalla.blit(Titulo, (250, DIMENSION_VENTANA[1] - 550))
                    pygame.display.flip()
		    muerto.stop()
                    pygame.mixer.music.play()
                    
                    reloj.tick(60)

            if level_2 == 1:
                pantalla.fill(NEGRO)
                pantalla.blit(texto, (200, DIMENSION_VENTANA[1] / 2 - 70))
                to_level_2.play()
            if level_2 == 2:
                pantalla.fill(NEGRO)
                pantalla.blit(texto3, (90, DIMENSION_VENTANA[1] / 2 - 70))
            if level_2 == 3:
                pantalla.fill(NEGRO)
                pantalla.blit(texto4, (200, DIMENSION_VENTANA[1] / 2 - 70))
            if level_2 == 4:
                hecho = False
                bandera = True
                pygame.mixer.music.stop()
                level2.Nivel_2(pantalla)

            pygame.display.flip()


        puntos_pantalla = fuente3.render(str(puntos_influencia), 0, Blanco)
        cursor.update()
        lista_enemigos1.update()
        lista_enemigos2.update()
        lista_enemigos3.update()
        lista_enemigos4.update()
        lista_jugadores1.update()
        lista_jugadores2.update()
        lista_jugadores3.update()
        lista_balas_jugadores.update()
        lista_balas_enemigo.update()
        boton.update(pantalla,cursor)
        boton1.update(pantalla,cursor)
        boton2.update(pantalla,cursor)
        boton_inicio.update(pantalla, cursor)
        boton_reset.update(pantalla, cursor)
        pantalla.blit(puntos_pantalla, (140,540))
        pantalla.blit(texto6, (12, 540))
        pantalla.blit(texto9,(10,65))
        pantalla.blit(texto10, (80, 65))
        pantalla.blit(texto11, (150, 65))
        lista_todos.draw(pantalla)
        pygame.display.flip()
        reloj.tick(60)

if __name__ == '__main__':

    pygame.init()
    pygame.mixer.music.play()

    salir = False
    opciones = [
                ("Jugar", Nivel_1),
                ("Creditos", menu.creditos),
                ("Salir", menu.salir_del_programa)
               ]

    pygame.font.init()
    pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
    pygame.display.set_caption("Galaxy War")
    menu = menu.Menu(opciones = opciones)

    while not salir:
        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        pantalla.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(pantalla)
        pantalla.blit(Titulo, (250, DIMENSION_VENTANA[1] - 550))
        pygame.display.flip()
        reloj.tick(60)
