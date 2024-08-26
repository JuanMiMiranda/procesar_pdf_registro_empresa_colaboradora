class NombreApellidosParser:
    
    def __init__(self, nombre_completo: str):
        self.nombre_completo = nombre_completo.strip()
        self.nombre = None
        self.apellido1 = None
        self.apellido2 = None
    

    def parse(self):
        """
        Divide el nombre completo en nombre, primer apellido y segundo apellido.
        Asume que el nombre es la primera palabra y que los apellidos pueden ser compuestos.
        """
        partes = self.nombre_completo.split()

        if len(partes) == 2:
            # Si hay solo dos partes, se asume que son nombre y primer apellido
            self.nombre = partes[0]
            self.apellido1 = partes[1]
            self.apellido2 = ""
        elif len(partes) == 3:
            # Si hay tres partes, se asume que la primera es el nombre, y las otras dos son apellidos
            self.nombre = partes[0]
            self.apellido1 = partes[1]
            self.apellido2 = partes[2]
        elif len(partes) > 3:
            # Detectar el nombre y apellidos compuestos
            self.nombre = partes[0]
            self.apellido1 = partes[1]
            self.apellido2 = " ".join(partes[2:])
            
            # Si la segunda palabra es una preposición, se considera parte del primer apellido
            if partes[1].lower() in ['de', 'del', 'la', 'los']:
                self.apellido1 = partes[1] + " " + partes[2]
                self.apellido2 = " ".join(partes[3:])
        else:
            # En caso de que solo se provea un nombre o esté mal escrito
            self.nombre = partes[0]
            self.apellido1 = ""
            self.apellido2 = ""

        return self.nombre, self.apellido1, self.apellido2