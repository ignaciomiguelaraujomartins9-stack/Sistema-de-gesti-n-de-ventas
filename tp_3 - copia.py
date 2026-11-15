"""
PROGRAMACIÓN 1 — LICENCIATURA EN SISTEMAS
Trabajo Práctico N.º 3 (tp_3.py) — Sistema de gestión de ventas: Kiosco "El Campus" V3

Integrantes del grupo:
    - Kevin Pavese
    - Araujo Martins, Ignacio Miguel
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

def buscar_codigo_secuencial(lista, producto):
    for i in range(len(lista)):
        if lista[i][CODIGO] == producto:
            return lista[i]
    return -1

#------------ BUSQUEDA - END -------------#

#------------ COMPLEMENTOS - START -------------#

def option(texto = "", destino = "", guardar = False):
    """
    Imprime un texto en pantalla o lo escribe en un archivo de destino según el parámetro booleano de control.
    Pre: 'texto' es la cadena a mostrar/guardar, 'destino' es un archivo abierto en modo escritura si 'guardar' es True, y 'guardar' es un valor booleano.
    Post: Escribe el texto seguido de un salto de línea en el archivo si 'guardar' es True; de lo contrario, lo imprime por pantalla utilizando print(texto).
    """
    if guardar:
        destino.write(texto + "\n")
    else:
        print(texto)

#------------ COMPLEMENTOS - END -------------#

#------------ RICH - START -------------#
MEDIOS = ("Efectivo", "Débito", "Crédito")   # medio 1, 2 y 3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
consola = Console()

def mensaje_ok(texto):
    """Post: muestra un mensaje de éxito en verde."""
    consola.print(f"[bold green]✔ {texto}[/]")

def mensaje_error(texto):
    """Post: muestra un mensaje de error en rojo."""
    consola.print(f"[bold red]✘ {texto}[/]")

def mensaje_aviso(texto):
    """Post: muestra un aviso en amarillo."""
    consola.print(f"[yellow]⚠ {texto}[/]")

def tabla_catalogo(catalogo):
    """Pre: catalogo es una lista de listas [código, nombre, categoría, precio, stock].
    Post: devuelve una tabla de rich (no la imprime)."""
    tabla = Table(title="CATÁLOGO", box=box.ROUNDED, header_style="bold cyan")
    tabla.add_column("Código", justify="right")
    tabla.add_column("Producto")
    tabla.add_column("Precio", justify="right")
    tabla.add_column("Stock", justify="right")
    for producto in catalogo:
        stock = str(producto[4])
        if producto[4] < STOCK_MINIMO:
            stock = f"[bold red]{stock}[/]"
        tabla.add_row(str(producto[0]), producto[1], formatear_importe(producto[3]), stock)
    return tabla


def mostrar_catalogo(catalogo):
    """Post: muestra el catálogo como tabla."""
    consola.print(tabla_catalogo(catalogo))

def mostrar_ticket_rich(cantidad, precio, nombre_producto, medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo, nro_venta):
    """Post: muestra el ticket de una venta dentro de un panel."""
    detalle = Table(box=None, show_header=False, padding=(0, 1))
    detalle.add_column()
    detalle.add_column(justify="right")
    detalle.add_row(f"{cantidad} Unidades de {nombre_producto} de ${formatear_importe(precio)}")
    detalle.add_row(f"Subtotal: ${formatear_importe(subtotal)}")
    detalle.add_row(f"Descuento por monto: ({PORCENTAJE_DESCUENTO_MONTO}%): -${formatear_importe(descuento)}")
    if medio_pago == 1:
        detalle.add_row(f"Descuento por efectivo ({PORCENTAJE_DESCUENTO_EFECTIVO}% sobre ${formatear_importe(subtotal_d)}): -${formatear_importe(descuento_efectivo)}")
    elif medio_pago == 2:
        detalle.add_row("Pagó con debito: no hay ajuste")
    elif medio_pago == 3:
        detalle.add_row(f"Recargo por crédito ({PORCENTAJE_RECARGO_CREDITO}% sobre ${formatear_importe(subtotal_d)}): +${formatear_importe(recargo)}")
    detalle.add_row(f"[bold]Importe final[/]: [bold green]${formatear_importe(importe_final)}[/]")
    detalle.add_row(f"Codigo de la suerte: {codigo}")
    consola.print(Panel(detalle, title=f"Venta N.º {nro_venta}", border_style="green", expand=False))

def guardar_tabla(tabla, nombre_archivo):
    """Pre: tabla es una tabla de rich.
    Post: escribe la tabla en el archivo, con el mismo dibujo que en pantalla
    y sin códigos de color.
    Lanza: OSError si no se puede escribir el archivo."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        consola_archivo = Console(file=archivo, width=70)
        consola_archivo.print(tabla)
#------------ RICH - END -------------#

#------------ ENTRADAS - START -------------#

def pedir_numero(mensaje, minimo, maximo, flotante = False):
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
    except ValueError:
        if flotante:
            entrada = float(entrada)
        else:
            raise ValueError(f"Error: el valor ingresado no es entero: '{entrada}'")
    except KeyboardInterrupt:
        raise KeyboardInterrupt(f"Error: se produjo una interrupción en el ingreso del número.")

    if not minimo <= entrada <= maximo:
        raise ValueError(f"Error: el valor ingresado no está entre {minimo} y {maximo}")
    else:
        return entrada

def busqueda_por_nombre(catalogo):
    """
    Busca productos cuyo nombre contenga el texto dado, sin distinguir mayúsculas.

    Recibe: catalogo (list)

    Devuelve: lista de productos del catálogo cuyo nombre contiene el texto buscado.
    
    Lista vacía si no hay coincidencias.
    """
    coincidencias = 0
    try:
        texto = input("Ingrese el producto a buscar: ").lower()
    except KeyboardInterrupt:
        raise KeyboardInterrupt("Aviso: se produjo una interrupción al momento de ingresar el producto a buscar.")
    for i in range(len(catalogo)):
        if texto in catalogo[i][NOMBRE].lower():
            coincidencias = 1
            mensaje_ok(catalogo[i][NOMBRE])
    if coincidencias == 0:
        mensaje_aviso("No se hallaron coincidencias")

def pedir_fecha():
    """
    Solicita al usuario el ingreso de una fecha por consola en formato correcto hasta que sea válida.
    Pre: Ninguna.
    Post: Devuelve una cadena de caracteres con la fecha ingresada y validada en formato "AAAA-MM-DD".
    """
    print("AAAA = año. MM = mes (01 a 12). DD = día (01 a 31).")
    fecha = input('Ingrese la fecha con el siguiente formato "AAAA-MM-DD": ').strip().replace(" ","")
    validar_fecha(fecha)
    return fecha

#------------ ENTRADAS - END -------------#

#------------ PROCESOS - START -------------#

def guardar_venta(fecha, venta):
    """
    Agrega una nueva venta al final del archivo de ventas en modo append.
    Pre: 'fecha' es una cadena con formato "AAAA-MM-DD" y 'venta' es una tupla con los datos de la transacción.
    Post: Añade una nueva línea formateada con la fecha y los elementos de la venta separados por el delimitador al archivo de ventas. 
    Si ocurre un problema de E/S, lanza OSError.
    """
    try:
        with open(ARCHIVO_VENTAS, "a", encoding=CODIFICACION) as ventas:
            v = f"{fecha}"
            for i in range(len(venta)):
                if i == len(venta) - 1:
                    v += f"{SEPARADOR}{venta[i]:.2f}"
                else:
                    v += f"{SEPARADOR}{venta[i]}"
            ventas.write(f"{v}\n")
    except OSError:
        raise OSError("Error: hay un problema con el archivo.")

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

def registrar_venta(catalogo, historial_ventas, fecha):
    """ 
        Función que registra la venta de un producto.

        Recibe: catalogo (int), historial de ventas (list), fecha (AAAA-MM-DD)

        Devuelve: No devuelve nada. Agrega las ventas a la lista.
        
        Pre: El catálogo debe estar ordenado.
        
        Post: Se emite el ticket y la venta se agrega al historial de ventas.
    """
    cod = pedir_numero("Ingrese el codigo del producto (Ingrese 0 para cancelar): ", 0 , float('inf'), True) 
    while cod != 0:
        producto = buscar_por_codigo(catalogo, cod)
        if producto == -1:
            raise ValueError(f"Aviso: el código no existe.")
        if producto[STOCK] == 0:
            raise ValueError(f"Aviso: el {producto[NOMBRE]!r} no tiene stock.")
        print(f"Nombre: {producto[NOMBRE]}")
        print(f"Precio: ${formatear_importe(producto[PRECIO])}")
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
        mostrar_ticket_rich(cantidad, producto[PRECIO], producto[NOMBRE], medio_pago, subtotal, subtotal_d, descuento, descuento_efectivo, recargo, importe_final, codigo, num_ventas)
        mensaje_aviso(f"AVISO: El stock de {producto[NOMBRE]} pasa de {producto[STOCK]} a {producto[STOCK] - cantidad}")
        producto[STOCK] -= cantidad
        venta = num_ventas, producto[CODIGO], cantidad, medio_pago, importe_final
        guardar_venta(fecha,venta)
        historial_ventas.append(venta)
        cod = pedir_numero("\nIngrese el codigo del siguiente producto (0 para cancelar): ", 0 , float('inf'), True) 

def calcular_ranking(catalogo, historial_ventas):
    """Calcula el ranking de productos vendidos en el día.

    Pre:  catalogo es una lista de productos; historial_ventas es la lista de
          tuplas (numero, codigo, cantidad, medio_pago, importe_final).
    Post: devuelve una lista de [nombre, unidades, importe] ordenada de mayor a
          menor cantidad de unidades. Solo incluye productos con ventas.
          No imprime ni modifica el catálogo ni las ventas.
    """
    ranking = []
    for i in range(len(catalogo)):
        unidades_vendidas = 0
        importe_vendido = 0.0
        for j in range(len(historial_ventas)):
            if catalogo[i][CODIGO] == historial_ventas[j][COD_PROD]:
                unidades_vendidas += historial_ventas[j][CANTIDAD]
                importe_vendido += historial_ventas[j][IMPORTE_FINAL]
        if unidades_vendidas > 0:
            ranking.append([catalogo[i][NOMBRE], unidades_vendidas, importe_vendido])
    ordenar(ranking, RANK_CANT, True)
    return ranking


def tabla_ranking(ranking):
    """Arma la tabla de Rich del ranking.

    Pre:  ranking es la lista que devuelve calcular_ranking.
    Post: devuelve una Table de Rich (no la imprime).
    """
    tabla = Table(title="RANKING DEL DÍA", box=box.ROUNDED, header_style="bold cyan")
    tabla.add_column("#", justify="right")
    tabla.add_column("Producto")
    tabla.add_column("Unidades", justify="right")
    tabla.add_column("Importe", justify="right")
    for i in range(len(ranking)):
        tabla.add_row(
            str(i + 1),
            ranking[i][RANK_NOM],
            str(ranking[i][RANK_CANT]),
            "$ " + formatear_importe(ranking[i][RANK_IMP]),
        )
    return tabla

def guardar_cierre(fecha, catalogo, ventas):
    """
    Crea cierre_AAAA-MM-DD.txt con el resumen, el ranking y los productos a reponer.
    Pre: 'fecha' es una cadena "AAAA-MM-DD", 'catalogo' es una lista válida de productos
    y 'ventas' es la lista de ventas del día.
    Post: escribe el archivo de cierre en disco.
    Lanza: OSError si no se puede escribir; quien la llama informa al usuario.
    """
    with open(f"{PREFIJO_CIERRE}{fecha}.txt", "w", encoding=CODIFICACION) as cierre:
        consola_archivo = Console(file=cierre, width=70)
        if len(ventas) > 0:
            consola_archivo.print(armar_resumen_del_dia(catalogo, ventas))
            consola_archivo.print(tabla_ranking(calcular_ranking(catalogo, ventas)))
        else:
            cierre.write("No se realizaron ventas.\n")

        cierre.write("\nProductos a reponer.\n")
        mostrar_reponer(productos_reponer(catalogo), cierre, True)

def copiar_binario(origen, destino):
    """
    Copia el contenido de un archivo a otro en modo binario ("rb" y "wb") e informa el total de bytes copiados.
    Pre: 'origen' y 'destino' son cadenas con las rutas válidas de los archivos a procesar.
    Post: Copia el archivo de origen al destino a nivel de bytes y devuelve una cadena indicando la cantidad de bytes copiados.
    """
    cantidad_bytes = 0
    contenido = ""
    try:
        with open(origen, "rb") as o, open(destino, "wb") as d:
            contenido = o.read()
            cantidad_bytes = len(contenido)
            o.seek(0)
            for linea_origen in o:
                d.write(linea_origen)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: no se encontró el archivo {origen}.")
    except PermissionError:
        raise PermissionError(f"Error: no hay permisos para manejar estos archivos: {origen} y {destino}")
    except OSError:
        raise OSError("Error: ocurrió un error inesperado.")
    else:
        return f"Se copiaron {cantidad_bytes} bytes"

def guardar_catalogo(catalogo):
    """
    Reescribe el archivo de productos con el catálogo actualizado de stock y precios, ordenado por código.
    Pre: 'catalogo' es una lista válida de productos ordenada de forma ascendente por código.
    Post: Actualiza y sobrescribe el archivo principal de productos en disco con la información vigente de la jornada.
    """
    texto = ''
    with open(ARCHIVO_PRODUCTOS, "w", encoding=CODIFICACION) as productos:
        for i in range(len(catalogo)):
            texto = f"{catalogo[i][CODIGO]}"
            texto += f"{SEPARADOR}{catalogo[i][NOMBRE]}"
            texto += f"{SEPARADOR}{catalogo[i][CATEGORIA]}"
            texto += f"{SEPARADOR}{catalogo[i][PRECIO]:.2f}"
            texto += f"{SEPARADOR}{catalogo[i][STOCK]}"
            productos.write(f"{texto}\n")

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

def armar_matriz(catalogo, historial_ventas):
    """
        Construye la matriz con la recaudación por categoría y medio de pago.

        Recibe: catálogo (list), historial de ventas (list)

        Devuelve: list. Matriz de 4 filas y 3 columnas. Cada fila representa una categoría
        y cada columna representa un medio de pago. Cada posición contiene el importe total 
        recaudado.

        Pre: catálogo debe de estar ordenado por código de producto.

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

def crear_producto(lista,campos):
    """Construye un producto a partir de los cinco campos leídos de una línea.

    Pre:  campos es una lista de cadenas (lo que devuelve linea.split(SEPARADOR)).
    Post: devuelve [codigo, nombre, categoria, precio, stock] con los tipos
          correctos y los valores validados.
    Lanza: ValueError si no hay exactamente 5 campos, si algún número no se puede
           convertir o si algún valor está fuera de rango. La función DETECTA el
           error; QUIEN LA LLAMA decide qué hacer con él (Clase 11).
    """
    if len(campos) != 5:
        raise ValueError(f"Aviso: se esperaban 5 campos y hay {len(campos)}")
    codigo = convertir(campos[CODIGO], int, "codigo")
    if buscar_codigo_secuencial(lista,codigo) != -1:
        raise ValueError(f"Aviso: el código {codigo!r} ya está almacenado")
    nombre = campos[NOMBRE].strip()
    categoria = convertir(campos[CATEGORIA], int, "categoria")
    precio = convertir(campos[PRECIO], float, "precio")
    stock = convertir(campos[STOCK], int, "stock")
    try:
        f"{campos[NOMBRE]}".encode("latin-1")
    except UnicodeEncodeError:
        raise ValueError(f"Error: hay uno o más caracteres con errores en: {campos[NOMBRE]}")
    if codigo <= 0:
        raise ValueError(f"Aviso: código inválido: {codigo}")
    if nombre == "":
        raise ValueError("Aviso: el nombre está vacío")
    if not 1 <= categoria <= len(CATEGORIAS):
        raise ValueError(f"Aviso: categoría inexistente: {categoria}")
    if precio <= 0:
        raise ValueError(f"Aviso: precio inválido: {precio}")
    if stock < 0:
        raise ValueError(f"Aviso: stock negativo: {stock}")
    return [codigo, nombre, categoria, precio, stock]

def cargar_catalogo(fecha):
    """
    Carga el catálogo de productos desde el archivo 'productos.csv' leyendo línea por línea, validando cada registro y registrando los errores detectados.
    Pre: 'fecha' es una cadena de caracteres con formato "AAAA-MM-DD" utilizada para estampar los registros de errores.
    Post: Devuelve una tupla que contiene la lista de productos válidos cargados, el contador de errores y un estado lógico. Si el archivo no existe o está vacío, utiliza el catálogo de respaldo y lo genera.
    """
    lista = []
    errores = 0
    contar_linea = 0
    if verificar_existencia_datos(ARCHIVO_PRODUCTOS) == 0:
        raise ValueError("Aviso: el archivo no contiene productos, se usará el catálogo de respaldo.")
    try:
        with open(ARCHIVO_PRODUCTOS, "r", encoding=CODIFICACION) as p:
            for linea in p:
                contar_linea += 1
                try:
                    lista.append(crear_producto(lista,linea.strip().split(SEPARADOR)))
                except ValueError as e:
                    imprimir_error(e)
                    registrar_error(fecha,ARCHIVO_PRODUCTOS,f"Linea {contar_linea}: {e}")
                    errores += 1
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: el archivo {ARCHIVO_PRODUCTOS} no existe, se usará el catálogo de respaldo.")
    except PermissionError:
        raise PermissionError(f"Error: no tiene permisos para abrir este archivo.")
    except OSError:
        raise OSError(f"Error: se produjo un error de sistema.")
    
    return lista, errores, 0

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
    validar_fecha(fecha)
    try:
        numero = int(campos[H_NUMERO])
    except ValueError:
        raise ValueError(f'Error: el número de venta no es numérico: {campos[H_NUMERO]!r}.')
    try:
        codigo = int(campos[H_CODIGO])
    except ValueError:
        raise ValueError(f'Error: el código no es numérico: {campos[H_CODIGO]!r}.')
    try:
        cantidad = int(campos[H_CANTIDAD])
    except ValueError:
        raise ValueError(f'Error: la cantidad vendida no es numérica: {campos[H_CANTIDAD]!r}.')
    try:
        medio = int(campos[H_MEDIO])
    except ValueError:
        raise ValueError(f'Error: el medio usado para la venta no es numérica: {campos[H_MEDIO]!r}.')
    try:
        importe = float(campos[H_IMPORTE])
    except ValueError:
        raise ValueError(f'Error: el importe no es numérico: {campos[H_IMPORTE]!r}.')
    if fecha == "":
        raise ValueError(f"la fecha no puede estar vacía: {fecha}")
    test_fecha = fecha.split("-")
    if test_fecha[0] == "":
        raise ValueError(f"el año de la fecha no puede estar vacía: {fecha}")
    if test_fecha[1] == "":
        raise ValueError(f"el mes de la fecha no puede estar vacía: {fecha}")
    if test_fecha[2] == "":
        raise ValueError(f"el día de la fecha no puede estar vacía: {fecha}")
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
    Post: devuelve la tupla (filas, total_general). filas es una lista de [fecha, importe] ordenada por fecha ascendente; total_general es la suma de todos los importes. No modifica el historial.
    """
    totales = acumular(historial, H_FECHA, H_IMPORTE)
    filas = []
    for fecha in totales:
        filas.append([fecha, totales[fecha]])
    ordenar(filas, TD_FECHA, False)
    return filas

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
        raise ValueError(f"Se esperaban 3 campos y hay {len(campos)}")
    try:
        codigo = int(campos[N_CODIGO])
    except ValueError:
        raise ValueError(f'El código no es un valor numérico: {campos[N_CODIGO]!r}.')
    try:
        precio = float(campos[N_PRECIO])
    except ValueError:
        raise ValueError(f'El precio no es un valor numérico: {campos[N_PRECIO]!r}.')
    try:
        cantidad = int(campos[N_CANTIDAD])
    except ValueError:
        raise ValueError(f'La cantidad no es un valor numérico: {campos[N_CANTIDAD]!r}.')
    if codigo <= 0:
        raise ValueError(f"Código inválido: {codigo}")
    if precio <= 0:
        raise ValueError(f"Precio inválido: {precio}")
    if cantidad < 0:
        raise ValueError(f"Cantidad negativa: {cantidad}")
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
                registrar_error(fecha, ARCHIVO_NOVEDADES, f"Línea {numero_linea}: {error}")
            else:
                producto = buscar_por_codigo(catalogo, codigo)
                if producto == -1:
                    rechazadas += 1
                    registrar_error(fecha, ARCHIVO_NOVEDADES, f"Línea {numero_linea}: código inexistente: {codigo}")
                else:
                    producto[PRECIO] = precio
                    producto[STOCK] += cantidad
                    aplicadas += 1
    with open(ARCHIVO_NOVEDADES, "w", encoding=CODIFICACION) as archivo:
        archivo.write("")
    return aplicadas, rechazadas

def armar_resumen_del_dia(catalogo, historial_ventas,):
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
    tabla = Table(title="RESUMEN DEL DÍA", box=box.SIMPLE_HEAVY, show_footer=True)
    tabla.add_row("[bold green]VENTAS REALIZADAS Y TOTAL RECAUDADO[/]")
    tabla.add_row(f"Ventas: {acumuladores[CANTIDAD_VENTAS]}")
    tabla.add_row(f"Recaudado: ${formatear_importe(acumuladores[TOTAL_RECAUDADO])}")
    tabla.add_row(f"Importe promedio por venta: ${formatear_importe(acumuladores[IMPORTE_PROMEDIO])}")
    tabla.add_row()
    tabla.add_row("[bold green]VENTA MÁS GRANDE[/]")
    tabla.add_row(f"Número de la venta: {venta_mas_grande[NUMERO_DE_LA_VENTA_GRANDE]}")
    tabla.add_row(f"Nombre del producto: {venta_mas_grande[PRODUCTO]}")
    tabla.add_row(f"Importe de la venta: ${formatear_importe(venta_mas_grande[VENTA_MAS_GRANDE])}")
    tabla.add_row()
    tabla.add_row("[bold green]TOTAL RECAUDADO POR CATEGORÍA DE PRODUCTO[/]")
    if recaudado_por_categoria[CAT1_TOTAL] == 0:
        tabla.add_row(f"Golosinas: No hay ventas de este tipo.")
    else:
        tabla.add_row(f"Golosinas: ${formatear_importe(recaudado_por_categoria[CAT1_TOTAL])}")
    if recaudado_por_categoria[CAT2_TOTAL] == 0:
        tabla.add_row(f"Bebidas: No hay ventas de este tipo.")
    else:
        tabla.add_row(f"Bebidas: ${formatear_importe(recaudado_por_categoria[CAT2_TOTAL])}")
    if recaudado_por_categoria[CAT3_TOTAL] == 0:
        tabla.add_row(f"Almacén: No hay ventas de este tipo.")
    else:
        tabla.add_row(f"Almacén: ${formatear_importe(recaudado_por_categoria[CAT3_TOTAL])}")
    if recaudado_por_categoria[CAT4_TOTAL] == 0:
        tabla.add_row(f"Librería: No hay ventas de este tipo.")
    else:
        tabla.add_row(f"Librería: ${formatear_importe(recaudado_por_categoria[CAT4_TOTAL])}")
    tabla.add_row()
    tabla.add_row("[bold green]CANTIDAD DE VENTAS POR MEDIO DE PAGO[/]")
    tabla.add_row(f"Efectivo: {cantidad_de_ventas_medio_pago[METODO_EFECTIVO] if cantidad_de_ventas_medio_pago[METODO_EFECTIVO] != 0 else 'No se realizaron ventas con este método'}")
    tabla.add_row(f"Débito: {cantidad_de_ventas_medio_pago[METODO_DEBITO] if cantidad_de_ventas_medio_pago[METODO_DEBITO] != 0 else 'No se realizaron ventas con este método'}")
    tabla.add_row(f"Crédito: {cantidad_de_ventas_medio_pago[METODO_CREDITO] if cantidad_de_ventas_medio_pago[METODO_CREDITO] != 0 else 'No se realizaron ventas con este método'}")
    if cantidad_de_ventas_medio_pago[METODO_CREDITO] == cantidad_de_ventas_medio_pago[METODO_DEBITO] and cantidad_de_ventas_medio_pago[METODO_CREDITO] == cantidad_de_ventas_medio_pago[METODO_EFECTIVO]:
        tabla.add_row("Los tres tienen un mismo uso")
        tabla.add_row(f"Efectivo {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s, Débito {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s y Crédito {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
    else:
        if cantidad_de_ventas_medio_pago[METODO_EFECTIVO] >= cantidad_de_ventas_medio_pago[METODO_DEBITO] and cantidad_de_ventas_medio_pago[METODO_EFECTIVO] >= cantidad_de_ventas_medio_pago[METODO_CREDITO]:
            if cantidad_de_ventas_medio_pago[METODO_EFECTIVO] == cantidad_de_ventas_medio_pago[METODO_DEBITO]:
                tabla.add_row("Los más usados fueron")
                tabla.add_row(f"Efectivo {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s y Débito {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s")
            elif cantidad_de_ventas_medio_pago[METODO_EFECTIVO] == cantidad_de_ventas_medio_pago[METODO_CREDITO]:
                tabla.add_row("Los más usados fueron")
                tabla.add_row(f"Efectivo {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s y Crédito {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
            else:
                tabla.add_row("El que más veces se usó fue")
                tabla.add_row(f"Efectivo con {cantidad_de_ventas_medio_pago[METODO_EFECTIVO]} uso/s")
        elif cantidad_de_ventas_medio_pago[METODO_DEBITO] >= cantidad_de_ventas_medio_pago[METODO_EFECTIVO] and cantidad_de_ventas_medio_pago[METODO_DEBITO] >= cantidad_de_ventas_medio_pago[METODO_CREDITO]:
                if cantidad_de_ventas_medio_pago[METODO_DEBITO] == cantidad_de_ventas_medio_pago[METODO_CREDITO]:
                    tabla.add_row("Los más usados fueron")
                    tabla.add_row(f"Débito {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s y Crédito {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
                else:
                    tabla.add_row("El que más veces se usó fue")
                    tabla.add_row(f"Débito con {cantidad_de_ventas_medio_pago[METODO_DEBITO]} uso/s")
        elif cantidad_de_ventas_medio_pago[METODO_CREDITO] >= cantidad_de_ventas_medio_pago[METODO_EFECTIVO] and cantidad_de_ventas_medio_pago[METODO_CREDITO] >= cantidad_de_ventas_medio_pago[METODO_DEBITO]:
            tabla.add_row("El que más veces se usó fue")
            tabla.add_row(f"Crédito con {cantidad_de_ventas_medio_pago[METODO_CREDITO]} uso/s")
    return tabla

def tabla_matriz(matriz):
    """Arma la tabla de Rich con la recaudación por categoría y medio de pago.

    Pre:  matriz es la que devuelve armar_matriz (4 filas x 3 columnas).
    Post: devuelve una Table de Rich con una fila por categoría, una columna por
          medio de pago, el total de cada fila y una última fila con los totales.
          No la imprime.
    """
    tabla = Table(title="TABLA CATEGORÍA POR MEDIO DE PAGO", box=box.ROUNDED, header_style="bold cyan")
    tabla.add_column("CATEGORÍA")
    tabla.add_column("EFECTIVO", justify="right")
    tabla.add_column("DÉBITO", justify="right")
    tabla.add_column("CRÉDITO", justify="right")
    tabla.add_column("TOTAL", justify="right")

    total_medios = [0, 0, 0]
    total_general = 0

    for i in range(len(matriz)):
        total_categoria = 0
        for j in range(len(matriz[i])):
            total_categoria += matriz[i][j]
            total_medios[j] += matriz[i][j]
        total_general += total_categoria
        tabla.add_row(
            CATEGORIAS[i],
            formatear_importe(matriz[i][0]),
            formatear_importe(matriz[i][1]),
            formatear_importe(matriz[i][2]),
            formatear_importe(total_categoria),
        )

    tabla.add_section()   # línea separadora antes de los totales
    tabla.add_row(
        "[bold]TOTAL[/]",
        f"[bold]{formatear_importe(total_medios[0])}[/]",
        f"[bold]{formatear_importe(total_medios[1])}[/]",
        f"[bold]{formatear_importe(total_medios[2])}[/]",
        f"[bold green]{formatear_importe(total_general)}[/]",
    )
    return tabla

#------------ PROCESOS - END -------------#

#------------ CONTROL - START -------------#

def verificar_entradas(cantidad):
    """
    Verifica si la cantidad de productos es mayor a 0 para verificar si mostrar el resumen del día o mostrar 'no se realizaron ventas este día'
    
    Recibe: cantidad (int).
    
    Devuelve: True si la cantidad es mayor a 0. False si la cantidad es menor o igual a 0.
    
    Pre: cantidad debe ser mayor a 0 y un número entero.

    Post: Retorna Ture si es mayor a 0. False si es mayor o igual.

    ."""
    
    return cantidad > 0

def verificar_cierre():
    """
    Comprueba si Don Ramón quiere finalizar el registro de las ventas de la jornada.

    Recibe: no recibe parámetros.
    
    Devuelve: el número correspondiente a la opción elegida.

    Pre: El usuario debe poder ingresar texto por teclado.

    Post: La función no finaliza si no recibe una entrada correcta, esta acpeta
    "S","s","si","Si","Sí" y "sí", a su vez acepta "n","N","No" y "no". Devuelve 9 cuando
    se confirma el cierre, cero cuando no se confirma el cierre.
    
    ."""
    continuar = input("¿Desea continuar con el cierre? (Si/No): ").lower().strip()
    if (continuar != "si" and continuar != "sí" and continuar != "s") and (continuar != "no" and continuar != "n"):
        raise ValueError("Aviso: Entrada inválida. Ingrese la opción: 'Si' para continuar, 'No' para salir.")
    if continuar == "si" or continuar == "sí" or continuar == "s":
        return 9
    return 0

def productos_reponer(catalogo):
    """
        Construye la lista con los stock que necesitan reposición

        Recibe: catálogo (list)

        Devuelve: lista con elementos que tienen sotck mínimo. 

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

def convertir(numero, tipo, categoria):
    """
    Intenta convertir un valor al tipo de dato especificado y gestiona los errores de conversión.
    Pre: 'numero' es el valor a convertir, 'tipo' es la función de conversión (ej. int, float) y 'categoria' es una cadena que identifica el campo.
    Post: Devuelve el valor convertido correctamente. Si la conversión falla, dispara un ValueError detallando el error en el campo correspondiente.
    """
    try:
        tipo(numero)
        return tipo(numero)
    except ValueError:
        raise ValueError(f"Aviso: el campo '{categoria}' debe tener un valor válido: {numero!r}")

def registrar_error(fecha, origen, detalle):
    """Agrega una línea al registro de errores.

    Pre:  fecha es una cadena AAAA-MM-DD; origen y detalle son cadenas.
    Post: errores.log tiene una línea más al final, con el formato
          "fecha | origen | detalle". Si el archivo no existe, lo crea.
          Si no se puede escribir, avisa por pantalla y el programa sigue.
    """
    with open(ARCHIVO_ERRORES, "a", encoding=CODIFICACION) as log:
        log.write(f"{fecha} | {origen} | {detalle}\n")

def verificar_existencia_datos(ruta):
    """
    Verifica la existencia de un archivo y comprueba si contiene datos en su interior para su posterior lectura.
    Pre: 'ruta' es una cadena de caracteres que representa la ruta válida del archivo a verificar.
    Post: Devuelve un indicador numérico basado en el contenido del archivo (utilizado para comprobar si está vacío). Si el archivo no existe, no hay permisos o surge un error de E/S, dispara la excepción correspondiente.
    """
    try:
        with open(ruta, "r", encoding=CODIFICACION) as log:
            for linea in log:
                lineas = linea.strip()
            return len(lineas)      
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: el archivo {ruta} no existe, se usará el catálogo de respaldo.")
    except PermissionError:
        raise PermissionError(f"Error: no tiene permisos para abrir este archivo.")
    except OSError:
        raise OSError(f"Error: se produjo un error al intentar leer el archivo.")

def validar_fecha(fecha):
    """
    Recorre y analiza la cadena de texto para verificar que la longitud, los separadores y los rangos numéricos de la fecha sean válidos.
    Pre: 'fecha' es una cadena de caracteres.
    Post: Si la fecha es correcta, la función finaliza de manera normal. 
    Si encuentra errores de formato o de rango, lanza ValueError detallando el motivo.
    """
    if len(fecha) != 10:
        raise ValueError(f'Debe contener 10 caracteres y contine: {len(fecha)!r}.')
    if len(fecha.split("-")) != 3:
        raise ValueError(f'Debe contener un guión "-" entre el año y el mes, además debe tener otro entre el mes y el día: {fecha!r}')
    test_fecha = fecha.split('-')
    try:
        int(test_fecha[0])
        int(test_fecha[1])
        int(test_fecha[2])
    except ValueError:
        raise ValueError(f'Aviso: se debe ingresar un valor numérico en cada campo: {test_fecha[0]}-{test_fecha[1]}-{test_fecha[2]}.')
    if not (int(test_fecha[1]) >= 1 and int(test_fecha[1]) <= 12):
        raise ValueError(f'El mes de la fecha no está entre 01 y 12: {fecha!r}')
    if not (int(test_fecha[2]) >= 1 and int(test_fecha[2]) <= 31):
        raise ValueError(f'El día de la fecha no está entre 01 y 31: {fecha!r}')
    if len(test_fecha[0]) != 4:
        raise ValueError(f'La fecha tiene más o menos caracteres de los permitidos en el año: {test_fecha[0]!r}.')
    if len(test_fecha[1]) != 2:
        raise ValueError(f'La fecha tiene más o menos caracteres de los permitidos en el mes: {test_fecha[1]!r}.')
    if len(test_fecha[2]) != 2:
        raise ValueError(f'La fecha tiene más o menos caracteres de los permitidos en el día: {test_fecha[2]!r}.')
    
#------------ CONTROL - END -------------#

#------------ SALIDAS - START -------------#

def mostrar_ranking(ranking):
    """Muestra el ranking por pantalla.

    Pre:  ranking es la lista que devuelve calcular_ranking (puede estar vacía).
    Post: imprime la tabla, o un aviso si no hay ventas.
    """
    if len(ranking) == 0:
        mensaje_aviso("No se han registrado ventas el día de hoy")
    else:
        consola.print(tabla_ranking(ranking))


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
    if verificar_entradas(len(historial_ventas)):
        consola.print(armar_resumen_del_dia(catalogo, historial_ventas))
    else:
        mensaje_aviso("Aún no se realizaron ingresos")
    print(" ")

def imprimir_ranking(catalogo, historial_ventas, guardar = False, destino = ""):
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
        option("No se han registrado ventas el dia de hoy", destino, guardar)
    else:
        mostrar_ranking(calcular_ranking(catalogo, historial_ventas))

def mostrar_matriz(catalogo, historial_ventas):
    """Muestra por pantalla la recaudación por categoría y medio de pago.

    Pre:  catalogo está ordenado por código; historial_ventas es la lista de
          ventas del día. armar_matriz y tabla_matriz están definidas.
    Post: imprime la tabla. No modifica el catálogo ni las ventas.
    """
    consola.print(tabla_matriz(armar_matriz(catalogo, historial_ventas)))

def mostrar_reponer(lista,destino="",guardar=False):
    """
        Muestra por pantalla los productos cuyo stock es menor al mínimo establecido.

        Recibe: catálogo (list)

        Devuelve: No devuelve nada. Muestra información por pantalla.

        Pre: Lista debe contener elementos que cumplan con la condición de su stock menor al mínimo deseado.

        Post: Imprime por código, nombre, categoría, precio y stock, a los productos que tienen menos del mínimo de stock deseado, avisandole
        con la palabra "¡REPONER!" al lado derecho del stock.
    """
    if lista:
        option("Código    Nombre                      Categoría        Precio           Stock", destino, guardar)
        for i in range(len(lista)):
            option(
                f"|{lista[i][0]:<8}"
                f"|{lista[i][1]:>20}"
                f"|{lista[i][2]:>15}"
                f"|{lista[i][3]:>13}"
                f"|{lista[i][4]:>11}"
                f" ¡REPONER!"
            , destino, guardar)
    else:
        option("No hay productos para reponer",destino, guardar)

def mostrar_total_por_dia(filas):
    """Muestra el total vendido por fecha y el total general.
 
    Pre:  filas y total_general son los que devuelve calcular_total_por_dia.
    Post: imprime una línea por fecha y una última con el total general.
    """
    total_por_dia = Table(title="TOTAL POR DÍA", box=box.SIMPLE_HEAVY, show_footer=True)
    total = 0 
    for fila in filas:
        total = total + fila[1]
    total_por_dia.add_column("Fecha", footer="TOTAL")
    total_por_dia.add_column("Importe", justify="right", footer=formatear_importe(total))
    for fila in filas:
        total_por_dia.add_row(fila[0], formatear_importe(fila[1]))
    consola.print(total_por_dia)
 
def mostrar_detalle_fecha(fecha, cantidad, por_medio):
    """Muestra la cantidad de ventas de una fecha y el importe por medio de pago.
 
    Pre:  cantidad y por_medio son los que devuelve calcular_detalle_fecha.
    Post: imprime el detalle, con cada medio por su nombre, o avisa si no hubo ventas.
    """
    if cantidad == 0:
        mensaje_aviso(f"No hay ventas registradas el {fecha}.")
        return
    palabra = "venta" if cantidad == 1 else "ventas"
    detalle = Table(box=None, show_header=False, padding=(0, 1))
    for medio in por_medio:
        detalle.add_row(f"{MEDIOS_PAGO[medio - 1]}  [bold green]${formatear_importe(por_medio[medio])}[/]")
    consola.print(Panel(detalle, title=f"[bold] DETALLE DEL {fecha}: {cantidad} {palabra} [/]", border_style="#EC7411" , expand=False))

def mostrar_ranking_historico(ranking):
    """Muestra el ranking histórico.
 
    Pre:  ranking es el que devuelve calcular_ranking_historico.
    Post: imprime una línea por producto con su posición, nombre y unidades.
    """
    tabla = Table(title="RANKING HISTÓRICO - TOP 5", box=box.ROUNDED, border_style="#EC7411", expand=False)
    tabla.add_column("PRODUCTO")
    tabla.add_column("UNIDADES VENDIDAS", justify="right")
    for i in range(len(ranking)):
        fila = ranking[i]
        tabla.add_row(f"{i + 1}. {fila[HR_NOMBRE]}", f"{fila[HR_UNIDADES]} un.")
    consola.print(tabla)

def imprimir_error(error):
    """
    Imprime un mensaje de error por pantalla con espaciado visual.
    Pre: 'error' es una cadena de caracteres con el mensaje descriptivo a mostrar.
    Post: Muestra el error formateado con líneas en blanco antes y después para mayor claridad.
    """
    print("")
    print(error)
    print("")

def imprimir_opciones(case = False):
    """
    Imprime por pantalla el menú principal de opciones del sistema o el submenú de opciones del catálogo según el parámetro booleano.
    Pre: 'case' es un valor booleano (True para mostrar el submenú del catálogo, False para el menú principal).
    Post: Muestra en la consola el bloque de opciones correspondiente formateado con separadores visuales.
    """
    if not case:
        opciones = (
        "[cyan]1)[/] Registrar una venta\n"
        "[cyan]2)[/] Consultar el catálogo\n"
        "[cyan]3)[/] Ver resumen del día\n"
        "[cyan]4)[/] Ranking de productos más vendidos\n"
        "[cyan]5)[/] Tabla categoría x medio de pago\n"
        "[cyan]6)[/] Historial de ventas\n"
        "[cyan]7)[/] Cargar novedades del proveedor\n"
        "[cyan]8)[/] Ver productos a reponer\n"
        "[cyan]9)[/] Cerrar caja y salir\n"
        )
        consola.print(Panel(opciones,
        title=f"KIOSCO EL CAMPUS v3",
        border_style="blue", expand=False))
    else:
        opciones = (
        "[cyan]1)[/] Listar el catálogo completo ordenado por código\n"
        "[cyan]2)[/] Buscar por código\n"
        "[cyan]3)[/] Buscar por nombre\n"
        "[cyan]4)[/] Listar por categoría\n"
        "[cyan]5)[/] Agregar un producto\n"
        "[cyan]6)[/] Volver al menú principal\n"
        )
        consola.print(Panel(opciones,
        title=f"CONSULTAS SOBRE EL CATÁLOGO",
        border_style="blue", expand=False))

def salir(catalogo, historial_ventas, existencia, fecha):
    """
    Muestra el resumen del día, realiza la cuenta atrás y sale del sistema solo si don Ramón confirma el cierre del sistema.
    
    Recibe: Catálogo (list), historial de ventas (list), fecha (AAAA-MM-DD), existencia (booleano que indica si el archivo de productos existe para realizar su backup)
    
    Devuelve: Devuelve 6 si acepta cerrar el programa e imprime el resumen del día, la cuenta regresiva. Devuelve 
    0 si desea continuar, sin mostrar nada en el proceso.
    
    Pre: Historial de ventas debe tener ventas realizadas para ejecutar el resumen del día e imprimir ranking. El usuario debe escribir Sí-si-s para contiunar con el cierre.

    Post: Se cierra el programa mostrando el resumen del día (si las hay), los productos a reponer (si los hay) y
    el ranking (si los hay) de ventas.
    ."""
    print("")
    opcion = verificar_cierre()
    if opcion == 9:
        if existencia:
            mensaje_ok(f"COPIA DEL ARCHIVO {ARCHIVO_PRODUCTOS!r} EN {ARCHIVO_BACKUP!r}.")
            mensaje_ok(copiar_binario(ARCHIVO_PRODUCTOS,ARCHIVO_BACKUP))
            guardar_catalogo(catalogo)
        else:
            mensaje_aviso(f"No se encontró el archivo {ARCHIVO_PRODUCTOS!r}, será creado mediante el catálogo de respaldo.")
            guardar_catalogo(catalogo)
            mensaje_ok(f"COPIA DEL ARCHIVO {ARCHIVO_PRODUCTOS!r} EN {ARCHIVO_BACKUP!r}.")
            mensaje_ok(copiar_binario(ARCHIVO_PRODUCTOS,ARCHIVO_BACKUP))
        guardar_cierre(fecha,catalogo,historial_ventas)
        if verificar_entradas(len(historial_ventas)):
            consola.print(armar_resumen_del_dia(catalogo, historial_ventas))
            lista = productos_reponer(catalogo)
            if lista:
                mostrar_reponer(lista)
            else:
                print("No hay productos a reponer")
            imprimir_ranking(catalogo, historial_ventas)
        else:
            print(" ")
            print("No se realizaron ventas este día.")
            lista = productos_reponer(catalogo)
            if lista:
                mostrar_reponer(lista)
            else:
                print("No hay productos a reponer")
            imprimir_ranking(catalogo, historial_ventas)
        print(cuenta_regresiva(5))
        return opcion
        # cuenta_regresiva_iterativo(5) Realiza la cuenta regresiva de forma iterativa
    else:
        return opcion 

#------------ SALIDAS - END -------------#

def menu(historial_ventas):
    """Menu principal donde se ingresan las opciones para registrar ventas, ver resumen del día y cerrar caja
    
    ."""

    while True:
        try:
            fecha = pedir_fecha()
            break
        except ValueError as e:
            imprimir_error(e)
        except KeyboardInterrupt as e:
            imprimir_error(e)

    no_existe_archivo_productos = True # Verificar existencia de archivo que se usará en salir
    opcion = 0
    try:
        catalogo, errores, opcion = cargar_catalogo(fecha)
        if len(catalogo) > 0:
            mensaje_ok(f'Se cargaron exitosamente {str(len(catalogo))!r} productos del archivo "productos.csv" a la lista.')
        else:
            mensaje_aviso(f'Aviso: el archivo no contiene productos, se usará el catálogo de respaldo.')
            catalogo = catalogo_inicial()
        if errores > 0:
            mensaje_error(f"Se cargaron {errores} errores al archivo 'errores.log', es necesario que los revise.")
    except (OSError,ValueError) as e:
        catalogo = catalogo_inicial()
        mensaje_error(registrar_error(fecha,ARCHIVO_PRODUCTOS,e))
        no_existe_archivo_productos = False
        mensaje_error(imprimir_error(e))
    except KeyboardInterrupt as e:
        mensaje_error(imprimir_error(e))

    ordenar(catalogo, CODIGO, False)
    opc = 0
    while opcion != 9:
        imprimir_opciones()
        try:
            opcion = pedir_numero("Elija una opción: ", 1, 9)
        except ValueError as e:
            mensaje_aviso(e)
        except KeyboardInterrupt as e:
            mensaje_aviso(e)

        match opcion:
            case 1:
                try:
                    registrar_venta(catalogo, historial_ventas, fecha)
                except (ValueError, OSError) as e:
                    mensaje_aviso(e)
                except KeyboardInterrupt as e:
                    mensaje_aviso(e)
                opcion = 0
            case 2:
                imprimir_opciones(True)
                while True:
                    try:
                        opc = pedir_numero("Seleccione una opción de catálogo: ", 1, 6)
                        break
                    except ValueError as e:
                        mensaje_aviso(e)
                    except KeyboardInterrupt as e:
                        mensaje_aviso(e)
                while opc != 6:
                    if opc == 1:
                        mostrar_catalogo(catalogo)
                    elif opc == 2:
                        while True:
                            try:
                                cod = pedir_numero("Ingrese el código del producto a buscar: ", 1 , float('inf'))
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        producto = buscar_por_codigo(catalogo, cod)
                        if producto != -1:
                            product = Table(box=None, show_header=False, padding=(0, 1))
                            product.add_column()
                            product.add_column(justify="right")
                            product.add_row(f"Codigo: {producto[CODIGO]}")
                            product.add_row(f"Nombre: {producto[NOMBRE]}")
                            product.add_row(f"Categoría: {CATEGORIAS[producto[CATEGORIA] - 1]}")
                            product.add_row(f"Precio: ${formatear_importe(producto[PRECIO])}")
                            product.add_row(f"Stock: {producto[STOCK]} unidades")
                            consola.print(Panel(product, title=f"PRODUCTO ENCONTRADO", border_style="cyan",expand=False))
                        else:
                            mensaje_aviso("El código ingresado no existe")
                    elif opc == 3:
                        try:
                            busqueda_por_nombre(catalogo)
                        except KeyboardInterrupt as e:
                            mensaje_aviso(e)
                    elif opc == 4:
                        reponer_prod = 0
                        for i in range(len(CATEGORIAS)):
                            print(f"{i+1} {CATEGORIAS[i]}")
                        while True:
                            try:
                                categoria = pedir_numero("Ingrese la categoría a buscar: ", 1, 4)
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        tabla = Table(title="CATEGORÍA BUSCADA", box=box.ROUNDED, header_style="bold cyan")
                        tabla.add_column("PRODUCTO")
                        tabla.add_column("STOCK", justify="right")
                        for i in range(len(catalogo)):
                            if categoria == catalogo[i][CATEGORIA]:
                                stock = str(catalogo[i][STOCK])
                                if int(stock) < STOCK_MINIMO:
                                    stock = f"[bold red]{stock}[/]"
                                tabla.add_row(str(catalogo[i][NOMBRE]), stock)
                                if catalogo[i][STOCK] < STOCK_MINIMO:
                                    reponer_prod += 1
                        consola.print(tabla)
                        if reponer_prod:
                            mensaje_aviso(f"{reponer_prod} Productos tienen stock por debajo del mínimo de reposición!")
                    elif opc == 5:
                        while True:
                            try:
                                codigo = pedir_numero("Ingrese el código del producto a agregar: ", 1 , float("inf"))
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        while buscar_por_codigo(catalogo, codigo) != -1:
                            mensaje_error("ERROR: El código no puede repetirse!")
                            while True:
                                try:
                                    codigo = pedir_numero("Ingrese el código del producto a agregar: ", 1 , float("inf"))
                                    break
                                except ValueError as e:
                                    mensaje_aviso(e)
                                except KeyboardInterrupt as e:
                                    mensaje_aviso(e)
                        while True:
                            try: 
                                nombre = input("Ingrese el nombre del producto a agregar: ").capitalize().replace("  ", " ").strip()
                                if nombre.isdigit():
                                    mensaje_aviso("No debe ser numérico.")
                                elif not nombre:
                                    mensaje_aviso("No debe estar vacío.")
                                else:
                                    break
                            except ValueError as e:
                                    mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                    mensaje_aviso(e)
                        
                        for i in range(len(CATEGORIAS)):
                            print(f"{i+1} {CATEGORIAS[i]}")
                        while True:
                            try:
                                categoria = pedir_numero("Ingrese la categoría a la que pertenece el producto: ", 1, 4)
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        while True:
                            try:
                                precio = pedir_numero("Ingrese el precio por unidad del producto: ", 1, float('inf'), True)
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        while True:
                            try:
                                stock = pedir_numero("Ingrese la cantidad de stock del producto: ", 0, float('inf'))
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        nuevo_producto = [codigo, nombre, categoria, precio, stock]
                        catalogo.append(nuevo_producto)
                        ordenar(catalogo, CODIGO, False)
                        mensaje_ok("Producto añadido exitosamente!")

                    imprimir_opciones(True)
                    while True:
                        try:
                            opc = pedir_numero("Seleccione una opción de catálogo: ", 1, 6)
                            break
                        except ValueError as e:
                            mensaje_aviso(e)
                        except KeyboardInterrupt as e:
                            mensaje_aviso(e)
                opcion = 0
            case 3:
                mostrar_resumen(catalogo, historial_ventas)
                opcion = 0
            case 4:
                mostrar_ranking(calcular_ranking(catalogo, historial_ventas))
                opcion = 0
            case 5:
                mostrar_matriz(catalogo, historial_ventas)
                opcion = 0
            case 6:
                historial = leer_historial(fecha)
                if len(historial) == 0:
                    mensaje_aviso("No hay ventas válidas registradas en el historial.\n")
                    continue
                op = 0
                opcion = 0
                while op != 4:
                    opcioness = (
                        "[cyan]1)[/] Total por día\n"
                        "[cyan]2)[/] Detalle de una fecha\n"
                        "[cyan]3)[/] Ranking historico\n"
                        "[cyan]4)[/] Volver al menú principal\n"
                    )
                    consola.print(Panel(opcioness, title=f"HISTORIAL DE VENTAS", border_style="blue", expand=False))
                    try:
                        op = pedir_numero("Seleccione una opción: ", 1, 4)
                    except ValueError as e:
                        mensaje_aviso(e)
                    except KeyboardInterrupt as e:
                        mensaje_aviso(e)
                    if op == 1:
                        filas = calcular_total_por_dia(historial)
                        mostrar_total_por_dia(filas)
                    elif op == 2:
                        while True:
                            try:
                                fecha_consulta = pedir_fecha()
                                break
                            except ValueError as e:
                                mensaje_aviso(e)
                            except KeyboardInterrupt as e:
                                mensaje_aviso(e)
                        cantidad, por_medio = calcular_detalle_fecha(historial, fecha_consulta)
                        mostrar_detalle_fecha(fecha_consulta, cantidad, por_medio)
                    elif op == 3:
                        ranking = calcular_ranking_historico(historial, catalogo)
                        mostrar_ranking_historico(ranking)
            case 7:
                try:
                    aplicadas, rechazadas = aplicar_novedades(catalogo, fecha)
                    if aplicadas > 0 and rechazadas == 0:
                        print(f"Se aplicaron {aplicadas} novedades.")
                    elif aplicadas == 0 and rechazadas > 0:
                        print(f"Se rechazaron {rechazadas} novedades.")
                    elif aplicadas > 0 and rechazadas > 0:
                        print(f"Se aplicaron {aplicadas} novedades y se rechazaron {rechazadas} novedades.")
                    else:
                        print(f"No se aplicaron novedades.")
                except FileNotFoundError:
                    print("No se encontró novedades.csv: no hay novedades para cargar.")
                except OSError:
                    print("No se pudo leer o vaciar novedades.csv.")
                except KeyboardInterrupt:
                    print("Se produjo un error de interrupción al ingresar un dato.")
                opcion = 0
            case 8:
                reponer = productos_reponer(catalogo)
                if reponer:
                    mostrar_reponer(reponer)
                else:
                    print("Aviso: no es necesario reponer productos.")
                opcion = 0
            case 9:
                try:
                    opcion = salir(catalogo, historial_ventas, no_existe_archivo_productos, fecha)
                except (OSError,ValueError,KeyboardInterrupt) as e:
                    imprimir_error(e)
                    opcion = 0

#------------ FUNCIONALIDADES DEL MENU - END -------------#

menu(historial_ventas)
