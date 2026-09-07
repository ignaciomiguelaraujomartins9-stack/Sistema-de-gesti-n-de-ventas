def pedir_entero_en_rango(mensaje, minimo, maximo):
    """Solicita al usuario un número entero dentro de un rango, reintentando
    hasta que la entrada sea válida.

    Recibe:  mensaje (str) a mostrar, minimo (int) y maximo (int) permitidos.
    Devuelve: el número ingresado (int), garantizado dentro del rango.

    Observar que esta función DEVUELVE el valor con return: no toma
    decisiones sobre qué hacer con él. Es reutilizable para leer la
    opción del menú, la cantidad de unidades, el medio de pago, etc.
    """
    entrada = input(mensaje)
    while not entrada.isdigit() or not (minimo <= int(entrada) <= maximo):
        print(f"Entrada inválida. Ingrese un número entero entre {minimo} y {maximo}.")
        entrada = input(mensaje)
    return int(entrada)
