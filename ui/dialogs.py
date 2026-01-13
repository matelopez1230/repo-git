"""
Diálogos para agregar/editar empresas y empleados
"""
from typing import Optional
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QLabel
from PyQt6.QtCore import Qt
from ui.widgets import BaseDialog, LabeledInput, StyledButton
from models.company import Company
from models.employee import Employee
from services.email_service import EmailService, EmailConfig


class AddCompanyDialog(BaseDialog):
    """Diálogo para agregar una nueva empresa"""
    
    def __init__(self, parent=None):
        self.result: Optional[Company] = None
        super().__init__(parent, "Agregar Empresa")
        self.setGeometry(100, 100, 400, 250)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.name_input = LabeledInput("Nombre de la Empresa", "ej: Acme Corp")
        self.email_input = LabeledInput("Email", "ej: contacto@acme.com")
        self.phone_input = LabeledInput("Teléfono", "ej: +54 11 1234-5678")
        self.address_input = LabeledInput("Dirección", "ej: Calle 123, CABA")
        
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.address_input)
        
        # Botones
        button_layout = QHBoxLayout()
        btn_save = StyledButton("Guardar", "success")
        btn_cancel = StyledButton("Cancelar")
        btn_cancel.apply_style("primary")
        
        btn_save.clicked.connect(self.save_company)
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_company(self):
        name = self.name_input.get_value()
        
        if not name:
            QMessageBox.warning(self, "Error", "El nombre de la empresa es requerido")
            return
        
        self.result = Company(
            name=name,
            email=self.email_input.get_value() or None,
            phone=self.phone_input.get_value() or None,
            address=self.address_input.get_value() or None
        )
        self.accept()


class EditCompanyDialog(AddCompanyDialog):
    """Diálogo para editar una empresa existente"""
    
    def __init__(self, company: Company, parent=None):
        self.company = company
        super().__init__(parent)
        self.setWindowTitle("Editar Empresa")
        self.load_data()
    
    def load_data(self):
        self.name_input.set_value(self.company.name)
        self.email_input.set_value(self.company.email or "")
        self.phone_input.set_value(self.company.phone or "")
        self.address_input.set_value(self.company.address or "")


class AddEmployeeDialog(BaseDialog):
    """Diálogo para agregar un nuevo empleado"""
    
    def __init__(self, company_name: str, parent=None):
        self.company_name = company_name
        self.result: Optional[Employee] = None
        super().__init__(parent, f"Agregar Empleado - {company_name}")
        self.setGeometry(100, 100, 450, 350)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.first_name_input = LabeledInput("Nombre", "ej: Juan")
        self.last_name_input = LabeledInput("Apellido", "ej: Pérez")
        self.email_input = LabeledInput("Email", "ej: juan.perez@empresa.com")
        self.phone_input = LabeledInput("Teléfono", "ej: +54 11 1234-5678")
        self.position_input = LabeledInput("Posición/Cargo", "ej: Desarrollador")
        
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.position_input)
        
        # Botones
        button_layout = QHBoxLayout()
        btn_save = StyledButton("Guardar", "success")
        btn_cancel = StyledButton("Cancelar")
        btn_cancel.apply_style("primary")
        
        btn_save.clicked.connect(self.save_employee)
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_employee(self):
        first_name = self.first_name_input.get_value()
        last_name = self.last_name_input.get_value()
        email = self.email_input.get_value()
        
        if not (first_name and last_name and email):
            QMessageBox.warning(self, "Error", "Nombre, apellido y email son requeridos")
            return
        
        # El company_id se asignará en main_window
        self.result = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=self.phone_input.get_value() or None,
            position=self.position_input.get_value() or None,
            company_id=0
        )
        self.accept()


class EditEmployeeDialog(AddEmployeeDialog):
    """Diálogo para editar un empleado existente"""
    
    def __init__(self, employee: Employee, company_name: str, parent=None):
        self.employee = employee
        super().__init__(company_name, parent)
        self.setWindowTitle(f"Editar Empleado - {company_name}")
        self.load_data()
    
    def load_data(self):
        self.first_name_input.set_value(self.employee.first_name)
        self.last_name_input.set_value(self.employee.last_name)
        self.email_input.set_value(self.employee.email)
        self.phone_input.set_value(self.employee.phone or "")
        self.position_input.set_value(self.employee.position or "")
    
    def save_employee(self):
        first_name = self.first_name_input.get_value()
        last_name = self.last_name_input.get_value()
        email = self.email_input.get_value()
        
        if not (first_name and last_name and email):
            QMessageBox.warning(self, "Error", "Nombre, apellido y email son requeridos")
            return
        
        self.result = Employee(
            id=self.employee.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=self.phone_input.get_value() or None,
            position=self.position_input.get_value() or None,
            company_id=self.employee.company_id
        )
        self.accept()


class EmailConfigDialog(BaseDialog):
    """Diálogo para configurar credenciales de email"""
    
    def __init__(self, parent=None):
        self.result: Optional[EmailConfig] = None
        super().__init__(parent, "Configurar Email")
        self.setGeometry(100, 100, 450, 300)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Selector de proveedor
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Proveedor:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["Gmail", "Outlook"])
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        
        layout.addLayout(provider_layout)
        
        # Inputs
        self.email_input = LabeledInput("Email", "ej: tu_email@gmail.com")
        self.password_input = LabeledInput("Contraseña/Token", "Password o token de aplicación")
        from PyQt6.QtWidgets import QLineEdit
        self.password_input.input.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        
        # Info
        info_label = QLabel(
            "⚠️ Para Gmail: usar Contraseña de Aplicación\n"
            "⚠️ Para Outlook: usar contraseña normal\n"
            "Los datos se guardan solo en esta sesión"
        )
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info_label)
        
        # Botones
        button_layout = QHBoxLayout()
        btn_test = StyledButton("🧪 Probar Conexión", "primary")
        btn_save = StyledButton("✅ Guardar", "success")
        btn_cancel = StyledButton("Cancelar")
        btn_cancel.apply_style("primary")
        
        btn_test.clicked.connect(self.test_connection)
        btn_save.clicked.connect(self.save_config)
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_test)
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def test_connection(self):
        """Prueba la conexión sin guardar"""
        email = self.email_input.get_value()
        password = self.password_input.get_value()
        provider = self.provider_combo.currentText().lower()
        
        if not (email and password):
            QMessageBox.warning(self, "Error", "Completar email y contraseña")
            return
        
        # Probar conexión
        success, message = EmailService.test_connection(provider, email, password)
        if success:
            QMessageBox.information(self, "Éxito", message)
        else:
            QMessageBox.warning(self, "Error", message)
    
    def save_config(self):
        """Guarda la configuración"""
        email = self.email_input.get_value()
        password = self.password_input.get_value()
        provider = self.provider_combo.currentText().lower()
        
        if not (email and password):
            QMessageBox.warning(self, "Error", "Completar todos los campos")
            return
        
        # Crear configuración
        self.result = EmailConfig(
            provider=provider,
            email=email,
            password=password
        )
        self.accept()

