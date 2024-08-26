import pyodbc

class Database:
    def __init__(self, db_path):
        self.connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={db_path};"
        )
        self.connection = None

    def connect(self):
        """Establece la conexión a la base de datos."""
        self.connection = pyodbc.connect(self.connection_string)

    def get_cursor(self):
        """Devuelve un cursor para realizar operaciones en la base de datos."""
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        """Confirma las transacciones si la conexión está activa."""
        if self.connection:
            self.connection.commit()

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None