"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico N.º 1 (tp_1.py) — Sistema de gestión de ventas: Kiosco "El Campus"

Integrantes del grupo:
    - Kevin Pavese
    - Araujo Martins, Ignaico Miguel

Este archivo es un punto de partida. Contiene la estructura general del
programa, las constantes del enunciado y UNA función de ejemplo ya resuelta
que muestra el estilo esperado (docstring, validación y uso de return).
El resto de las funciones deben diseñarlas y programarlas ustedes,
respetando los requerimientos técnicos de la consigna.
"""

#------------ OPCIONES DEL MENU - START -------------#

MONTO_MINIMO_DESCUENTO = 25000      # subtotal a partir del cual hay descuento
PORCENTAJE_DESCUENTO_MONTO = 10     # % de descuento por superar el monto
PORCENTAJE_DESCUENTO_EFECTIVO = 5   # % de descuento por pagar en efectivo
PORCENTAJE_RECARGO_CREDITO = 8      # % de recargo por pagar con crédito

def pedir_numero(mensaje, min, max):
    """Función reutilizable que pide un número en un rango al usuario hasta que sea válido.

    Recibe: mensaje (str) a mostrar, minimo (int) y máximo (int) permitido del número
    
    Retorna: el número ya validado dentro de el rango (int)

    ."""
    entrada = input(mensaje)
    while not entrada.isdigit() or not (min <= int(entrada) <= max):
        print(f"Opción inválida. Ingrese un número entre {min} y {max}")
        entrada = input(mensaje)
    return int(entrada)

def descuento_monto(precio, cantidad):
    """Calcula el descuento si se supera el monto minimo de descuento.

    Recibe: precio (int) y cantidad (int)
    
    Devuelve: subtotal (variable sin el descuento aplicado) (int), descuento (int),
    subtotal_d (variable con el descuento aplicado) (int)
    
    ."""
    descuento = 0
    subtotal = precio * cantidad
    subtotal_d = subtotal
    if subtotal > MONTO_MINIMO_DESCUENTO:
        descuento = (subtotal * PORCENTAJE_DESCUENTO_MONTO) / 100
        subtotal_d = subtotal - descuento
    return subtotal, descuento, subtotal_d

def ajuste_medio_pago(subtotal_d, medio_pago):
    """Realiza el ajuste según el medio de pago ingresado.

    Recibe: subtotal_d (Subtotal con descuento de monto aplicado) (int), medio_pago (int)
    
    Devuelve: Importe final (int), descuento por efectivo (int), recargo por crédito (int)
    
    ."""
    importe_final = subtotal_d
    descuento_efectivo = 0
    recargo = 0
    if medio_pago == 1:
        descuento_efectivo = (subtotal_d * PORCENTAJE_DESCUENTO_EFECTIVO) / 100
        importe_final = subtotal_d - descuento_efectivo
    elif medio_pago == 3:
        recargo = (subtotal_d * PORCENTAJE_RECARGO_CREDITO) / 100
        importe_final = subtotal_d + recargo
    return importe_final, descuento_efectivo, recargo

def mostrar_ticket(cantidad, precio, categoria, medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo):
    """Muestra en pantalla el ticket con toda la información calculada por las otras funciones
    
    
    ."""
    
    match categoria:
        case 1:
            cat = "Golosinas"
        case 2:
            cat = "Bebidas"
        case 3:
            cat = "Almacén"
        case 4:
            cat = "Librería"

    print("============ TICKET ============")
    print(f"{cantidad} Unidades de {cat} de ${precio}")
    print(f"Subtotal: ${subtotal}")
    print(f"Descuento por monto (10%): -${descuento}")
    if medio_pago == 1:
        print(f"Descuento por efectivo ({PORCENTAJE_DESCUENTO_EFECTIVO}% sobre ${subtotal_d}): -${descuento_efectivo}")
    elif medio_pago == 2:
        print("Pagó con débito: no hay ajuste")
    elif medio_pago == 3:
        print(f"Recargo por crédito ({PORCENTAJE_RECARGO_CREDITO}% sobre ${subtotal_d}): +${recargo}")
    print(f"Importe final: ${importe_final}")
    print(f"Codigo de la suerte: {codigo}")
    print("================================")

#------------ CODIGO DE LA SUERTE - START -------------#

def codigo_suerte(importe):
    """Desafío del código de la suerte: Algoritmo recursivo que suma los dígitos
    del importe final hasta que quede 1 solo dígito
    Recibe: Importe final (float)
    
    Devuelve: Codigo de la suerte (int)
    
    ."""
    if importe < 10:
        return importe
    else:
        suma = (importe % 10) + codigo_suerte(importe // 10)
    return codigo_suerte(int(suma)) 

#------------ CODIGO DE LA SUERTE - END -------------#

def verificar_cierre():
    """
    Comprueba si Don Ramón quiere finalizar el registro de las ventas de la jornada.

    Recibe: no recibe parámetros.
    
    Devuelve el número correspondiente a la opción elegida: si es 'sí', llama a la función 'cuenta_regresiva' e imprime
    el valor que esta devuelve, luego retorna el valor 3 para finalizar el sistema. Si el valor es 'no', retorna 0.
    
    ."""
    continuar = input("¿Desea continuar con el cierre? (Si/No): ").lower()
    while (continuar != "si" and continuar != "sí") and continuar != "no":
        print("Entrada inválida. Ingrese la opción: 'Si' para continuar, 'No' para salir.")
        continuar = input("Si/No: ").lower()
    if continuar == "si" or continuar == "sí":
        return 3
    return 0

#------------ OPCIONES DEL MENU - END -------------#

#------------ CUENTA REGRESIVA - START -------------#

def cuenta_regresiva(cuenta):
    """
    Realiza la cuenta atrás (de forma recursiva) cuando Don Ramón ingresa la opción 'si'. Mediante la función 'mostrar_cuenta' permite
    mostrar el número de 5 a 1.

    Recibe el parámetro 'cuenta' (int) que contiene el valor 5 para la cuenta regresiva.
    
    Devuelve 'Caja cerrada' (str) luego de que el caso base se ejecute.
    
    ."""
    if cuenta == 0:
        return "¡Caja cerrada!"
    mostrar_cuenta(cuenta)
    return cuenta_regresiva(cuenta - 1)

def cuenta_regresiva_iterativo(cuenta):
    """
    Realiza la cuenta atrás (de forma iterativa) cuando Don Ramón ingresa la opción 'si'.

    Recibe el parámetro 'cuenta' (int) que contiene el valor 5 para la cuenta regresiva.
    
    Devuelve: No devuelve nada, solo imprime la cuenta regresiva e imprime Caja cerrada cuando la condición
    deja de ser verdadera.
    
    ."""
    while cuenta > 0:
        print(cuenta)
        cuenta -= 1
    else: print("¡Caja cerrada!")

def mostrar_cuenta(cuenta):
    """
    Muestra los números de la cuenta atrás.

    Recibe el parámetro cuenta que viene desde 'cuenta_regresiva'.
    
    Devuelve: no devuelve ningún valor (solo imprime el número).
    
    ."""
    print(cuenta)

#------------ CUENTA REGRESIVA - END -------------#

#------------ RESUMEN DEL DIA - START -------------#

def verificar_entradas(cantidad):
    """
    Verifica si la cantidad de productos es mayor a 0 para verificar si mostrar el resumen del día o mostrar 'no se realizaron ventas este día'
    
    Recibe: cantidad (int).
    
    Devuelve: True si la cantidad es mayor a 0. False si la cantidad es menor a 0.
    
    ."""
    
    return cantidad > 0

def resumen_del_dia(cantidad, total, promedio_venta, mayor_venta, cat1, cat2, cat3, cat4, ventas_pago1, ventas_pago2, ventas_pago3):
    """
    Se encarga de mostrar de forma ordenada las ventas, el total recaudado, qué método de pago fue el más usado y el total recaudado por cada categoría en el día.
    
    Recibe: cantidad (int), total (float), promedio_venta (float), mayor_venta (float), cat1 (float [cantidad recaudada por la categoría 1]), 
    cat2 (float [cantidad recaudada por la categoría 2]), cat3 (float [cantidad recaudada por la categoría 3]), 
    cat4 (float [cantidad recaudada por la categoría 4]), ventas_pago1 (int [Cantidad de ventas realizadas con el método de pago efectivo]), 
    ventas_pago2 (int [Cantidad de ventas realizadas con el método de pago débito]),
    ventas_pago3 (int [Cantidad de ventas realizadas con el método de pago crédito])
    
    Devuelve: no devuelve nada (imprime una lista ordenada).
    
    ."""
    
    print(" ")
    print("===================================================================")
    print("Cantidad de ventas realizadas y total recaudado")
    print(f"Ventas: {cantidad}")
    print(f"Recaudado: ${total:.2f}")
    print("===================================================================")
    print(f"Importe promedio por venta: ${promedio_venta:.2f}")
    print(f"Importe de la venta más alta: ${mayor_venta:.2f}")
    print("===================================================================")
    print(f"Total recaudado por cada categoría de producto")
    if cat1 == 0:
        print(f"Golosinas: No hay ventas de este tipo.")
    else:
        print(f"Golosinas: ${cat1:.2f}")
    if cat2 == 0:
        print(f"Bebidas: No hay ventas de este tipo.")
    else:
        print(f"Bebidas: ${cat2:.2f}")
    if cat3 == 0:
        print(f"Almacén: No hay ventas de este tipo.")
    else:
        print(f"Almacén: ${cat3:.2f}")
    if cat4 == 0:
        print(f"Librería: No hay ventas de este tipo.")
    else:
        print(f"Librería: ${cat4:.2f}")
    print("===================================================================")
    print("Cantidad de ventas por cada medio de pago")
    print(f"Efectivo: {ventas_pago1 if ventas_pago1 != 0 else 'No se realizaron ventas con este método'}")
    print(f"Débito: {ventas_pago2 if ventas_pago2 != 0 else 'No se realizaron ventas con este método'}")
    print(f"Crédito: {ventas_pago3 if ventas_pago3 != 0 else 'No se realizaron ventas con este método'}")
    if ventas_pago3 == ventas_pago2 and ventas_pago3 == ventas_pago1:
        print("Los tres tienen un mismo uso")
        print(f"Efectivo {ventas_pago1} uso/s, Débito {ventas_pago2} uso/s y Crédito {ventas_pago3} uso/s")
    else:
        if ventas_pago1 >= ventas_pago2 and ventas_pago1 >= ventas_pago3:
            if ventas_pago1 == ventas_pago2:
                print("Los más usados fueron")
                print(f"Efectivo {ventas_pago1} uso/s y Débito {ventas_pago2} uso/s")
            elif ventas_pago1 == ventas_pago3:
                print("Los más usados fueron")
                print(f"Efectivo {ventas_pago1} uso/s y Crédito {ventas_pago3} uso/s")
            else:
                print("El que más veces se usó fue")
                print(f"Efectivo con {ventas_pago1} uso/s")
        elif ventas_pago2 >= ventas_pago1 and ventas_pago2 >= ventas_pago3:
            if ventas_pago2 == ventas_pago3:
                print("Los más usados fueron")
                print(f"Débito {ventas_pago2} uso/s y Crédito {ventas_pago3} uso/s")
            else:
                print("El que más veces se usó fue")
                print(f"Débito con {ventas_pago2} uso/s")
        elif ventas_pago3 >= ventas_pago1 and ventas_pago3 >= ventas_pago2:
            print("El que más veces se usó fue")
            print(f"Crédito con {ventas_pago3} uso/s")
    print("===================================================================")

def acumulador(cantidad_total, dinero_total, importe_promedio_por_venta, cantidad, importe_final, mayor_venta, categoria, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3, medio_pago):
    """
    Acumula todas las variables calculadas por tipo para luego imprimirlas en el resumen del día.
    
    Recibe: cantidad_total (int [Variable acumuladora]), dinero_total (float [Variable acumuladora]), importe_promedio_por_venta (float [Variable acumuladora]), cantidad (int [Valor ingresado por don Ramón]), importe_final (float [Valor ingresado por don Ramón]), mayor_venta (float [Variable acumuladora]), categoria (int [Valor ingresado por don Ramón]), total_cat1 (float [Variable acumuladora]), total_cat2 (float [Variable acumuladora]), total_cat3 (float [Variable acumuladora]), total_cat4 (float [Variable acumuladora]),
    ventas_pago1 (int [Variable acumuladora]), ventas_pago2 (int [Variable acumuladora]), ventas_pago3 (int [Variable acumuladora]), medio_pago (int [Valor ingresado por don Ramón])
    
    Devuelve: todas las variables acumulativas con los valores de las ventas del día. cantidad_total, dinero_total, importe_promedio_por_venta, mayor_venta, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3.
    
    ."""
    cantidad_total += cantidad
    dinero_total += importe_final
    importe_promedio_por_venta = dinero_total/cantidad_total
    if importe_final > mayor_venta:
        mayor_venta = importe_final
    match categoria:
        case 1:
            total_cat1 += importe_final
        case 2:
            total_cat2 += importe_final
        case 3:
            total_cat3 += importe_final
        case 4:
            total_cat4 += importe_final
    match medio_pago:
        case 1:
            ventas_pago1 += 1
        case 2:
            ventas_pago2 += 1
        case 3:
            ventas_pago3 += 1
    return cantidad_total, dinero_total, importe_promedio_por_venta, mayor_venta, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3

#------------ RESUMEN DEL DIA - END -------------#

def menu():
    """Menu principal donde se ingresan las opciones para registrar ventas, ver resumen del día y cerrar caja
    
    ."""
    cantidad_total, dinero_total, importe_promedio_por_venta, opcion, mayor_venta, total_cat1, total_cat2, total_cat3, total_cat4  = 0, 0, 0, 0, 0, 0, 0, 0, 0
    ventas_pago1, ventas_pago2, ventas_pago3 = 0, 0, 0
    
    while opcion != 3:
        print("=== KIOSCO EL CAMPUS ===")
        print("1. Registrar una venta")
        print("2. Ver resumen del día")
        print("3. Cerrar caja y salir")
        opcion = pedir_numero("Elija una opción (1/2/3): ", 1, 3)
        match opcion:
            case 1:
                print("1. Golosinas")
                print("2. Bebidas")
                print("3. Almacén")
                print("4. Librería")
                categoria = pedir_numero("Elija la categoría del producto (1/2/3/4): ", 1, 4)
                precio = pedir_numero("Ingrese el precio del producto: ", 1, float('inf')) # Se usa float('inf') como tope para precio y cantidades de producto
                cantidad = pedir_numero("Ingrese la cantidad de producto: ", 1, float('inf'))

                print("============")
                print("1. Efectivo")
                print("2. Débito")
                print("3. Crédito")
                medio_pago = pedir_numero("Ingrese el medio de pago (1/2/3): ", 1, 3)

                subtotal, descuento, subtotal_d = descuento_monto(precio, cantidad)
                importe_final, descuento_efectivo, recargo = ajuste_medio_pago(subtotal_d, medio_pago)
                codigo = codigo_suerte(int(importe_final))
                mostrar_ticket(cantidad, precio, categoria, medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo)

                cantidad_total, dinero_total, importe_promedio_por_venta, mayor_venta, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3 = acumulador(cantidad_total, dinero_total, importe_promedio_por_venta, cantidad, importe_final, mayor_venta, categoria, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3, medio_pago)
            case 2:
                print(" ")
                print("===========================================================================")
                if verificar_entradas(cantidad_total):
                    resumen_del_dia(cantidad_total, dinero_total, importe_promedio_por_venta, mayor_venta, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3)
                else:
                    print("Aún no se realizaron ingresos")
                print("===========================================================================")
                print(" ")
            case 3:
                print("")
                if verificar_cierre() == 3:
                    if verificar_entradas(cantidad_total):
                        resumen_del_dia(cantidad_total, dinero_total, importe_promedio_por_venta, mayor_venta, total_cat1, total_cat2, total_cat3, total_cat4, ventas_pago1, ventas_pago2, ventas_pago3)
                    else:
                        print(" ")
                        print("===================================================================")
                        print("No se realizaron ventas este día.")
                        print("===================================================================")
                        print(" ")
                    print(cuenta_regresiva(5))
                    cuenta_regresiva_iterativo(5)
                else:
                    opcion = 0
                    print(" ")
    print("¡Hasta mañana, Don Ramón!")

menu()