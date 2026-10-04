"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico N.º 1 (tp_1.py) — Sistema de gestión de ventas: Kiosco "El Campus"

Integrantes del grupo:
    - Kevin Pavese
    - Araujo Martins, Ignacio Miguel

Este archivo es un punto de partida. Contiene la estructura general del
programa, las constantes del enunciado y UNA función de ejemplo ya resuelta
que muestra el estilo esperado (docstring, validación y uso de return).
El resto de las funciones deben diseñarlas y programarlas ustedes,
respetando los requerimientos técnicos de la consigna.
"""

#------------ VARIABLES CONSTANTES - START -------------#

#------------ DESCUENTO Y MONTO - START -------------#

MONTO_MINIMO_DESCUENTO = 25000      # subtotal a partir del cual hay descuento
PORCENTAJE_DESCUENTO_MONTO = 10     # % de descuento por superar el monto
PORCENTAJE_DESCUENTO_EFECTIVO = 5   # % de descuento por pagar en efectivo
PORCENTAJE_RECARGO_CREDITO = 8      # % de recargo por pagar con crédito

#------------ DESCUENTO Y MONTO - END -------------#


#------------ POSICIONES - START -------------#

CODIGO, NOMBRE, CATEGORIA, PRECIO, STOCK = 0, 1, 2, 3, 4

#------------ POSICIONES - END -------------#

#------------ CATEGORIAS - START -------------#

CATEGORIAS = ["Golosinas", "Bebidas", "Almacén", "Librería"]   # índice + 1 = número de categoría
MEDIOS_PAGO = ["Efectivo", "Débito", "Crédito"]                 # índice + 1 = número de medio
STOCK_MINIMO = 5   

#------------ CATEGORIAS - END -------------#

#------------ VARIABLES CONSTANTES - END -------------#

#------------ CATALOGO - START -------------#

def catalogo_inicial():
    """Devuelve el catálogo de partida del kiosco (lista de listas)."""
    return [
        [305, "Alfajor triple",           1, 1500.0, 24],
        [112, "Agua saborizada 500 ml",   2, 1900.0, 10],
        [421, "Cuaderno",                 4, 10000.0, 15],
        [208, "Galletitas surtidas",      3, 2800.0,  8],
        [117, "Gaseosa 1.5 L",            2, 4000.0,  6],
        [302, "Chicles",                  1,  700.0, 40],
        [415, "Birome azul",              4, 1200.0,  3],
        [210, "Fideos 500 g",             3, 2100.0, 12],
        [310, "Chocolate con leche",      1, 3200.0,  4],
        [119, "Jugo en polvo",            2,  900.0, 30],
    ]

#------------ CATALOGO - END -------------#

# =====================================================================
# HISTORIAL DE VENTAS, CONSTANTES + RANKING
# =====================================================================

historial_ventas = []
NRO_VENTA, COD_PROD, CANTIDAD, MEDIO_PAGO, IMPORTE_FINAL = 0, 1, 2, 3, 4
RANK_NOM, RANK_CANT, RANK_IMP = 0, 1, 2

#------------ ORDENAMIENTO - START -------------#

def ord_insercion(lista, campo, descendiente = False):
    for i in range(1, len(lista)):
        v = lista[i]
        j = i - 1
        while j >= 0 and ((not descendiente and lista[j][campo] > v[campo]) or (descendiente and lista[j][campo] < v[campo])):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = v

#------------ ORDENAMIENTO - END -------------#

#------------ BUSQUEDA - START -------------#

def buscar_por_codigo(lista, producto):
    izq = 0
    der = len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio][CODIGO] == producto:
            return medio
        elif lista[medio][CODIGO] > producto:
            der = medio - 1
        else:
            izq = medio + 1
    return -1

#------------ BUSQUEDA - END -------------#

#------------ OPCIONES DEL MENU - START -------------#

def pedir_numero(mensaje, min, max):
    """Función reutilizable que pide un número en un rango al usuario hasta que sea válido.

    Recibe: mensaje (str) a mostrar, minimo (int) y máximo (int) permitido del número
    
    Devuelve: el número ya validado dentro de el rango (int)

    ."""
    entrada = input(mensaje)
    while not entrada.isdigit() or not (min <= int(entrada) <= max):
        print(f"Opción inválida. Ingrese un número entre {min} y {max}")
        entrada = input(mensaje)
    return int(entrada)

def descuento_monto(precio, cantidad):
    """Calcula el descuento si se supera el monto minimo de descuento.

    Recibe: precio (int) y cantidad (int)
    
    Devuelve: subtotal (variable sin el descuento aplicado) (int), descuento (float),
    subtotal_d (variable con el descuento aplicado) (float)
    
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

    Recibe: subtotal_d (Subtotal con descuento de monto aplicado) (float), medio_pago (int)
    
    Devuelve: Importe final (float), descuento por efectivo (float), recargo por crédito (float)
    
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

def mostrar_ticket(cantidad, precio, nombre_producto, medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo, nro_venta):
    """Muestra en pantalla el ticket con toda la información calculada por las otras funciones"""
    
    print("============ TICKET ============")
    print(f"Venta N° {nro_venta}")
    print(f"{cantidad} Unidades de {nombre_producto} de ${formatear_importe(precio)}")
    print(f"Subtotal: ${formatear_importe(subtotal)}")
    print(f"Descuento por monto ({PORCENTAJE_DESCUENTO_MONTO}%): -${formatear_importe(descuento)}")
    if medio_pago == 1:
        print(f"Descuento por efectivo ({PORCENTAJE_DESCUENTO_EFECTIVO}% sobre ${formatear_importe(subtotal_d)}): -${formatear_importe(descuento_efectivo)}")
    elif medio_pago == 2:
        print("Pagó con débito: no hay ajuste")
    elif medio_pago == 3:
        print(f"Recargo por crédito ({PORCENTAJE_RECARGO_CREDITO}% sobre ${formatear_importe(subtotal_d)}): +${formatear_importe(recargo)}")
    print(f"Importe final: ${formatear_importe(importe_final)}")
    print(f"Codigo de la suerte: {codigo}")
    print("================================")

def registrar_venta(catalogo, historial_ventas):
    cod = pedir_numero("Ingrese el codigo de otro producto (Ingrese 0 para cancelar): ", 0 , maximo_catalogo(catalogo)) 
    while cod != 0:
        producto = buscar_por_codigo(catalogo, cod)
        if producto != -1:
            if catalogo[producto][STOCK] != 0:
                print(f"Nombre: {catalogo[producto][NOMBRE]}")

                print(f"Precio: ${formatear_importe(catalogo[producto][PRECIO])}")
                print(f"Stock: {catalogo[producto][STOCK]} unidades")

                cantidad = pedir_numero("Ingrese la cantidad: ", 1, catalogo[producto][STOCK])

                print("============")
                print("1. Efectivo")
                print("2. Débito")
                print("3. Crédito")
                medio_pago = pedir_numero("Ingrese el medio de pago (1/2/3): ", 1, 3)

                num_ventas = len(historial_ventas) + 1

                subtotal, descuento, subtotal_d = descuento_monto(catalogo[producto][PRECIO], cantidad)
                importe_final, descuento_efectivo, recargo = ajuste_medio_pago(subtotal_d, medio_pago)
                codigo = codigo_suerte(int(importe_final))
                mostrar_ticket(cantidad, catalogo[producto][PRECIO], catalogo[producto][NOMBRE], medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo, num_ventas)

                print(f"AVISO: El stock de {catalogo[producto][NOMBRE]} pasa de {catalogo[producto][STOCK]} a {catalogo[producto][STOCK] - cantidad}")
                catalogo[producto][STOCK] -= cantidad
                venta = num_ventas, catalogo[producto][CODIGO], cantidad, medio_pago, importe_final
                historial_ventas.append(venta)
                break
            else:
                print()
                print(f"Producto sin stock (es necesario reponer: '{catalogo[producto][NOMBRE]}')")
                cod = pedir_numero("Ingrese el codigo de otro producto (Ingrese 0 para cancelar): ", 0 , maximo_catalogo(catalogo)) 
        else:
            print()
            print("Producto no encontrado")
            cod = pedir_numero("Ingrese el codigo del producto (Ingrese 0 para cancelar): ", 0 , maximo_catalogo(catalogo)) 

def maximo_catalogo(catalogo):
    ord_insercion(catalogo,CODIGO,False)
    codigo = catalogo[-1][CODIGO]
    return codigo

def armar_ranking(catalogo, historial_ventas):
    ranking = []

    for i in range(len(catalogo)):
        cod_prod = catalogo[i][CODIGO]
        nom_prod = catalogo[i][NOMBRE]
        unidades_vendidas = 0
        importe_vendido = 0.0

        for j in range(len(historial_ventas)):
            if cod_prod == historial_ventas[j][COD_PROD]:
                unidades_vendidas += historial_ventas[j][CANTIDAD]
                importe_vendido += historial_ventas[j][IMPORTE_FINAL]

        if unidades_vendidas:
            ranking.append([nom_prod, unidades_vendidas, importe_vendido])
    return ranking

def mostrar_resumen(catalogo, historial_ventas):
    """
    Muestra el resumen de las ventas realizado el día de hoy.
    
    Recibe: las variables acumuladas.
    
    Devuelve: imprime el resumen del día con las variables acumuladas solo si se realizaron ventas y devuelve las variables acumuladas. Caso contrario, solo muestra "Aún no se realizaron 
    ingresos" y devuelve las variables acumuladas.
    
    ."""
    print(" ")
    print("===========================================================================")
    if verificar_entradas(len(historial_ventas)):
        resumen_del_dia(catalogo, historial_ventas)
    else:
        print("Aún no se realizaron ingresos")
    print("===========================================================================")
    print(" ")

def salir(catalogo, historial_ventas):
    """
    Muestra el resumen del día, realiza la cuenta atrás y sale del sistema solo si don Ramón acepta nuevamente el cierre del sistema.
    
    Recibe: las variables acumuladas para mostrarlas si se realizaron ventas.
    
    Devuelve: imprime el resumen del día, la cuenta regresiva y sale del sistema devolviendo las variables acumuladas.
    
    ."""
    print("")
    opcion = verificar_cierre()
    if opcion == 6:
        if verificar_entradas(len(historial_ventas)):
            resumen_del_dia(catalogo, historial_ventas)
        else:
            print(" ")
            print("===================================================================")
            print("No se realizaron ventas este día.")
            print("===================================================================")
            print(" ")
        print(cuenta_regresiva(5))
        return opcion
        # cuenta_regresiva_iterativo(5) Realiza la cuenta regresiva de forma iterativa
    else:
        return opcion 
        

#------------ CODIGO DE LA SUERTE - START -------------#

def codigo_suerte(importe):
    """Desafío del código de la suerte: Algoritmo recursivo que suma los dígitos
    del importe final hasta que quede 1 solo dígito
    
    Recibe: Importe final (int)
    
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
    
    Devuelve: el número correspondiente a la opción elegida.
    
    ."""
    continuar = input("¿Desea continuar con el cierre? (Si/No): ").lower().strip()
    while (continuar != "si" and continuar != "sí" and continuar != "s") and (continuar != "no" and continuar != "n"):
        print("Entrada inválida. Ingrese la opción: 'Si' para continuar, 'No' para salir.")
        continuar = input("Si/No: ").lower().strip()
    if continuar == "si" or continuar == "sí" or continuar == "s":
        return 6
    return 0

#------------ OPCIONES DEL MENU - END -------------#

#------------ CUENTA REGRESIVA - START -------------#

def cuenta_regresiva(cuenta):
    """
    Realiza la cuenta atrás (de forma recursiva) cuando Don Ramón ingresa la opción 'si'. Mediante la función 'mostrar_cuenta' permite
    mostrar el número de 5 a 1.

    Recibe: el parámetro 'cuenta' (int)
    
    Devuelve: 'Caja cerrada'
    
    ."""
    if cuenta == 0:
        return "¡Caja cerrada!"
    mostrar_cuenta(cuenta)
    return cuenta_regresiva(cuenta - 1)

# def cuenta_regresiva_iterativo(cuenta):
#     """
#     Realiza la cuenta atrás (de forma iterativa) cuando Don Ramón ingresa la opción 'si'.

#     Recibe: el parámetro 'cuenta' (int)
    
#     Devuelve: No devuelve nada, solo imprime la cuenta regresiva e imprime Caja cerrada.
    
#     ."""
#     while cuenta > 0:
#         mostrar_cuenta(cuenta)
#         cuenta -= 1
#     else: print("¡Caja cerrada!") 

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

#------------ ACUMULADOR - START -------------#

def acumulador(catalogo, historial_ventas, acumuladores, venta_mas_grande, recaudado_por_categoria, cantidad_de_ventas_medio_pago):
    venta_mas_grande[0] = historial_ventas[0][IMPORTE_FINAL]
    venta_mas_grande[1] = historial_ventas[0][NRO_VENTA]
    posicion = buscar_por_codigo(catalogo,historial_ventas[0][COD_PROD])
    venta_mas_grande[2] =  catalogo[posicion][NOMBRE]
    for i in range(len(historial_ventas)):
        acumuladores[1] += historial_ventas[i][IMPORTE_FINAL]
        if historial_ventas[i][IMPORTE_FINAL] > venta_mas_grande[0]:
            venta_mas_grande[0] = historial_ventas[i][IMPORTE_FINAL]
            venta_mas_grande[1] = historial_ventas[i][NRO_VENTA]
            posicion = buscar_por_codigo(catalogo,historial_ventas[i][COD_PROD])
            venta_mas_grande[2] = catalogo[posicion][NOMBRE]
        categoria, medio_pago, importe = obtener_datos_venta(i,catalogo, historial_ventas)
        recaudado_por_categoria[categoria - 1] += importe
        cantidad_de_ventas_medio_pago[medio_pago - 1] += 1
    acumuladores[0] = len(historial_ventas)
    acumuladores[2] = acumuladores[1]/acumuladores[0]


#------------ ACUMULADOR DE CATEGORIA - START -------------#

def obtener_datos_venta(i, catalogo, historial_ventas):
    venta = historial_ventas[i] # num_ventas, producto[CODIGO], cantidad, medio_pago, importe_final

    posicion = buscar_por_codigo(catalogo, venta[COD_PROD])
    producto = catalogo[posicion]

    categoria = producto[CATEGORIA]
    medio_pago = venta[MEDIO_PAGO]
    importe = venta[IMPORTE_FINAL]

    return categoria, medio_pago, importe


#------------ ACUMULADOR DE CATEGORIA  - END -------------#

#------------ ACUMULADOR - END -------------#

#------------ FORMATEAR IMPORTE - START -------------#

def formatear_importe(importe):
    """
    Formatea un importe con separador de miles '.' y decimales ','.

    Pre:
        - importe es un número.

    Post:
        - Devuelve el importe con formato argentino.
    """
    importe = f"{importe:,.2f}"
    importe = importe.replace(",", "X")
    importe = importe.replace(".", ",")
    importe = importe.replace("X", ".")

    return importe

#------------ FORMATEAR IMPORTE - END -------------#

def resumen_del_dia(catalogo, historial_ventas):
    """
    Se encarga de mostrar de forma ordenada las ventas, el total recaudado, qué método de pago fue el más usado y el total recaudado por cada categoría en el día.
    
    Recibe: las variables acumuladas a mostar de forma organizada.
    
    Devuelve: no devuelve nada (imprime una lista ordenada).

    Pre:
        - catalogo contiene productos válidos.
        - historial_ventas contiene ventas válidas.

    Post:
        - Si no hay ventas, informa que no hay ventas.
        - Si hay ventas, muestra el resumen completo.
    
    ."""
    acumuladores = [
        0,      #   Cantidad de ventas
        0,      #   Total recaudado
        0,      #   Importe promedio
    ]

    venta_mas_grande = [
        0,      #   Venta más grande
        0,      #   Número de la venta
        ""      #   Producto
    ]

    recaudado_por_categoria = [
        0,      #   Categoría 1
        0,      #   Categoría 2
        0,      #   Categoría 3
        0       #   Categoría 4
    ]

    cantidad_de_ventas_medio_pago = [
        0,      # Efectivo
        0,      # Débito
        0       # Crédito
    ]

    acumulador(catalogo, historial_ventas, acumuladores, venta_mas_grande, recaudado_por_categoria, cantidad_de_ventas_medio_pago)

    print(" ")
    print("========= Ventas realizadas y total recaudado ==========")
    print(f"Ventas: {acumuladores[0]}")
    print(f"Recaudado: ${formatear_importe(acumuladores[1])}")
    print(f"Importe promedio por venta: ${formatear_importe(acumuladores[2])}")
    print("================= Venta más grande =====================")
    print(f"Número de la venta: {venta_mas_grande[1]}")
    print(f"Nombre del producto: {venta_mas_grande[2]}")
    print(f"Importe de la venta: ${formatear_importe(venta_mas_grande[0])}")
    print("===================================================================")
    print(f"Total recaudado por cada categoría de producto")
    if recaudado_por_categoria[0] == 0:
        print(f"Golosinas: No hay ventas de este tipo.")
    else:
        print(f"Golosinas: ${formatear_importe(recaudado_por_categoria[0])}")
    if recaudado_por_categoria[1] == 0:
        print(f"Bebidas: No hay ventas de este tipo.")
    else:
        print(f"Bebidas: ${formatear_importe(recaudado_por_categoria[1])}")
    if recaudado_por_categoria[2] == 0:
        print(f"Almacén: No hay ventas de este tipo.")
    else:
        print(f"Almacén: ${formatear_importe(recaudado_por_categoria[2])}")
    if recaudado_por_categoria[3] == 0:
        print(f"Librería: No hay ventas de este tipo.")
    else:
        print(f"Librería: ${formatear_importe(recaudado_por_categoria[3])}")
    print("===================================================================")
    print("Cantidad de ventas por cada medio de pago")
    print(f"Efectivo: {cantidad_de_ventas_medio_pago[0] if cantidad_de_ventas_medio_pago[0] != 0 else 'No se realizaron ventas con este método'}")
    print(f"Débito: {cantidad_de_ventas_medio_pago[1] if cantidad_de_ventas_medio_pago[1] != 0 else 'No se realizaron ventas con este método'}")
    print(f"Crédito: {cantidad_de_ventas_medio_pago[2] if cantidad_de_ventas_medio_pago[2] != 0 else 'No se realizaron ventas con este método'}")
    if cantidad_de_ventas_medio_pago[2] == cantidad_de_ventas_medio_pago[1] and cantidad_de_ventas_medio_pago[2] == cantidad_de_ventas_medio_pago[0]:
        print("Los tres tienen un mismo uso")
        print(f"Efectivo {cantidad_de_ventas_medio_pago[0]} uso/s, Débito {cantidad_de_ventas_medio_pago[1]} uso/s y Crédito {cantidad_de_ventas_medio_pago[2]} uso/s")
    else:
        if cantidad_de_ventas_medio_pago[0] >= cantidad_de_ventas_medio_pago[1] and cantidad_de_ventas_medio_pago[0] >= cantidad_de_ventas_medio_pago[2]:
            if cantidad_de_ventas_medio_pago[0] == cantidad_de_ventas_medio_pago[1]:
                print("Los más usados fueron")
                print(f"Efectivo {cantidad_de_ventas_medio_pago[0]} uso/s y Débito {cantidad_de_ventas_medio_pago[1]} uso/s")
            elif cantidad_de_ventas_medio_pago[0] == cantidad_de_ventas_medio_pago[2]:
                print("Los más usados fueron")
                print(f"Efectivo {cantidad_de_ventas_medio_pago[0]} uso/s y Crédito {cantidad_de_ventas_medio_pago[2]} uso/s")
            else:
                print("El que más veces se usó fue")
                print(f"Efectivo con {cantidad_de_ventas_medio_pago[0]} uso/s")
        elif cantidad_de_ventas_medio_pago[1] >= cantidad_de_ventas_medio_pago[0] and cantidad_de_ventas_medio_pago[1] >= cantidad_de_ventas_medio_pago[2]:
            if cantidad_de_ventas_medio_pago[1] == cantidad_de_ventas_medio_pago[2]:
                print("Los más usados fueron")
                print(f"Débito {cantidad_de_ventas_medio_pago[1]} uso/s y Crédito {cantidad_de_ventas_medio_pago[2]} uso/s")
            else:
                print("El que más veces se usó fue")
                print(f"Débito con {cantidad_de_ventas_medio_pago[1]} uso/s")
        elif cantidad_de_ventas_medio_pago[2] >= cantidad_de_ventas_medio_pago[0] and cantidad_de_ventas_medio_pago[2] >= cantidad_de_ventas_medio_pago[1]:
            print("El que más veces se usó fue")
            print(f"Crédito con {cantidad_de_ventas_medio_pago[2]} uso/s")
    print("===================================================================")

#------------ RESUMEN DEL DIA - END -------------#

#------------ FUNCIONALIDADES DEL MENU - START -------------#

def armar_matriz(catalogo, historial_ventas):
    matriz = [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]

    for i in range(len(historial_ventas)):
        posicion = buscar_por_codigo(catalogo,historial_ventas[i][COD_PROD])

        producto = catalogo[posicion]
        categoria = producto[CATEGORIA]
        medio_pago = historial_ventas[i][MEDIO_PAGO]
        importe = historial_ventas[i][IMPORTE_FINAL]

        matriz[categoria - 1][medio_pago - 1] += importe

    return matriz

def mostrar_matriz(catalogo, historial_ventas):
    matriz = armar_matriz(catalogo, historial_ventas)

    nombre_categoria = [
        "Golosinas",
        "Bebidas",
        "Almacén",
        "Librería"
    ]

    nombre_medios_pago = [
        "Efectivo",
        "Débito",
        "Crédito"
    ]
    
    total_medios = [
        0,
        0,
        0
    ]

    total_general = [
        0
    ]
    print()
    print("Categoría       ___Efectivo_________Débito_________Crédito_________TOTAL")

    for i in range(len(matriz)):
        total_categoria = 0
        for j in range(len(matriz[i])):
            total_categoria += matriz[i][j]
            total_medios[j] += matriz[i][j]
        
        total_general[0] += total_categoria

        print(
            f"{nombre_categoria[i]:<15}|"
            f"{formatear_importe(matriz[i][0]):>11}"
            f"{formatear_importe(matriz[i][1]):>15}"
            f"{formatear_importe(matriz[i][2]):>16}"
            f"{formatear_importe(total_categoria):>14}"
        )
    
    print(
        f"{'TOTAL':<15}|"
        f"{formatear_importe(total_medios[0]):>11}"
        f"{formatear_importe(total_medios[1]):>15}"
        f"{formatear_importe(total_medios[2]):>16}"
        f"{formatear_importe(total_general[0]):>14}"
    )
    print()


#------------ FUNCIONALIDADES DEL MENU - END -------------#

#------------ FUNCIONALIDADES DEL MENU - START -------------#

def menu():
    """Menu principal donde se ingresan las opciones para registrar ventas, ver resumen del día y cerrar caja
    
    ."""

    opcion = 0
    opc = 0
    while opcion != 6:
        print("=== KIOSCO EL CAMPUS v2 ===")
        print("1) Registrar una venta")
        print("2) Consultar el catálogo")
        print("3) Ver resumen del día")
        print("4) Ranking de productos más vendidos")
        print("5) Tabla categoría x medio de pago")
        print("6) Cerrar caja y salir")
        opcion = pedir_numero("Elija una opción: ", 1, 6)

        match opcion:
            case 1:
                registrar_venta(catalogo, historial_ventas)
            case 2:
                print("=====================================================")
                print("1) Listar el catálogo completo ordenado por código")
                print("2) Buscar por código")
                print("3) Buscar por nombre")
                print("4) Listar por categoría")
                print("5) Agregar un producto")
                print("6) Volver al menú principal")
                
                opc = pedir_numero("Seleccione una opción de catálogo: ", 1, 6)
                while opc != 6:
                    if opc == 1:
                        print("CÓDIGO | NOMBRE | CATEGORÍA | PRECIO | STOCK")
                        for i in range(len(catalogo)):
                            print(f"{catalogo[i][CODIGO]} | {catalogo[i][NOMBRE]} | {CATEGORIAS[catalogo[i][CATEGORIA] -1]} | ${formatear_importe(catalogo[i][PRECIO])} | {catalogo[i][STOCK]}")
                    elif opc == 2:
                        cod = pedir_numero("Ingrese el código del producto a buscar: ", 1 , maximo_catalogo(catalogo)) 
                        producto = buscar_por_codigo(catalogo, cod)
                        if producto != -1:
                            print(f"Codigo: {catalogo[producto][CODIGO]}")
                            print(f"Nombre: {catalogo[producto][NOMBRE]}")
                            print(f"Categoría: {CATEGORIAS[catalogo[producto][CATEGORIA] - 1]}")
                            print(f"Precio: ${formatear_importe(catalogo[producto][PRECIO])}")
                            print(f"Stock: {catalogo[producto][STOCK]} unidades")
                        else:
                            print("El código ingresado no existe")
                    elif opc == 3:
                        coincidencias = 0
                        texto = input("Ingrese el producto a buscar: ").lower()
                        for i in range(len(catalogo)):
                            if texto in catalogo[i][NOMBRE].lower():
                                coincidencias = 1
                                print(catalogo[i][NOMBRE])
                        if coincidencias == 0:
                            print("No se hallaron coincidencias")
                    elif opc == 4:
                        reponer_prod = 0
                        for i in range(len(CATEGORIAS)):
                            print(f"{i+1}) {CATEGORIAS[i]}")
                        categoria = pedir_numero("Ingrese la categoría a buscar: ", 1, 4)
                        for i in range(len(catalogo)):
                            if categoria == catalogo[i][CATEGORIA]:
                                print(f"Producto: {catalogo[i][NOMBRE]} | Stock: {catalogo[i][STOCK]}")
                                if catalogo[i][STOCK] < STOCK_MINIMO:
                                    reponer_prod += 1
                        if reponer_prod:
                            print(f"{reponer_prod} Productos tienen stock por debajo del mínimo de reposición!")
                    elif opc == 5:
                        codigo = pedir_numero("Ingrese el código del producto a agregar: ", 1 , float("inf"))
                        while buscar_por_codigo(catalogo, codigo) != -1:
                            print("ERROR: El código no puede repetirse!")
                            codigo = pedir_numero("Ingrese el código del producto a agregar: ", 1 , float("inf"))
                        nombre = input("Ingrese el nombre del producto a agregar: ").capitalize().replace("  ", " ")
                        for i in range(len(CATEGORIAS)):
                            print(f"{i+1}) {CATEGORIAS[i]}")
                        categoria = pedir_numero("Ingrese la categoría a la que pertenece el producto: ", 1, 4)
                        precio = pedir_numero("Ingrese el precio por unidad del producto: ", 0, float('inf'))
                        stock = pedir_numero("Ingrese la cantidad de stock del producto: ", 0, float('inf'))
                        nuevo_producto = [codigo, nombre, categoria, precio, stock]
                        catalogo.append(nuevo_producto)
                        ord_insercion(catalogo, CODIGO, False)

                    print("=====================================================")
                    print("1) Listar el catálogo completo ordenado por código")
                    print("2) Buscar por código")
                    print("3) Buscar por nombre")
                    print("4) Listar por categoría")
                    print("5) Agregar un producto")
                    print("6) Volver al menú principal")
                    
                    opc = pedir_numero("Seleccione una opción de catálogo: ", 1, 6)
            case 3:
                mostrar_resumen(catalogo, historial_ventas)
            case 4:
                if len(historial_ventas) == 0:
                    print("No se han registrado ventas el dia de hoy")
                else:
                    ranking = armar_ranking(catalogo, historial_ventas)
                    ord_insercion(ranking, RANK_CANT, True)

                    print("=== RANKING DEL DIA ===")
                    for i in range(len(ranking)):
                        print(f"{i+1}. {ranking[i][RANK_NOM]} | {ranking[i][RANK_CANT]} un. | ${ranking[i][RANK_IMP]:.2f}")
            case 5:
                mostrar_matriz(catalogo, historial_ventas)
            case 6:
                opcion = salir(catalogo, historial_ventas)

#------------ FUNCIONALIDADES DEL MENU - END -------------#

catalogo = catalogo_inicial()
ord_insercion(catalogo, CODIGO, False)
menu()