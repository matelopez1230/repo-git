"""
Componentes reutilizables PyQt6
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class BaseDialog(QDialog):
    """Diálogo base con estilos comunes"""
    
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        """Método para que las subclases implementen la UI"""
        pass


class LabeledInput(QWidget):
    """Widget con etiqueta + input reutilizable"""
    
    def __init__(self, label_text: str, placeholder: str = ""):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label_font = QFont()
        label_font.setBold(True)
        label.setFont(label_font)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        
        layout.addWidget(label)
        layout.addWidget(self.input)
        
        self.setLayout(layout)
    
    def get_value(self) -> str:
        return self.input.text().strip()
    
    def set_value(self, value: str):
        self.input.setText(value)
    
    def clear(self):
        self.input.clear()


class StyledButton(QPushButton):
    """Botón con estilos predeterminados"""
    
    def __init__(self, text: str, style_type: str = "primary"):
        super().__init__(text)
        self.apply_style(style_type)
    
    def apply_style(self, style_type: str):
        if style_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #007ACC;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #005A9E;
                }
                QPushButton:pressed {
                    background-color: #003E66;
                }
            """)
        elif style_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #D32F2F;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #B71C1C;
                }
            """)
        elif style_type == "success":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #388E3C;
                    color: white;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2E7D32;
                }
            """)
