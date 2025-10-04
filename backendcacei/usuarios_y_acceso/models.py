from django.db import models

# Create your models here.

class Usuarios():
    ADMIN = 1
    PROFESOR = 2
    COORDINADOR = 3
    INVITADO = 4

    ROL_CHOICES = [
        (ADMIN, 'Administrador'),
        (PROFESOR, 'Profesor'),
        (COORDINADOR, 'Coordinador'),
        (INVITADO, 'Invitado'),
    ]

    ACTIVO = 1
    INACTIVO = 2
    BLOQUEADO = 3

    ESTATUS_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (BLOQUEADO, 'Bloqueado'),
    ]

    usuario_id = models.IntegerField()
    username = models.TextField()
    password_hash = models.TextField()
    email = models.TextField()
    nombre_completo = models.TextField()
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default=INVITADO)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ACTIVO)
    last_login = models.DateField()
    created_at = models.DateField()
    updated_at = models.DateField()
    
    def __str__(self):
        return f"Usuarix {self.usuario_id} - {self.username} - {self.rol} - {self.estatus}"


class UsuariosProgramas():
    usuario_programa_id = models.IntegerField()
    usuario_id = models.IntegerField()
    programa_id = models.IntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()
    
    def __str__(self):
        return f"Usuarix {self.usuario_programa_id} - {self.usuario_id}"

# Create your models here.
