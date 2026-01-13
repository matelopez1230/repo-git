"""
Punto de entrada de la aplicación
"""
import sys
from PyQt6.QtWidgets import QApplication
from config.database import DatabaseConfig
from ui.main_window import MainWindow


def main():
    """Función principal"""
    # Inicializar BD
    DatabaseConfig.init_database()
    
    # Crear app
    app = QApplication(sys.argv)
    
    # Crear y mostrar ventana principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
