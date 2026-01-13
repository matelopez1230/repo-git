"""
Repositorio de acceso a datos (CRUD)
"""
from typing import List, Optional
from config.database import DatabaseConfig
from models.company import Company
from models.employee import Employee


class CompanyRepository:
    """Operaciones CRUD para empresas"""
    
    @staticmethod
    def create(company: Company) -> int:
        """Crea una nueva empresa, retorna su ID"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO companies (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        """, (company.name, company.email, company.phone, company.address))
        
        company_id: int = cursor.lastrowid or 0
        conn.commit()
        conn.close()
        return company_id
    
    @staticmethod
    def read(company_id: int) -> Optional[Company]:
        """Obtiene una empresa por ID"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Company(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                address=row['address'],
                created_at=row['created_at']
            )
        return None
    
    @staticmethod
    def read_all() -> List[Company]:
        """Obtiene todas las empresas"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM companies ORDER BY name ASC")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Company(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                address=row['address'],
                created_at=row['created_at']
            )
            for row in rows
        ]
    
    @staticmethod
    def update(company: Company) -> bool:
        """Actualiza una empresa existente"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE companies 
            SET name = ?, email = ?, phone = ?, address = ?
            WHERE id = ?
        """, (company.name, company.email, company.phone, company.address, company.id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    @staticmethod
    def delete(company_id: int) -> bool:
        """Elimina una empresa"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM companies WHERE id = ?", (company_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success


class EmployeeRepository:
    """Operaciones CRUD para empleados"""
    
    @staticmethod
    def create(employee: Employee) -> int:
        """Crea un nuevo empleado, retorna su ID"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, phone, company_id, position)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (employee.first_name, employee.last_name, employee.email, 
              employee.phone, employee.company_id, employee.position))
        
        employee_id: int = cursor.lastrowid or 0
        conn.commit()
        conn.close()
        return employee_id
    
    @staticmethod
    def read(employee_id: int) -> Optional[Employee]:
        """Obtiene un empleado por ID"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Employee(
                id=row['id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                company_id=row['company_id'],
                position=row['position'],
                created_at=row['created_at']
            )
        return None
    
    @staticmethod
    def read_all() -> List[Employee]:
        """Obtiene todos los empleados"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employees ORDER BY first_name ASC")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Employee(
                id=row['id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                company_id=row['company_id'],
                position=row['position'],
                created_at=row['created_at']
            )
            for row in rows
        ]
    
    @staticmethod
    def read_by_company(company_id: int) -> List[Employee]:
        """Obtiene todos los empleados de una empresa"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM employees WHERE company_id = ? ORDER BY first_name ASC",
            (company_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Employee(
                id=row['id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                phone=row['phone'],
                company_id=row['company_id'],
                position=row['position'],
                created_at=row['created_at']
            )
            for row in rows
        ]
    
    @staticmethod
    def update(employee: Employee) -> bool:
        """Actualiza un empleado existente"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE employees 
            SET first_name = ?, last_name = ?, email = ?, phone = ?, position = ?
            WHERE id = ?
        """, (employee.first_name, employee.last_name, employee.email, 
              employee.phone, employee.position, employee.id))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    @staticmethod
    def delete(employee_id: int) -> bool:
        """Elimina un empleado"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success


class MessageTemplateRepository:
    """Operaciones CRUD para templates de mensajes"""
    
    @staticmethod
    def create(name: str, template: str) -> int:
        """Crea un nuevo template, retorna su ID"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO message_templates (name, template)
            VALUES (?, ?)
        """, (name, template))
        
        template_id: int = cursor.lastrowid or 0
        conn.commit()
        conn.close()
        return template_id
    
    @staticmethod
    def read_all() -> List[tuple]:
        """Obtiene todos los templates"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM message_templates ORDER BY name ASC")
        rows = cursor.fetchall()
        conn.close()
        
        return [(row['id'], row['name'], row['template']) for row in rows]
    
    @staticmethod
    def delete(template_id: int) -> bool:
        """Elimina un template"""
        conn = DatabaseConfig.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM message_templates WHERE id = ?", (template_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
