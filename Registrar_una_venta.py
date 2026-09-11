"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico N.º 1 (tp_1.py) — Sistema de gestión de ventas: Kiosco "El Campus"

Integrantes del grupo:
    - Apellido, Nombre
    - Apellido, Nombre

Este archivo es un punto de partida. Contiene la estructura general del
programa, las constantes del enunciado y UNA función de ejemplo ya resuelta
que muestra el estilo esperado (docstring, validación y uso de return).
El resto de las funciones deben diseñarlas y programarlas ustedes,
respetando los requerimientos técnicos de la consigna.
"""

# =====================================================================
# CONSTANTES
# ---------------------------------------------------------------------
# Definir los valores del enunciado como constantes (en MAYÚSCULAS)
# evita "números mágicos" repetidos por todo el código: si mañana
# Don Ramón cambia un porcentaje, se modifica en un solo lugar.
# =====================================================================
MONTO_MINIMO_DESCUENTO = 25000      # subtotal a partir del cual hay descuento
PORCENTAJE_DESCUENTO_MONTO = 10     # % de descuento por superar el monto
PORCENTAJE_DESCUENTO_EFECTIVO = 5   # % de descuento por pagar en efectivo
PORCENTAJE_RECARGO_CREDITO = 8      # % de recargo por pagar con crédito


# =====================================================================
# FUNCIÓN DE EJEMPLO (ya implementada: úsenla como modelo de estilo)
# =====================================================================
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


# =====================================================================
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------
# El bloque principal solo coordina: contiene los acumuladores del día,
# el ciclo del menú y las llamadas a funciones. Nada de lógica de
# cálculo ni validaciones sueltas acá.
# =====================================================================
def main():
    """Punto de entrada del programa: menú principal del kiosco."""

    # TODO: definir los acumuladores del día (variables simples):
    #       total recaudado, cantidad de ventas, venta más alta,
    #       totales por categoría y contadores por medio de pago.

    opcion = 0
    while opcion != 3:
        # TODO: reemplazar por una función que muestre el menú
        print("\n=== KIOSCO EL CAMPUS ===")
        print("1) Registrar una venta")
        print("2) Ver resumen del día")
        print("3) Cerrar caja y salir")
        opcion = pedir_entero_en_rango("Elija una opción: ", 1, 3)

        if opcion == 1:
            # TODO: registrar una venta (categoría, precio, cantidad,
            #       medio de pago), calcular el importe final, mostrar
            #       el ticket y actualizar los acumuladores.
            print("Opción en construcción...")
        elif opcion == 2:
            # TODO: mostrar el resumen del día (contemplar el caso
            #       de que todavía no haya ventas registradas).
            print("Opción en construcción...")
        else:
            # TODO: pedir confirmación (S/N); si confirma, mostrar el
            #       resumen final y la cuenta regresiva recursiva;
            #       si no, volver al menú (pista: modificar 'opcion').
            print("Opción en construcción...")

    print("¡Hasta mañana, Don Ramón!")


main()