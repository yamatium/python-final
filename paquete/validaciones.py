def validar_nombre() -> str:
    #valida que el nombre no esta vacio
    #retorna una cadena no vacia
    bandera = False
    nombre = input(f"Ingrese el nobre del jugador: ")
    while not bandera:
        if nombre != '':
            bandera = True
        else:
            print(f"el nombre no puede estar vacio,intentelo otra vez")
            nombre = input(f"Ingrese el nobre del jugador: ")
    
    return nombre


def validar_numero() ->int:
    #valida que sea un numero al pedir al usuario
    #retorna un numero int validado
    bandera = False
    numero = input("ingrese el numero de jugadores del 1 al 10: ")
    while not bandera:
        if numero.isdigit():
            numero = int(numero)
            bandera = True
        else:
            print("por favor ingrese un numero valido")
            numero = input("por favor ingrese el numero de jugadores del 1 al 10: ")
    return numero


def validar_cantidad_jugadores(torneo:bool) ->int:
    #valida que la cantidad de jugadores sea un numero de tipo int entre 0 y 10 si torneo es falso, sino revisa entre 1 y 10
    #retorna un numero int

    if torneo:
        bandera = False
        numero_jugadores = validar_numero()
        while not bandera:
            if 1 <= numero_jugadores <= 10:
                #cambiar min por 2 en torneo
                bandera = True
            else:
                print("")
                numero_jugadores = validar_numero()
    else:
      bandera = False
      numero_jugadores = validar_numero()
      while not bandera:
         if 1 <= numero_jugadores <= 10:
            bandera = True
         else:
            print("")
            numero_jugadores = validar_numero()
    return numero_jugadores