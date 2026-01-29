from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, Proyecto, Tarea, SubTarea
from .serializers import (
    ClienteSerializer,
    ProyectoSerializer,
    TareaSerializer,
    SubTareaSerializer
)
from .permissions import EsAdmin, SoloLecturaCliente


class ClienteViewSet(ModelViewSet):
    """
    CRUD de clientes.
    - Admin: CRUD completo
    - Cliente: Solo lectura
    Eliminación lógica usando el campo 'activo'.
    """
    queryset = Cliente.objects.filter(activo=True)
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, EsAdmin | SoloLecturaCliente]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre']

    def perform_destroy(self, instance):
        """Eliminación lógica: marcar como inactivo en lugar de eliminar"""
        instance.activo = False
        instance.save()


class ProyectoViewSet(ModelViewSet):
    """
    Proyectos asociados a clientes.
    - Admin: Ve y modifica todos los proyectos
    - Cliente: Solo lectura de sus propios proyectos
    """
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated, EsAdmin | SoloLecturaCliente]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['cliente', 'estado']
    search_fields = ['nombre']
    ordering_fields = ['fecha_inicio', 'estado']

    def get_queryset(self):
        """Filtrar proyectos según el rol del usuario"""
        user = self.request.user
        if user.is_staff:
            return Proyecto.objects.all()
        # Los clientes solo ven sus propios proyectos
        return Proyecto.objects.filter(cliente__email=user.email)


class TareaViewSet(ModelViewSet):
    """
    CRUD de tareas.
    - Admin: CRUD completo sobre todas las tareas
    - Cliente: Solo lectura de tareas de sus proyectos
    """
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated, EsAdmin | SoloLecturaCliente]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['proyecto', 'estado']
    search_fields = ['titulo']
    ordering_fields = ['fecha_creacion', 'estado']

    def get_queryset(self):
        """Filtrar tareas según el rol del usuario"""
        user = self.request.user
        if user.is_staff:
            return Tarea.objects.all()
        # Los clientes solo ven tareas de sus propios proyectos
        return Tarea.objects.filter(proyecto__cliente__email=user.email)

    def perform_create(self, serializer):
        """Al crear una tarea, actualizar el progreso del proyecto"""
        tarea = serializer.save()
        self._actualizar_progreso_proyecto(tarea.proyecto)

    def perform_update(self, serializer):
        """Al actualizar una tarea, actualizar el progreso del proyecto"""
        tarea = serializer.save()
        self._actualizar_progreso_proyecto(tarea.proyecto)

    def perform_destroy(self, instance):
        """Al eliminar una tarea, actualizar el progreso del proyecto"""
        proyecto = instance.proyecto
        instance.delete()
        self._actualizar_progreso_proyecto(proyecto)

    def _actualizar_progreso_proyecto(self, proyecto):
        """Calcular y actualizar el progreso del proyecto basado en sus tareas"""
        tareas = proyecto.tareas.all()
        if tareas.exists():
            progreso_promedio = sum(t.progreso for t in tareas) / tareas.count()
            proyecto.progreso = int(progreso_promedio)
        else:
            proyecto.progreso = 0
        proyecto.save()


class SubTareaViewSet(ModelViewSet):
    """
    CRUD de subtareas.
    - Admin: CRUD completo sobre todas las subtareas
    - Cliente: Solo lectura de subtareas de sus proyectos
    """
    serializer_class = SubTareaSerializer
    permission_classes = [IsAuthenticated, EsAdmin | SoloLecturaCliente]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['tarea', 'completada']
    search_fields = ['titulo']
    ordering_fields = ['fecha_creacion', 'completada']

    def get_queryset(self):
        """Filtrar subtareas según el rol del usuario"""
        user = self.request.user
        if user.is_staff:
            return SubTarea.objects.all()
        # Los clientes solo ven subtareas de tareas de sus propios proyectos
        return SubTarea.objects.filter(tarea__proyecto__cliente__email=user.email)