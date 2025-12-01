# BackendCacei
## Carpeta Cedulas

### models.py
<p> Este es el archivo más importante de la aplicación. Define el modelo principal <code>Cedula</code> y múltiples modelos auxiliares.
La clase <code>Cedula</code> actúa como un gestor de reportes históricos o "snapshots". Su método <code>save()</code> contiene una lógica compleja que, dependiendo del tipo de cédula (ej. <em>CV Sintético</em>, <em>Plan de Mejora</em>, <em>Organización Curricular</em>), recopila datos "vivos" de otras aplicaciones (como <code>core</code>, <code>gestion_academica</code>, etc.) y guarda una copia estática en tablas específicas (como <code>CursoObligatorio</code>, <code>HallazgoCedula</code>). Esto garantiza que el reporte refleje la información tal como existía en el momento de su creación, protegiéndolo de cambios futuros en los datos originales. </p>

```python
from django.db import models
# ... importaciones de otros módulos ...

class Cedula(models.Model):
    # Opciones para los tipos de cédula (CV Sintético, Plan de Mejora, etc.)
    ORGANIZACION_CURRICULAR = 'organizacion_curricular'
    CV_SINTETICO = 'cv_sintetico'
    # ... otras constantes ...
    
    TIPO_CHOICES = [
        (ORGANIZACION_CURRICULAR, 'Organización Curricular'),
        (CV_SINTETICO, 'CV Sintético'),
        # ... otros tipos ...
    ]
    
    # Relaciones con datos principales
    programa = models.ForeignKey('core.ProgramaEducativo', ...)
    periodo = models.ForeignKey('core.Periodo', ...)
    profesor = models.ForeignKey('core.Profesor', ...)
    tipo = models.CharField(choices=TIPO_CHOICES, ...)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Lógica de Snapshot:
        # Si es Organización Curricular, congela cursos obligatorios/optativos.
        if self.tipo == Cedula.ORGANIZACION_CURRICULAR and self.programa:
            # ... lógica para copiar datos de Cursos a CursoObligatorio, etc. ...
            pass
            
        # Si es CV Sintético, congela la info del profesor (formación, logros, etc.).
        if self.tipo == Cedula.CV_SINTETICO and self.profesor:
            # ... lógica para copiar datos del Profesor a tablas _Cedula ...
            pass

        # ... bloques similares para Plan de Mejora, Valoración de Objetivos, etc. ...

# Modelos auxiliares para almacenar la data congelada (Snapshots)
class CursoObligatorio(models.Model):
    # Almacena una copia de los cursos obligatorios vinculados a esta cédula
    pass

class ActualizacionDisciplinarCedula(models.Model):
    # Almacena una copia de las actualizaciones del profesor vinculadas a esta cédula
    pass

# ... resto de modelos auxiliares ...
```

### serializers.py
<p> Define cómo se convierte la información de la base de datos a formato JSON para ser enviada por la API. Contiene un serializador específico para cada tipo de cédula (ej. <code>CedulaCvSinteticoSerializer</code>), asegurando que se envíe la estructura de datos correcta para cada reporte. También incluye serializadores anidados para manejar la información detallada que fue congelada en los modelos auxiliares. </p>

```python
from rest_framework import serializers
from cedulas.models import *

# Serializadores auxiliares para los detalles (ej. Ejes, Hallazgos)
class CursoObligatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoObligatorio
        fields = ["id", "curso_clave", "curso_nombre", "ejes"]

# Serializadores principales por tipo de Cédula
class CedulaOrganizacionCurricularSerializer(serializers.ModelSerializer):
    # Incluye listas de cursos obligatorios, optativos y curriculares
    obligatorios = CursoObligatorioSerializer(many=True, ...)
    pass

class CedulaCvSinteticoSerializer(serializers.ModelSerializer):
    # Incluye toda la info profesional del profesor (formación, premios, etc.)
    pass

class CedulaPlanMejoraSerializer(serializers.ModelSerializer):
    # Incluye hallazgos y acciones de mejora
    pass

# ... resto de serializadores específicos ...
```

### urls.py
<p> Este archivo gestiona el enrutamiento de las direcciones URL para la API de cédulas. Utiliza un <code>SimpleRouter</code> de Django REST Framework para registrar automáticamente el <code>CedulaViewSet</code>.



Esto significa que no es necesario definir manualmente cada ruta (como <em>ver</em>, <em>crear</em> o <em>editar</em>); el router genera dinámicamente los endpoints estándar (por ejemplo, <code>GET /</code> para listar y <code>POST /</code> para crear) y los conecta con la lógica definida en las vistas. Finalmente, la lista <code>urlpatterns</code> expone estas rutas generadas para que sean accesibles desde el proyecto principal. </p>

```python
from rest_framework import routers
from cedulas.views import CedulaViewSet

# Configuración del router para generar rutas automáticas
router = routers.SimpleRouter()
router.register(r'', CedulaViewSet, basename='cedulas')

urlpatterns = router.urls
```

### views.py
<p> Controla la lógica de la API. Define el <code>CedulaViewSet</code>, que gestiona las peticiones HTTP (GET, POST, etc.). Su función principal es determinar dinámicamente qué serializador utilizar basándose en el tipo de cédula solicitada (o creada). Esto permite que un solo punto de acceso (endpoint) pueda devolver estructuras de datos completamente diferentes según el reporte que se necesite. </p>

```python
from rest_framework import viewsets
from .models import Cedula
from .serializers import (
    CedulaOrganizacionCurricularSerializer,
    CedulaCvSinteticoSerializer,
    # ... otras importaciones
)

class CedulaViewSet(viewsets.ModelViewSet):
    queryset = Cedula.objects.all()
    
    def get_serializer_class(self):
        # Determina el serializador basándose en el parámetro 'tipo'
        tipo = self.request.data.get("tipo") or self.request.query_params.get("tipo")
        
        if tipo == Cedula.CV_SINTETICO:
            return CedulaCvSinteticoSerializer
        elif tipo == Cedula.PLAN_MEJORA:
            return CedulaPlanMejoraSerializer
        elif tipo == Cedula.VALORACION_OBJETIVOS:
            return CedulaValoracionObjetivosSerializer
        # ... otros casos ...
            
        # Serializador por defecto
        return CedulaOrganizacionCurricularSerializer
```
## Carpeta Core

### models.py
<p>
Este archivo define la columna vertebral de la base de datos del sistema. Aquí se encuentran los "Datos Maestros" o entidades fundamentales que serán referenciadas por el resto de los módulos (como Cédulas o Gestión Académica). <br><br>
Define estructuras para almacenar información de los <strong>Profesores</strong> (y su vinculación con usuarios del sistema), los <strong>Programas Educativos</strong> (carreras), los <strong>Cursos</strong> (asignaturas), así como la estructura jerárquica institucional (<strong>Institución</strong> y <strong>Organización</strong>) y la gestión temporal mediante <strong>Periodos</strong>.
</p>

```python
from django.db import models
from django.contrib.auth.models import User

class Profesor(models.Model):
    # Vinculación con el sistema de autenticación de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    numero_empleado = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    # ... otros campos demográficos y profesionales ...

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"

class ProgramaEducativo(models.Model):
    # Define las carreras o programas (ej. Ingeniería en Software)
    nombre = models.CharField(max_length=255)
    clave = models.CharField(max_length=50)
    # ...

class Curso(models.Model):
    # Catálogo de asignaturas disponibles
    nombre = models.CharField(max_length=255)
    clave = models.CharField(max_length=50)
    programa = models.ForeignKey(ProgramaEducativo, on_delete=models.CASCADE)
    # ...

class Periodo(models.Model):
    # Define los ciclos escolares (ej. Enero-Junio 2024)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    # ...

# Modelos adicionales: Institucion, Organizacion...
```
### serializers.py
<p> Se encarga de transformar los objetos complejos de la base de datos "Core" (Profesores, Cursos, etc.) en formato JSON para que puedan ser consumidos por el Frontend, y viceversa.

Al ser datos maestros, estos serializadores suelen ser estándar (utilizando <code>ModelSerializer</code>), exponiendo todos o la mayoría de los campos para permitir una gestión completa de los catálogos principales del sistema. </p>

```python
from rest_framework import serializers
from core.models import (
    Profesor, ProgramaEducativo, Curso, 
    Institucion, Organizacion, Periodo
)

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__' # Expone todos los campos del profesor

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaEducativo
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

# Serializadores restantes: Institucion, Organizacion, Periodo...
```

### views.py
<p> Define la lógica de negocio para interactuar con los datos del núcleo del sistema. Utiliza <code>ModelViewSet</code>, lo que proporciona funcionalidad completa CRUD (Crear, Leer, Actualizar, Borrar) de forma predeterminada sin necesidad de escribir código repetitivo.

Cada clase vincula un modelo de la base de datos (QuerySet) con su serializador correspondiente, permitiendo que la API responda a las peticiones del cliente de manera estandarizada y segura. </p>
```python
from rest_framework import viewsets
from core.models import Profesor, ProgramaEducativo, Curso, Institucion, Organizacion, Periodo
from core.serializers import (
    ProfesorSerializer, ProgramaEducativoSerializer, CursoSerializer,
    InstitucionSerializer, OrganizacionSerializer, PeriodoSerializer
)

class ProfesorViewSet(viewsets.ModelViewSet):
    # Permite gestionar el catálogo de profesores
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class ProgramaEducativoViewSet(viewsets.ModelViewSet):
    # Permite gestionar los programas educativos
    queryset = ProgramaEducativo.objects.all()
    serializer_class = ProgramaEducativoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    # Permite gestionar el catálogo de cursos
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Vistas restantes para Institucion, Organizacion y Periodo...
```
## Carpeta Evaluacion_Acreditacion

### models.py
<p>
Este archivo gestiona toda la lógica relacionada con el aseguramiento de la calidad y la mejora continua del programa educativo. A diferencia de otros módulos que solo almacenan datos estáticos, aquí se modelan procesos de auditoría y evaluación. <br><br>
Los modelos clave incluyen <strong>Hallazgo</strong> (para registrar detecciones o áreas de oportunidad) y <strong>AccionMejora</strong> (para dar seguimiento a las soluciones de esos hallazgos). También maneja la medición académica a través de <strong>Indicador</strong> y <strong>EvaluacionIndicador</strong>, permitiendo evaluar si los cursos cumplen con los criterios de desempeño establecidos. Adicionalmente, incluye un modelo de <strong>Auditoria</strong> que registra automáticamente quién hizo qué cambios en el sistema (trazabilidad), y modelos para registrar la participación de los profesores (<strong>AportacionPE</strong> y <strong>GestionAcademica</strong>).
</p>

```python
from django.db import models
# ... importaciones

class Hallazgo(models.Model):
    # Registra oportunidades de mejora detectadas en el programa
    programa = models.ForeignKey('core.ProgramaEducativo', ...)
    descripcion = models.TextField()
    # ... vinculación con objetivos y atributos ...

class AccionMejora(models.Model):
    # Plan de trabajo para solventar un Hallazgo
    hallazgo = models.ForeignKey(Hallazgo, ...)
    estatus = models.CharField(choices=ESTATUS_CHOICES, default='pendiente')
    resultado_esperado = models.TextField()
    # ... metas y responsables ...

class EvaluacionIndicador(models.Model):
    # Medición real de un indicador dentro de un curso específico
    indicador = models.ForeignKey(Indicador, ...)
    curso = models.ForeignKey('core.Curso', ...)
    valoracion = models.CharField(choices=[('si', 'Sí'), ('no', 'No')])
    # ... análisis de resultados ...

class Auditoria(models.Model):
    # Sistema de registro de seguridad (quién modificó qué y cuándo)
    accion = models.CharField(max_length=50)
    tabla_afectada = models.CharField(max_length=50)
```
### serializers.py
<p> Transforma la compleja información de calidad y auditoría en formato JSON.

Dado que estos datos se utilizan para reportes de acreditación, los serializadores aquí son directos y exponen la mayoría de los campos. Por ejemplo, <code>AuditoriaSerializer</code> permite visualizar los cambios históricos de los datos (el "antes" y "después" almacenados en JSON), mientras que <code>EvaluacionIndicadorSerializer</code> estructura los resultados de las evaluaciones para que puedan ser analizados gráficamente o en tablas en el Frontend. </p>

```python
from rest_framework import serializers
from evaluacion_acreditacion.models import (
    AccionMejora, Hallazgo, Auditoria, EvaluacionIndicador, # ...
)

class HallazgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hallazgo
        fields = ['id', 'programa', 'descripcion', 'objetivo', 'atributo_pe', ...]

class AccionMejoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionMejora
        fields = ['id', 'hallazgo', 'descripcion', 'estatus', 'responsable', ...]

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        # Incluye datos_anteriores y datos_nuevos para ver el historial de cambios
        fields = ['id', 'accion', 'tabla_afectada', 'datos_anteriores', 'datos_nuevos', ...]

# Resto de serializadores para Indicador, AportacionPE, etc.
```

### urls.py
<p> Define las rutas para acceder a los recursos de evaluación y calidad. Utiliza <code>SimpleRouter</code> para generar automáticamente los endpoints CRUD.

Aquí se exponen rutas críticas como <code>hallazgos/</code> y <code>acciones_mejora/</code> que permiten gestionar el ciclo de mejora continua, así como <code>auditorias/</code>, que probablemente sea un recurso de solo lectura o acceso restringido para monitorear la integridad del sistema. </p>

```python
from rest_framework import routers
from evaluacion_acreditacion.views import (
    AccionMejoraViewSet, HallazgoViewSet, AuditoriaViewSet, # ...
)

router = routers.SimpleRouter()

# Rutas para el ciclo de calidad
router.register(r'hallazgos', HallazgoViewSet, basename='hallazgo')
router.register(r'acciones_mejora', AccionMejoraViewSet, basename='accion-mejora')

# Rutas para evaluación y seguimiento
router.register(r'indicadores', IndicadorViewSet, basename='indicador')
router.register(r'evaluaciones_indicador', EvaluacionIndicadorViewSet, basename='evaluacion-indicador')

# Rutas de auditoría y gestión
router.register(r'auditorias', AuditoriaViewSet, basename='auditoria')
router.register(r'gestion_academica', GestionAcademicaViewSet, basename='gestion-academica')
# ...

urlpatterns = router.urls
```

### views.py
<p> Implementa la lógica de interacción con la base de datos para los módulos de acreditación.

Cada <code>ModelViewSet</code> aquí habilita las operaciones estándar. Por ejemplo, <code>HallazgoViewSet</code> permite registrar nuevos hallazgos detectados, mientras que <code>AuditoriaViewSet</code> provee acceso a los logs del sistema. Aunque el código es breve gracias a la herencia de clases de Django REST Framework, estas vistas son el motor que permite a los coordinadores de calidad alimentar y consultar el sistema de mejora continua. </p>

```python
from rest_framework import viewsets
from evaluacion_acreditacion.models import AccionMejora, Hallazgo, Auditoria # ...
from evaluacion_acreditacion.serializers import AccionMejoraSerializer, HallazgoSerializer # ...

class HallazgoViewSet(viewsets.ModelViewSet):
    # Gestión de los hallazgos del programa
    queryset = Hallazgo.objects.all()
    serializer_class = HallazgoSerializer

class AccionMejoraViewSet(viewsets.ModelViewSet):
    # Gestión y seguimiento de las acciones correctivas
    queryset = AccionMejora.objects.all()
    serializer_class = AccionMejoraSerializer

class AuditoriaViewSet(viewsets.ModelViewSet):
    # Visualización del registro de auditoría del sistema
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer

# Vistas restantes para Indicadores, Aportaciones, etc.
```

## Carpeta Gestion Academica

### models.py
<p>
Este archivo es el corazón de la estructura curricular y pedagógica del sistema. Modela todos los elementos necesarios para definir un plan de estudios completo y alinearlo con estándares de acreditación (como CACEI). <br><br>
Aquí se definen los <strong>Objetivos Educacionales</strong> y <strong>Atributos de Egreso</strong> (<code>AtributoPE</code>), así como su vinculación con los cursos. También gestiona el detalle fino de cada asignatura: <strong>Unidades Temáticas</strong>, <strong>Bibliografía</strong>, <strong>Horas por Semana</strong>, y las estrategias tanto de enseñanza como de evaluación. Finalmente, cierra el ciclo académico incorporando a los <strong>Alumnos</strong> y sus <strong>Calificaciones</strong>, permitiendo evaluar si se están cumpliendo los objetivos planteados.
</p>

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Estructura Curricular y Acreditación
class ObjetivoEducacional(models.Model):
    # Metas generales del programa educativo
    programa = models.ForeignKey('core.ProgramaEducativo', ...)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(...)

class AtributoPE(models.Model):
    # Atributos de Egreso del Programa (Student Outcomes)
    nombre = models.CharField(max_length=100)
    # ...

class AtributoCACEI(models.Model):
    # Estándares específicos del organismo acreditador CACEI
    wk_referencia = models.CharField(...) 
    # ...

# Detalle de los Cursos (Carta Descriptiva)
class UnidadTematica(models.Model):
    curso = models.ForeignKey('core.Curso', ...)
    numero = models.IntegerField()
    # ...

class Bibliografia(models.Model):
    # Referencias bibliográficas para los cursos
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    # ...

# Gestión de Alumnos y Evaluación
class Alumno(models.Model):
    matricula = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50)
    # ...

class Calificacion(models.Model):
    # Registro del desempeño del alumno
    alumno = models.ForeignKey(Alumno, ...)
    valor = models.PositiveSmallIntegerField(validators=[...])
    # ...
```

### serializers.py
<p> Se encarga de traducir la compleja red de relaciones académicas a formato JSON.

Debido a la gran cantidad de catálogos y definiciones (estrategias, ejes, criterios), este archivo contiene numerosos serializadores. Su función principal es asegurar que, al consultar un curso o un atributo, se obtenga toda la información relacionada de manera estructurada, permitiendo al Frontend desplegar planes de estudio completos o reportes de calificaciones sin complicaciones. </p>
```python
from rest_framework import serializers
from gestion_academica.models import (
    Alumno, AtributoPE, Bibliografia, Calificacion, 
    ObjetivoEducacional, UnidadTematica, # ... y muchos más
)

class ObjetivoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoEducacional
        fields = ['id', 'programa', 'codigo', 'descripcion']

class AtributoPESerializer(serializers.ModelSerializer):
    class Meta:
        model = AtributoPE
        fields = ['id', 'programa', 'codigo', 'nombre', 'descripcion']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['id', 'alumno', 'profesor_curso', 'valor']

# ... resto de serializadores para Unidades, Bibliografía, etc. ...
```

### urls.py

<p> Gestiona el enrutamiento para una de las áreas más extensas del sistema. Utiliza un <code>SimpleRouter</code> para exponer una gran cantidad de endpoints (puntos de acceso).

Aquí se definen las rutas para administrar todo el inventario académico: desde la creación de <strong>Unidades Temáticas</strong> (<code>unidades_tematicas/</code>) y <strong>Bibliografías</strong>, hasta la gestión de <strong>Alumnos</strong> y el registro de <strong>Calificaciones</strong>. Es esencialmente el mapa de acceso a toda la data operativa académica. </p>

```python
from rest_framework import routers
from gestion_academica.views import (
    AlumnoViewSet, CalificacionViewSet, ObjetivoEducacionalViewSet, 
    UnidadTematicaViewSet, # ...
)

router = routers.SimpleRouter()

# Rutas de Estructura Curricular
router.register(r'objetivos_educacionales', ObjetivoEducacionalViewSet, basename='objetivo-educacional')
router.register(r'atributos_pe', AtributoPEViewSet, basename='atributo-pe')

# Rutas de Detalle de Curso
router.register(r'unidades_tematicas', UnidadTematicaViewSet, basename='unidad-tematica')
router.register(r'bibliografia', BibliografiaViewSet, basename='bibliografia')

# Rutas de Operación Académica
router.register(r'alumnos', AlumnoViewSet, basename='alumno')
router.register(r'calificaciones', CalificacionViewSet, basename='calificacion')

# ... registro del resto de rutas ...
urlpatterns = router.urls
```

### views
<p> Provee la lógica para crear, leer, actualizar y eliminar (CRUD) cada uno de los elementos académicos.

Al igual que en otros módulos, se basa en <code>ModelViewSet</code> para estandarizar el comportamiento. Esto permite que los administradores o profesores puedan, por ejemplo, agregar nuevas referencias bibliográficas a un curso, actualizar los objetivos educacionales de un programa, o subir las calificaciones de los alumnos, todo a través de una interfaz de programación consistente. </p>

```python
from rest_framework import viewsets
from gestion_academica.models import Alumno, Calificacion, ObjetivoEducacional, UnidadTematica # ...
from gestion_academica.serializers import AlumnoSerializer, CalificacionSerializer, ObjetivoEducacionalSerializer # ...

class ObjetivoEducacionalViewSet(viewsets.ModelViewSet):
    # Gestión de objetivos del programa
    queryset = ObjetivoEducacional.objects.all()
    serializer_class = ObjetivoEducacionalSerializer

class UnidadTematicaViewSet(viewsets.ModelViewSet):
    # Gestión del contenido de los cursos
    queryset = UnidadTematica.objects.all()
    serializer_class = UnidadTematicaSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    # Administración del padrón de estudiantes
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CalificacionViewSet(viewsets.ModelViewSet):
    # Registro y consulta de calificaciones
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

# ... resto de ViewSets ...
```

## Carpeta Gestion de Profesoras

### models.py
<p>
Este archivo actúa como el repositorio detallado del perfil profesional del docente. Su objetivo es almacenar toda la información requerida para evaluar la competencia del profesor, algo esencial para los procesos de acreditación. <br><br>
[cite_start]Aquí se definen modelos para cada sección de un CV: <strong>Formación Académica</strong> (títulos y grados) [cite: 7][cite_start], <strong>Experiencia Profesional</strong> (trabajos en la industria) [cite: 9][cite_start], y <strong>Experiencia en Diseño</strong>[cite: 10]. [cite_start]También registra la productividad a través de <strong>Producto Académico</strong> (papers, patentes, proyectos) [cite: 14] [cite_start]y el desarrollo continuo mediante <strong>Capacitación Docente</strong> y <strong>Actualización Disciplinar</strong>[cite: 13]. [cite_start]Finalmente, el modelo <strong>ProfesorCurso</strong> sirve como "puente", vinculando al profesor con una materia específica en un periodo determinado y definiendo su rol (Responsable o Instructor)[cite: 6].
</p>

```python
from django.db import models

class ProfesorCurso(models.Model):
    # Vincula al profesor con una asignatura en un periodo específico
    profesor = models.ForeignKey('core.Profesor', on_delete=models.PROTECT)
    curso = models.ForeignKey('core.Curso', on_delete=models.PROTECT)
    tipo = models.CharField(choices=TIPO_CHOICES, default=RESPONSABLE)
    # ...

class FormacionAcademica(models.Model):
    # Registra los grados académicos (Licenciatura, Maestría, Doctorado)
    profesor = models.ForeignKey('core.Profesor', ...)
    institucion = models.ForeignKey('core.Institucion', ...)
    nivel = models.CharField(choices=NIVEL_CHOICES, default=LICENCIATURA)
    cedula_profesional = models.CharField(...)
    # ...

class ExperienciaProfesional(models.Model):
    # Historial laboral fuera de la academia
    puesto = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    actividades = models.TextField(...)
    # ...

class ProductoAcademico(models.Model):
    # Evidencias de investigación y desarrollo
    tipo = models.CharField(choices=TIPO_CHOICES, default=PUBLICACION)
    descripcion = models.TextField()
    # ...
```

### serializers.py
<p> Se encarga de transformar la información de los modelos en formato JSON para que pueda ser consumida por el Frontend.
    
Dado que el perfil del profesor está fragmentado en muchas secciones (una lista de premios, una lista de trabajos, etc.), existe un serializador específico para cada modelo (ej. <code>FormacionAcademicaSerializer</code>, <code>LogroProfesionalSerializer</code>). Estos serializadores protegen la integridad de los datos configurando campos de solo lectura, como el ID, y validando la entrada de datos antes de guardar. </p>

```python
from rest_framework import serializers
from gestion_de_profesores.models import *

class ProfesorCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorCurso
        fields = ['id', 'profesor', 'curso', 'tipo', 'periodo']
        read_only_fields = ['id']

class FormacionAcademicaSerializer(serializers.ModelSerializer):
    # Serializador para los grados académicos
    class Meta:
        model = FormacionAcademica
        fields = ['id', 'profesor', 'institucion', 'nivel', 'cedula_profesional', ...]
        read_only_fields = ['id']

class ProductoAcademicoSerializer(serializers.ModelSerializer):
    # Serializador para publicaciones y proyectos
    class Meta:
        model = ProductoAcademico
        fields = ['id', 'profesor', 'descripcion', 'anio', 'tipo', 'detalles']
        read_only_fields = ['id']

# ... resto de serializadores (Experiencia, Premios, Capacitaciones) ...
```
### urls.py
<p> Define la estructura de navegación de la API para esta carpeta. Utiliza un <code>SimpleRouter</code> para generar automáticamente las rutas de acceso a cada sección del currículum.
Gracias a esta configuración, el sistema expone endpoints claros y organizados, como <code>/formacion_academica/</code> o <code>/experiencia_profesional/</code>. Esto permite que la aplicación cliente (Frontend) pueda consultar o actualizar partes específicas del perfil del docente de manera modular, sin tener que cargar toda la información en una sola petición gigante. </p>

```python
from rest_framework import routers
from gestion_de_profesores.views import *

router = routers.SimpleRouter()

# Rutas para la gestión del CV
router.register(r'formacion_academica', FormacionAcademicaViewSet, basename='formacion-academica')
router.register(r'experiencia_profesional', ExperienciaProfesionalViewSet, basename='experiencia-profesional')
router.register(r'logros_profesionales', LogroProfesionalViewSet, basename='logro-profesional')

# Rutas para asignación y productividad
router.register(r'profesores_cursos', ProfesorCursoViewSet, basename='profesor-curso')
router.register(r'productos_academicos', ProductoAcademicoViewSet, basename='producto-academico')
# ... registro del resto de rutas ...

urlpatterns = router.urls
```

### views.py
<p> Contiene la lógica que conecta la base de datos con las peticiones del usuario. Cada clase aquí hereda de <code>ModelViewSet</code>, lo que proporciona automáticamente las funciones para Crear, Leer, Actualizar y Borrar registros (CRUD)
Por ejemplo, <code>ProfesorCursoViewSet</code> permite asignar una materia a un profesor , mientras que <code>CapacitacionDocenteViewSet</code> permite registrar nuevos cursos o diplomados que el profesor haya tomado. Estas vistas aseguran que la gestión del expediente del profesor sea dinámica y sencilla de mantener. </p>

```python
from rest_framework import viewsets
from gestion_de_profesores.models import *
from gestion_de_profesores.serializers import *

class ProfesorCursoViewSet(viewsets.ModelViewSet):
    # Vista para gestionar la carga académica
    queryset = ProfesorCurso.objects.all()
    serializer_class = ProfesorCursoSerializer

class FormacionAcademicaViewSet(viewsets.ModelViewSet):
    # Vista para gestionar los grados académicos
    queryset = FormacionAcademica.objects.all()
    serializer_class = FormacionAcademicaSerializer

class ExperienciaProfesionalViewSet(viewsets.ModelViewSet):
    # Vista para gestionar la trayectoria laboral
    queryset = ExperienciaProfesional.objects.all()
    serializer_class = ExperienciaProfesionalSerializer

# ... resto de ViewSets para las demás secciones ...
```

## Carpeta Usuarios y Acceso

### models.py
<p>
Este archivo personaliza el sistema de usuarios por defecto de Django. En lugar de usar el modelo de usuario estándar, se define un <code>CustomUser</code> que añade lógica específica para la institución.<br><br>
[cite_start]La característica más importante es la definición de <strong>Roles</strong> (Administrador, Coordinador y Docente)[cite: 7]. Esto permite implementar un control de acceso basado en roles (RBAC). [cite_start]Además, incluye validaciones personalizadas, como asegurar que todos los usuarios con rol de "Docente" tengan obligatoriamente un correo electrónico registrado [cite: 12][cite_start], y propiedades auxiliares (<code>is_admin</code>, <code>is_docente</code>) que facilitan la verificación de permisos en otras partes del código[cite: 11].
</p>

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Definición de roles disponibles en el sistema
    ADMIN = 'admin'
    COORDINADOR = 'coordinador'
    DOCENTE = 'docente'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (COORDINADOR, 'Coordinador'),
        (DOCENTE, 'Docente'),
    ]
    
    # Campo para almacenar el rol, por defecto es Docente
    role = models.CharField(choices=ROLE_CHOICES, default=DOCENTE, ...)
    
    @property
    def is_docente(self):
        return self.role == self.DOCENTE
    
    def clean(self):
        # Validación: Los docentes deben tener email obligatoriamente
        if self.role == self.DOCENTE and not self.email:
            raise ValidationError('Los docentes deben tener un email registrado.')
```

### serializers.py

<p> Gestiona el flujo de datos entre el cliente (Frontend) y el sistema de usuarios. A diferencia de otros módulos, aquí hay varios serializadores para distintas acciones de seguridad.
El <code>UserRegisterSerializer</code> es el más complejo: no solo crea el usuario, sino que valida que las contraseñas coincidan y, crucialmente, <strong>vincula al usuario con un Profesor existente</strong> mediante el número de empleado. Esto conecta la cuenta de acceso con el perfil académico del docente. También existen serializadores para cambiar la contraseña de forma segura (verificando la anterior) y para ver o actualizar el perfil básico. </p>

```python
from rest_framework import serializers
from usuarios_y_acceso.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Serializer para mostrar datos del usuario y su perfil docente vinculado
    profesor_id = serializers.SerializerMethodField()
    # ...

class UserRegisterSerializer(serializers.ModelSerializer):
    # Maneja el registro, validación de contraseñas y vinculación con Profesores
    profesor_numero_empleado = serializers.CharField(required=False, ...)
    
    def validate(self, data):
        # Verifica que el número de empleado exista y no tenga usuario ya asignado
        if data.get('profesor_numero_empleado'):
            # Lógica de validación contra el modelo Profesor...
            pass
        return data

    def create(self, validated_data):
        # Crea el usuario y actualiza el modelo Profesor para vincularlos
        pass

class ChangePasswordSerializer(serializers.Serializer):
    # Valida la contraseña antigua y confirma la nueva
    def validate_old_password(self, value):
        # ...
        pass
```

### urls.py
<p> Organiza las rutas de acceso y seguridad del sistema. Expone endpoints claros para procesos de autenticación y gestión de cuentas.
Incluye rutas para el registro de nuevos usuarios (<code>register/</code>), la obtención de tokens de acceso (login) mediante JWT, y la gestión del propio perfil (<code>profile/</code>, <code>change-password/</code>). También reserva una ruta exclusiva para administradores (<code>users/</code>) que permite listar todos los usuarios del sistema. </p>

```python
from django.urls import path
from usuarios_y_acceso.views import *

urlpatterns = [
    # Rutas de Autenticación (Login/Registro)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    
    # Rutas de Gestión de Perfil Personal
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Rutas Administrativas
    path('users/', UserListView.as_view(), name='user_list'),
]
```

### views

<p> Controla la lógica de las peticiones de usuarios. Aquí se define <strong>quién</strong> puede hacer <strong>qué</strong> mediante las clases de permisos (<code>permission_classes</code>).
Por ejemplo, <code>RegisterView</code> permite la creación de usuarios (puede estar abierta o restringida). <code>UserProfileView</code> permite a un usuario autenticado ver y editar sus <em>propios</em> datos, pero no los de otros. Por último, <code>ChangePasswordView</code> maneja la lógica delicada de actualización de credenciales , y <code>UserListView</code> está protegida estrictamente para que solo los administradores puedan ver el listado completo del personal. </p>

```python
from rest_framework import generics
from usuarios_y_acceso.models import CustomUser
from usuarios_y_acceso.serializers import *

class RegisterView(generics.CreateAPIView):
    # Vista para registrar nuevos usuarios
    permission_classes = (AllowAny,) # O IsAdminUser según política
    serializer_class = UserRegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    # Permite al usuario ver y editar SU propio perfil
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        # Retorna el usuario que hace la petición (request.user)
        return self.request.user

class UserListView(generics.ListAPIView):
    # Vista administrativa para listar usuarios
    permission_classes = (IsAdmin,) # Solo admins
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
```
