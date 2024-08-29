# import pyodbc
from models.operador_model import Operador
from models.usuario_operador_model import Usuario_Operador

class OperadorDAL:
    def __init__(self, db):
        self.db = db

    def map_row_to_operador(self, row):
        return Operador(
            nif_operador=row.get('NIF_OPERADOR'),
            razon_social=row.get('RAZON_SOCIAL'),
            cob_fwa=row.get('COB_FWA'),
            cob_movil=row.get('COB_MOVIL'),
            nif_grupo_operador=row.get('NIF_GRUPO_OPERADOR'),
            grupo_operador=row.get('GRUPO_OPERADOR'),
            nif_replegal=row.get('NIF_REPLEGAL'),
            nombre_replegal=row.get('NOMBRE_REPLEGAL'),
            nif_notificacion=row.get('NIF_NOTIFICACION'),
            representante_notificacion=row.get('REPRESENTANTE_NOTIFICACION'),
            email_notificacion=row.get('EMAIL_NOTIFICACION'),
        )

    def get_all_records(self):
        cursor = self.db.get_cursor()
        try:
            cursor.execute('SELECT * FROM Tabla_Operadores')
            columns = [column[0] for column in cursor.description]
            # Cargar como un diccionario con acceso a los nombres de las columnas. 
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            operadores = [self.map_row_to_operador(row) for row in rows]
            return operadores
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
        finally:
            cursor.close()


    def get_record_by_nif(self, nif):
        cursor = self.db.get_cursor()
        try:
            query = 'SELECT * FROM Tabla_Operadores WHERE NIF_OPERADOR = ?'
            cursor.execute(query, (nif,))
            row = cursor.fetchone()  # Obtener solo una fila
            if row:
                columns = [column[0] for column in cursor.description]
                row_dict = dict(zip(columns, row))
                return self.map_row_to_operador(row_dict)
            else:
                return None  # Si no se encuentra el usuario
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        finally:
            cursor.close()


    def insert(self, operador, representate_legal):
        cursor = self.db.get_cursor()
        try:
            query = '''
            INSERT INTO Tabla_Operadores (
                NIF_OPERADOR,
                RAZON_SOCIAL,
                COB_FWA,
                COB_MOVIL,
                NIF_GRUPO_OPERADOR,
                GRUPO_OPERADOR,
                NIF_REPLEGAL,
                NOMBRE_REPLEGAL,
                NIF_NOTIFICACION,
                REPRESENTANTE_NOTIFICACION,
                EMAIL_NOTIFICACION
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            # Ejecutar la consulta con los valores del operador
            cursor.execute(query, (
                operador.nif_operador,
                operador.razon_social,
                operador.cob_fwa,
                operador.cob_movil,
                operador.nif_grupo_operador,
                operador.grupo_operador,
                # operador.nif_replegal,
                representate_legal.nif,
                #operador.nombre_replegal,
                representate_legal.nombre_completo,
                operador.nif_notificacion,
                operador.representante_notificacion,
                #operador.email_notificacion
                representate_legal.email
            ))

            # Confirmar la transacción
            self.db.commit()
            print("Operador insertado exitosamente.")
        
        except Exception as e:
            print(f"An error occurred while inserting the operator: {str(e)}")
            self.db.connection.rollback()  # Revertir la transacción en caso de error
        
        finally:
            cursor.close()


    def update_operador(self, operador: Operador, representate_legal: Usuario_Operador) -> bool:
        """
        Actualiza los datos del operador en la base de datos.

        Parámetros:
        - operador: La instancia del operador con los datos a actualizar.
        - representate_legal: La instancia del representante legal con los datos a actualizar.

        Retorna:
        - bool: True si la actualización fue exitosa, False si ocurrió un error.
        """
        cursor = self.db.get_cursor()
        try:
            query = '''
            UPDATE Tabla_Operadores
            SET
                RAZON_SOCIAL = ?,
                COB_FWA = ?,
                COB_MOVIL = ?,
                NIF_GRUPO_OPERADOR = ?,
                GRUPO_OPERADOR = ?,
                NIF_REPLEGAL = ?,
                NOMBRE_REPLEGAL = ?,
                NIF_NOTIFICACION = ?,
                REPRESENTANTE_NOTIFICACION = ?,
                EMAIL_NOTIFICACION = ?
            WHERE
                NIF_OPERADOR = ?
            '''
            
            # Ejecutar la consulta con los valores del operador
            cursor.execute(query, (
                operador.razon_social,
                operador.cob_fwa,
                operador.cob_movil,
                operador.nif_grupo_operador,
                operador.grupo_operador,
                representate_legal.nif,
                representate_legal.nombre_completo,
                operador.nif_notificacion,
                operador.representante_notificacion,
                representate_legal.email,
                operador.nif_operador  # Condición para la actualización
            ))

            # Confirmar la transacción
            self.db.commit()
            print("Operador actualizado exitosamente.")
        
        except Exception as e:
            print(f"An error occurred while updating the operator: {str(e)}")
            self.db.connection.rollback()  # Revertir la transacción en caso de error
        
        finally:
            cursor.close()