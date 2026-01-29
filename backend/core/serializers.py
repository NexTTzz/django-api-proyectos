from rest_framework import serializers
from .models import Tarea, Proyecto, Cliente, SubTarea


def validar_progreso(valor):
    """Validar que el progreso esté entre 0 y 100"""
    if valor < 0 or valor > 100:
        raise serializers.ValidationError("El progreso debe estar entre 0 y 100")
    return valor


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Cliente"""
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['fecha_creacion']


class TareaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Tarea con validación de progreso"""
    progreso = serializers.IntegerField(validators=[validar_progreso])

    class Meta:
        model = Tarea
        fields = '__all__'
        read_only_fields = ['fecha_creacion']

    def validate(self, data):
        """Validaciones adicionales para Tarea"""
        # Validar que el progreso esté entre 0 y 100
        if 'progreso' in data:
            validar_progreso(data['progreso'])
        return data


class ProyectoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Proyecto.
    El progreso se calcula automáticamente en base a las tareas.
    """
    progreso = serializers.IntegerField(read_only=True)

    class Meta:
        model = Proyecto
        fields = '__all__'
        read_only_fields = ['progreso']

    def validate(self, data):
        """Validar fechas del proyecto"""
        if 'fecha_inicio' in data and 'fecha_entrega' in data:
            if data['fecha_inicio'] > data['fecha_entrega']:
                raise serializers.ValidationError(
                    "La fecha de inicio no puede ser posterior a la fecha de entrega"
                )
        return data

    def create(self, validated_data):
        """Al crear un proyecto, inicializar progreso en 0"""
        proyecto = Proyecto.objects.create(**validated_data)
        proyecto.progreso = 0
        proyecto.save()
        return proyecto

    def update(self, instance, validated_data):
        """
        Al actualizar un proyecto, recalcular el progreso automáticamente
        basado en el promedio de progreso de sus tareas
        """
        instance = super().update(instance, validated_data)
        
        # Recalcular progreso basado en tareas
        tareas = instance.tareas.all()
        if tareas.exists():
            progreso_promedio = sum(t.progreso for t in tareas) / tareas.count()
            instance.progreso = int(progreso_promedio)
        else:
            instance.progreso = 0
        
        instance.save()
        return instance


class SubTareaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SubTarea.
    Valida que la subtarea pertenezca a una tarea existente.
    """
    class Meta:
        model = SubTarea
        fields = '__all__'
        read_only_fields = ['fecha_creacion']

    def validate_tarea(self, value):
        """
        Validar que la tarea existe antes de crear/actualizar una subtarea.
        Esto asegura que una SubTarea solo puede asociarse a una tarea válida.
        """
        if not value:
            raise serializers.ValidationError("Debe especificar una tarea válida")
        
        # Verificar que la tarea existe
        if not Tarea.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("La tarea especificada no existe")
        
        return value

    def validate(self, data):
        """
        Validación adicional: una SubTarea solo puede marcarse como completada
        si pertenece a una tarea existente (ya validado en validate_tarea)
        """
        if 'completada' in data and data['completada']:
            # La tarea ya fue validada en validate_tarea
            if 'tarea' not in data and not self.instance:
                raise serializers.ValidationError(
                    "No se puede marcar como completada una subtarea sin tarea asociada"
                )
        
        return data