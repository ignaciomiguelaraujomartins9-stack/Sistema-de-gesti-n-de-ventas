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

H_FECHA, H_NUMERO, H_CODIGO, H_CANTIDAD, H_MEDIO, H_IMPORTE = 0, 1, 2, 3, 4, 5

#------------ ARCHIVOS - START -------------#

ARCHIVO_PRODUCTOS = "productos.csv"
ARCHIVO_BACKUP = "productos_backup.csv"
ARCHIVO_VENTAS = "ventas.csv"
ARCHIVO_NOVEDADES = "novedades.csv"
ARCHIVO_ERRORES = "errores.log"
PREFIJO_CIERRE = "cierre_"          # el cierre del día se guarda en cierre_AAAA-MM-DD.txt
SEPARADOR = ";"
CODIFICACION = "utf-8"

#------------ ARCHIVOS - END -------------#

#------------ POSICIONES - END -------------#

#------------ CATEGORIAS - START -------------#

CATEGORIAS = ["Golosinas", "Bebidas", "Almacén", "Librería"]   # índice + 1 = número de categoría
MEDIOS_PAGO = ["Efectivo", "Débito", "Crédito"]                 # índice + 1 = número de medio
STOCK_MINIMO = 5   
TOP_RANKING = 5  

#------------ CATEGORIAS - END -------------#

# Posiciones de una fila del total por día: [fecha, importe]
TD_FECHA, TD_IMPORTE = 0, 1

# Posiciones de una fila del ranking histórico: [codigo, nombre, unidades]
HR_CODIGO, HR_NOMBRE, HR_UNIDADES = 0, 1, 2

# Posiciones de los campos de una línea de novedades.csv
N_CODIGO, N_PRECIO, N_CANTIDAD = 0, 1, 2

#------------ VARIABLES CONSTANTES - END -------------#

#------------ CATALOGO - START -------------#

# =============================================================================
# CATÁLOGO DE RESPALDO
# -----------------------------------------------------------------------------
# Es el catálogo del TP2. Se usa SOLAMENTE si productos.csv no existe: en ese
# caso el programa avisa, arranca con estos productos y crea el archivo.
# =============================================================================
def catalogo_inicial():
    """Devuelve el catálogo de respaldo del kiosco (lista de listas, sin ordenar)."""
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

#------------ HISTORIAL DE VENTAS, CONSTANTES + RANKING - START -------------#

historial_ventas = []
NRO_VENTA, COD_PROD, CANTIDAD, MEDIO_PAGO, IMPORTE_FINAL = 0, 1, 2, 3, 4
RANK_NOM, RANK_CANT, RANK_IMP = 0, 1, 2

#------------ HISTORIAL DE VENTAS, CONSTANTES + RANKING - END -------------#

#------------ ACUMULADOR, VENTA MAS GRANDE, CATEGORIA TOTAL, MEDIO DE PAGO TOTAL - START -------------#

CANTIDAD_VENTAS, TOTAL_RECAUDADO, IMPORTE_PROMEDIO = 0,1,2

VENTA_MAS_GRANDE, NUMERO_DE_LA_VENTA_GRANDE, PRODUCTO = 0,1,2

CAT1_TOTAL, CAT2_TOTAL, CAT3_TOTAL, CAT4_TOTAL = 0,1,2,3

METODO_EFECTIVO, METODO_DEBITO, METODO_CREDITO = 0,1,2

#------------ HISTORIAL DE VENTAS, CONSTANTES + RANKING - END -------------#

#------------ ORDENAMIENTO - START -------------#

def ordenar(lista, campo, descendente = False):
    """
    Función reutilizable que ordena los elementos de una lista por el método de inserción.
    
    Recibe: lista (list), campo (int), descendiente (booleano)

    Devuelve: No devuelve ningún valor. Modifica a la lista.

    Pre: los elementos de la lista deben ser comparables, además, se debe indicar el campo 
    por el cual se ordenará (este debe de ser un número) y de qué forma ordenar (descendiente o ascendiente)
    
    Post: La lista queda ordenada según el campo elegido.
    """
    for i in range(1, len(lista)):
        v = lista[i]
        j = i - 1
        while j >= 0 and ((not descendente and lista[j][campo] > v[campo]) or (descendente and lista[j][campo] < v[campo])):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = v

#------------ ORDENAMIENTO - END -------------#

#------------ BUSQUEDA - START -------------#

def buscar_por_codigo(lista, producto):
    """ Función que realiza la búsqueda de un elemento mediante el método de busqueda binaria.
        
        Recibe: lista (list), producto (int)

        Devuelve: devuelve la lista que contenga el códgio del producto buscado, en caso de no 
        encontraro, devuelve -1.

        Pre: La lista debe estar ordenada. El código debe de exisitir o debe de encontrarse dentro
        dentro de la categoría. El código debe de ser un entero.

        Post: Devuelve lista[medio], que es el producto para 
        utilizarse en el registro de una venta, la búsqueda de un producto por nombre o el registro
        de un producto nuevo. Si no existe, devuelve -1
    """
    izq = 0
    der = len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio][CODIGO] == producto:
            return lista[medio]
        elif lista[medio][CODIGO] > producto:
            der = medio - 1
        else:
            izq = medio + 1
    return -1

#------------ BUSQUEDA - END -------------#

#------------ OPCIONES DEL MENU - START -------------#

def pedir_numero(mensaje, min, max, fecha = False):
    """
    Función reutilizable que pide un número en un rango al usuario hasta que sea válido.

    Recibe: Mensaje (str) a mostrar, minimo (int) y máximo (int) permitido del número
    
    Devuelve: El número ya validado dentro de el rango (int)

    Pre: Mensaje debe ser un dígito y debe de estar entre max y min. Max y Min deben ser enteros.

    Post: Devuelve el número entero. El número cumple con ser menor que max y mayor que min.

    ."""
    entrada = input(mensaje)
    try:
        entrada = int(entrada)
    except ValueError as e:
        raise ValueError(f"Error, el valor ingresado no es numérico: '{entrada}'")

    while not (min <= entrada <= max):
        print(f"Opción inválida. Ingrese un número entre {min} y {max}")
        entrada = input(mensaje)
        try:
            entrada = int(entrada)
        except ValueError as e:
            raise ValueError(f"Error, el valor ingresado no es numérico: '{entrada}'")
    if fecha:
        if entrada > 0 and entrada < 10:
            entrada = "0" + str(entrada)
    return entrada

def descuento_monto(precio, cantidad):
    """Calcula el descuento si se supera el monto minimo de descuento.

    Recibe: precio (int) y cantidad (int)
    
    Devuelve:
        Tupla. subtotal (variable sin el descuento aplicado) (int), descuento (float),
    subtotal_d (variable con el descuento aplicado) (float)
    
    Pre: Precio y cantidad deben ser un entero. MONTO MINIMIO DESCUENTO debe de estar previamente
    definido, así como PORCENTAJE DESCUENTO MONTO. 

    Post: El subtotal debe de ser mayor al monto mínimo para recibir un descuento, si no, no recibe
    descuento. Devuelve la tupla.

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

    Recibe: Subtotal_d (Subtotal con descuento de monto aplicado) (float), medio_pago (int)
    
    Devuelve: Importe final (float), descuento por efectivo (float), recargo por crédito (float)
    
    Pre: Medio de pago debe de ser 1 o 3 para recibir descuento ya sea en efectivo o crédito.

    Post: Devuelve el importe final con descuento en efectivo si el método de pago es con efectivo o
    devuelve el importe final con descuento en crédito si el método de pago es con crédito. Además,
    devuelve una tupla con el importe final, el descuento y el recargo.

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
    """
    
    Muestra en pantalla el ticket con toda la información calculada por las otras funciones

    Recibe: cantidad (int), precio (float), nombre_producto (str), medio_pago (int), subtotal (float), subtotal_d (Subtotal con descuento de monto aplicado), descuento (float), descuento_efectivo (float), recargo (flotat), importe_final (float), nro_venta (int)

    Devuelve: No devuelve nada. Muestra el ticket en pantalla.

    Pre: Se debe de realizar una venta.

    Post: Muestra en pantalla un ticket con los datos de la venta informando descuento o recargos
    correspondientes al medio de pago.
    
    """
    
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

def guardar_venta(fecha, venta):
    with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as ventas:
        v = f"{fecha}"
        for i in range(len(venta)):
            v += f";{venta[i]}"
        ventas.write(f"{v}\n")

def registrar_venta(catalogo, historial_ventas, fecha, verificado):
    """ 
        Función que registra la venta de un producto.

        Recibe: catalogo (int), historial de ventas (list)

        Devuelve: No devuelve nada. Agrega las ventas a la lista.
        
        Pre: El catálogo debe estar ordenado.
        
        Post: Se emite el ticket y la venta se agrega al historial de ventas.
    """
    cod = pedir_numero("Ingrese el codigo del producto (Ingrese 0 para cancelar): ", 0 , float('inf')) 
    while cod != 0:
        producto = buscar_por_codigo(catalogo, cod)
        if producto != -1:
            if producto[STOCK] != 0:
                print(f"Nombre: {producto[NOMBRE]}")

                print(f"Precio: ${formatear_importe(producto[PRECIO])}")
                print(f"Stock: {producto[STOCK]} unidades")

                cantidad = pedir_numero("Ingrese la cantidad: ", 1, producto[STOCK])

                print("============")
                print("1. Efectivo")
                print("2. Débito")
                print("3. Crédito")
                medio_pago = pedir_numero("Ingrese el medio de pago (1/2/3): ", 1, 3)
                
                if not verificado:
                    verificado, historial_ventas = buscar_por_fecha(ARCHIVO_VENTAS, fecha, historial_ventas)
                
                num_ventas = len(historial_ventas) + 1

                subtotal, descuento, subtotal_d = descuento_monto(producto[PRECIO], cantidad)
                importe_final, descuento_efectivo, recargo = ajuste_medio_pago(subtotal_d, medio_pago)
                codigo = codigo_suerte(int(importe_final))
                mostrar_ticket(cantidad, producto[PRECIO], producto[NOMBRE], medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo, num_ventas)

                print(f"AVISO: El stock de {producto[NOMBRE]} pasa de {producto[STOCK]} a {producto[STOCK] - cantidad}")
                producto[STOCK] -= cantidad
                venta = num_ventas, producto[CODIGO], cantidad, medio_pago, importe_final
                guardar_venta(fecha,venta)
                historial_ventas.append(venta)
                return verificado
            else:
                print()
                print(f"Producto sin stock (es necesario reponer: '{producto[NOMBRE]}')")
                cod = pedir_numero("Ingrese el codigo de otro producto (Ingrese 0 para cancelar): ", 0 , float('inf')) 
        else:
            print()
            print("El código ingresado no existe")
            cod = pedir_numero("Ingrese el codigo del producto (Ingrese 0 para cancelar): ", 0 , float('inf')) 

def armar_ranking(catalogo, historial_ventas):
    """ 
        Función que permite generar el ranking de los productos más vendidos en el día

        Recibe: catálogo (list), historial de venta (list)

        Devuelve: El ranking de los productos más vendidos en el día.
        
        Pre: El catálogo debe estar ordenado, el historial de ventas debe poseer al menos un elemento
        
        Post: Devuelve el ranking de ventas donde cada elemento posee el nombre del producto, las
        unidades vendidas su  monto total
    ."""
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
    
    Recibe: catálogo (list), historial_ventas (list)
    
    Devuelve: No devuelve nada. Imprime el resumen del día solo si hay ventas, en caso de que
    no existan ventas, imprime "Aún no se realizaron ingresos" para evitar división por cero.
    
    Pre: Deben de existir ventas para imprimir el resumen del día.

    Post: Imprime el resumen del día o el mensaje de que aún no se realizaron ingresos.

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
    Muestra el resumen del día, realiza la cuenta atrás y sale del sistema solo si don Ramón confirma el cierre del sistema.
    
    Recibe: Catálogo (list), historial de ventas (list).
    
    Devuelve: Devuelve 6 si acepta cerrar el programa e imprime el resumen del día, la cuenta regresiva. Devuelve 
    0 si desea continuar, sin mostrar nada en el proceso.
    
    Pre: Historial de ventas debe tener ventas realizadas para ejecutar el resumen del día e imprimir ranking. El usuario debe escribir Sí-si-s para contiunar con el cierre.

    Post: Se cierra el programa mostrando el resumen del día (si las hay), los productos a reponer (si los hay) y
    el ranking (si los hay) de ventas.
    ."""
    print("")
    opcion = verificar_cierre()
    if opcion == 6:
        if verificar_entradas(len(historial_ventas)):
            print("=====================================================================================")
            resumen_del_dia(catalogo, historial_ventas)
            print("=====================================================================================")
            lista = productos_reponer(catalogo)
            if lista:
                mostrar_repone(lista)
            else:
                print("No hay productos a reponer")
            print("=====================================================================================")
            imprimir_ranking(catalogo, historial_ventas)
            print("=====================================================================================")
            print(" ")
        else:
            print(" ")
            print("=====================================================================================")
            print("No se realizaron ventas este día.")
            print("=====================================================================================")
            lista = productos_reponer(catalogo)
            if lista:
                mostrar_repone(lista)
            else:
                print("No hay productos a reponer")
            print("=====================================================================================")
            imprimir_ranking(catalogo, historial_ventas)
            print("=====================================================================================")
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
    
    Pre: importe debe de ser entero y mayor o igual a cero.

    Post: Devuelve un único dígito que surge de la suma repetida de los dígitos de importe,
    si importe es 0, devuelve 0

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

    Pre: El usuario debe poder ingresar texto por teclado.

    Post: La función no finaliza si no recibe una entrada correcta, esta acpeta
    "S","s","si","Si","Sí" y "sí", a su vez acepta "n","N","No" y "no". Devuelve 6 cuando
    se confirma el cierre, cero cuando no se confirma el cierre.
    
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
    
    Pre: Cuenta debe ser un número entero mayor a 0. mostrar cuenta debe de estar definida

    Post: Muestra mediante mostrar cuenta la cuenta regresiva hasta que llegue a cero y devuelva
    "¡Caja cerrada!"

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

    Recibe: El parámetro cuenta que viene desde 'cuenta_regresiva'.
    
    Devuelve: No devuelve ningún valor (solo imprime el número).
    
    Pre: Debe de contener algo.

    Post: Imprime el valor que contenga cuenta sin modificar el valor recibido.
    ."""
    print(cuenta)

#------------ CUENTA REGRESIVA - END -------------#

#------------ RESUMEN DEL DIA - START -------------#

def verificar_entradas(cantidad):
    """
    Verifica si la cantidad de productos es mayor a 0 para verificar si mostrar el resumen del día o mostrar 'no se realizaron ventas este día'
    
    Recibe: cantidad (int).
    
    Devuelve: True si la cantidad es mayor a 0. False si la cantidad es menor o igual a 0.
    
    Pre: cantidad debe ser mayor a 0 y un número entero.

    Post: Retorna Ture si es mayor a 0. False si es mayor o igual.

    ."""
    
    return cantidad > 0

#------------ ACUMULADOR - START -------------#

def acumulador(catalogo, historial_ventas, acumuladores, venta_mas_grande, recaudado_por_categoria, cantidad_de_ventas_medio_pago):
    """
        Obtiene los valores de cada venta para acumularlos en sus listas correspondientes para luego
        ser imprimidos en resumen del día

        Recibe: catálogo (list), historial_ventas (list), acumuladores (list), venta_mas_grande (list), recaudado_por_categoria (list), cantidad_de_ventas_medio_pago

        Devuelve: No devuelve nada. Modifica cada lista con sus datos correspondientes.

        Pre: Las listas deben de estar definidas y no ser globales. Historial de ventas no debe ser 0. Historial ventas debe
        estar ordenado. Obtener datos venta debe estar definida.

        Post: Obtiene los valores de cada lista y los acumula o almacena en sus listas correspondientes sin devolver ningún valor.
        
        """

    venta_mas_grande[VENTA_MAS_GRANDE] = historial_ventas[0][IMPORTE_FINAL]
    venta_mas_grande[NUMERO_DE_LA_VENTA_GRANDE] = historial_ventas[0][NRO_VENTA]
    producto = buscar_por_codigo(catalogo,historial_ventas[0][COD_PROD])
    venta_mas_grande[PRODUCTO] =  producto[NOMBRE]
    for i in range(len(historial_ventas)):
        acumuladores[TOTAL_RECAUDADO] += historial_ventas[i][IMPORTE_FINAL]
        if historial_ventas[i][IMPORTE_FINAL] > venta_mas_grande[VENTA_MAS_GRANDE]:
            venta_mas_grande[VENTA_MAS_GRANDE] = historial_ventas[i][IMPORTE_FINAL]
            venta_mas_grande[NUMERO_DE_LA_VENTA_GRANDE] = historial_ventas[i][NRO_VENTA]
            producto = buscar_por_codigo(catalogo,historial_ventas[i][COD_PROD])
            venta_mas_grande[PRODUCTO] = producto[NOMBRE]
        categoria, medio_pago, importe = obtener_datos_venta(i,catalogo, historial_ventas)
        recaudado_por_categoria[categoria - 1] += importe
        cantidad_de_ventas_medio_pago[medio_pago - 1] += 1
    acumuladores[CANTIDAD_VENTAS] = len(historial_ventas)
    acumuladores[IMPORTE_PROMEDIO] = acumuladores[TOTAL_RECAUDADO]/acumuladores[CANTIDAD_VENTAS]

#------------ ACUMULADOR DE CATEGORIA - START -------------#

def obtener_datos_venta(i, catalogo, historial_ventas):
    """
        Obtiene la categoría, el medio de pago y el importe final correspondiente a una venta.

        Recibe: i (int), catálogo (list), historial ventas (list)

        Devuelve: Tupla. Categoría, medio de pago e importe.

        Pre: i debe ser un entero y un índice válido de historial de ventas. La venta que se 
        ubica en el historial de ventas debe tener el formato esperado. El código debe existir
        en el catálogo.

        Post: Devuelve la categoría del producto vendido. Devuelve el medio de pago usado. 
        Devuelve el importe final de la venta. No modifica el catálogo ni el historial de ventas.
    
    """
    venta = historial_ventas[i] 

    producto = buscar_por_codigo(catalogo, venta[COD_PROD])

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

    Recibe: Importe (float)

    Devuelve: importe con decimales, punto como separador de miles y coma como separador decimal.

    Pre: importe es un número.

    Post: Devuelve el importe con formato argentino. Utiliza "." como separador de miles y "," como 
    separado decimal.
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
    
    Recibe: catálogo (list), historial de ventas (list).
    
    Devuelve: no devuelve nada. Imprime una lista ordenada.

    Pre: catálogo contiene productos válidos. Historial_ventas contiene ventas válidas.

    Post: Si no hay ventas, informa que no hay ventas. Si hay ventas, muestra el resumen completo.
    
    ."""
    acumuladores = [
        0,      #   Cantidad de ventas
        0,      #   Total recaudado
        0       #   Importe promedio
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
    print(f"Ventas: {acumuladores[CANTIDAD_VENTAS]}")
    print(f"Recaudado: ${formatear_importe(acumuladores[TOTAL_RECAUDADO])}")
    print(f"Importe promedio por venta: ${formatear_importe(acumuladores[IMPORTE_PROMEDIO])}")
    print("================= Venta más grande =====================")
    print(f"Número de la venta: {venta_mas_grande[NUMERO_DE_LA_VENTA_GRANDE]}")
    print(f"Nombre del producto: {venta_mas_grande[PRODUCTO]}")
    print(f"Importe de la venta: ${formatear_importe(venta_mas_grande[VENTA_MAS_GRANDE])}")
    print("===================================================================")
    print(f"Total recaudado por cada categoría de producto")
    if recaudado_por_categoria[CAT1_TOTAL] == 0:
        print(f"Golosinas: No hay ventas de este tipo.")
    else:
        print(f"Golosinas: ${formatear_importe(recaudado_por_categoria[CAT1_TOTAL])}")
    if recaudado_por_categoria[CAT2_TOTAL] == 0:
        print(f"Bebidas: No hay ventas de este tipo.")
    else:
        print(f"Bebidas: ${formatear_importe(recaudado_por_categoria[CAT2_TOTAL])}")
    if recaudado_por_categoria[CAT3_TOTAL] == 0:
        print(f"Almacén: No hay ventas de este tipo.")
    else:
        print(f"Almacén: ${formatear_importe(recaudado_por_categoria[CAT3_TOTAL])}")
    if recaudado_por_categoria[CAT4_TOTAL] == 0:
        print(f"Librería: No hay ventas de este tipo.")
    else:
        print(f"Librería: ${formatear_importe(recaudado_por_categoria[CAT4_TOTAL])}")
    print("===================================================================")
    print("Cantidad de ventas por cada medio de pago")
    print(f"Efectivo: {cantidad_de_ventas_medio_pago[METODO_EFECTIVO] if cantidad_de_ventas_medio_pago[METODO_EFECTIVO] != 0 else 'No se realizaron ventas con este método'}")
    print(f"Débito: {cantidad_de_ventas_medio_pago[METODO_DEBITO] if cantidad_de_ventas_medio_pago[METODO_DEBITO] != 0 else 'No se realizaron ventas con este método'}")
    print(f"Crédito: {cantidad_de_ventas_medio_pago[METODO_CREDITO] if cantidad_de_ventas_medio_pago[METODO_CREDITO] != 0 else 'No se realizaron ventas con este método'}")
    if cantidad_de_ventas_medio_pago[METODO_CREDITO] == cantidad_de_ventas_medio_pago[METODO_DEBITO] and cantidad_de_ventas_medio_pago[METODO_CREDITO] == cantidad_de_ventas_medio_pago[METODO_EFECTIVO]:
        print("Los tres tienen un mismo uso")
        print(f"Efectivo {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s, Débito {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s y Crédito {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
    else:
        if cantidad_de_ventas_medio_pago[METODO_EFECTIVO] >= cantidad_de_ventas_medio_pago[METODO_DEBITO] and cantidad_de_ventas_medio_pago[METODO_EFECTIVO] >= cantidad_de_ventas_medio_pago[METODO_CREDITO]:
            if cantidad_de_ventas_medio_pago[METODO_EFECTIVO] == cantidad_de_ventas_medio_pago[METODO_DEBITO]:
                print("Los más usados fueron")
                print(f"Efectivo {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s y Débito {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s")
            elif cantidad_de_ventas_medio_pago[METODO_EFECTIVO] == cantidad_de_ventas_medio_pago[METODO_CREDITO]:
                print("Los más usados fueron")
                print(f"Efectivo {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s y Crédito {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
            else:
                print("El que más veces se usó fue")
                print(f"Efectivo con {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s")
        elif cantidad_de_ventas_medio_pago[METODO_DEBITO] >= cantidad_de_ventas_medio_pago[METODO_EFECTIVO] and cantidad_de_ventas_medio_pago[METODO_DEBITO] >= cantidad_de_ventas_medio_pago[METODO_CREDITO]:
            if cantidad_de_ventas_medio_pago[METODO_DEBITO] == cantidad_de_ventas_medio_pago[METODO_CREDITO]:
                print("Los más usados fueron")
                print(f"Débito {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s y Crédito {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
            else:
                print("El que más veces se usó fue")
                print(f"Débito con {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s")
        elif cantidad_de_ventas_medio_pago[METODO_CREDITO] >= cantidad_de_ventas_medio_pago[METODO_EFECTIVO] and cantidad_de_ventas_medio_pago[METODO_CREDITO] >= cantidad_de_ventas_medio_pago[METODO_DEBITO]:
            print("El que más veces se usó fue")
            print(f"Crédito con {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
    print("===================================================================")

#------------ RESUMEN DEL DIA - END -------------#

#------------ FUNCIONALIDADES DEL MENU - START -------------#


def imprimir_ranking(catalogo, historial_ventas):
    """
        Construye mediante armar ranking el ranking de los productos más vendidos en el día y lo imprime

        Recibe: Catálogo (list), historial de ventas (list)
        
        Devuelve: No devuelve nada. 

        Pre: Historial de ventas debe contener una o más ventas. Armar ranking debe de estar definido.
        Ordenar insercion debe de estar definida. 

        Post: Se imprime el ranking del día si hay más de una o más ventas e imprime el ranking.
        Si no hay ventas, imprime el mensaje c "No se han registrado ventas el dia de hoy"
    """

    if len(historial_ventas) == 0:
        print("No se han registrado ventas el dia de hoy")
    else:
        ranking = armar_ranking(catalogo, historial_ventas)
        ordenar(ranking, RANK_CANT, True)
        print("=== RANKING DEL DIA ===")
        for i in range(len(ranking)):
            print(f"{i+1}. {ranking[i][RANK_NOM]} | {ranking[i][RANK_CANT]} un. | ${ranking[i][RANK_IMP]:.2f}")
    
def armar_matriz(catalogo, historial_ventas):
    """
        Construye la matriz con la recaudación por categoría y medio de pago.

        Recibe: catálogo (list), historial de ventas (list)

        Devuelve: list. Matriz de 4 filas y 3 columnas. Cada fila representa una categoría
        y cada columna representa un medio de pago. Cada posición contiene el importe total 
        recaudado.

        Pre: catálogo debe de estar ordenado por códgio de producto.

        Post: Se acumulan las ventas en las posiciones correspondientes a su categoría y medio de pago.

    """

    matriz = [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]

    for i in range(len(historial_ventas)):
        producto = buscar_por_codigo(catalogo,historial_ventas[i][COD_PROD])

        categoria = producto[CATEGORIA]
        medio_pago = historial_ventas[i][MEDIO_PAGO]
        importe = historial_ventas[i][IMPORTE_FINAL]

        matriz[categoria - 1][medio_pago - 1] += importe

    return matriz

def mostrar_matriz(catalogo, historial_ventas):
    """
        Muestra por pantalla la recaudación total agrupada por categoría y medio de pago.

        Recibe: catálogo (list), historial de ventas (list)

        Pre: catálogo debe estar ordenado por código de producto. Armar matriz debe estar 
        definida y devuelve una matriz de 4 filas y 3 columnas. Formatear importe está definida
        y recibe el importe.

        Post: Se muestra por la pantalla la matriz con la recaudación de cáda categoría según el
        método de pago sin modificar al catálogo ni al hisotrial de ventas.
    """

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

def productos_reponer(catalogo):
    """
        Construye la lista con los stock que necesitan reposición

        Recibe: catálogo (list)

        Devuelve: No devuelve nada. 

        Pre: Cada producto debe contener mínimo, su código, nombre, categoría, precio y stock. 
        Catálogo debe estar ordenado por stock de forma ascendiente. Ordenar insercion está
        definida.

        Post: El catálogo queda ordenado de forma ascendente. Retorna la lista con los valores que se obtienen de catálogo. Ordena
        nuevamente por código de forma ascendente 
    """
    lista = []
    ordenar(catalogo,STOCK,False)
    for i in range(len(catalogo)):
        if catalogo[i][STOCK] < STOCK_MINIMO:
            lista.append([
                catalogo[i][CODIGO],
                catalogo[i][NOMBRE],
                CATEGORIAS[catalogo[i][CATEGORIA] - 1],
                catalogo[i][PRECIO],
                catalogo[i][STOCK],
                "¡REPONER!"])
    ordenar(catalogo, CODIGO, False)
    return lista

def mostrar_repone(lista):
    """
        Muestra por pantalla los productos cuyo stock es menor al mínimo establecido.

        Recibe: catálogo (list)

        Devuelve: No devuelve nada. Muestra información por pantalla.

        Pre: Lista debe contener elementos que cumplan con la condición de su stock menor al mínimo deseado.

        Post: Imprime por código, nombre, categoría, precio y stock, a los productos que tienen menos del mínimo de stock deseado, avisandole
        con la palabra "¡REPONER!" al lado derecho del stock.
    """
    print("Código    Nombre                      Categoría        Precio           Stock")
    for i in range(len(lista)):
        print(
            f"|{lista[i][0]:<8}"
            f"|{lista[i][1]:>20}"
            f"|{lista[i][2]:>15}"
            f"|{lista[i][3]:>13}"
            f"|{lista[i][4]:>11}"
            f"¡REPONER!"
        )

def busqueda_por_nombre(catalogo, historial_ventas):
    """
    Busca productos cuyo nombre contenga el texto dado, sin distinguir mayúsculas.

    Recibe: catalogo (list), texto (str)

    Devuelve: lista de productos del catálogo cuyo nombre contiene el texto buscado.
    
    Lista vacía si no hay coincidencias.
    """
    coincidencias = 0
    texto = input("Ingrese el producto a buscar: ").lower()
    for i in range(len(catalogo)):
        if texto in catalogo[i][NOMBRE].lower():
            coincidencias = 1
            print(catalogo[i][NOMBRE])
    if coincidencias == 0:
        print("No se hallaron coincidencias")

def convertir(numero, tipo, categoria):
    try:
        tipo(numero)
    except ValueError:
        raise ValueError(f"Error, el campo '{categoria}' debe tener un valor válido: {numero!r}")
    else:
        return tipo(numero)

def crear_producto(campos):
    """Construye un producto a partir de los cinco campos leídos de una línea.

    Pre:  campos es una lista de cadenas (lo que devuelve linea.split(SEPARADOR)).
    Post: devuelve [codigo, nombre, categoria, precio, stock] con los tipos
          correctos y los valores validados.
    Lanza: ValueError si no hay exactamente 5 campos, si algún número no se puede
           convertir o si algún valor está fuera de rango. La función DETECTA el
           error; QUIEN LA LLAMA decide qué hacer con él (Clase 11).
    """
    if len(campos) != 5:
        raise ValueError(f"se esperaban 5 campos y hay {len(campos)}")
    codigo = convertir(campos[CODIGO], int, "codigo")
    nombre = campos[NOMBRE].strip()
    categoria = convertir(campos[CATEGORIA], int, "categoria")
    precio = convertir(campos[PRECIO], float, "precio")
    stock = convertir(campos[STOCK], int, "stock")
    if codigo <= 0:
        raise ValueError(f"código inválido: {codigo}")
    if nombre == "":
        raise ValueError("el nombre está vacío")
    if not 1 <= categoria <= len(CATEGORIAS):
        raise ValueError(f"categoría inexistente: {categoria}")
    if precio <= 0:
        raise ValueError(f"precio inválido: {precio}")
    if stock < 0:
        raise ValueError(f"stock negativo: {stock}")
    return [codigo, nombre, categoria, precio, stock]

def registrar_error(fecha, origen, detalle):
    """Agrega una línea al registro de errores.

    Pre:  fecha es una cadena AAAA-MM-DD; origen y detalle son cadenas.
    Post: errores.log tiene una línea más al final, con el formato
          "fecha | origen | detalle". Si el archivo no existe, lo crea.
          Si no se puede escribir, avisa por pantalla y el programa sigue.
    """
    try:
        with open(ARCHIVO_ERRORES, "a", encoding=CODIFICACION) as log:
            log.write(f"{fecha} | {origen} | {detalle}\n")
    except OSError:
        raise OSError("Aviso: no se pudo escribir en el registro de errores.")

def verificar_existencia_datos(ruta):
    with open(ruta, "r", encoding=CODIFICACION) as log:
        lineas = log.read() 
        return len(lineas)      

def pedir_fecha():
    print("Ingrese la fecha de hoy (se usará en todo el programa)")
    año = str(pedir_numero("Ingrese el año actual: ", 2026, 2030))
    mes = str(pedir_numero("Ingrese el mes actual (01-12): ", 1, 12, True))
    dia = str(pedir_numero("Ingrese el día actual (01-30): ", 1, 30, True))
    fecha = f"{año}-{mes}-{dia}"
    return fecha

def cargar_catalogo(fecha):
    lista = []
    errores = 0
    try:
        with open(ARCHIVO_PRODUCTOS, "r", encoding="utf-8") as p:
            if verificar_existencia_datos(ARCHIVO_PRODUCTOS) == 0:
                raise ValueError("Error: el archivo no contiene productos, se usará el catálogo de respaldo.")
            for linea in p:
                try:
                    lista.append(crear_producto(linea.strip().split(";")))
                except ValueError as e:
                    errores += 1
                    registrar_error(fecha,ARCHIVO_PRODUCTOS,e)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: el archivo 'productos.csv' no existe, se usará el catálogo de respaldo.")
    except OSError:
        raise OSError(f"Error: se produjo un error de sistema.")
    else:
        return lista, errores

def leer_historial(fecha):
    """
    Lee ventas.csv completo y devuelve las ventas válidas.
    Pre:  fecha es la fecha de HOY (AAAA-MM-DD); se usa solo para registrar errores.
    Post: devuelve una lista de tuplas de seis elementos (una por línea válida).
    Las líneas inválidas se registran en errores.log y se saltean.
    Si ventas.csv no existe, devuelve una lista vacía.
    """

    historial = []
    try:
        with open(ARCHIVO_VENTAS, "r", encoding=CODIFICACION) as archivo:
            numero_linea = 0
            for linea in archivo:
                numero_linea += 1
                if linea.strip() == "":
                    continue
                campos = linea.strip().split(SEPARADOR)
                try:
                    venta = crear_venta(campos)
                except ValueError as error:
                    registrar_error(fecha, ARCHIVO_VENTAS, f"línea {numero_linea}: {error}")
                else:
                    historial.append(venta)
    except FileNotFoundError:
        return []
    return historial

def acumular(registros, campo_clave, campo_valor):
    """
    Suma, por cada valor distinto de campo_clave, los valores de campo_valor.
    Pre:  registros es una lista de tuplas/listas; campo_clave y campo_valor son
    posiciones válidas y los valores de campo_valor se pueden sumar.
    Post: devuelve un diccionario {clave: suma}. Recorre la lista una sola vez
    y no modifica registros.
    """
    totales = {}
    for registro in registros:
        clave = registro[campo_clave]
        if clave in totales:
            totales[clave] += registro[campo_valor]
        else:
            totales[clave] = registro[campo_valor]
    return totales

def crear_venta(campos):
    """Convierte los campos de una línea de ventas.csv en una venta del historial.
 
    Pre:  campos es una lista de cadenas (lo que devuelve linea.split(SEPARADOR)).
    Post: devuelve la tupla (fecha, numero, codigo, cantidad, medio, importe)
          con los tipos correctos (str, int, int, int, int, float).
    Lanza: ValueError si no hay exactamente 6 campos, si la fecha no es válida,
           si algún número no se puede convertir o si algún valor está fuera
           de rango. La función DETECTA el error; quien la llama decide qué hacer.
    """
    if len(campos) != 6:
        raise ValueError(f"se esperaban 6 campos y hay {len(campos)}")
    fecha = campos[H_FECHA].strip()
    numero = int(campos[H_NUMERO])
    codigo = int(campos[H_CODIGO])
    cantidad = int(campos[H_CANTIDAD])
    medio = int(campos[H_MEDIO])
    importe = float(campos[H_IMPORTE])
    if numero <= 0:
        raise ValueError(f"número de venta inválido: {numero}")
    if codigo <= 0:
        raise ValueError(f"código inválido: {codigo}")
    if cantidad <= 0:
        raise ValueError(f"cantidad inválida: {cantidad}")
    if not 1 <= medio <= len(MEDIOS_PAGO):
        raise ValueError(f"medio de pago inexistente: {medio}")
    if importe < 0:
        raise ValueError(f"importe negativo: {importe}")
    return (fecha, numero, codigo, cantidad, medio, importe)
 
def calcular_total_por_dia(historial):
    """Calcula el importe vendido en cada fecha del historial.
 
    Pre:  historial es una lista de tuplas de seis elementos (la de leer_historial).
    Post: devuelve la tupla (filas, total_general). filas es una lista de
          [fecha, importe] ordenada por fecha ascendente; total_general es la
          suma de todos los importes. No modifica el historial.
    """
    totales = acumular(historial, H_FECHA, H_IMPORTE)
    filas = []
    total_general = 0
    for fecha in totales:
        filas.append([fecha, totales[fecha]])
        total_general += totales[fecha]
    ordenar(filas, TD_FECHA, False)
    return filas, total_general
 
def mostrar_total_por_dia(filas, total_general):
    """Muestra el total vendido por fecha y el total general.
 
    Pre:  filas y total_general son los que devuelve calcular_total_por_dia.
    Post: imprime una línea por fecha y una última con el total general.
    """
    print("TOTAL POR DÍA")
    for fila in filas:
        print(f"{fila[TD_FECHA]}   $ {formatear_importe(fila[TD_IMPORTE]):>12}")
    print(f"{'TOTAL':<10}   $ {formatear_importe(total_general):>12}")
 
def calcular_detalle_fecha(historial, fecha):
    """Calcula cuántas ventas hubo en una fecha y el importe de cada medio de pago.
 
    Pre:  historial es una lista de tuplas de seis elementos; fecha es AAAA-MM-DD.
    Post: devuelve la tupla (cantidad, por_medio): cantidad de ventas de esa fecha
          y un diccionario {numero_de_medio: importe}. Si no hubo ventas, devuelve
          (0, {}). No modifica el historial.
    """
    del_dia = []
    for venta in historial:
        if venta[H_FECHA] == fecha:
            del_dia.append(venta)
    por_medio = acumular(del_dia, H_MEDIO, H_IMPORTE)
    return len(del_dia), por_medio
 
 
def mostrar_detalle_fecha(fecha, cantidad, por_medio):
    """Muestra la cantidad de ventas de una fecha y el importe por medio de pago.
 
    Pre:  cantidad y por_medio son los que devuelve calcular_detalle_fecha.
    Post: imprime el detalle, con cada medio por su nombre, o avisa si no hubo ventas.
    """
    if cantidad == 0:
        print(f"No hay ventas registradas el {fecha}.")
        return
    palabra = "venta" if cantidad == 1 else "ventas"
    print(f"DETALLE DEL {fecha}: {cantidad} {palabra}")
    for medio in por_medio:
        print(f"  {MEDIOS_PAGO[medio - 1]:<10} $ {formatear_importe(por_medio[medio]):>12}")
 
def calcular_ranking_historico(historial, catalogo):
    """Arma el ranking de los productos con más unidades vendidas en el historial.
 
    Pre:  historial es una lista de tuplas de seis elementos; catalogo está
          ordenado por código (la búsqueda binaria lo necesita).
    Post: devuelve una lista de hasta TOP_RANKING filas [codigo, nombre, unidades],
          ordenada de mayor a menor cantidad de unidades. Si un código del
          historial no está en el catálogo, se muestra un nombre de aviso.
    """
    unidades = acumular(historial, H_CODIGO, H_CANTIDAD)
    ranking = []
    for codigo in unidades:
        producto = buscar_por_codigo(catalogo, codigo)
        if producto == -1:
            nombre = f"(código {codigo} fuera del catálogo)"
        else:
            nombre = producto[NOMBRE]
        ranking.append([codigo, nombre, unidades[codigo]])
    ordenar(ranking, HR_UNIDADES, True)
    return ranking[:TOP_RANKING]
 
 
def mostrar_ranking_historico(ranking):
    """Muestra el ranking histórico.
 
    Pre:  ranking es el que devuelve calcular_ranking_historico.
    Post: imprime una línea por producto con su posición, nombre y unidades.
    """
    print(f"RANKING HISTÓRICO (TOP {TOP_RANKING})")
    for i in range(len(ranking)):
        fila = ranking[i]
        print(f"{i + 1}. {fila[HR_NOMBRE]:<25} {fila[HR_UNIDADES]:>4} un.")

def crear_novedad(campos):
    """Convierte los campos de una línea de novedades.csv en una novedad.
 
    Pre:  campos es una lista de cadenas (lo que devuelve linea.split(SEPARADOR)).
    Post: devuelve la tupla (codigo, precio, cantidad) con los tipos correctos
          (int, float, int).
    Lanza: ValueError si no hay exactamente 3 campos, si algún número no se puede
           convertir, si el código o el precio no son mayores que cero o si la
           cantidad es negativa. La función DETECTA el error; quien la llama decide.
    """
    if len(campos) != 3:
        raise ValueError(f"se esperaban 3 campos y hay {len(campos)}")
    codigo = int(campos[N_CODIGO])
    precio = float(campos[N_PRECIO])
    cantidad = int(campos[N_CANTIDAD])
    if codigo <= 0:
        raise ValueError(f"código inválido: {codigo}")
    if precio <= 0:
        raise ValueError(f"precio inválido: {precio}")
    if cantidad < 0:
        raise ValueError(f"cantidad negativa: {cantidad}")
    return (codigo, precio, cantidad)
 
 
def aplicar_novedades(catalogo, fecha):
    """Aplica al catálogo las novedades del proveedor y vacía novedades.csv.
 
    Pre:  catalogo es una lista de productos ORDENADA por código; fecha es la
          fecha de HOY (AAAA-MM-DD), se usa solo para registrar errores.
    Post: cada novedad válida reemplaza el precio del producto y suma la cantidad
          a su stock. Las inválidas (línea mal formada, valores fuera de rango o
          código inexistente) se registran en errores.log y se saltean.
          Devuelve la tupla (aplicadas, rechazadas). Al terminar, novedades.csv
          queda vacío para que no se apliquen dos veces.
    Lanza: FileNotFoundError si novedades.csv no existe y OSError si no se puede
           leer o vaciar; quien la llama informa al usuario.
    """
    aplicadas = 0
    rechazadas = 0
    with open(ARCHIVO_NOVEDADES, "r", encoding=CODIFICACION) as archivo:
        numero_linea = 0
        for linea in archivo:
            numero_linea += 1
            if linea.strip() == "":
                continue
            campos = linea.strip().split(SEPARADOR)
            try:
                codigo, precio, cantidad = crear_novedad(campos)
            except ValueError as error:
                rechazadas += 1
                registrar_error(fecha, ARCHIVO_NOVEDADES, f"línea {numero_linea}: {error}")
            else:
                producto = buscar_por_codigo(catalogo, codigo)
                if producto == -1:
                    rechazadas += 1
                    registrar_error(fecha, ARCHIVO_NOVEDADES, f"línea {numero_linea}: código inexistente: {codigo}")
                else:
                    producto[PRECIO] = precio
                    producto[STOCK] += cantidad
                    aplicadas += 1
    with open(ARCHIVO_NOVEDADES, "w", encoding=CODIFICACION) as archivo:
        archivo.write("")
    return aplicadas, rechazadas

def menu(historial_ventas):
    """Menu principal donde se ingresan las opciones para registrar ventas, ver resumen del día y cerrar caja
    
    ."""
    while True:
        try:
            fecha = pedir_fecha()
        except ValueError as e:
            print(e)
            print("")
        except KeyboardInterrupt as e:
            print(e)
            print("")
        else:
            break
    
    while True:
        try:
            catalogo, errores = cargar_catalogo(fecha)
            print(f'Se cargaron exitosamente {str(len(catalogo))!r} productos del archivo "productos.csv" a la lista.')
        except FileNotFoundError as e:
            catalogo = catalogo_inicial()
            print(e)
            break
        except OSError as e:
            catalogo = catalogo_inicial()
            print(e)
            break
        except ValueError as e:
            catalogo = catalogo_inicial()
            print(e)
            break
        except KeyboardInterrupt as e:
            print(e)
            print("")
        else:
            break

    ordenar(catalogo, CODIGO, False)
    if errores > 0:
        print(f"Se cargaron {errores} errores al archivo 'errores.log', es necesario que los revise.")
    opcion = 0
    opc = 0
    verificado = False
    while opcion != 6:
        print("=== KIOSCO EL CAMPUS v2 ===")
        print("1 Registrar una venta")
        print("2 Consultar el catálogo")
        print("3 Ver resumen del día")
        print("4 Ranking de productos más vendidos")
        print("5 Tabla categoría x medio de pago")
        print("6 Historial de ventas")
        print("7 Cargar novedades del proveedor")
        print("8 Ver productos a reponer")
        print("9 Cerrar caja y salir")
        try:
            opcion = pedir_numero("Elija una opción: ", 1, 9)
        except ValueError as e:
            print(e)
            print("")
        except KeyboardInterrupt as e:
            print(e)
            print("")

        match opcion:
            case 1:
                verificado = registrar_venta(catalogo, historial_ventas, fecha, verificado)
                
            case 2:
                print("=====================================================")
                print("1 Listar el catálogo completo ordenado por código")
                print("2 Buscar por código")
                print("3 Buscar por nombre")
                print("4 Listar por categoría")
                print("5 Agregar un producto")
                print("6 Volver al menú principal")
                
                opc = pedir_numero("Seleccione una opción de catálogo: ", 1, 9)
                while opc != 6:
                    if opc == 1:
                        print("CÓDIGO | NOMBRE | CATEGORÍA | PRECIO | STOCK")
                        for i in range(len(catalogo)):
                            print(f"{catalogo[i][CODIGO]} | {catalogo[i][NOMBRE]} | {CATEGORIAS[catalogo[i][CATEGORIA] -1]} | ${formatear_importe(catalogo[i][PRECIO])} | {catalogo[i][STOCK]}")
                    elif opc == 2:
                        cod = pedir_numero("Ingrese el código del producto a buscar: ", 1 , float('inf')) 
                        producto = buscar_por_codigo(catalogo, cod)
                        if producto != -1:
                            print(f"Codigo: {producto[CODIGO]}")
                            print(f"Nombre: {producto[NOMBRE]}")
                            print(f"Categoría: {CATEGORIAS[producto[CATEGORIA] - 1]}")
                            print(f"Precio: ${formatear_importe(producto[PRECIO])}")
                            print(f"Stock: {producto[STOCK]} unidades")
                        else:
                            print("El código ingresado no existe")
                    elif opc == 3:
                        busqueda_por_nombre(catalogo,historial_ventas)
                    elif opc == 4:
                        reponer_prod = 0
                        for i in range(len(CATEGORIAS)):
                            print(f"{i+1} {CATEGORIAS[i]}")
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
                        nombre = input("Ingrese el nombre del producto a agregar: ").capitalize().replace("  ", " ").strip()
                        while not nombre or nombre.isdigit():
                            nombre = input("ERROR, no puede quedar vacío. Ingrese el nombre del producto a agregar: ").capitalize().replace("  ", " ").strip()
                        for i in range(len(CATEGORIAS)):
                            print(f"{i+1} {CATEGORIAS[i]}")
                        categoria = pedir_numero("Ingrese la categoría a la que pertenece el producto: ", 1, 4)
                        precio = pedir_numero("Ingrese el precio por unidad del producto: ", 1, float('inf'))
                        stock = pedir_numero("Ingrese la cantidad de stock del producto: ", 0, float('inf'))
                        nuevo_producto = [codigo, nombre, categoria, precio, stock]
                        catalogo.append(nuevo_producto)
                        ordenar(catalogo, CODIGO, False)

                    print("=====================================================")
                    print("1 Listar el catálogo completo ordenado por código")
                    print("2 Buscar por código")
                    print("3 Buscar por nombre")
                    print("4 Listar por categoría")
                    print("5 Agregar un producto")
                    print("6 Volver al menú principal")
                    
                    opc = pedir_numero("Seleccione una opción de catálogo: ", 1, 6)
            case 3:
                mostrar_resumen(catalogo, historial_ventas)
            case 4:
                imprimir_ranking(catalogo,historial_ventas)
            case 5:
                mostrar_matriz(catalogo, historial_ventas)
            case 6:
                historial = leer_historial(fecha)
                if len(historial) == 0:
                    print("No hay ventas válidas registradas en el historial.")
                    return
                op = 0
                
                while op != 4:
                    print("=" * 40)
                    print("1) Total por día")
                    print("2) Detalle de una fecha")
                    print("3) Ranking histórico")
                    print("4) Volver al menú principal")
                    op = pedir_numero("Seleccione una opción:", 1, 4)
                    if op == 1:
                        filas, total_general = calcular_total_por_dia(historial)
                        mostrar_total_por_dia(filas, total_general)
                    elif op == 2:
                        fecha_consulta = pedir_fecha()
                        cantidad, por_medio = calcular_detalle_fecha(historial, fecha_consulta)
                        mostrar_detalle_fecha(fecha_consulta, cantidad, por_medio)
                    elif op == 3:
                        ranking = calcular_ranking_historico(historial, catalogo)
                        mostrar_ranking_historico(ranking)
            case 7:
                try:
                    aplicadas, rechazadas = aplicar_novedades(catalogo, fecha)
                except FileNotFoundError:
                    print("No se encontró novedades.csv: no hay novedades para cargar.")
                except OSError:
                    print("No se pudo leer o vaciar novedades.csv.")
                else:
                    print(f"Se aplicaron {aplicadas} novedades y se rechazaron {rechazadas}.")
            case 8:
                pass
            case 9:
                opcion = salir(catalogo, historial_ventas)

#------------ FUNCIONALIDADES DEL MENU - END -------------#

menu(historial_ventas)