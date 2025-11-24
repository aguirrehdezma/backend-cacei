from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class CustomUser(AbstractUser):
    """
    Usuario personalizado con tres roles:
    - Admin: Acceso completo a todo el sistema
    - Coordinador: Puede gestionar profesores, cursos, evaluaciones
    - Docente: Solo puede ver/editar su propia información como profesor
    """
    ADMIN = 'admin'
    COORDINADOR = 'coordinador'
    DOCENTE = 'docente'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (COORDINADOR, 'Coordinador'),
        (DOCENTE, 'Docente'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default=DOCENTE,
        help_text='Rol del usuario en el sistema'
    )
    
    # Overridear groups y user_permissions para evitar conflictos con AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_coordinador(self):
        return self.role == self.COORDINADOR
    
    @property
    def is_docente(self):
        return self.role == self.DOCENTE
    
    @property
    def tiene_profesor_asociado(self):
        return hasattr(self, 'profesor_profile')
    
    def clean(self):
        super().clean()
        # Si es docente, debe tener email
        if self.role == self.DOCENTE and not self.email:
            raise ValidationError('Los docentes deben tener un email registrado.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
