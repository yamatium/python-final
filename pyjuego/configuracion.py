import pygame, random

pygame.mixer.init()
pygame.font.init()

def crear_superficie_pantalla()-> pygame.Surface:
    #regresa una superficie para para ver el juego 
    ancho = 1280 
    alto = 720
    return pygame.display.set_mode((ancho, alto))

def elejir_numero(inicio:int , fin: int)-> int:
    #trae un numero aleatorio
    numero_elejido = random.randint(inicio,fin)
    return numero_elejido

def crear_fuente(tamanio: int)-> pygame.font:
    #crea una fuente para usar, el tamanio normal es 50
    #tamanio = 50
    fuente = pygame.font.SysFont(None, tamanio)
    return fuente

COLORS = {
    "gray": "gray",
    "white": "#ffffff",
    "black": "black",
    "red": "red",
    "royalblue": "#141828",
    "lightblue": "#87CEFA",
}

preguntas = {
     0:{
     "pregunta": "¿Que hace el metodo append, con un elemento?",
     "opciones": ["a.lo agrega al final de la lista", "b.pinta de azul la pantalla" ,"c.nada" ,"d.termina el programa"],
     "respuesta": "a",
     "valor_puntaje":5
     },
     1:{
     "pregunta": "¿Los diccionarios como guardan valores?",
     "opciones": ["a.en llave:valor", "b.con una variable" ,"c.en una lista" ,"d.no guardan"],
     "respuesta": "a",
     "valor_puntaje":10
     },
     2:{
     "pregunta": "¿Qué tipo de dato es el resultado de, 5 / 2 en Python 3?",
     "opciones": ["a.int", "b.float" ,"c.str" ,"d.bool"],
     "respuesta": "b",
     "valor_puntaje":15
     },
     3:{
     "pregunta": "¿Cuál es la forma correcta de crear una lista vacía?",
     "opciones": ["a.[]", "b.print()" ,"c.none" ,"d.()"],
     "respuesta": "a",
     "valor_puntaje":20
     },
     4:{
     "pregunta": "¿Qué imprime el siguiente código?, print('Hola'* 2)",
     "opciones": ["a.HolaHola", "b.Hola Hola" ,"c.Error" ,"d.Hola2"],
     "respuesta": "a",
     "valor_puntaje":12   
     },
     5:{
     "pregunta": "¿Qué palabra clave se usa, para definir una función en Python?",
     "opciones": ["a.function", "b.define" ,"c.def" ,"d.fun"],
     "respuesta": "c",
     "valor_puntaje":9   
     },
     6:{
     "pregunta": "¿Cuál es el operador lógico para 'y'?",
     "opciones": ["a.or", "b.and" ,"c.>" ,"d.+"],
     "respuesta": "b",
     "valor_puntaje":18   
     },
     7:{
     "pregunta": "¿Qué devuelve un len de 3 elementos?",
     "opciones": ["a.3", "b.error" ,"c.5" ,"d.0"],
     "respuesta": "a",
     "valor_puntaje":23   
     },
     8:{
     "pregunta": "¿Qué tipo de estructura es un diccionario?",
     "opciones": ["a.indexada", "b.clave-valor" ,"c.str" ,"d.ninguna"],
     "respuesta": "b",
     "valor_puntaje":30   
     },
     9:{
     "pregunta": "¿Qué resultado tiene 3 ** 2?",
     "opciones": ["a.5", "b.6" ,"c.9" ,"d.8"],
     "respuesta": "c",
     "valor_puntaje":9   
     },
     10:{
     "pregunta": "¿Cuál es el resultado de True and False?",
     "opciones": ["a.False", "b.True" ,"c.None" ,"d.Error"],
     "respuesta": "a",
     "valor_puntaje":31   
     },
     11:{
     "pregunta": "¿Qué se usa ,para hacer comentarios en una línea en Python?",
     "opciones": ["a.||", "b.<!---->" ,"c.#" ,"d.()"],
     "respuesta": "c",
     "valor_puntaje":33   
     },
     12:{
     "pregunta": "¿Qué imprime este código? print(type('Hola')",
     "opciones": ["a.string", "b.<class 'str'>" ,"c.str" ,"d.text"],
     "respuesta": "b",
     "valor_puntaje":3   
     },
     13:{
     "pregunta": "¿Qué función se usa para, convertir un string en un entero?",
     "opciones": ["a.int()", "b.float()" ,"c.str()" ,"d.input()"],
     "respuesta": "a",
     "valor_puntaje":26   
     },
     14:{
     "pregunta": "¿Cuál es el resultado de 10 // 3?",
     "opciones": ["a.3.33", "b.3" ,"c.3.0" ,"d.error"],
     "respuesta": "b",
     "valor_puntaje":35   
     },
     15:{
     "pregunta": "¿Qué palabra clave ,se usa para terminar un ciclo?",
     "opciones": ["a.continue", "b.exit" ,"c.stop" ,"d.break"],
     "respuesta": "d",
     "valor_puntaje":40   
     },
     16:{
     "pregunta": "¿Cuál es el índice ,del primer elemento en una lista?",
     "opciones": ["a.0", "b.1" ,"c.-1" ,"d.None"],
     "respuesta": "a",
     "valor_puntaje":44   
     },
     17:{
     "pregunta": "¿Cuál estructura se usa para manejar excepciones?",
     "opciones": ["a.if/else", "b.try/except" ,"c.catch/throw" ,"d.while/except"],
     "respuesta": "b",
     "valor_puntaje":60   
     },
     18:{
     "pregunta": "¿Cuál es la salida de bool('')",
     "opciones": ["a.True", "b.False" ,"c.Error" ,"d.None"],
     "respuesta": "b",
     "valor_puntaje":55   
     },
     19:{
     "pregunta": "¿En que año se creo python?",
     "opciones": ["a.1980", "b.1995" ,"c.1991" ,"d.2005"],
     "respuesta": "b",
     "valor_puntaje":91   
     },
     20:{
     "pregunta": "¿Cual de las siguientes es una tupla?",
     "opciones": ["a.{1, 2, 3}", "b.||" ,"c.[1, 2, 3] " ,"d.(1, 2, 3)"],
     "respuesta": "d",
     "valor_puntaje":100   
     },
}