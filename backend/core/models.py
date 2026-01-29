from django.db import models


class Cliente(models.Model):
    """
    Modelo para los clientes que contratan proyectos.
    La eliminación es lógica (campo activo).
    """
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    empresa = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"


class Proyecto(models.Model):
    """
    Modelo para proyectos contratados por clientes.
    El progreso se calcula automáticamente basado en las tareas.
    """
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Desarrollo', 'En Desarrollo'),
        ('En Pruebas', 'En Pruebas'),
        ('Finalizado', 'Finalizado'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    progreso = models.IntegerField(default=0)
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE,
        related_name='proyectos'
    )
    fecha_inicio = models.DateField()
    fecha_entrega = models.DateField()

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"

    def actualizar_progreso(self):
        """
        Calcula y actualiza el progreso del proyecto
        basado en el promedio de progreso de sus tareas.
        """
        tareas = self.tareas.all()
        if tareas.exists():
            progreso_promedio = sum(t.progreso for t in tareas) / tareas.count()
            self.progreso = int(progreso_promedio)
        else:
            self.progreso = 0
        self.save()


class Tarea(models.Model):
    """
    Modelo para tareas asociadas a un proyecto.
    Cada tarea contribuye al progreso general del proyecto.
    """
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Bloqueada', 'Bloqueada'),
        ('Completada', 'Completada'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    progreso = models.IntegerField(default=0)
    proyecto = models.ForeignKey(
        Proyecto, 
        on_delete=models.CASCADE, 
        related_name='tareas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - {self.proyecto.nombre}"


class SubTarea(models.Model):
    """
    Modelo para subtareas asociadas a una tarea.
    Son elementos más pequeños que componen una tarea.
    """
    titulo = models.CharField(max_length=100)
    completada = models.BooleanField(default=False)
    tarea = models.ForeignKey(
        Tarea, 
        on_delete=models.CASCADE,
        related_name='subtareas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SubTarea"
        verbose_name_plural = "SubTareas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - {self.tarea.titulo}"