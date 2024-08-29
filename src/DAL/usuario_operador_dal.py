# import pyodbc
from models.usuario_operador_model import Usuario_Operador
from DAL.operador_dal import OperadorDAL

class Usuario_OperadorDAL:
    def __init__(self, db):
        self.db = db

    def map_row_to_usuario_operador(self, row):
        return Usuario_Operador(
            id=row.get('Id'),
            nombre=row.get('Nombre'),
            apellido1=row.get('Apellido1'),
            apellido2=row.get('Apellido2'),
            nif=row.get('NIF'),
            email=row.get('e-mail'),
            telefono=row.get('Telefono'),
        )
    
    def map_row_to_operadoras(self, usuario_operador, row_dict):
        """
        Mapea las operadoras asociadas a un usuario y las añade a la propiedad 'operadoras' del objeto Usuario_Operador.

        :param usuario_operador: Objeto Usuario_Operador al que se le asignarán las operadoras.
        :param row_dict: Diccionario con los datos del usuario.
        :return: Objeto Usuario_Operador con la propiedad 'operadoras' cargada.
        """
        try:
            # Mapear una operadora desde row_dict usando el método map_row_to_operador de la OperadorDAL
            operador_dal = OperadorDAL(None)
            operadora = operador_dal.map_row_to_operador(row_dict)
            
            # Añadir la operadora a la lista de operadoras del usuario
            usuario_operador.operadoras.append(operadora)
        
        except Exception as e:
            print(f"An error occurred while mapping operadoras: {str(e)}")
        
        # Devolver el objeto Usuario_Operador con la propiedad 'operadoras' cargada
        return usuario_operador

    def get_all_records(self):
        cursor = self.db.get_cursor()
        try:
            cursor.execute('SELECT * FROM Tabla_Usuarios_UNICODatos')
            columns = [column[0] for column in cursor.description]
            # Cargar como un diccionario con acceso a los nombres de las columnas. 
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            usuarios_operadores = [self.map_row_to_usuario_operador(row) for row in rows]
            return usuarios_operadores
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
        finally:
            cursor.close()


    def get_record_by_nif(self, nif):
        cursor = self.db.get_cursor()
        try:
            query = 'SELECT * FROM Tabla_Usuarios_UNICODatos WHERE NIF = ?'
            cursor.execute(query, (nif,))
            row = cursor.fetchone()  # Obtener solo una fila
            if row:
                columns = [column[0] for column in cursor.description]
                row_dict = dict(zip(columns, row))
                return self.map_row_to_usuario_operador(row_dict)
            else:
                return None  # Si no se encuentra el usuario
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        finally:
            cursor.close()


    def insert(self, usuario_operador):
        cursor = self.db.get_cursor()
        try:
            # Consulta de inserción
            query = '''
            INSERT INTO Tabla_Usuarios_UNICODatos (
                Nombre,
                Apellido1,
                Apellido2,
                NIF,
                [e-mail],
                [Teléfono]
            ) VALUES (?, ?, ?, ?, ?, ?)
            '''
            
            # Ejecutar la consulta con los valores del usuario_operador
            cursor.execute(query, (
                usuario_operador.nombre,
                usuario_operador.apellido1,
                usuario_operador.apellido2,
                usuario_operador.nif,
                usuario_operador.email,
                usuario_operador.telefono
            ))

            # Obtener el ID del último registro insertado
            cursor.execute("SELECT @@IDENTITY")
            usuario_operador.id = cursor.fetchone()[0]
            
            # Confirmar la transacción
            self.db.commit()
            print("Usuario operador insertado exitosamente.")
            
            # Retornar el objeto con el ID asignado
            return usuario_operador
            
        except Exception as e:
            # En caso de error, deshacer la transacción
            self.db.rollback()
            print(f"An error occurred while inserting the usuario operador: {str(e)}")
            return None
            
        finally:
            cursor.close()

    def get_usuario_con_relacion_de_operadoras(self, usuario_operador):
        """
        Retorna objeto usuario operador cargado con las operadoras que representa.
        """
        cursor = self.db.get_cursor()
        try:
            query = 'SELECT * FROM Tabla_Usuarios_Operadores UO INNER JOIN Tabla_Operadores O ON O.NIF_OPERADOR = UO.CIF_Operador  WHERE Id_Usuario = ?'
            cursor.execute(query, (usuario_operador.id))
            row = cursor.fetchone()  # Obtener solo una fila
            if row:
                columns = [column[0] for column in cursor.description]
                row_dict = dict(zip(columns, row))
                return self.map_row_to_operadoras(usuario_operador, row_dict)
            else:
                usuario_operador.operadoras = []
                return usuario_operador  # Si no se encuentra el usuario
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        finally:
            cursor.close()


    def add_usuario_relacion_con_operadora(self, usuario_operador, operadora):
        """
        Inserta una relación entre un usuario y una operadora en la base de datos.
        """
        cursor = self.db.get_cursor()
        try:
            # Comprobar si ya existe la relación entre el usuario y la operadora
            query_check = '''
            SELECT COUNT(*) FROM Tabla_Usuarios_Operadores 
            WHERE Id_Usuario = ? AND CIF_Operador = ?
            '''
            cursor.execute(query_check, (usuario_operador.id, operadora.nif_operador))
            existe = cursor.fetchone()[0]

            if existe == 0:
                # Si no existe la relación, la insertamos
                query_insert = '''
                INSERT INTO Tabla_Usuarios_Operadores (Id_Usuario, CIF_Operador) 
                VALUES (?, ?)
                '''
                cursor.execute(query_insert, (usuario_operador.id, operadora.nif_operador))
                self.db.connection.commit()
                print("Relación entre usuario y operadora insertada correctamente.")
            else:
                print("La relación entre el usuario y la operadora ya existe.")

        except Exception as e:
            print(f"An error occurred while inserting the relationship: {str(e)}")
            self.db.connection.rollback()
        finally:
            cursor.close()


    def update_usuario(self, usuario_operador):
        cursor = self.db.get_cursor()
        try:
            # Consulta de actualización
            query = '''
            UPDATE Tabla_Usuarios_UNICODatos
            SET
                Nombre = ?,
                Apellido1 = ?,
                Apellido2 = ?,
                [e-mail] = ?,
                [Teléfono] = ?
            WHERE
                NIF = ?
            '''
            # Ejecutar la consulta con los valores del usuario_operador
            cursor.execute(query, (
                usuario_operador.nombre,
                usuario_operador.apellido1,
                usuario_operador.apellido2,
                usuario_operador.email,
                usuario_operador.telefono,
                usuario_operador.nif  # Condición para identificar el usuario a actualizar
            ))

            # Confirmar la transacción
            self.db.commit()
            print("Usuario operador actualizado exitosamente.")

            # Recuperar el ID del registro actualizado
            cursor.execute('''
            SELECT ID FROM Tabla_Usuarios_UNICODatos WHERE NIF = ?
            ''', (usuario_operador.nif,))
            usuario_operador.id = cursor.fetchone()[0]
            
            # Retornar True para indicar que la actualización fue exitosa
            return True
                
        except Exception as e:
            # En caso de error, deshacer la transacción
            self.db.rollback()
            print(f"An error occurred while updating the usuario operador: {str(e)}")
            return False
                
        finally:
            cursor.close()
    
  