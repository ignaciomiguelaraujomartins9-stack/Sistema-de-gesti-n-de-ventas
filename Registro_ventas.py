MONTO_MINIMO_DESCUENTO = 25000      # subtotal a partir del cual hay descuento
PORCENTAJE_DESCUENTO_MONTO = 10     # % de descuento por superar el monto
PORCENTAJE_DESCUENTO_EFECTIVO = 5   # % de descuento por pagar en efectivo
PORCENTAJE_RECARGO_CREDITO = 8      # % de recargo por pagar con crédito

def pedir_numero(mensaje, min, max):
    """Función reutilizable que pide un número en un rango al usuario hasta que sea válido.
    
    Recibe: mensaje (str) a mostrar, minimo (int) y máximo (int) permitido del número
    Retorna: el número ya validado dentro de el rango (int)
    """
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

def mostrar_ticket(cantidad, precio, categoria, medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo):
    """Muestra en pantalla el ticket con toda la información calculada por las otras funciones"""

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
        print(f"Descuento por efectivo ({PORCENTAJE_DESCUENTO_MONTO}% sobre ${subtotal_d}): -${descuento_efectivo}")
    elif medio_pago == 2:
        print("Pagó con débito: no hay ajuste")
    elif medio_pago == 3:
        print(f"Recargo por crédito ({PORCENTAJE_RECARGO_CREDITO}% sobre ${subtotal_d}): +${recargo}")
    print(f"Importe final: ${importe_final}")
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

def menu():
    """Menu principal donde se ingresan las opciones para registrar ventas, 
    ver resumen del día y cerrar caja"""

    opcion = 0
    while opcion != 3:
        print("=== KIOSCO EL CAMPUS ===")
        print("1. Registrar una venta")
        print("2. Ver resumen del día")
        print("3. Cerrar caja y salir")
        opcion = pedir_numero("Elija una opción:", 1, 3)


        match opcion:
            case 1:
                print("1. Golosinas")
                print("2. Bebidas")
                print("3. Almacén")
                print("4. Librería")
                categoria = pedir_numero("Elija la categoría del producto: ", 1, 4)
                precio = pedir_numero("Ingrese el precio del producto: ", 0, float('inf')) # Se usa float('inf') como tope para precio y cantidades de producto
                cantidad = pedir_numero("Ingrese la cantidad de producto: ", 0, float('inf'))

                print("============")
                print("1. Efectivo")
                print("2. Débito")
                print("3. Crédito")
                medio_pago = pedir_numero("Ingrese el medio de pago: ", 1, 3)

                subtotal, descuento, subtotal_d = descuento_monto(precio, cantidad)
                importe_final, descuento_efectivo, recargo = ajuste_medio_pago(subtotal_d, medio_pago)
                codigo = codigo_suerte(importe_final)
                mostrar_ticket(cantidad, precio, categoria, medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo)
            case 3:
                print("Nos vemos giles")
            case _:
                print("Opción a cargo de Miguel xd")

menu()           
            
