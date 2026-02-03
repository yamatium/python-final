def jijo() -> None:
    #imprime
    print("jijoxido de potasio")
import random
from .validaciones import *
from .acertijos import * 

MAX_INTENTOS_SALA = 2
CANTIDAD_SALAS = 4
CANTIDAD_PREGUNTAS = 20

def menu() -> None:
    salir = False
    while not salir:
        mostar_menu_opciones()
        opcion = input("Seleccione una opcion: ")
        match opcion:
            case "1":
                print("comenzar juego")
                #sala_inicial()
                ciclo_segun_jugadores()
            case "2":
                print("comenzar torneo")
                modo_torneo()
            case "3":
                print("Ver archivo puntaje")
                leer_puntuacion()
                #leer puntaje.csv
            case "4":
                print("Gracias por usar el programa. ¡Hasta luego!")
                salir = True
            case _:
                pass

def mostar_menu_opciones() -> None:
    #imprime las opciones al empezar el programa
    print("Bienvenido!")
    print("1. Modo normal")
    print("2. Modo torneo")
    print("3. Ver puntuaciones")
    print("4. Salir")

def elegir_numero(cantidad_preguntas:int) -> int:
    #elije un numero para traer una pregunta del diccionario
    maximo = cantidad_preguntas
    numero_elejido = random.randint(0,maximo)
    #print(numero_elejido)
    return numero_elejido

def llamar_pregunta(numero:int,jugar:bool,puntaje:int):

    intentos = 0
    while intentos < MAX_INTENTOS_SALA:
        print(preguntas[numero]['pregunta'])
        for opcion in preguntas[numero]['opciones']:
            print(opcion)
        print("-----------------------------")
        respuesta = input("ingrese su respuesta: ")
        if respuesta == preguntas[numero]['respuesta']:
            print('correcto')
            print("-----------------------------")
            puntaje += preguntas[numero]['valor_puntaje']
            break
        else:
            respuesta_incorrecta()
        intentos +=1
    else:
        jugar = False
    return jugar,puntaje

def respuesta_incorrecta() -> None:
    #imprime un mensaje de respuesta incorrecta
    print("-----------------------------")
    print("respuesta incorrecta")
    print("-----------------------------")


def sala_inicial() -> None:
    #traer diccionario de acertijos,una lista de numeros y un numero para agarrar una pregunta de aceritjos.py 
    #estado_juego si puede jugar segun sus intentos
    nombre = nombre_jugador()
    puede_jugar = True
    puntaje = 0
    sala_actual = 1
    numero = elegir_numero(CANTIDAD_PREGUNTAS)

    while puede_jugar and sala_actual <= CANTIDAD_SALAS:
        puede_jugar, puntaje = llamar_pregunta(numero,puede_jugar,puntaje)
        sala_actual +=1
        numero = elegir_numero(CANTIDAD_PREGUNTAS)
    else:
        #estado = estado_juego_final(puede_jugar)
        #terminar_juego(nombre,puede_jugar,puntaje)
        #grabar_resultados(nombre,puntaje,puede_jugar)
        terminar_juego(nombre,puede_jugar,puntaje)

def ciclo_segun_jugadores() -> None:
    torneo = False
    cant_jugadores = validar_cantidad_jugadores(torneo)
    for i in range(cant_jugadores):
        sala_inicial()

def nombre_jugador() -> str:
    #pregunta nombre del jugador y lo devuelve validado
    nombre = validar_nombre()
    print(f"bienvenido {nombre} al juego ")
    return nombre

def estado_juego_final(estado_juego:bool):
    #regrese el estado final de las salas del jugador para grabar archivo

    if estado_juego:
        estado = "completo"
    else:
        estado = 'no completo'
    
    return estado


def terminar_juego(nombre:str, estado_partida:bool, puntaje:int):

    if estado_partida:
        estado_juego = "termino"
        print("-----------------------------")
        print(f"Felicidades {nombre} \nhas ganado con un puntaje de : {puntaje} \nestado final: completo")
        print("-----------------------------")
    else:
        estado_juego = "No termino"
        print("-----------------------------")
        print(f"Has perdido {nombre} \ncon un puntaje de : {puntaje} \nestado final: no completo")
        print("-----------------------------")

    with open("puntajes.csv", 'a') as archivo:
        archivo.write(f"Jugador: {nombre} | estado final: { estado_juego} | puntaje: {puntaje}\n")


def leer_puntuacion() -> None:
    print("-" * 50)
    with open("puntajes.csv", "r") as archivo:
        lista_texto = archivo.readlines()
        for linea in lista_texto:
            print(linea, end="")
    print("-" * 50)


def modo_torneo():
    ciclo_segun_torneo()

def ciclo_segun_torneo() -> None:

    torneo = True    
    cant_jugadores = validar_cantidad_jugadores(torneo)
    jugadores = []
    #la lista empieza aca sino en sala_torneo se borra y solo manda el ultimo jugador
    for i in range(cant_jugadores):
        jugador = sala_torneo()
        jugadores.append(jugador)
        #cuando termine el loop comparar y encontrar el puntaje maximo o su empate
        #comparar_resultados(jugador,)
    mostrar_datos_torneo(jugadores)


def sala_torneo() -> list:
    nombre = nombre_jugador()
    puede_jugar = True
    puntaje = 0
    sala_actual = 0
    numero = elegir_numero(CANTIDAD_PREGUNTAS)

    while puede_jugar and sala_actual <= CANTIDAD_SALAS:
        puede_jugar, puntaje = llamar_pregunta(numero,puede_jugar,puntaje)
        sala_actual +=1
        numero = elegir_numero(CANTIDAD_PREGUNTAS)
    else:
        #envia los datos del jugador arreglada en nested list para ser usada en ciclo_segun_torneo()
        return [nombre, [puntaje, puede_jugar, sala_actual]] #traer sala actual


def mostrar_datos_torneo(jugadores: list) -> None:
    print("\nResultados torneo: ")
    for jugador in jugadores:
        nombre = jugador[0]
        puntuacion = jugador[1][0]
        termino = jugador[1][1]
        print("-----------------------------")
        print(nombre,puntuacion,termino)
    
    print("-----------------------------")
    ganadores, maximo_puntaje = comparar_resultados_torneo(jugadores)
    if len(ganadores) >= 2:
        print(f"Los ganadores fueron {ganadores}, con un puntaje de {maximo_puntaje}")
        print("-----------------------------")
    else:
        print(f"El ganador fue {ganadores}, con un puntaje de {maximo_puntaje}")
        print("-----------------------------")
    ganadores_sala , maximo_sala = comparar_salas_resultado(jugadores)
    if len(ganadores_sala) >= 2:
        print(f"Los jugadores que mas lejos llegaron fueron {ganadores_sala}, con {maximo_sala} salas")
        print("-----------------------------")
    else:
        print(f"El jugador que mas lejos llego fue {ganadores_sala}, con {maximo_sala} salas")
        print("-----------------------------")


def comparar_resultados_torneo(jugadores:list)-> list:
    #maximo = primerArguemnto
    #comparar los puntajes con el maximo if maximo < siguiente puntaje then maximo = siguienteputanje
    maximo_puntaje = jugadores[0][1][0]
    ganadores = []

    for jugador in jugadores:
        nombre = jugador[0]
        puntaje = jugador[1][0]

        if puntaje > maximo_puntaje:
            maximo_puntaje = puntaje
            ganadores = [nombre]

        elif puntaje == maximo_puntaje:
            ganadores.append(nombre)
    
    return ganadores, maximo_puntaje

def comparar_salas_resultado(jugadores:list)-> list:

    maxima_sala = jugadores[0][1][2]
    ganadores = []

    for jugador in jugadores:
        nombre = jugador[0]
        sala = jugador[1][2] #tenes que traer la cant de salas del jugador

        if sala > maxima_sala:
            maxima_sala = sala
            ganadores = [nombre]
        elif sala == maxima_sala:
            ganadores.append(nombre)
        
    return ganadores, maxima_sala



#ahora mandar los datos del torneo a puntajes.csv
def grabar_resultados_torneo():
    pass