from rest_framework import serializers
from .models import Tarea, Proyecto, Cliente

def validar_progreso(valor):
    if valor < 0 or valor > 100:
        raise serializers.ValidationError("Progreso debe estar entre 0 y 100")
    return valor


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class TareaSerializer(serializers.ModelSerializer):
    progreso = serializers.IntegerField(validators=[validar_progreso])

    class Meta:
        model = Tarea
        fields = '__all__'

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        tareas = instance.tareas.all()
        if tareas.exists():
            instance.progreso = int(sum(t.progreso for t in tareas) / tareas.count())
            instance.save()
        return instance