"""
Modelo de datos para Empresa
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Company:
    """Representa una empresa en el sistema"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def __str__(self) -> str:
        return self.name
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at
        }
