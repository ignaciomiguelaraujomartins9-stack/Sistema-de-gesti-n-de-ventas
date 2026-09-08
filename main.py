"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico N.º 1 (tp_1.py) — Sistema de gestión de ventas: Kiosco "El Campus"

Integrantes del grupo:
    - 
    - Araujo Martins, Ignaico Miguel

Este archivo es un punto de partida. Contiene la estructura general del
programa, las constantes del enunciado y UNA función de ejemplo ya resuelta
que muestra el estilo esperado (docstring, validación y uso de return).
El resto de las funciones deben diseñarlas y programarlas ustedes,
respetando los requerimientos técnicos de la consigna.
"""

#------------ OPCIONES DEL MENU - START -------------#

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

def opciones():
    """
    Muestra las opciones disponibles que tiene el programa
    
    Recibe: no recibe parámetros.
    Devuelve el número que se ingresó en 'pedir_entero_en_rango' para su uso en la función 
    'validar_opciones'
    """
    print("\n=== KIOSCO EL CAMPUS ===")
    print("1) Registrar una venta")
    print("2) Ver resumen del día")
    print("3) Cerrar caja y salir")
    opcion = pedir_entero_en_rango("Elija una opción: ", 1, 3)
    return validar_opciones(opcion)

def validar_opciones(opcion):
    """
    Valida la opción que ingresa Don Ramón para realizar: Registrar una venta, Ver resumen del día o Cerrar la caja y 
    salir.
    
    Recibe el parámetro 'opcion' que contiene el número elegido por el usuario
    Devuelve el número correspondiente al resultado de esa opción: si es 1 o 2, devuelve ese mismo número luego de 
    realizar su funcionamiento. Si es 3, llama a la función 'comprobar' para confirmar que Don ramón realmente quiere
    cerrar la caja, y devuelve lo que esa función retorne.
    """
    if opcion == 1:
        print("Opción en construcción...")
        return opcion
    elif opcion == 2:
        print("Opción en construcción...")
        return opcion
    else:
        opcion = comprobar()
        return opcion

#------------ OPCIONES DEL MENU - END -------------#

# =====================================================================
# FUNCIONES A DESARROLLAR POR EL GRUPO
# ---------------------------------------------------------------------
# Diseñar acá las funciones del programa. Decidir ustedes cuántas son,
# cómo se llaman, qué parámetros reciben y qué devuelven forma parte
# de la evaluación ("Diseño del algoritmo"). Como guía, la consigna
# exige como mínimo funciones para:
#
#   - mostrar el menú y devolver la opción elegida (ya validada)
#   - solicitar y validar un número dentro de un rango  -> ¡ya la tienen!
#   - calcular el descuento por monto
#   - calcular el ajuste según el medio de pago
#   - calcular el importe final de una venta
#   - mostrar el ticket de una venta
#   - mostrar el resumen del día
#   - realizar la cuenta regresiva del cierre de caja (RECURSIVA)
#
# Recordar: las funciones de cálculo devuelven valores y no imprimen;
# las funciones de mostrar imprimen y no calculan.
# =====================================================================

#------------ CUENTA REGRESIVA - START -------------#

def cuenta_regresiva(cuenta):
    """
    Realiza la cuenta atrás cuando Don Ramón ingresa la opción 'si' mediante la función 'mostrar_cuenta' que permite 
    mostrar el número de 5 a 1
    
    Recibe el parámetro 'cuenta' que contiene el valor 5 para la cuenta regresiva, evitando que el valor se pise por la
    recursividad.
    Devuelve 'Caja cerrada' luego de que el caso base se ejecute. 
    """
    if cuenta == 0: 
        return "¡Caja cerrada!"
    mostrar_cuenta(cuenta) # Llama a la función 'mostrar_cuenta' para imprimir los números de la cuenta regresiva
    return cuenta_regresiva(cuenta - 1) 

def mostrar_cuenta(cuenta):
    """
    Muestra los números de la cuenta atrás.
    
    Recibe el parámetro cuenta que viene desde 'cuenta_regresiva'.
    Devuelve: no devuelve ningún valor (solo imprime el número).
    """
    print(cuenta)

# def resuem_final_del_dia():
    

def comprobar():
    """
    Comprueba si Don Ramón quiere finalizar el registro de las ventas de la jornada.
    
    Recibe: no recibe parámetros.
    Devuelve el número correspondiente a la opción elegida: si es 'sí', llama a la función 'cuenta_regresiva' e imprime
    el valor que esta devuelve, luego retorna el valor 3 para finalizar el sistema. Si el valor es 'no', devuelve 0
    para continuar con el sistema.
    """
    continuar = input("¿Desea continuar con el cierre? (Si/No): ").lower()
    while (continuar != "si" and continuar != "sí") and continuar != "no":
        print("Entrada inválida. Ingrese la opción: 'Si' para continuar, 'No' para salir.")
        continuar = input("Si/No: ").lower()
    if continuar == "si" or continuar == "sí":
        print(cuenta_regresiva(5))
        return 3
    elif continuar == "no":
        return 0

#------------ CUENTA REGRESIVA - END -------------#

# =====================================================================
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------
# El bloque principal solo coordina: contiene los acumuladores del día,
# el ciclo del menú y las llamadas a funciones. Nada de lógica de
# cálculo ni validaciones sueltas acá.
# =====================================================================

def main():
    """Punto de entrada del programa: menú principal del kiosco."""
    
    opcion = 0
    while opcion != 3:
        opcion = opciones()
        
    print("¡Hasta mañana, Don Ramón!")

main()