"""
Servicio para manejo de mensajes con variables dinámicas
"""
from typing import Dict, List
from models.employee import Employee


class MessageService:
    """Servicio para procesar y renderizar mensajes con variables"""
    
    # Variables disponibles en templates
    AVAILABLE_VARIABLES = {
        '{nombre}': 'Nombre del empleado',
        '{apellido}': 'Apellido del empleado',
        '{nombre_completo}': 'Nombre completo',
        '{email}': 'Email del empleado',
        '{telefono}': 'Teléfono del empleado',
        '{posicion}': 'Posición/Cargo del empleado',
        '{empresa}': 'Nombre de la empresa'
    }
    
    @staticmethod
    def render_message(template: str, employee: Employee, company_name: str) -> str:
        """
        Renderiza un template de mensaje con datos del empleado
        
        Args:
            template: Texto del template con variables
            employee: Objeto Employee
            company_name: Nombre de la empresa
        
        Returns:
            Mensaje completo con variables reemplazadas
        """
        message = template
        replacements = {
            '{nombre}': employee.first_name,
            '{apellido}': employee.last_name,
            '{nombre_completo}': employee.full_name,
            '{email}': employee.email,
            '{telefono}': employee.phone or '',
            '{posicion}': employee.position or '',
            '{empresa}': company_name
        }
        
        for variable, value in replacements.items():
            message = message.replace(variable, str(value))
        
        return message
    
    @staticmethod
    def render_for_all_employees(
        template: str, 
        employees: List[Employee], 
        company_name: str
    ) -> Dict[str, str]:
        """
        Renderiza un mensaje para múltiples empleados
        
        Args:
            template: Template del mensaje
            employees: Lista de empleados
            company_name: Nombre de la empresa
        
        Returns:
            Diccionario {email: mensaje_renderizado}
        """
        result = {}
        for employee in employees:
            rendered = MessageService.render_message(template, employee, company_name)
            result[employee.email] = rendered
        return result
    
    @staticmethod
    def get_variables_help() -> str:
        """Retorna ayuda sobre las variables disponibles"""
        help_text = "Variables disponibles en templates:\n\n"
        for var, description in MessageService.AVAILABLE_VARIABLES.items():
            help_text += f"• {var:<20} - {description}\n"
        return help_text
    
    @staticmethod
    def validate_template(template: str) -> tuple[bool, str]:
        """
        Valida que un template tenga variables válidas
        
        Returns:
            (es_válido, mensaje_error)
        """
        if not template.strip():
            return False, "El template no puede estar vacío"
        
        # Verificar que no hay variables inválidas (opcional)
        return True, ""
