from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProyectoViewSet, TareaViewSet, SubTareaViewSet

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('proyectos', ProyectoViewSet)
router.register('tareas', TareaViewSet)
router.register('subtareas', SubTareaViewSet)

urlpatterns = router.urls
