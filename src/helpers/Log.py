import logging
from datetime import datetime

class Log:
    def __init__(self, log_file="app.log", level=logging.INFO):
        """
        Inicializa la clase Log.

        :param log_file: Nombre del archivo de log.
        :param level: Nivel de registro (por defecto, INFO).
        """
        self.logger = logging.getLogger("AplicacionLog")
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Crear el manejador para archivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        
        # Crear el manejador para la consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """Registra un mensaje de información."""
        self.logger.info(message)

    def warning(self, message):
        """Registra un mensaje de advertencia."""
        self.logger.warning(message)

    def error(self, message):
        """Registra un mensaje de error."""
        self.logger.error(message)

    def debug(self, message):
        """Registra un mensaje de depuración."""
        self.logger.debug(message)

    def log_to_file(self, file_path, message):
        """Escribe un mensaje específico en un archivo de log."""
        with open(file_path, 'a') as f:
            f.write(f"{datetime.now()} - {message}\n")