Trabajo universitario de Programación 1.

Este proyecto es una aplicación de consola desarrollada en **Python** que simula un sistema integral de gestión académica. Permite administrar alumnos, profesores, cursos y el control de asistencias, utilizando persistencia de datos en múltiples formatos.


 Características Principales

El sistema maneja tres perfiles de usuario con permisos diferenciados:

### 👨‍🏫 Perfil Profesor
* **Pasar Lista:** Registro de asistencia (Presente, Ausente, Tarde) validando fechas y cupos.
* **Gestión:** Visualización de clases asignadas y listado de alumnos.
* **Modificación:** Capacidad de corregir estados de asistencia pasados.

### 👨‍🎓 Perfil Estudiante
* **Autogestión:** Consulta de asistencias en tiempo real por materia o visión general.
* **Reportes:** Visualización de porcentaje de faltas en formato tabular.

### 🛠 Perfil Administrador
* **ABM de Alumnos:** Alta, Baja y Modificación de estudiantes.
* **Inscripciones:** Asignación de alumnos a materias validando **conflictos de horarios** y cupos.
* **Mantenimiento del Sistema:** Funcionalidad de "Reinicio del Sistema" que procesa los logs de cambios y actualiza los archivos maestros.

## 💻 Aspectos Técnicos Destacados

Este proyecto va más allá de un simple script, implementando lógica de negocio compleja:

* **Persistencia de Datos Híbrida:** Manejo simultáneo de archivos **CSV** (para listados), **JSON** (para configuraciones y diccionarios complejos) y **TXT** (para registros planos).
* **Sistema de Logs y Batch Processing:** Los cambios no se escriben directamente en los archivos maestros para evitar corrupciones. Se generan archivos de "cambios" (logs) que luego se procesan en lote mediante la función `comparar_archivos()` y `aplicar_cambios_*`.
* **Algoritmos de Búsqueda y Validación:** Validaciones robustas de tipos de datos, rangos numéricos y existencia de registros.
* **Recursividad:** Implementada en la navegación de menús y listado de materias (`mostrar_nombres_materias`).

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Librerías:** `json`, `os` (Librerías estándar, sin dependencias externas).

## 📋 Estructura de Archivos

El sistema depende de la siguiente estructura de datos para funcionar:

* `Segunda_entrega_1.py`: Código fuente principal.
* `estudiantes.csv`: Base de datos de alumnos.
* `profesores.csv` / `admin.json`: Credenciales de acceso.
* `ids_clases.json`: Metadatos de las materias (Horarios, Nombres).
* `asistencia_alumnos.txt`: Historial de asistencias (JSON Lines).
