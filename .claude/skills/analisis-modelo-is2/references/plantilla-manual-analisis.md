# Plantilla «Manual de Análisis» (Ing. del Software 2)

Orden de secciones de la plantilla y qué completar en cada una. Regla general: borrar todo el texto resaltado antes de entregar. El orden de los diagramas lo fija `modelo/gen/plan.py`; `gen/gen_docx.py` arma el documento siguiéndolo.

| Sección | Qué va | Cómo se obtiene |
|---|---|---|
| Portada | Grupo Nº, alumnos (Apellido, Nombre) | El estudiante lo completa a mano |
| Nombre del Proyecto | Nombre | `meta.sistema` de `modelo.yaml` |
| Objetivo del Proyecto | Objetivo general, borrador de 2–3 oraciones con el alcance | Redactar a partir del TPF; marcar como borrador |
| Modelo de Requerimientos | Enlace al documento de requerimientos | Pedirlo al estudiante |
| Actores | Tabla Actor / Descripción | `actores` de `modelo.yaml` |
| Lista de Requerimientos | Tabla Id / Requerimiento; cambios en colores («Se agregaron xx, se eliminaron xx y se redefinieron xx») | `requisitos`; los conteos de cambios los aporta el estudiante |
| Diagrama de Casos de Uso (Alto Nivel) | Por procesos o por actores | `casos-de-uso-alto-nivel.png`, por procesos: un caso de alto nivel por subsistema, unido a los actores de sus casos |
| Diagrama de Generalización de Actores | Jerarquía de actores | `generalizacion-actores.png`, desde `generalizacion_actores` (padres abstractos, D-20) |
| Diagramas de Casos de Uso | Refinados, con relaciones, validados con actores | `casos-de-uso-A.png` y `casos-de-uso-B.png` (uno por subsistema); la validación con actores la hace el estudiante |
| Caso de Uso (uno por cada CU) | Descripción, Modelo Estructural, Modelo Dinámico, Otros diagramas | Ver abajo |
| Matriz de Requerimientos vs Casos de Uso | Cuadrícula completa | Matriz del documento y de `modelo-de-analisis.md`, generada desde `requisitos[].casos_uso` |

Verificación que pide la plantilla: todo CU tiene al menos un requerimiento y todo requerimiento al menos un CU.

## Sección de cada CU

Las cuatro subsecciones de la plantilla, para los 16 casos de uso:

| Subsección | Qué pide la plantilla | Qué se genera |
|---|---|---|
| Descripción | Ficha: nombre, versión, creado y modificado por, descripción, actores, pre y poscondiciones, flujo normal, flujo alternativo (sección aparte de las excepciones), excepciones, requerimientos | Contexto y contenedores C4 como introducción (`c4/C4-CUxx-contexto.png`, `c4/C4-CUxx-contenedores.png`) y la ficha desde `casos_uso[]` |
| Modelo Estructural | Diagrama de clases que participan para resolver el caso de uso | `CU-xx-clases.png`, desde `clases_cu` |
| Modelo Dinámico | Diagrama de interacción (secuencia o colaboración) de objetos de las clases anteriores | `CU-xx-secuencia.png` desde `secuencias`, y la vista dinámica `c4/C4-CUxx.png` |
| Otros diagramas | Estados, actividades, etc., necesarios para explicar el caso, evitando redundancias | `CU-xx-actividades.png` si el flujo se ramifica; `estado-<Entidad>.png` en el caso que dispara más transiciones de esa entidad, y una referencia a esa figura en los demás |

Lo que el material no sustente se deja marcado como pendiente en lugar de inventarlo. Un caso no detallado conserva sus cuatro subsecciones, con la ficha base del catálogo y los modelos marcados como pendientes.
