def esNumero(carga):
    try:
        int(carga)
    except ValueError:
        return False
    else: 
        return True

def str_to_list(string):
    
    newlist = []
    palabra = str()
    
    for car in string:
        if car not in ['[', ']', "'", ' ', ',']:
            palabra += car
        elif car == ',' or car == ']':
            newlist.append(palabra)
            palabra = str()
    
    return newlist

def checkInput(opciones, mensaje, menu):
    
    print(menu)
    opcion = input(mensaje)

    while opcion not in opciones:
        print('ERROR, esa opcion no se encuentra dentro de las anteriormente mostradas. Por favor cargue una opcion valida')
        print(menu)
        opcion = input(mensaje)
    
    try:
        return int(opcion)
    except ValueError:
        return opcion.lower()

if __name__ == '__main__':
    print(esNumero('4'))
    palabra = "['Esto', 'es', 'algo']"
    print(str_to_list(palabra))
