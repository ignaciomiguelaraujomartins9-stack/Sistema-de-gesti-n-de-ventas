from funciones import pedir_entero_en_rango

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
