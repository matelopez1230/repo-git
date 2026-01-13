"""
Modelo de datos para Empleado
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Employee:
    """Representa un empleado en el sistema"""
    first_name: str
    last_name: str
    email: str
    company_id: int
    phone: Optional[str] = None
    position: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Retorna nombre completo"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self) -> str:
        return self.full_name
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company_id': self.company_id,
            'position': self.position,
            'created_at': self.created_at
        }
