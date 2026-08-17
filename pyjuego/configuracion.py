import pygame

#pygame.init()
pygame.mixer.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
#font = pygame.font.SysFont(None, 150) font gigante

entrar_sfx = pygame.mixer.Sound("pyjuego/sonidos/SD_0099.mp3")
salir_sfx = pygame.mixer.Sound("pyjuego/sonidos/SD_0111.mp3")
musica_menu = pygame.mixer.music.load("pyjuego/sonidos/eugene.mp3")
pygame.mixer.music.play()

def entrar_sonido():
    entrar_sfx.play()
    pygame.time.wait(int(salir_sfx.get_length() * 1000))

def salir_sonido():
    salir_sfx.play()
    pygame.time.wait(int(salir_sfx.get_length() * 1000)) #regresa y convierte segundos en ms para time.wait

def musica_menu():
    pygame.mixer.music.load("pyjuego/sonidos/eugene.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def manejar_musica():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

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
     "pregunta": "¿Que hace el metodo append?",
     "opciones": ["a.agrega un elemento al final de la lista", "b.imprime un mensaje en consola" ,"c.nada" ,"d.termina el programa"],
     "respuesta": "a",
     "valor_puntaje":5
     },
     1:{
     "pregunta": "¿Los diccionarios como guardan valores?",
     "opciones": ["a.en valor llave:valor", "b.con una variable" ,"c.en una lista" ,"d.no guardan"],
     "respuesta": "a",
     "valor_puntaje":10
     },
     2:{
     "pregunta": "¿Qué tipo de dato es el resultado de 5 / 2 en Python 3?",
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
     "pregunta": "¿Qué imprime el siguiente código? print('Hola' * 2)",
     "opciones": ["a.HolaHola", "b.Hola Hola" ,"c.Error" ,"d.Hola2"],
     "respuesta": "a",
     "valor_puntaje":12   
     },
     5:{
     "pregunta": "¿Qué palabra clave se usa para definir una función en Python?",
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
     "pregunta": "¿Qué devuelve len([1, 2, 3])",
     "opciones": ["a.3", "b.error" ,"c.5" ,"d.0"],
     "respuesta": "a",
     "valor_puntaje":23   
     },
     8:{
     "pregunta": "¿Qué tipo de estructura es un diccionario?",
     "opciones": ["a.indexada", "b.clave-valor" ,"c.str" ,"d.Inmutable"],
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
     "pregunta": "¿Qué se usa para hacer comentarios en una línea en Python?",
     "opciones": ["a.||", "b.<!-- -->" ,"c.#" ,"d.()"],
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
     "pregunta": "¿Qué función se usa para convertir un string en un entero?",
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
     "pregunta": "¿Qué palabra clave se usa para terminar un ciclo anticipadamente?",
     "opciones": ["a.continue", "b.exit" ,"c.stop" ,"d.break"],
     "respuesta": "d",
     "valor_puntaje":40   
     },
     16:{
     "pregunta": "¿Cuál es el índice del primer elemento en una lista?",
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

#esto es un nested diccionary