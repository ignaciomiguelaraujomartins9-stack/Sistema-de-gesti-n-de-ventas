# =====================================================================
# CONSTANTES
# =====================================================================
MONTO_MINIMO_DESCUENTO = 25000      # subtotal a partir del cual hay descuento
PORCENTAJE_DESCUENTO_MONTO = 10     # % de descuento por superar el monto
PORCENTAJE_DESCUENTO_EFECTIVO = 5   # % de descuento por pagar en efectivo
PORCENTAJE_RECARGO_CREDITO = 8      # % de recargo por pagar con crédito

CATEGORIAS = ["Golosinas", "Bebidas", "Almacén", "Librería"]   # índice + 1 = número de categoría
MEDIOS_PAGO = ["Efectivo", "Débito", "Crédito"]                 # índice + 1 = número de medio
STOCK_MINIMO = 5                    # por debajo de este stock, el producto va a reposición

# Posiciones de los campos dentro de la lista que representa un producto.
# Usar estos nombres en lugar de "números mágicos": producto[NOMBRE], no producto[1].
CODIGO, NOMBRE, CATEGORIA, PRECIO, STOCK = 0, 1, 2, 3, 4


# =====================================================================
# CATÁLOGO INICIAL
# ---------------------------------------------------------------------
# Lista de productos. Cada producto es una LISTA (mutable: el stock cambia):
#     [codigo, nombre, categoria, precio, stock]
# Observar que NO está ordenado por código: ordenarlo al iniciar el
# programa es parte del trabajo (y condición para la búsqueda binaria).
# =====================================================================
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


# =====================================================================
# HISTORIAL DE VENTAS, CONSTANTES + RANKING
# =====================================================================

historial_ventas = []
NRO_VENTA, COD_PROD, CANTIDAD, MEDIO_PAGO, IMPORTE_FINAL = 0, 1, 2, 3, 4
RANK_NOM, RANK_CANT, RANK_IMP = 0, 1, 2

# =====================================================================
# OPCIONES DEL MENU
# =====================================================================
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

def ord_insercion(lista, campo, descendente):
    """Función reutilizable que ordena los elementos de una lista por el método de inserción.
    Pre: los elementos de la lista deben ser comparables
    Post: La lista está ordenada
    """

    for i in range (1, len(lista)):
        v = lista[i]
        j = i - 1
        if descendente == True:
            while j >= 0 and lista[j][campo] < v[campo]:
                lista[j+1] = lista[j]
                j -= 1
            lista[j+1] = v
        else:
            while j >= 0 and lista[j][campo] > v[campo]:
                lista[j+1] = lista[j]
                j -= 1
            lista[j+1] = v
    return lista

def busqueda_binaria(lista, producto):
    """ Función que realiza la búsqueda de un elemento mediante el método de busqueda binaria.
        Pre: La lista debe estar ordenada.
        Post: Devuelve lista[medio], que vendría siendo el producto para 
        utilizarse en el registro de una venta, la búsqueda de un producto por nombre o el registro
        de un producto nuevo.
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

def registrar_venta(catalogo, historial_ventas):
    """ Función que registra la venta de un producto.
        Pre: El catálogo debe estar ordenado.
        Post: Se emite el ticket y la venta se agrega al historial de ventas.
    """
    cod = int(input("Ingrese el codigo del producto (Ingrese 0 para cancelar): "))
    while cod != 0:
        producto = busqueda_binaria(catalogo, cod)
    
        if producto != -1:
            print(f"Nombre: {producto[NOMBRE]}")
            print(f"Precio: ${producto[PRECIO]}")
            print(f"Stock: {producto[STOCK]} unidades")
    
            cantidad = pedir_numero("Ingrese la cantidad: ", 1, producto[STOCK])
    
            print("============")
            print("1. Efectivo")
            print("2. Débito")
            print("3. Crédito")
            medio_pago = pedir_numero("Ingrese el medio de pago (1/2/3): ", 1, 3)
    
            num_ventas = len(historial_ventas) + 1
    
            subtotal, descuento, subtotal_d = descuento_monto(producto[PRECIO], cantidad)
            importe_final, descuento_efectivo, recargo = ajuste_medio_pago(subtotal_d, medio_pago)
            codigo = codigo_suerte(int(importe_final))
            mostrar_ticket(cantidad, producto[PRECIO], producto[NOMBRE], medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo, num_ventas)
    
            print(f"AVISO: El stock de {producto[NOMBRE]} pasa de {producto[STOCK]} a {producto[STOCK] - cantidad}")
            producto[STOCK] -= cantidad
            venta = num_ventas, producto[CODIGO], cantidad, medio_pago, importe_final
            historial_ventas.append(venta)
            break
        else:
            print("Producto no encontrado")
            cod = int(input("Ingrese el codigo del producto (Ingrese 0 para cancelar): "))

def armar_ranking(catalogo, historial_ventas):
    """ Función que permite generar el ranking de productos más vendidos en el día
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
        



def descuento_monto(precio, cantidad):
    """Calcula el descuento si se supera el monto minimo de descuento.
    
    Recibe: precio (int) y cantidad (int)
    Devuelve: subtotal (variable sin el descuento aplicado) (int), descuento (float), 
    subtotal_d (variable con el descuento aplicado) (float)
    """
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
    Devuelve: Importe final (float), descuento por efectivo (float) , recargo por crédito (float) 
    """
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
    print(f"{cantidad} Unidades de {nombre_producto} de ${precio:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Descuento por monto ({PORCENTAJE_DESCUENTO_MONTO}%): -${descuento:.2f}")
    if medio_pago == 1:
        print(f"Descuento por efectivo ({PORCENTAJE_DESCUENTO_EFECTIVO}% sobre ${subtotal_d:.2f}): -${descuento_efectivo:.2f}")
    elif medio_pago == 2:
        print("Pagó con débito: no hay ajuste")
    elif medio_pago == 3:
        print(f"Recargo por crédito ({PORCENTAJE_RECARGO_CREDITO}% sobre ${subtotal_d:.2f}): +${recargo:.2f}")
    print(f"Importe final: ${importe_final:.2f}")
    print(f"Codigo de la suerte: {codigo}")
    print("================================")

def codigo_suerte(importe):
    """Desafío del código de la suerte: Algoritmo recursivo que suma los dígitos
    del importe final hasta que quede 1 solo dígito
    Recibe: Importe final (float)
    Devuelve: Codigo de la suerte (int)
    """
    if importe < 10:
        return importe
    else:
        suma = (importe % 10) + codigo_suerte(importe // 10)
    return codigo_suerte(int(suma)) 

# =====================================================================
# MENU
# =====================================================================
def menu():
    """Menu principal donde se ingresan las opciones para registrar ventas, ver resumen del día y cerrar caja
    
    ."""
    opcion = 0
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
                            print(f"{catalogo[i][CODIGO]} | {catalogo[i][NOMBRE]} | {CATEGORIAS[catalogo[i][CATEGORIA] -1]} | ${catalogo[i][PRECIO]} | {catalogo[i][STOCK]}")
                    elif opc == 2:
                        cod = int(input("Ingrese el codigo del producto a buscar: "))
                        producto = busqueda_binaria(catalogo, cod)
                        if producto != -1:
                            print(f"Codigo: {producto[CODIGO]}")
                            print(f"Nombre: {producto[NOMBRE]}")
                            print(f"Categoría: {CATEGORIAS[producto[CATEGORIA] - 1]}")
                            print(f"Precio: ${producto[PRECIO]}")
                            print(f"Stock: {producto[STOCK]} unidades")
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
                        codigo = int(input("Ingrese el código del producto a agregar: "))
                        while busqueda_binaria(catalogo, codigo) != -1:
                            print("ERROR: El código no puede repetirse!")
                            codigo = int(input("Ingrese el código del producto a agregar: "))
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
            case 4:
                if len(historial_ventas) == 0:
                    print("No se han registrado ventas el dia de hoy")
                else:
                    ranking = armar_ranking(catalogo, historial_ventas)
                    ord_insercion(ranking, RANK_CANT, True)

                    print("=== RANKING DEL DIA ===")
                    for i in range(len(ranking)):
                        print(f"{i+1}. {ranking[i][RANK_NOM]} | {ranking[i][RANK_CANT]} un. | ${ranking[i][RANK_IMP]:.2f}")
            case _:
                print("Opciones en construcción...")
                        
                    
                                    
                                



catalogo = catalogo_inicial()
ord_insercion(catalogo, CODIGO, False)
menu()