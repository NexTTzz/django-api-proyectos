from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, Proyecto, Tarea
from .serializers import (
    ClienteSerializer,
    ProyectoSerializer,
    TareaSerializer
)


class ClienteViewSet(ModelViewSet):
    """
    CRUD de clientes.
    Eliminación lógica usando el campo 'activo'.
    """
    queryset = Cliente.objects.filter(activo=True)
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre']

    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()


class ProyectoViewSet(ModelViewSet):
    """
    Proyectos asociados a clientes.
    - Admin ve todos
    - Usuario normal ve solo sus proyectos
    """
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['cliente', 'estado']
    search_fields = ['nombre']
    ordering_fields = ['fecha_inicio', 'estado']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Proyecto.objects.all()
        return Proyecto.objects.filter(cliente__email=user.email)


class TareaViewSet(ModelViewSet):
    """
    CRUD de tareas
    """
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['proyecto', 'estado']
    search_fields = ['titulo']
    ordering_fields = ['fecha_creacion', 'estado']
