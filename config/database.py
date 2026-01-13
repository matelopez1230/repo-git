"""
Configuración de base de datos SQLite3
"""
import sqlite3
import os
from pathlib import Path

# Ruta de la base de datos
DB_PATH = Path(__file__).parent.parent / "database.db"


class DatabaseConfig:
    """Configuración y conexión a SQLite"""
    
    @staticmethod
    def get_connection():
        """Obtiene conexión a BD"""
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row  # Permite acceder por nombre de columna
        return conn
    
    @staticmethod
    def init_database():
        """Inicializa schema de BD si no existe"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        # Tabla de Empresas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de Empleados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                company_id INTEGER NOT NULL,
                position TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
            )
        """)
        
        # Tabla de Templates de Mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                template TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    DatabaseConfig.init_database()
    print("✅ Base de datos inicializada correctamente")
