from rest_framework import serializers

from usuarios_y_acceso.models import CustomUser
from core.models import Profesor

class UserSerializer(serializers.ModelSerializer):
    # Serializer para mostrar información del usuario
    profesor_id = serializers.SerializerMethodField()
    profesor_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role', 
            'is_active', 'profesor_id', 'profesor_nombre', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'profesor_id', 'profesor_nombre']
    
    def get_profesor_id(self, obj):
        # Retorna el ID del profesor si existe
        if obj.is_docente and obj.tiene_profesor_asociado:
            return obj.profesor_profile.id
        return None
    
    def get_profesor_nombre(self, obj):
        # Retorna el nombre completo del profesor si existe
        if obj.is_docente and obj.tiene_profesor_asociado:
            return obj.profesor_profile.nombre_completo
        return None

class UserRegisterSerializer(serializers.ModelSerializer):
    # Serializer para registro de nuevos usuarios
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    profesor_numero_empleado = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text='Número de empleado del profesor (solo para docentes)'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password', 'password_confirm', 'email', 'role', 
            'first_name', 'last_name', 'profesor_numero_empleado'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, data):
        # Validaciones personalizadas
        # Verificar que las contraseñas coincidan
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        
        # Si es docente, debe proporcionar número de empleado
        if data.get('role') == CustomUser.DOCENTE and not data.get('profesor_numero_empleado'):
            raise serializers.ValidationError({
                "profesor_numero_empleado": "Los docentes deben proporcionar su número de empleado."
            })
        
        # Verificar que el profesor existe si se proporciona número de empleado
        if data.get('profesor_numero_empleado'):
            try:
                profesor = Profesor.objects.get(numero_empleado=data['profesor_numero_empleado'])
                # Verificar que el profesor no tenga ya un usuario asignado
                if profesor.user is not None:
                    raise serializers.ValidationError({
                        "profesor_numero_empleado": "Este profesor ya tiene un usuario asignado."
                    })
                data['profesor'] = profesor
            except Profesor.DoesNotExist:
                raise serializers.ValidationError({
                    "profesor_numero_empleado": "No existe un profesor con este número de empleado."
                })
        
        return data
    
    def create(self, validated_data):
        # Crear usuario y vincular con profesor si aplica
        # Remover campos que no son del modelo User
        validated_data.pop('password_confirm')
        profesor = validated_data.pop('profesor', None)
        validated_data.pop('profesor_numero_empleado', None)
        
        # Crear el usuario
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data.get('role', CustomUser.DOCENTE),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        # Vincular con profesor si es docente
        if profesor:
            profesor.user = user
            profesor.save()
        
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    # Serializer para actualizar datos del usuario
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
    
    def validate_email(self, value):
        """Validar que el email no esté en uso por otro usuario"""
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value

class ChangePasswordSerializer(serializers.Serializer):
    # Serializer para cambio de contraseña
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True, min_length=8)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Las contraseñas no coinciden."})
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
