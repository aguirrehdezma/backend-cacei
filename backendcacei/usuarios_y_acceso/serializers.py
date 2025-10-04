from rest_framework import serializers
from usuarios_y_acceso.models import Usuarios
from usuarios_y_acceso.models import UsuariosProgramas

# Create your serializers here.

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = [
            'usuario_id',
            'username',
            'password_hash',
            'email',
            'nombre_completo',
            'rol',
            'estatus',
            'last_login',
            'created_at',
            'updated_at'
        ]


class UsuariosProgamasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuariosProgramas
        fields = [
            'usuario_programa_id',
            'usuario_id',
            'programa_id',
            'created_at',
            'updated_at'
        ]

