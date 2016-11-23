import pygame
import sys
import random
import level1_main
import menu
from pygame.locals import *

pygame.init()

reloj = pygame.time.Clock()
opciones = [
                ("Jugar", level1_main.Nivel_1),
                ("Creditos", menu.creditos),
                ("Salir", menu.salir_del_programa)
               ]
menu = menu.Menu(opciones = opciones)

def Nivel_2(pantalla):
    level1_main.pygame.mixer.music.play()
    puntos_influencia = 20
    contador = 0
    contador_inicio = 0
    num_jugadores = 0
    pag = 0
    level_2 = 0
    bool_pag = False
    bool_level2 = False
    bool_lose = False
    bandera = True
    cursor = level1_main.Cursor()
    hecho = False

    jugador_aux = level1_main.Jugador('Sprites/nave2.png')
    jugador_aux_3 = level1_main.Jugador('Sprites/nave2.png')
    jugador_aux_2 = level1_main.Jugador('Sprites/nave.png')
    jugador_aux_4 = level1_main.Jugador('Sprites/nave3.png')

    # inicializacion del Enemigo Boss
    enemigo = level1_main.Boss('Sprites/Bossnave.png')
    enemigo.rect.x = level1_main.DIMENSION_VENTANA[0] - 300
    enemigo.rect.y = random.randrange(0, level1_main.DIMENSION_VENTANA[1] - 300)
    enemigo.disparar = random.randrange(30, 100)
    vida_Boss = level1_main.fuente3.render(str(enemigo.vida), 0, level1_main.Blanco)

############### LISTAS #######################
    lista_todos =  pygame.sprite.Group()
    lista_enemigo = pygame.sprite.Group()
    lista_jugadores1 = pygame.sprite.Group()
    lista_jugadores2 = pygame.sprite.Group()
    lista_jugadores3 = pygame.sprite.Group()
    lista_balas_jugadores = pygame.sprite.Group()
    lista_balas_enemigo = pygame.sprite.Group()
###########################################

    while not hecho and bandera:
	pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(level1_main.boton.rect): # nave 1 en pantalla
                    level1_main.seleccion_nave.play()
                    jugador_aux = jugador_aux_3
                    contador += 1
                    lista_todos.add(jugador_aux)
                if cursor.colliderect(level1_main.boton1.rect): # nave 2 en pantalla
                    level1_main.seleccion_nave.play()
                    jugador_aux = jugador_aux_2
                    contador += 1
                    lista_todos.add(jugador_aux)
                if cursor.colliderect(level1_main.boton2.rect): #nave 3 en pantalla
                    level1_main.seleccion_nave.play()
                    jugador_aux = jugador_aux_4
                    contador += 1
                    lista_todos.add(jugador_aux)
                if cursor.colliderect(level1_main.boton_inicio.rect) and contador_inicio == 0:
		    lista_enemigo.add(enemigo)
    		    lista_todos.add(enemigo)
                    contador_inicio += 1
                    level1_main.pygame.mixer.music.stop()
                    level1_main.juego.play()
                   
            if evento.type == pygame.MOUSEBUTTONUP and contador > 0:
                contador -= 1
                if puntos_influencia > 0:
                    if jugador_aux == jugador_aux_2:
                        if puntos_influencia >= 3:
                            nave = level1_main.Jugador('Sprites/nave.png')
                            nave.vida += 1
                            lista_jugadores1.add(nave)
                            lista_todos.add(nave)
                            num_jugadores += 1
                            puntos_influencia -= 3
                            bool_lose = True
                    if jugador_aux == jugador_aux_3:
                        if puntos_influencia >= 2:
                            nave = level1_main.Jugador('Sprites/nave2.png')
                            lista_jugadores2.add(nave)
                            lista_todos.add(nave)
                            num_jugadores += 1
                            puntos_influencia -= 2
                            bool_lose = True
                    if jugador_aux == jugador_aux_4:
                        if puntos_influencia >= 5:
                            nave = level1_main.Jugador('Sprites/nave3.png')
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
            for a in lista_enemigo:
                if a.disparar == 0:
                    balae1 = level1_main.Laser1('Sprites/Sol.png')
		    balae2 = level1_main.Laser2('Sprites/Sol.png')
		    balae3 = level1_main.Laser3('Sprites/Sol.png')
		    balae4 = level1_main.Laser4('Sprites/Sol.png')
		    balae5 = level1_main.Laser5('Sprites/Sol.png')
                    balae1.rect.x = a.rect.x - 30
                    balae1.rect.y = a.rect.y
		    balae2.rect.x = a.rect.x - 30
                    balae2.rect.y = a.rect.y
		    balae3.rect.x = a.rect.x - 30
                    balae3.rect.y = a.rect.y
                    balae4.rect.x = a.rect.x - 30
                    balae4.rect.y = a.rect.y
		    balae5.rect.x = a.rect.x - 30
                    balae5.rect.y = a.rect.y
		    lista_balas_enemigo.add(balae1)
                    lista_todos.add(balae1)
		    lista_balas_enemigo.add(balae2)
                    lista_todos.add(balae2)
		    lista_balas_enemigo.add(balae3)
                    lista_todos.add(balae3)
		    lista_balas_enemigo.add(balae4)
                    lista_todos.add(balae4)
		    lista_balas_enemigo.add(balae5)
                    lista_todos.add(balae5)

            #### llenado de proyectiles de las naves ("jugadores")
            for e in lista_jugadores1:
               if e.disparar == 0:
                   balaj = level1_main.Proyectil_1('Sprites/proyectil.png')
                   balaj.rect.x = e.rect.x + 40
                   balaj.rect.y = e.rect.y + 10
                   lista_balas_jugadores.add(balaj)
                   lista_todos.add(balaj)
                   level1_main.sonido.play()
            for f in lista_jugadores2:
               if f.disparar == 0:
                   balaj = level1_main.Proyectil('Sprites/proyectil.png')
                   balaj.rect.x = f.rect.x + 40
                   balaj.rect.y = f.rect.y + 10
                   lista_balas_jugadores.add(balaj)
                   lista_todos.add(balaj)
                   level1_main.sonido.play()
            for g in lista_jugadores3:
               if g.disparar == 0:
                   balaj = level1_main.Proyectil_2('Sprites/proyectil.png')
                   balaj2 = level1_main.Proyectil_3('Sprites/proyectil.png')
                   balaj2.rect.x = g.rect.x + 40
                   balaj.rect.x = g.rect.x + 40
                   balaj2.rect.y = g.rect.y + 10
                   balaj.rect.y = g.rect.y + 10
                   lista_balas_jugadores.add(balaj)
                   lista_balas_jugadores.add(balaj2)
                   lista_todos.add(balaj)
                   lista_todos.add(balaj2)
                   level1_main.sonido.play()

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
                    level1_main.desaparece.play()

        for h2 in lista_jugadores2:
            ls_impactoe = pygame.sprite.spritecollide(h2, lista_balas_enemigo, True)
            for imp2 in ls_impactoe:
                print (h2.vida)
                h2.vida -= 1
                if h2.vida == 1:
                    lista_jugadores2.remove(h2)
                    lista_todos.remove(h2)
                    num_jugadores -= 1
                    level1_main.desaparece.play()

        for h3 in lista_jugadores3:
            ls_impactoe = pygame.sprite.spritecollide(h3, lista_balas_enemigo, True)
            for imp3 in ls_impactoe:
                print (h3.vida)
                h3.vida -= 1
                if h3.vida == 1:
                    lista_jugadores3.remove(h3)
                    lista_todos.remove(h3)
                    num_jugadores -= 1
                    level1_main.desaparece.play()

 ########### Colision de una bala del jugador con un enemigo ###########################
        for k in lista_balas_jugadores:
            ls_impacto1 = pygame.sprite.spritecollide(k, lista_enemigo, False)
            for impacto1 in ls_impacto1:
                lista_balas_jugadores.remove(k)
                lista_todos.remove(k)
		puntos_influencia += 1
		print("Boss_life: %d" % enemigo.vida )
		vida_Boss = level1_main.fuente3.render(str(enemigo.vida), 0, level1_main.Blanco)
                level1_main.explosion.play()
		if enemigo.vida > 0:
                	enemigo.vida -= 1
		
########################################################################################

        jugador_aux.rect.x = pos[0] - 30
        jugador_aux.rect.y = pos[1] - 30

        if enemigo.vida == 0:
            level_2 = 1
            bool_level2 = True
	    bandera = False
            level1_main.juego.stop()
	    level1_main.win.play()

        if num_jugadores == 0 and bool_lose:
            pag += 1
            bandera = False
            bool_pag = True
            level1_main.juego.stop()
            level1_main.pygame.mixer.music.stop()
            level1_main.explosion2.play()
            level1_main.muerto.play()


        pantalla.blit(level1_main.fondo, [0, 0])
                   
        while (not bandera):
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP and bool_pag:
                    pag += 1
                if event.type == pygame.KEYUP and bool_level2:
                    level_2 += 1
           	if pag == 1:
                    pantalla.blit(level1_main.muerte, [0, 0])
                    level1_main.to_level_2.play()
                if pag == 2:
                    level1_main.juego.stop()
                    level1_main.pygame.mixer.music.stop()
                    while not bandera:
                        for e in pygame.event.get():
                            if e.type == QUIT:
                                bandera = True
                        pantalla.blit(level1_main.fondo, (0, 0))
                        menu.actualizar()
                        menu.imprimir(pantalla)
                        pantalla.blit(level1_main.Titulo, (280, level1_main.DIMENSION_VENTANA[1] / 2 - 280))
			level1_main.pygame.mixer.music.play()
			level1_main.muerto.stop()
                        pygame.display.flip()
			
                        level1_main.muerto.stop()
                        reloj.tick(60)
                    
                if level_2 == 1:
                    pantalla.fill(level1_main.NEGRO)
                    pantalla.blit(level1_main.texto3, (90, level1_main.DIMENSION_VENTANA[1] / 2 - 70))                    
                if level_2 == 2:
                    pantalla.fill(level1_main.NEGRO)
                    pantalla.blit(level1_main.texto7, (250, level1_main.DIMENSION_VENTANA[1] / 2 - 70))
                if level_2 == 3:
		    level1_main.win.stop()
                    while not bandera:
                        for e in pygame.event.get():
                            if e.type == QUIT:
                                bandera = True
				quit()
                        pantalla.blit(level1_main.fondo, (0, 0))
                        menu.actualizar()
                        menu.imprimir(pantalla)
			pantalla.blit(level1_main.Titulo, (280, level1_main.DIMENSION_VENTANA[1] / 2 - 280))
                        level1_main.pygame.mixer.music.play()
                        level1_main.juego.stop()
                        level1_main.muerto.stop()
			pygame.display.flip()
                        reloj.tick(60)

           pygame.display.flip()

	puntos_pantalla = level1_main.fuente3.render(str(puntos_influencia), 0, level1_main.Blanco)
	cursor.update()
        lista_enemigo.update()
        lista_jugadores1.update()
        lista_jugadores2.update()
        lista_jugadores3.update()
        lista_balas_jugadores.update()
        lista_balas_enemigo.update()
        level1_main.boton.update(pantalla,cursor)
        level1_main.boton1.update(pantalla,cursor)
        level1_main.boton2.update(pantalla,cursor)
        level1_main.boton_inicio.update(pantalla, cursor)
        level1_main.boton_reset.update(pantalla, cursor)
        pantalla.blit(puntos_pantalla, (140,540))
        pantalla.blit(vida_Boss, (880, 10))
        pantalla.blit(level1_main.texto8, (700, 10))
      	pantalla.blit(level1_main.texto6, (12, 540))
	pantalla.blit(level1_main.texto9,(10,65))
        pantalla.blit(level1_main.texto10, (80, 65))
        pantalla.blit(level1_main.texto11, (150, 65))
        lista_todos.draw(pantalla)
        pygame.display.flip()
        reloj.tick(60)


