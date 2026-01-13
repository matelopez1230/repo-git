"""
Ventana principal de la aplicación
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QMessageBox,
    QTextEdit, QLabel, QComboBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from db.repository import CompanyRepository, EmployeeRepository, MessageTemplateRepository
from models.company import Company
from models.employee import Employee
from ui.dialogs import (
    AddCompanyDialog, EditCompanyDialog, AddEmployeeDialog, EditEmployeeDialog,
    EmailConfigDialog
)
from ui.widgets import StyledButton
from services.message_service import MessageService
from services.email_service import EmailService


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Empresas y Empleados")
        self.setGeometry(100, 100, 1200, 700)
        
        self.current_company = None
        self.current_employees = []
        self.email_service = None  # Servicio de email (se configura en sesión)
        
        self.init_ui()
        self.load_companies()
    
    def init_ui(self):
        """Inicializa la interfaz gráfica"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Título
        title = QLabel("Gestor de Empresas y Comunicaciones")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Empresas
        self.tab_companies = self.create_companies_tab()
        self.tabs.addTab(self.tab_companies, "Empresas")
        
        # Tab 2: Empleados
        self.tab_employees = self.create_employees_tab()
        self.tabs.addTab(self.tab_employees, "Empleados")
        
        # Tab 3: Mensajes
        self.tab_messages = self.create_messages_tab()
        self.tabs.addTab(self.tab_messages, "Mensajes")
        
        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
    
    def create_companies_tab(self):
        """Crea el tab de gestión de empresas"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Tabla de empresas
        self.companies_table = QTableWidget()
        self.companies_table.setColumnCount(5)
        self.companies_table.setHorizontalHeaderLabels(["ID", "Nombre", "Email", "Teléfono", "Dirección"])
        header = self.companies_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.companies_table.itemSelectionChanged.connect(self.on_company_selected)
        
        layout.addWidget(QLabel("Empresas Registradas:"))
        layout.addWidget(self.companies_table)
        
        # Botones
        buttons_layout = QHBoxLayout()
        button_add = StyledButton("+ Agregar Empresa", "success")
        button_edit = StyledButton("✎ Editar", "primary")
        button_delete = StyledButton("🗑 Eliminar", "danger")
        
        button_add.clicked.connect(self.add_company)
        button_edit.clicked.connect(self.edit_company)
        button_delete.clicked.connect(self.delete_company)
        
        buttons_layout.addWidget(button_add)
        buttons_layout.addWidget(button_edit)
        buttons_layout.addWidget(button_delete)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        tab.setLayout(layout)
        return tab
    
    def create_employees_tab(self):
        """Crea el tab de gestión de empleados"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Selector de empresa
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Empresa:"))
        self.company_combo = QComboBox()
        self.company_combo.currentIndexChanged.connect(self.on_company_filter_changed)
        selector_layout.addWidget(self.company_combo)
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Tabla de empleados
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(6)
        self.employees_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Email", "Teléfono", "Posición"])
        header = self.employees_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(QLabel("Empleados:"))
        layout.addWidget(self.employees_table)
        
        # Botones
        buttons_layout = QHBoxLayout()
        button_add_employee = StyledButton("+ Agregar Empleado", "success")
        button_edit_employee = StyledButton("✎ Editar", "primary")
        button_delete_employee = StyledButton("🗑 Eliminar", "danger")
        
        button_add_employee.clicked.connect(self.add_employee)
        button_edit_employee.clicked.connect(self.edit_employee)
        button_delete_employee.clicked.connect(self.delete_employee)
        
        buttons_layout.addWidget(button_add_employee)
        buttons_layout.addWidget(button_edit_employee)
        buttons_layout.addWidget(button_delete_employee)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        tab.setLayout(layout)
        return tab
    
    def create_messages_tab(self):
        """Crea el tab de envío de mensajes"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Selector de empresa
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Empresa:"))
        self.msg_company_combo = QComboBox()
        self.msg_company_combo.currentIndexChanged.connect(self.on_message_company_changed)
        selector_layout.addWidget(self.msg_company_combo)
        selector_layout.addStretch()
        
        layout.addLayout(selector_layout)
        
        # Template de mensaje
        layout.addWidget(QLabel("Template de Mensaje:"))
        self.message_template = QTextEdit()
        self.message_template.setPlaceholderText(
            "Escribe tu mensaje usando variables:\n"
            "{nombre} - Nombre\n"
            "{apellido} - Apellido\n"
            "{nombre_completo} - Nombre completo\n"
            "{email} - Email\n"
            "{telefono} - Teléfono\n"
            "{posicion} - Posición\n"
            "{empresa} - Empresa"
        )
        self.message_template.setMaximumHeight(150)
        layout.addWidget(self.message_template)
        
        # Vista previa
        layout.addWidget(QLabel("Vista Previa (todos los empleados):"))
        self.preview_area = QTextEdit()
        self.preview_area.setReadOnly(True)
        layout.addWidget(self.preview_area)
        
        # Botones
        buttons_layout = QHBoxLayout()
        button_preview = StyledButton("👁 Generar Vista Previa", "primary")
        button_copy_recipients = StyledButton("📋 Copiar Destinatarios", "success")
        button_configure_email = StyledButton("⚙️ Configurar Email", "primary")
        button_send_emails = StyledButton("📧 Enviar Emails", "success")
        button_variables_help = StyledButton("? Variables", "primary")
        
        button_preview.clicked.connect(self.generate_preview)
        button_copy_recipients.clicked.connect(self.copy_recipients)
        button_configure_email.clicked.connect(self.configure_email)
        button_send_emails.clicked.connect(self.send_emails)
        button_variables_help.clicked.connect(self.show_variables_help)
        
        buttons_layout.addWidget(button_preview)
        buttons_layout.addWidget(button_copy_recipients)
        buttons_layout.addWidget(button_configure_email)
        buttons_layout.addWidget(button_send_emails)
        buttons_layout.addWidget(button_variables_help)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        tab.setLayout(layout)
        return tab
    
    # ========== MÉTODOS DE EMPRESAS ==========
    
    def load_companies(self):
        """Carga todas las empresas en la tabla"""
        companies = CompanyRepository.read_all()
        self.companies_table.setRowCount(len(companies))
        
        for row, company in enumerate(companies):
            self.companies_table.setItem(row, 0, QTableWidgetItem(str(company.id)))
            self.companies_table.setItem(row, 1, QTableWidgetItem(company.name))
            self.companies_table.setItem(row, 2, QTableWidgetItem(company.email or ""))
            self.companies_table.setItem(row, 3, QTableWidgetItem(company.phone or ""))
            self.companies_table.setItem(row, 4, QTableWidgetItem(company.address or ""))
        
        self.update_company_combos()
    
    def update_company_combos(self):
        """Actualiza los combobox de empresas"""
        companies = CompanyRepository.read_all()
        
        # Limpiar combos
        self.company_combo.blockSignals(True)
        self.msg_company_combo.blockSignals(True)
        
        self.company_combo.clear()
        self.msg_company_combo.clear()
        
        for company in companies:
            self.company_combo.addItem(company.name, company.id)
            self.msg_company_combo.addItem(company.name, company.id)
        
        self.company_combo.blockSignals(False)
        self.msg_company_combo.blockSignals(False)
    
    def on_company_selected(self):
        """Evento cuando se selecciona una empresa"""
        row = self.companies_table.currentRow()
        if row >= 0:
            item = self.companies_table.item(row, 0)
            if item is not None:
                company_id = int(item.text())
                self.current_company = CompanyRepository.read(company_id)
    
    def on_company_filter_changed(self):
        """Evento cuando cambia el filtro de empresa"""
        company_id = self.company_combo.currentData()
        if company_id:
            self.load_employees_for_company(company_id)
    
    def on_message_company_changed(self):
        """Evento cuando cambia empresa en tab de mensajes"""
        company_id = self.msg_company_combo.currentData()
        if company_id:
            self.current_employees = EmployeeRepository.read_by_company(company_id)
            self.generate_preview()
    
    def add_company(self):
        """Abre diálogo para agregar empresa"""
        dialog = AddCompanyDialog(self)
        if dialog.exec() == 1:  # Aceptado
            try:
                if dialog.result is None:
                    QMessageBox.warning(self, "Error", "No se completó el diálogo correctamente")
                    return
                company_id = CompanyRepository.create(dialog.result)
                self.load_companies()
                QMessageBox.information(self, "Éxito", f"Empresa agregada (ID: {company_id})")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar empresa: {str(e)}")
    
    def edit_company(self):
        """Edita la empresa seleccionada"""
        if not self.current_company:
            QMessageBox.warning(self, "Error", "Selecciona una empresa primero")
            return
        
        dialog = EditCompanyDialog(self.current_company, self)
        if dialog.exec() == 1:
            try:
                if dialog.result is None:
                    QMessageBox.warning(self, "Error", "No se completó el diálogo correctamente")
                    return
                dialog.result.id = self.current_company.id
                CompanyRepository.update(dialog.result)
                self.load_companies()
                QMessageBox.information(self, "Éxito", "Empresa actualizada")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al editar empresa: {str(e)}")
    
    def delete_company(self):
        """Elimina la empresa seleccionada"""
        if not self.current_company:
            QMessageBox.warning(self, "Error", "Selecciona una empresa primero")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Eliminar empresa '{self.current_company.name}' y todos sus empleados?"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.current_company.id is not None:
                    CompanyRepository.delete(self.current_company.id)
                self.load_companies()
                QMessageBox.information(self, "Éxito", "Empresa eliminada")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar empresa: {str(e)}")
    
    # ========== MÉTODOS DE EMPLEADOS ==========
    
    def load_employees_for_company(self, company_id: int):
        """Carga empleados de una empresa específica"""
        employees = EmployeeRepository.read_by_company(company_id)
        self.employees_table.setRowCount(len(employees))
        
        for row, employee in enumerate(employees):
            self.employees_table.setItem(row, 0, QTableWidgetItem(str(employee.id)))
            self.employees_table.setItem(row, 1, QTableWidgetItem(employee.first_name))
            self.employees_table.setItem(row, 2, QTableWidgetItem(employee.last_name))
            self.employees_table.setItem(row, 3, QTableWidgetItem(employee.email))
            self.employees_table.setItem(row, 4, QTableWidgetItem(employee.phone or ""))
            self.employees_table.setItem(row, 5, QTableWidgetItem(employee.position or ""))
    
    def add_employee(self):
        """Abre diálogo para agregar empleado"""
        company_id = self.company_combo.currentData()
        if not company_id:
            QMessageBox.warning(self, "Error", "Selecciona una empresa primero")
            return
        
        company = CompanyRepository.read(company_id)
        if company is None:
            QMessageBox.warning(self, "Error", "No se pudo cargar la empresa")
            return
        
        dialog = AddEmployeeDialog(company.name, self)
        
        if dialog.exec() == 1:
            try:
                if dialog.result is None:
                    QMessageBox.warning(self, "Error", "No se completó el diálogo correctamente")
                    return
                dialog.result.company_id = company_id
                employee_id = EmployeeRepository.create(dialog.result)
                self.load_employees_for_company(company_id)
                QMessageBox.information(self, "Éxito", f"Empleado agregado (ID: {employee_id})")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar empleado: {str(e)}")
    
    def edit_employee(self):
        """Edita el empleado seleccionado"""
        row = self.employees_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Selecciona un empleado primero")
            return
        
        item = self.employees_table.item(row, 0)
        if item is None:
            QMessageBox.warning(self, "Error", "No se pudo leer ID del empleado")
            return
        
        employee_id = int(item.text())
        employee = EmployeeRepository.read(employee_id)
        if employee is None:
            QMessageBox.warning(self, "Error", "No se pudo cargar el empleado")
            return
        
        company = CompanyRepository.read(employee.company_id)
        if company is None:
            QMessageBox.warning(self, "Error", "No se pudo cargar la empresa")
            return
        
        dialog = EditEmployeeDialog(employee, company.name, self)
        
        if dialog.exec() == 1:
            try:
                if dialog.result is None:
                    QMessageBox.warning(self, "Error", "No se completó el diálogo correctamente")
                    return
                EmployeeRepository.update(dialog.result)
                self.load_employees_for_company(employee.company_id)
                QMessageBox.information(self, "Éxito", "Empleado actualizado")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al editar empleado: {str(e)}")
    
    def delete_employee(self):
        """Elimina el empleado seleccionado"""
        row = self.employees_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Error", "Selecciona un empleado primero")
            return
        
        item = self.employees_table.item(row, 0)
        if item is None:
            QMessageBox.warning(self, "Error", "No se pudo leer ID del empleado")
            return
        
        employee_id = int(item.text())
        employee = EmployeeRepository.read(employee_id)
        if employee is None:
            QMessageBox.warning(self, "Error", "No se pudo cargar el empleado")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Eliminar empleado '{employee.full_name}'?"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                EmployeeRepository.delete(employee_id)
                self.load_employees_for_company(employee.company_id)
                QMessageBox.information(self, "Éxito", "Empleado eliminado")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar empleado: {str(e)}")
    
    # ========== MÉTODOS DE MENSAJES ==========
    
    def generate_preview(self):
        """Genera preview de mensajes para todos los empleados"""
        if not self.current_employees:
            self.preview_area.setText("No hay empleados para esta empresa")
            return
        
        template = self.message_template.toPlainText()
        if not template.strip():
            self.preview_area.setText("Escribe un template primero")
            return
        
        company_id = self.msg_company_combo.currentData()
        company = CompanyRepository.read(company_id)
        if company is None:
            self.preview_area.setText("No se pudo cargar la empresa")
            return
        
        messages = MessageService.render_for_all_employees(
            template, self.current_employees, company.name
        )
        
        preview = "VISTA PREVIA DE MENSAJES\n"
        preview += "=" * 50 + "\n\n"
        
        for email, message in messages.items():
            preview += f"📧 {email}\n"
            preview += "-" * 50 + "\n"
            preview += message + "\n\n"
        
        self.preview_area.setText(preview)
    
    def copy_recipients(self):
        """Copia todos los emails como destinatarios"""
        if not self.current_employees:
            QMessageBox.warning(self, "Error", "No hay empleados")
            return
        
        emails = ";".join([emp.email for emp in self.current_employees])
        
        # Usar el portapapeles de PyQt6
        from PyQt6.QtGui import QClipboard
        from PyQt6.QtWidgets import QApplication
        
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(emails)
            QMessageBox.information(
                self, "✅ Éxito",
                f"Emails copiados al portapapeles:\n{emails}"
            )
        else:
            QMessageBox.warning(self, "Error", "No se pudo acceder al portapapeles")
    
    def configure_email(self):
        """Abre diálogo para configurar email"""
        dialog = EmailConfigDialog(self)
        if dialog.exec() == 1:
            try:
                if dialog.result is None:
                    QMessageBox.warning(self, "Error", "No se completó el diálogo correctamente")
                    return
                # Crear servicio con la configuración
                self.email_service = EmailService(dialog.result)
                
                # Probar conexión
                success, message = self.email_service.connect()
                if success:
                    QMessageBox.information(self, "✅ Éxito", f"{message}\nEmail configurado correctamente")
                else:
                    self.email_service = None
                    QMessageBox.critical(self, "Error", message)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {str(e)}")
    
    def send_emails(self):
        """Envía emails a todos los empleados"""
        if not self.current_employees:
            QMessageBox.warning(self, "Error", "No hay empleados en esta empresa")
            return
        
        if not self.email_service:
            QMessageBox.warning(
                self, "Error",
                "Email no configurado.\nClick en '⚙️ Configurar Email' primero"
            )
            return
        
        # Obtener template
        template = self.message_template.toPlainText()
        if not template.strip():
            QMessageBox.warning(self, "Error", "Escribe un template primero")
            return
        
        # Generar asunto simple
        subject = "Mensaje de " + (self.current_company.name if self.current_company else "Empresa")
        
        # Generar mensajes
        if self.current_company is None:
            QMessageBox.warning(self, "Error", "No se pudo cargar la empresa")
            return
        
        messages = MessageService.render_for_all_employees(
            template,
            self.current_employees,
            self.current_company.name
        )
        
        # Obtener emails
        emails = list(messages.keys())
        
        # Confirmar envío
        respuesta = QMessageBox.question(
            self, "Confirmar envío",
            f"¿Enviar emails a {len(emails)} empleados?\n\n{', '.join(emails)}"
        )
        
        if respuesta != QMessageBox.StandardButton.Yes:
            return
        
        # Enviar
        try:
            success, message, sent_count = self.email_service.send_emails(
                emails,
                subject,
                messages,
                self.current_company.name
            )
            
            if success:
                QMessageBox.information(self, "✅ Éxito", message)
            else:
                QMessageBox.warning(self, "Error", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al enviar: {str(e)}")
    
    def __del__(self):
        """Limpia recursos"""
        if self.email_service:
            self.email_service.disconnect()
    
    def show_variables_help(self):
        """Muestra ayuda sobre variables disponibles"""
        help_text = MessageService.get_variables_help()
        QMessageBox.information(self, "Variables Disponibles", help_text)
