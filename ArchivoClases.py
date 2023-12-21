class Producto:
    def __init__(self, codigo, nombre, color, precio, stock, categoria, estado=True):
        self.codigo = codigo
        self.nombre = nombre
        self.color = color
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.estado = estado
    
    def __str__(self):
        mensaje = 'Nombre del producto: ' + str(self.nombre) + '\n' + 'Codigo del producto: ' + str(self.codigo) + '\n' + 'Precio: $' + str(self.precio)  
        mensaje += '\n' + 'Color: ' 
        if type(self.color) == list: 
            for i in range(len(self.color)):
                mensaje += self.color[i] + ', '
        else:
            mensaje += self.color
        
        mensaje += '\n' + 'Stock actual: ' + str(self.stock) + '\n' + 'Categoria: ' + str(self.categoria) + '\n'
        
        if self.estado:
            mensaje += 'Estado: Habilitado' + '\n'
        else:
            mensaje += 'Estado: Deshabilitado' + '\n'
        
        return mensaje

    def cargador(self):
        return {'codigo': self.codigo, 'nombre': self.nombre,'colores': self.color,'precio': self.precio,'stock': self.stock, 
                'nombre_categoria': self.categoria,'estado': self.estado}
    
class Categoria:
    def __init__(self, nombre, aumento):
        self.nombre = nombre
        self.aumento = aumento
        self.estado = True
    
    def __str__(self):
        mensaje = 'Nombre de la categoria: ' + self.nombre +  '\n' + 'Aumento general promedio: ' + str(self.aumento) + '\n'
        if self.estado:
            mensaje += 'Estado: Habilitado' + '\n'
        else:
            mensaje += 'Estado: Deshabilitado' + '\n'
        
        return mensaje
    
    def cargador(self):
        return {'nombre': self.nombre, 'aumento': self.aumento, 'estado': self.estado} 

if __name__ == '__main__':
    producto = Producto('0002', 'El increible hombre que me la araña', 'Morado', 5000, 0, 'Bazar')
    print(producto)