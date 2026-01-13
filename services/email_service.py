"""
Servicio de envío de emails SMTP
Soporta: Gmail, Outlook, y otros SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class EmailConfig:
    """Configuración de email"""
    provider: str  # "gmail" o "outlook"
    email: str
    password: str
    
    @property
    def smtp_server(self) -> str:
        """Retorna servidor SMTP según proveedor"""
        servers = {
            "gmail": "smtp.gmail.com",
            "outlook": "smtp-mail.outlook.com"
        }
        return servers.get(self.provider, "smtp.gmail.com")
    
    @property
    def smtp_port(self) -> int:
        """Puerto SMTP (TLS)"""
        return 587


class EmailService:
    """Servicio para envío de emails"""
    
    def __init__(self, config: EmailConfig):
        self.config = config
        self.connection = None
    
    def connect(self) -> Tuple[bool, str]:
        """
        Conecta al servidor SMTP
        Returns: (éxito, mensaje)
        """
        try:
            self.connection = smtplib.SMTP(
                self.config.smtp_server,
                self.config.smtp_port,
                timeout=10
            )
            self.connection.starttls()
            self.connection.login(self.config.email, self.config.password)
            return True, "✅ Conectado exitosamente"
        except smtplib.SMTPAuthenticationError:
            return False, "❌ Error de autenticación (credenciales incorrectas)"
        except smtplib.SMTPException as e:
            return False, f"❌ Error SMTP: {str(e)}"
        except Exception as e:
            return False, f"❌ Error de conexión: {str(e)}"
    
    def disconnect(self):
        """Desconecta del servidor"""
        if self.connection:
            try:
                self.connection.quit()
            except:
                pass
            self.connection = None
    
    def send_emails(
        self,
        recipient_emails: List[str],
        subject: str,
        body_template: Dict[str, str],
        company_name: str
    ) -> Tuple[bool, str, int]:
        """
        Envía emails a múltiples destinatarios
        
        Args:
            recipient_emails: Lista de emails
            subject: Asunto del email
            body_template: Dict {email: mensaje personalizado}
            company_name: Nombre de la empresa
        
        Returns:
            (éxito, mensaje, cantidad_enviados)
        """
        if not self.connection:
            return False, "No hay conexión activa. Conectar primero.", 0
        
        if not recipient_emails:
            return False, "No hay destinatarios.", 0
        
        sent_count = 0
        failed_emails = []
        
        try:
            for email_recipient in recipient_emails:
                try:
                    # Crear mensaje
                    msg = MIMEMultipart('alternative')
                    msg['From'] = self.config.email
                    msg['To'] = email_recipient
                    msg['Subject'] = subject
                    msg['CC'] = ";".join([e for e in recipient_emails if e != email_recipient])
                    
                    # Cuerpo del mensaje
                    body = body_template.get(email_recipient, "")
                    
                    # Agregar aclaración de CC
                    footer = f"\n\n---\n📋 Copia enviada a otros empleados de {company_name}:\n"
                    otros_empleados = [e for e in recipient_emails if e != email_recipient]
                    footer += ", ".join(otros_empleados)
                    
                    body_completo = body + footer
                    
                    # Adjuntar contenido
                    msg.attach(MIMEText(body_completo, 'plain', 'utf-8'))
                    
                    # Enviar
                    self.connection.send_message(msg)
                    sent_count += 1
                    
                except Exception as e:
                    failed_emails.append(email_recipient)
            
            # Retornar resultado
            if sent_count == len(recipient_emails):
                mensaje = f"✅ {sent_count} emails enviados exitosamente"
                return True, mensaje, sent_count
            elif sent_count > 0:
                mensaje = f"⚠️ {sent_count}/{len(recipient_emails)} emails enviados. Fallos: {', '.join(failed_emails)}"
                return True, mensaje, sent_count
            else:
                mensaje = f"❌ Error al enviar emails: {', '.join(failed_emails)}"
                return False, mensaje, 0
        
        except Exception as e:
            return False, f"❌ Error durante envío: {str(e)}", sent_count
    
    @staticmethod
    def test_connection(provider: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Prueba la conexión sin guardar
        Returns: (éxito, mensaje)
        """
        config = EmailConfig(provider=provider, email=email, password=password)
        service = EmailService(config)
        success, message = service.connect()
        service.disconnect()
        return success, message
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
