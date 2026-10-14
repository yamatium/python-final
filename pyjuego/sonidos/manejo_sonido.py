import pygame

entrar_sfx = pygame.mixer.Sound("pyjuego/sonidos/pistas_audio/SD_0099.mp3")
salir_sfx = pygame.mixer.Sound("pyjuego/sonidos/pistas_audio/SD_0111.mp3")

def entrar_sonido()-> None:
    #sonido al hacer click

    entrar_sfx.play()
    pygame.time.wait(int(salir_sfx.get_length() * 1000))

def salir_sonido()-> None:
    #sonido al salir de alguna pantalla, silenciar musica
    salir_sfx.play()
    pygame.time.wait(int(salir_sfx.get_length() * 1000)) #regresa y convierte segundos en ms para time.wait

def musica_menu(cancion:int)-> None:
    #musica del menu y juego
    if cancion == 1:
        pygame.mixer.music.load("pyjuego/sonidos/pistas_audio/eugene.mp3")
    else:
        pygame.mixer.music.load("pyjuego/sonidos/pistas_audio/safe_place.mp3")
    
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def manejar_musica()-> None:
    #manejo del boton de musica
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()