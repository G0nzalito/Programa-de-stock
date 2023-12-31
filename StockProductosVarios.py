import os
from ArchivoClases import *
from FuncionesExtra import *
import csv
from time import sleep
from pydrive.auth import GoogleAuth
import pydrive.drive 

# Debo los extras obvios que faltan. (Mostrar un producto por codigo o nombre, Cambiar el aumento de las categoria, investigar sobre la interfaz grafica T_T)

def manejoDeDrive(tipoOperacion):
    gauth = GoogleAuth()
    drive = pydrive.drive.GoogleDrive(gauth)
    if tipoOperacion == 'subir':
        
        gauth.LoadCredentialsFile("creds.json")
        gauth.LoadClientConfigFile('C:\\Users\\Usuario\\Documents\\Programa de stock\\client_secret.json')
        gauth.LocalWebserverAuth()  # Abre una ventana del navegador para autenticación
        gauth.SaveCredentialsFile("creds.json")
        # Acceso al Google Drive
        

        # Ruta del archivo CSV local que deseas subir
        # Crear un archivo en Google Drive
        archivo_drive_productos = drive.CreateFile()
        try:
            archivo_drive_productos.SetContentFile(rutaArchivoProductos)  # Establecer el contenido del archivo
        except FileNotFoundError:
            pass
        archivo_drive_productos.Upload()  # Subir el archivo
        archivo_drive_categorias = drive.CreateFile()
        try:
            archivo_drive_categorias.SetContentFile(rutaArchivoCategorias)
        except FileNotFoundError:
            pass

        print('Subiendo archivo a Google drive')
        
        archivo_drive_categorias.Upload()

        print("Archivo subido exitosamente a Google Drive.")
        sleep(1)
    elif tipoOperacion == 'actualizar':
        gauth.LoadCredentialsFile("creds.json")
        if gauth.credentials is None:
            gauth.LoadClientConfigFile('C:\\Users\\Usuario\\Documents\\Programa de stock\\Pruebas insanas\\client_secret.json')
            gauth.LocalWebserverAuth()

            # Guarda las credenciales en un archivo (creds.json) para su uso posterior
            gauth.SaveCredentialsFile("creds.json")
        elif gauth.access_token_expired:
            # Si las credenciales están presentes pero expiraron, refresca el token
            gauth.Refresh()
        else:
            # Las credenciales existen y no han expirado
            pass

        opcion = checkInput(['1', '2', '3'], 'Ingrese el numero de archivo que usted quiera subir: ', '1) Base de datos de Productos \n 2) Base de datos de categorias \n 3) Ambos')


        if opcion == 1:
            # Crear un archivo en Google Drive
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoProductos})
            archivo_drive.SetContentFile(rutaArchivoProductos)  # Establecer el contenido del archivo
            archivo_drive.Upload()  # Subir el archivo
        elif opcion == 2: 
            # Crear un archivo en Google Drive
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoCategorias})
            archivo_drive.SetContentFile(rutaArchivoCategorias)  # Establecer el contenido del archivo
            archivo_drive.Upload()  # Subir el archivo
        else:
            # Crear un archivo en Google Drive
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoProductos})
            archivo_drive.SetContentFile(rutaArchivoProductos)  # Establecer el contenido del archivo
            archivo_drive.Upload()  # Subir el archivo
            # Crear un archivo en Google Drive
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoCategorias})
            archivo_drive.SetContentFile(rutaArchivoCategorias)  # Establecer el contenido del archivo
            archivo_drive.Upload()  # Subir el archivo

        print('Archivo actualizado con exito en google drive')

    elif tipoOperacion == 'bajar':
        gauth.LoadCredentialsFile("creds.json")

        if gauth.credentials is None:
            # Si no hay credenciales almacenadas, realiza el proceso de autenticación y autorización
            gauth.LoadClientConfigFile('C:\\Users\\Usuario\\Documents\\Programa de stock\\Pruebas insanas\\client_secret.json')
            gauth.LocalWebserverAuth()

            # Guarda las credenciales en un archivo (creds.json) para su uso posterior
            gauth.SaveCredentialsFile("creds.json")
        elif gauth.access_token_expired:
            # Si las credenciales están presentes pero expiraron, refresca el token
            gauth.Refresh()
        else:
            # Las credenciales existen y no han expirado
            pass

        # Crear un archivo en Google Drive

        opcion = checkInput(['1', '2', '3'], 'Ingrese el numero de archivo que usted quiera bajar: ', '1) Base de datos de Productos \n 2) Base de datos de categorias \n 3) Ambos')


        if opcion == 1:
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoProductos})
            archivo_drive.GetContentFile(rutaArchivoProductos)
        elif opcion == 2: 
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoCategorias})
            archivo_drive.GetContentFile(rutaArchivoCategorias)
        else:
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoProductos})
            archivo_drive.GetContentFile(rutaArchivoProductos)
            archivo_drive = drive.CreateFile({'id': idEspecificaArchivoCategorias})
            archivo_drive.GetContentFile(rutaArchivoCategorias)

        print("Archivo bajado exitosamente de Google Drive.")
        sleep(1)

def modificacion_a_archivo(nombreArchivo, fieldNames, tipoCampoClave, campoClave, campoAModificar, modificación):
    with open(nombreArchivo, 'r') as archivo:
        lector = csv.DictReader(archivo, delimiter='|')
        lineas = list(lector)
        for line in lineas:
            campoClaveOrg = line[tipoCampoClave]
            if campoClave == campoClaveOrg:
                line[campoAModificar] = modificación
    
    with open(rutaArchivoCategorias, 'w') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldNames, delimiter='|')
        escritor.writeheader()
        escritor.writerows(lineas)

def cambiarAumento(categoria):
    nuevoAumento = input('Ingrese el nuevo aumento que quiere agregar a la categoria seleccionada: ')
    while not esNumero(nuevoAumento):
        print('ERROR, usted esta intentando ingresar un valor no numerico como un aumento, por favor, ingrese un aumento valido')
        nuevoAumento = input('Ingrese el nuevo aumento que quiere agregar a la catgoria seleccionada: ')

    modificacion_a_archivo(rutaArchivoCategorias, fieldNamesCat, 'nombre', categoria, 'aumento', nuevoAumento)
    
    

def buscarProducto(campo):

    if esNumero(campo):
        with open(rutaArchivoProductos, 'r') as archivo:
            lector = csv.DictReader(archivo, delimiter='|')
            lineas = list(lector)

            for line in lineas:
                codigo = line['codigo']
                nombre = line['nombre']
                if codigo == campo:
                    producto = Producto(line['codigo'], line['nombre'], str_to_list(line['colores']), line['precio'], line['stock'], line['nombre_categoria'])
                    print(producto)
                    decision = checkInput(['y','Y',str()], '¿Quiere vender este producto?(Ingrese "y" para si, no ingrese nada para no)', str())
                    if decision != str():
                        cantidad = input('Ingrese la cantidad de productos vendidos: ')
                        while not(esNumero(cantidad)) or (int(cantidad) > int(line['stock'])):
                            print('ERROR, la cantidad esta mal cargada o excede la cantidad que tenemos en stock, por favor ingrese un número')
                            cantidad = input('Ingrese la cantidad de productos vendidos: ')
                        mensaje = 'El precio por ' + str(cantidad) + ' unidad/es del producto ' + line['nombre'] + ' es ' + str(int(line['precio']) * int(cantidad)) 
                        print(mensaje)
                        decision = checkInput(['y', 'Y', str()], 'Ingrese "Y", para confirmar la baja del stock, no ingrese nada para cancelar la venta', str())
                        if decision != str():
                            modificarStock(codigo, int(cantidad))
    else:
        with open(rutaArchivoProductos, 'r') as archivo:
            lector = csv.DictReader(archivo, delimiter='|')
            lineas = list(lector)
            mostroAlgo = False
            for line in lineas:
                nombre = line['nombre']
                if campo in nombre or campo in nombre.lower():
                    producto = Producto(line['codigo'], line['nombre'], str_to_list(line['colores']), line['precio'], line['stock'], line['nombre_categoria'])
                    print(producto)
                    mostroAlgo = True
            if mostroAlgo:
                decision = checkInput(['y','Y',str()], '¿Desea vender algun producto de los enlistados anteriormente?(Ingrese "y" para si, no ingrese nada para no)', str())
                if decision != str():
                    codigo = input('Ingrese el codigo del producto que quiere vender: ')
                    while not(existeCodigo(codigo)):
                        print('ERROR, este codigo no existe en la base de datos, por favor revise lo que cargó')
                        codigo = input('Ingrese el codigo del producto que quiere vender: ')

                    buscarProducto(codigo)
    

def modificarCampoEsp(codigo):

    opciones = ['nombre', 'colores', 'precio', 'categoria']

    campo = 'jaja'

    while campo not in opciones:

        campo = input('Ingrese la opcion que desea cambiar: ')

        if esNumero(campo):
            campo = opciones[int(campo) - 1]
        
        campo = campo.lower()

        if campo == 'nombre':
            while True:
                banderaIgual = False
                cambio = input('Ingrese el nombre del producto que desea cargar: ')

                while esNumero(cambio):
                    print('El nombre solo puede llevar letras o caracteres especiales, por favor, vuelva a cargarlo')
                    cambio = input('Ingrese el nombre del producto que desea cargar: ')

                if os.path.exists(rutaArchivoProductos):
                    with open(rutaArchivoProductos, 'r') as archivo:
                        lector = csv.DictReader(archivo, delimiter='|')
                        for line in lector:
                            nombre = line['nombre']
                            if nombre == cambio:
                                print('ERROR, este nombre ya esta cargado en el sistema, por favor, cargue otro nombre')
                                banderaIgual = True
                                continue
                    if banderaIgual:
                        continue
                    break
                else:
                    break
        elif campo == 'colores':

            cambio = asignarColores()
        
        elif campo == 'precio':

            cambio = input('Ingrese el precio que tendra este producto: $')
            while not esNumero(cambio):
                print('Los precios son unicamente en numeros, por favor vuelva a cargarlo')
                cambio = input('Ingreseme el precio que tendra este producto: $')
        elif campo == 'categoria':
            cambio = asignarCategoria()
            campo = 'nombre_categoria'
            break
        else:
            print('Opcion incorrecta, por favor, cargue alguna de las opciones anteriores.')
    

    with open(rutaArchivoProductos, 'r') as archivo:
        lector = csv.DictReader(archivo, delimiter='|')
        lineas = list(lector)
        for line in lineas:
            codigoCar = line['codigo']
            if codigo == codigoCar:
                line[campo] = cambio
    
    with open(rutaArchivoProductos, 'w') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldNamesProd, delimiter='|')
        escritor.writeheader()
        escritor.writerows(lineas)
    
    

def aumentarPrecioCategoria(categoria):

    contador = 0
    
    with open(rutaArchivoCategorias, 'r') as archivo:
        lector = csv.DictReader(archivo, delimiter='|')
        lineas = list(lector)
        for line in lineas:
            catLeida = line['nombre']
            if categoria == catLeida:
                aumento = line['aumento']
                break

    menu = 'Desea aumentar los productos de la categoria ' + str(categoria) + '\n 1) el porcentaje que usted ingreso (siendo este ' + str(aumento) + '%)'  
    menu += '\n 2)Aumentarlo un porcentaje personalizado \n '

    decision = checkInput(['1','2'], 'Ingrese el número de opcion que quiere: ', menu)

    if decision == 2:
        aumento = input('Ingrese el porcentaje de aumento que prefiere en esta ocasion (Recuerde que puede cambiar el aumento predeterminado en la opcion numero 9): ')
        while not(esNumero(aumento)):
            print('ERROR, usted esta intentando ingresar un valor no numerico como un aumento, por favor, ingrese un aumento valido')
            aumento = input('Ingrese el porcentaje de aumento que prefiere en esta ocasion (Recuerde que puede cambiar el aumento predeterminado en la opcion numero 9): ')

    with open(rutaArchivoProductos, 'r') as archivo:
        lector = csv.DictReader(archivo, delimiter='|')
        lineas = list(lector)
        for line in lineas:
            cateProd = line['nombre_categoria']
            if categoria == cateProd:
                nuevoPrecio = float(line['precio']) * (1 + float(aumento)/100)
                line['precio'] = str(nuevoPrecio)
                contador += 1
    
    with open(rutaArchivoProductos, 'w') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldNamesProd, delimiter='|')
        escritor.writeheader()
        escritor.writerows(lineas)

    return contador


def bajaElemento(campoClave, tipo):
    
    encontrado = False

    if tipo == 'Producto':
        with open(rutaArchivoProductos, 'r+') as archivo:
            lector = csv.DictReader(archivo, delimiter="|")
            lineas = list(lector)
            for line in lineas:
                codigo = line['codigo']
                if codigo == campoClave:
                    lineas.remove(line)
                    encontrado = True
                    break
        
        if encontrado:
            with open(rutaArchivoProductos, 'w') as archivo:    
                escritor = csv.DictWriter(archivo, fieldNamesProd, delimiter='|')
                escritor.writeheader()
                escritor.writerows(lineas)
            
            return True
        else:
            return False
    elif tipo == 'Categoria':
        with open(rutaArchivoCategorias, 'r+') as archivo:
            lector = csv.DictReader(archivo, delimiter="|")
            lineas = list(lector)
            for line in lineas:
                nombre = line['nombre']
                if nombre == campoClave:
                    lineas.remove(line)
                    encontrado = True
                    break
        
        if encontrado:
            with open(rutaArchivoCategorias, 'w') as archivo:    
                escritor = csv.DictWriter(archivo, fieldNamesCat, delimiter='|')
                escritor.writeheader()
                escritor.writerows(lineas)
            
            return True
        else:
            return False

def modificarStock(codigoCar, cantidadCar = 0):

    encontrado = False

    with open(rutaArchivoProductos, 'r+') as archivo:
        lector = csv.DictReader(archivo, delimiter="|")
        lineas = list(lector)
        for line in lineas:
            codigo = line['codigo']
            if codigo == codigoCar:
                if cantidadCar == 0:
                    stock = line['stock']
                    nombre = line['nombre']
                    mensaje = 'Tenemos ' + str(stock) + ' unidad/es del producto ' + str(nombre) + ' en stock.'
                    while not encontrado:
                        print(mensaje)
                        modificacion = int(input('Ingrese la cantidad de producto que se vendio precedido con un "-", o la cantidad de producto que entró: '))
                        nuevoStock = int(line['stock']) + modificacion
                        if nuevoStock < 0:
                            print('No tenemos la cantidad necesaria de producto en stock para realizar esta venta. Por favor revise el valor que cargó')
                            continue
                        line['stock'] = str(nuevoStock)
                        encontrado = True
                        break
                else:
                    nuevoStock = int(line['stock']) - cantidadCar
                    line['stock'] = str(nuevoStock)
                    encontrado = True
                    break
    if encontrado:
        with open(rutaArchivoProductos, 'w') as archivo:    
            escritor = csv.DictWriter(archivo, fieldNamesProd, delimiter='|')
            escritor.writeheader()
            escritor.writerows(lineas)
        
        return True
    else:
        return False


def existeNombre(nombreCar):
    if os.path.exists(rutaArchivoCategorias):
        with open(rutaArchivoCategorias, 'rt') as archivo:
            lector = csv.DictReader(archivo, delimiter='|')
            for line in lector:
                nombre = line['nombre']
                if nombreCar == nombre:
                    return True
        return False
    else:
        return False

def crearNuevaCategoria():
    decision = 'y'
    if not(os.path.exists(rutaArchivoCategorias)) or os.path.getsize(rutaArchivoCategorias) < 25:
        with open(rutaArchivoCategorias, 'wt') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames = fieldNamesCat, delimiter='|')
            escritor.writeheader()
            nombre = input('Ingrese un nombre para la nueva categoria: ')
            while esNumero(nombre):
                print('ERROR, las categorias solo llevan letras en el nombre, por favor revise lo que ingreso')
                nombre = input('Ingrese un nombre para la nueva categoria: ')
            aumento = input('Ingrese el aumento general que tendran los productos de esta categoria: ')
            while not(esNumero(aumento)):
                print('ERROR, los aumentos son porcentuales, por lo tanto no se pueden ingresar letras. Por faovr, revise lo que ingreso')
                aumento = input('Ingrese el aumento general que tendras los productos de esta categoria: ')
            diccionario = {'nombre': nombre, 'aumento': aumento, 'estado': True}
            escritor.writerow(diccionario)
            archivo.flush()
    else:
        with open(rutaArchivoCategorias, 'at') as archivo:
            while decision != 'n':
                escritor = csv.DictWriter(archivo, fieldnames = fieldNamesCat, delimiter='|')
                nombre = input('Ingrese un nombre para la nueva categoria: ')
                while existeNombre(nombre) or esNumero(nombre):
                    print('ERROR, este nombre de categoria ya se encuentra cargado o esta intentando cargar un nombre de categoria con numeros, por favor, revise lo que ingreso')
                    nombre = input('Ingrese un nombre para la nueva categoria: ')

                aumento = input('Ingrese el aumento general que tendran los productos de esta categoria: ')
                while not(esNumero(aumento)):
                    print('ERROR, los aumentos van cargados en numeros, por favor, revise lo que ingresó')
                    aumento = input('Ingrese el aumento general que tendran los productos de esta categoria: ')

                diccionario = {'nombre': nombre, 'aumento': aumento, 'estado': True}
                escritor.writerow(diccionario)
                archivo.flush()
                decision = checkInput(['y','n','Y','N'], 'Si desea cargar más categorias, escriba una "y", de lo contrario, cargue una "n": ', " ")


def asignarCategoria():

    categorias = []
    contador = 0
    if os.path.exists(rutaArchivoCategorias):
        print('Categorias posibles')
        with open(rutaArchivoCategorias, 'r') as archivo:
            lector = csv.DictReader(archivo, delimiter='|')
            for line in lector:
                nomCategoria = line['nombre']
                aumCategoria = line['aumento']
                categorias.append(nomCategoria)
                contador += 1
                mensaje = str(contador) + ') ' + nomCategoria + '(Aumento predeteminado para esta categoria: ' + aumCategoria + ')'
                print(mensaje)
        categoria = input('Seleccione una categoria de las anteriormente mostradas: ')
        while not esNumero(categoria) or (int(categoria) <= 0 or int(categoria) > len(categorias)):
            print('Error, usted esta intentando cargar una categoria que no existe, por favor cargue el numero de la categoria que quiere cargar en el producto')
            categoria = input('Seleccione una categoria de las anteriormente mostradas(Ingrese el numero de las categorias ): ')

        return categorias[int(categoria) - 1]    
            
    else:
        print('Usted no cargo ninguna categoria, por favor, cargue antes todas las categorias para despues cargar los productos')
        return   

def existeCodigo(codigoCar):
    if os.path.exists(rutaArchivoProductos):
        with open(rutaArchivoProductos, 'r') as archivo:
            lector = csv.DictReader(archivo, delimiter='|')
            for line in lector:
                codigo = line['codigo']
                if codigo == codigoCar:
                    return True
        return False
    else:
        return False


def asignarColores():
    colores = []
    color = input('Ingrese el color del objeto(Ingrese uno al menos): ')
    while esNumero(color):
        print('ERROR, usted esta ingresando un color como si fuera un numero. Los colores solo llevan letras, por favor vuelva a ingresarlo')
        color = input('Ingrese el color del objeto(Ingrese uno al menos): ')

    while color != str():
        colores.append(color)
        color = input('Ingrese otro color que desea cargar(Presione enter con el campo vacio para dejar de cargar colores): ')
        while esNumero(color) and color != str():
            print('ERROR, usted esta ingresando un color como si fuera un numero. Los colores solo llevan letras, por favor vuelva a ingresarlo')
            color = input('Ingrese otro color que desea cargar(Presione enter con el campo vacio para dejar de cargar colores): ')

    return colores

def asignarValores():
    newCodigo = input('Ingrese el codigo de este producto: ')
    while not esNumero(newCodigo) or existeCodigo(newCodigo):
        print('ERROR, el codigo cargado ya esta cargado en la base de datos o esta mal cargado, por favor vuelva a cargarlo')
        newCodigo = input('Ingrese el codigo de este producto: ')

    while True:
        banderaIgual = False
        newNombre = input('Ingrese el nombre del producto que desea cargar: ')
        while esNumero(newNombre):
            print('El nombre solo puede llevar letras o caracteres especiales, por favor, vuelva a cargarlo')
            newNombre = input('Ingrese el nombre del producto que desea cargar: ')
            
        if os.path.exists(rutaArchivoProductos):
            with open(rutaArchivoProductos, 'r') as archivo:
                lector = csv.DictReader(archivo, delimiter='|')
                for line in lector:
                    nombre = line['nombre']
                    if nombre == newNombre:
                        print('ERROR, este nombre ya esta cargado en el sistema, por favor, cargue otro nombre')
                        banderaIgual = True
                        continue
            if banderaIgual:
                continue
            break
        else:
            break
    precio = input('Ingrese el precio que tendra este producto: $')
    while not esNumero(precio):
        print('Los precios son unicamente en numeros, por favor vuelva a cargarlo')
        precio = input('Ingreseme el precio que tendra este producto: $')
    
    colores = asignarColores()

    stock = input('Ingrese el stock inicial que tendra este producto: ')
    while not esNumero(stock):
        print('El stock es unicamente en numeros, por favor vuelva a cargarlo')
        stock = input('Ingreseme el stock inicial que tendra este producto: ')
    
    categoria = asignarCategoria()

    return newCodigo, newNombre, colores, precio, stock, categoria 

def cargarProductos():
    while True:
        codigo, nombre, colores, precio, stock, categoria = asignarValores()
        if categoria == None:
            return

        producto = Producto(codigo, nombre, colores, precio, stock, categoria)


        if not(os.path.exists(rutaArchivoProductos)) or os.path.getsize(rutaArchivoProductos) < 60:
            with open(rutaArchivoProductos, 'wt') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=fieldNamesProd, delimiter='|')
                escritor.writeheader()
                escritor.writerow(producto.cargador())
        else:
            with open(rutaArchivoProductos, 'at') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=fieldNamesProd, delimiter='|')
                escritor.writerow(producto.cargador())
    
        decision = checkInput(['y' , 'n', 'Y', 'N'], '¿Desea cargar más prodcutos?(Ingrese "y" para si o ingrese "n" para no): ', menu=str())
        
        if decision == 'n':
            break
    


def main():
    global rutaArchivoProductos
    global rutaArchivoCategorias 
    global fieldNamesProd
    global fieldNamesCat
    global idEspecificaArchivoProductos
    global idEspecificaArchivoCategorias


    idEspecificaArchivoProductos = '1if16_12xy-PV6kp1blyzUtZ7B7cj0uTo'
    idEspecificaArchivoCategorias = '1rJPLwpcpMAXsNqaUO_KQI_JlobkhuVSz'
    rutaArchivoProductos = os.path.join('ArchivosBaseDatos', 'DataBase.csv')
    rutaArchivoCategorias = os.path.join('ArchivosBaseDatos', 'CategoriesFile.csv')
    fieldNamesProd = ['codigo', 'nombre', 'colores', 'precio', 'stock', 'nombre_categoria', 'estado']
    fieldNamesCat = ['nombre', 'aumento', 'estado'] 

    alfabeto_opciones = ['1','2','3','4','5','6','7','8', '9', 'nuncadebeserejecutada', '10', '11','s', 'print1', 'print2']
    menu = 'Menú de opciones:\n 1) Buscar un producto por codigo o nombre \n 2) Cargar nuevos productos \n 3) Modificar stock de un producto \n '
    menu += '4) Crear nueva categoria \n 5) Eliminar categoria \n 6) Modificar informacion de un producto \n 7) Dar de baja un producto '
    menu += '\n 8) Aplicar aumento generalizado a una categoria \n 9) Cambiar el aumento general predeterminado a una categoria \n '
    menu += '10) Cargar modificaciones en la base de datos online \n '
    menu += '11) Bajar las actualizaciones desde la base de datos online \n S) Salir'
    opcion = -1

    while opcion != str('s'):
        os.system('cls')
        opcion = checkInput(alfabeto_opciones, 'Ingrese la opcion que desea: ', menu)
        print(opcion)
        
        if opcion == 1:
            
            print('Usted selecciono la opcion 1: Buscar un producto por codigo o nombre')
            campo = input('Ingrese el codigo o nombre del producto que quiere buscar: ')
            buscarProducto(campo)
            input('Ingerse enter para continuar')



        elif opcion == 2:

            print('Usted selecciono la opcion 2: Cargar nuevos productos')
            cargarProductos()
            input('Ingerse enter para continuar')
        
        elif opcion == 3:
           
            print('Usted ingreso la opcion 3: Modificar stock de un producto')
            codigo = input('Ingrese el codigo del producto al cual quiere modificar su stock: ')
            while not(esNumero(codigo)):
                print('ERROR, usted esta intentando cargar un codigo con una letra. Los codigos son con numeros, por favor, cargue un numero')
                codigo = input('Ingrese el codigo del producto al cual quiere modificar su stock: ')

            if modificarStock(codigo):
                print('El stock del producto fue actualizado con exito')
                input('Ingerse enter para continuar')
            elif not(modificarStock(codigo)):
                print('No se encontró ningun producto con el codigo especificado, por favor ingrese otro codigo.')
                input('Ingerse enter para continuar')
        elif opcion == 4:
    
            print('Usted selecciono la opcion 4: Crear nueva categoria')
            crearNuevaCategoria()
            print('Categoria creada correctamente')
            input('Ingerse enter para continuar')

        elif opcion == 5:

            print('Usted selecciono la opcion 5: Eliminar una categoria')
            nombre = input('Ingrese el nombre de la categoria que quiere eliminar: ')
            while esNumero(nombre):
                print('ERROR, usted esta intentando cargar el nombre de una categoria con un numero. Los nombres son con letras, por favor, cargue un numero')
                nombre = input('Ingrese el nombre de la categoria que quiere eliminar: ')

            if bajaElemento(nombre, 'Categoria'):
                print('La categoria fue eliminada con exito')
                input('Ingerse enter para continuar')
            elif not(bajaElemento(nombre,'Categoria')):
                print('No se ha encontrado la categoria con el nombre especificado, por favor ingrese otro nombre.')
                input('Ingerse enter para continuar')

        elif opcion == 6:

            print('Usted eligio la opcion 6: Modificar informacion de un producto')
            codigo = input('Ingrese el codigo del producto que quiere cambiar su información: ')
            
            while (not(esNumero(codigo))) or (not(existeCodigo(codigo))):
                print('ERROR, usted esta intentando cargar un codigo invalido o inexistente, recuerde que los codigos son con numeros, por favor, cargue un numero')
                codigo = input('Ingrese el codigo del producto al cual quiere modificar su stock: ')

            menu_cambios = '1) nombre' + '\n' + '2) Colores' + '\n' + '3) Precio' + '\n' + '4) Categoria' + '\n'
            print(menu_cambios)
            modificarCampoEsp(codigo)
            input('Ingerse enter para continuar')
        
        
        elif opcion == 7:

            print('Usted selecciono la opcion 7: Dar de baja un producto')
            codigo = input('Ingrese el codigo del producto que quiere eliminar: ')
            while not(esNumero(codigo)):
                print('ERROR, usted esta intentando cargar un codigo con una letra. Los codigos son con numeros, por favor, cargue un numero')
                codigo = input('Ingrese el codigo del producto que quiere eliminar: ')

            if bajaElemento(codigo, 'Producto'):
                print('El producto fue eliminado con exito.')
                input('Ingerse enter para continuar')
            elif not(bajaElemento(codigo,'Producto')):
                print('No se ha encontrado un producto con el codigo especificado, por favor ingrese otro codigo.')
                input('Ingerse enter para continuar')

        
        elif opcion == 8: 
            
            print('Usted selecciono la opcion 8: Aplicar un aumento generalizado a una categoria en especifico')
            categoria = asignarCategoria()
            contador = aumentarPrecioCategoria(categoria)
            mensaje = 'Se le cambio el precio a ' + str(contador) + ' productos'
            print(mensaje)
            input('Ingerse enter para continuar')

        elif opcion == 9:
            print('Usted selecciono la opcion 9: Cambiar el aumento general predeterminado de una categoria')
            categoria = asignarCategoria()
            cambiarAumento(categoria)
            input('Ingerse enter para continuar')

        elif opcion == 'nuncadebeserejecutada':
            print('Usted selecciono la opcion _: Cargar un archivo en Google Drive')
            manejoDeDrive('subir')
        
        elif opcion == 10:
            print('Usted selecciono la opcion 10: Cargar modificaciones en la base de datos online')
            manejoDeDrive('actualizar')
            input('Ingerse enter para continuar')

        elif opcion == 11:
            print('Usted selecciono la opcion 11: Bajar las actualizaciones desde la base de datos online')
            manejoDeDrive('bajar')
            input('Ingerse enter para continuar')

        elif opcion == 's':
            print('Muchas gracias por usar el programa, que tenga un lindo dia')
            sleep(1)
        

if __name__ == '__main__':
    main()
    #Codigo finalizado hasta posible actualización

