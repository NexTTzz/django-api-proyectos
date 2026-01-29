from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProyectoViewSet, TareaViewSet, SubTareaViewSet

router = DefaultRouter()
router.register('clientes', ClienteViewSet, basename='cliente')
router.register('proyectos', ProyectoViewSet, basename='proyecto') 
router.register('tareas', TareaViewSet, basename='tarea')
router.register('subtareas', SubTareaViewSet, basename='subtarea')

urlpatterns = router.urls