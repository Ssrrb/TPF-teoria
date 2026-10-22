# Plantilla «Manual de Análisis» (Ing. del Software 2)

Orden de secciones de la plantilla y qué completar en cada una. Regla general: borrar todo el texto resaltado antes de entregar.

| Sección | Qué va | Cómo se obtiene |
|---|---|---|
| Portada | Grupo Nº, alumnos (Apellido, Nombre) | El estudiante lo completa a mano |
| Nombre del Proyecto | Nombre | `meta.sistema` de `modelo.yaml` |
| Objetivo del Proyecto | Objetivo general, borrador de 2–3 oraciones con el alcance | Redactar a partir del TPF; marcar como borrador |
| Modelo de Requerimientos | Enlace al documento de requerimientos | Pedirlo al estudiante |
| Actores | Tabla Actor / Descripción | `actores` de `modelo.yaml` |
| Lista de Requerimientos | Tabla Id / Requerimiento; cambios en colores («Se agregaron xx, se eliminaron xx y se redefinieron xx») | `requisitos`; los conteos de cambios los aporta el estudiante |
| Diagrama de Casos de Uso (Alto Nivel) | Por procesos o por actores | Pendiente: no hay generador todavía (agregarlo a `gen/gen_puml.py` desde `subsistemas`) |
| Diagrama de Generalización de Actores | Jerarquía de actores | Pendiente: el YAML no declara jerarquía de actores; agregarla y el generador solo si el docente la espera |
| Diagramas de Casos de Uso | Refinados, con relaciones, validados con actores | `modelo/out/01-…` y `02-…` (uno por subsistema); la validación con actores la hace el estudiante |
| Caso de Uso (uno por cada CU) | Descripción, flujo normal, **flujo alternativo** (sección aparte de las excepciones), modelo estructural, modelo dinámico | Introducción C4, ficha y modelos del CU (ver abajo) |
| Matriz de Requerimientos vs Casos de Uso | Cuadrícula completa | Matriz del documento y de `modelo-de-analisis.md`, generada desde `requisitos[].casos_uso` |

Verificación que pide la plantilla: todo CU tiene al menos un requerimiento y todo requerimiento al menos un CU.

## Ficha de cada CU

Cada CU abre con su introducción C4 (contexto para todos; contenedores para los detallados), seguida del modelo estructural y dinámico cuando el CU está detallado. Luego, para cada CU dar: ID y nombre, subsistema, actores, requerimientos, precondición, postcondición y notas. Dejar claramente marcado lo que falta redactar (flujo normal, flujo alternativo, excepciones, modelo estructural, modelo dinámico) en lugar de inventarlo; esos textos dependen del enunciado del TPF.
