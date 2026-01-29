from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Cliente, Proyecto
from .serializers import ClienteSerializer, ProyectoSerializer  


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.filter(activo=True)
    serializer_class = ClienteSerializer


    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()

class ProyectoViewSet(ModelViewSet):
    serializer_class = ProyectoSerializer
    filterset_fields = ['cliente', 'estado']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Proyecto.objects.all()
        return Proyecto.objects.filter(cliente__email=user.email)