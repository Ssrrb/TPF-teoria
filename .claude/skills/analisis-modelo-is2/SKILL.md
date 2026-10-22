---
name: analisis-modelo-is2
description: Trabaja el modelo de análisis del TPF de Ingeniería del Software 2 (Obra Studio, plantilla «Manual de Análisis») sobre modelo/modelo.yaml, que es la única fuente de verdad. Edita el YAML, valida, regenera diagramas UML, vistas C4-PlantUML, documento y archivo de apoyo, y genera los diagramas en el orden que exige la plantilla (alto nivel, generalización de actores, casos de uso refinados y, por cada caso de uso, descripción, modelo estructural, modelo dinámico y otros diagramas). Usar siempre que el usuario mencione TPF, Modelo de Análisis, Manual de Análisis, casos de uso, actores, requerimientos (RF/RNF/PR), matriz de requerimientos vs casos de uso, diagramas UML o C4 del proyecto, o pida renombrar una clase, agregar un caso de uso o revisar la coherencia del análisis, aunque no nombre la skill.
---

# Modelo de análisis del TPF (Obra Studio)

**`modelo/modelo.yaml` manda.** Actores, requisitos, casos de uso, entidades, estados, secuencias y decisiones viven ahí. Todo lo demás (diagramas UML, vistas C4, documento, archivo de apoyo) se genera y se sobrescribe en cada build. No se edita ningún archivo generado, y no se crea un segundo modelo paralelo (ni JSON ni otro formato).

Esquema y reglas del YAML: `references/formato-modelo-yaml.md`. Leerlo antes de tocar el modelo.

## Flujo de trabajo

1. **Editar solo `modelo/modelo.yaml`.** Para un renombre, cambiar el `nombre:` de la entidad, componente o puerto; nada más repite el nombre. Para agregar algo, declararlo con `id` y `nombre` y referenciarlo por id.
2. **Validar:** `cd modelo && uv run --quiet --with pyyaml python3 gen/validar.py`. Los errores se corrigen en el YAML. Un id inexistente, un nombre de clase escrito a mano en un texto o un requisito sin caso de uso hacen fallar la validación.
3. **Regenerar:** `./build.sh` ejecuta validación, UML, C4, workspace de Structurizr, archivo de apoyo, documento y verificación del documento contra el modelo. Sin `plantuml` en el PATH, `PLANTUML="java -jar /ruta/plantuml.jar" ./build.sh`. Si faltan otras herramientas (`soffice`, `pdftotext`, java 21 para Structurizr), correr los generadores individuales (`gen/gen_puml.py`, `gen/gen_c4.py`, `gen/gen_md.py`, `gen/gen_docx.py` con `--with python-docx`, `gen/verificar_salida.py`, que sin PDF verifica el docx) y decirle al usuario qué parte del build no se ejecutó.
4. **Revisar la coherencia semántica** con `references/checklist-semantico.md`. El validador comprueba reglas; el checklist cubre lo que exige leer los textos (actor del catálogo vs. del flujo, precondiciones vs. estados, separación de funciones).
5. **Registrar lo que no se pueda decidir** en `decisiones:` del YAML o en la lista de pendientes, con la forma «qué dice A / qué dice B / qué decisión falta». No inventar requerimientos, casos de uso ni textos de flujo que el material no sustente.

## Orden de los diagramas que exige la plantilla

La plantilla obliga a presentar los diagramas en este orden. `modelo/gen/plan.py` lo declara una sola vez: decide qué figura va en cada sección, cómo se llama su archivo y qué número de figura lleva; `gen_puml.py`, `gen_c4.py`, `gen_docx.py`, `gen_md.py` y `verificar_salida.py` lo leen. Los archivos se nombran por su contenido (`CU-07-clases`, `estado-Certificado`), no por un número de orden, así que agregar un caso de uso no renombra los demás. Para cambiar el orden o agregar un tipo de diagrama se toca `plan.py`, no cada generador.

**Antes de los casos de uso** (en `modelo/out/`):

| Sección de la plantilla | Diagrama | Archivo | Sale de |
|---|---|---|---|
| Diagrama de Casos de Uso (Alto Nivel) | Por procesos: cada subsistema es un caso de alto nivel unido a sus actores | `casos-de-uso-alto-nivel.png` | `subsistemas` y `casos_uso[].actores` |
| Diagrama de Generalización de Actores | Padres abstractos y sus hijos, con todos los actores | `generalizacion-actores.png` | `generalizacion_actores` |
| Diagramas de Casos de Uso | Refinados, uno por subsistema, con include y extend | `casos-de-uso-A.png`, `casos-de-uso-B.png` | `casos_uso`, `relaciones_cu` |

**Por cada caso de uso**, en las cuatro subsecciones de la plantilla:

| Subsección | Contenido | Archivo |
|---|---|---|
| Descripción | Contexto C4 y contenedores C4 como introducción, de lo general a lo particular; luego la ficha (descripción, actores, requerimientos, pre y poscondiciones, flujo normal, flujo alternativo, excepciones) | `c4/C4-CUxx-contexto.png`, `c4/C4-CUxx-contenedores.png` |
| Modelo Estructural | Clases que participan, por capa (Boundary, Control, Entity) y puertos | `CU-xx-clases.png` |
| Modelo Dinámico | Diagrama de interacción (secuencia) y la misma colaboración entre componentes C4 | `CU-xx-secuencia.png`, `c4/C4-CUxx.png` |
| Otros diagramas | Actividades del flujo, si se ramifica (alternativas o excepciones con `paso`); máquina de estados de las entidades cuyas transiciones dispara el caso | `CU-xx-actividades.png`, `estado-<Entidad>.png` |

«Evitar redundancias», como pide la plantilla: cada máquina de estados se dibuja completa una sola vez, en el caso de uso que dispara más transiciones (ante empate, el que llega a un estado final; luego, el primero del catálogo). Los demás casos que crean la entidad o disparan alguna de sus transiciones la citan por número de figura. Un caso sin flujo ramificado ni transiciones dice que no requiere otros diagramas.

Los 16 casos están detallados. Si se agrega uno sin detallar, el documento le reserva igual sus cuatro subsecciones y marca como pendientes la ficha, el modelo estructural y el dinámico; el validador avisa. Para detallarlo hay que completar en el YAML los campos de la ficha, su `clases_cu` y su `secuencias`, y anclar con `paso` las alternativas y excepciones que bifurcan el flujo; con eso aparecen solos sus contenedores, clases, secuencia, vista dinámica y actividades.

Después de la matriz, el Modelo de Diseño lleva las clases persistentes (`clases-persistentes-A/B.png`) y el diagrama de entidad relación (`entidad-relacion.png`). Las vistas C4 del sistema completo (`C4-Contexto`, `C4-Contenedores`, `C4-Componentes`) y el modelo conceptual (`modelo-conceptual.png`) van al archivo de apoyo, porque la plantilla no tiene sección para ellas. Todas las vistas C4 se generan con `gen/gen_c4.py` usando la librería C4-PlantUML (stdlib de PlantUML, sin descargas).

## Criterios que conviene respetar

- **Cada requisito en al menos un caso de uso y cada caso de uso con al menos un requisito.** El validador lo exige; la matriz cierra en ambos sentidos.
- **Los requisitos transversales** (control de acceso, idioma) aparecen en todos los casos; está bien, pero no confundirlos con falta de análisis.
- **Un actor no es un rol.** Los roles del sistema son pocos: admin, miembro y visualizador, más miembro ERP y miembro ECMS (D-08). No imponer separación de funciones ni flujos de aprobación que ningún requisito pida; ante una contradicción, preferir la solución con menos estados y reglas.
- **La generalización de actores agrupa acceso común, no metas.** El hijo hereda todos los casos del padre, por eso los padres de `generalizacion_actores` son abstractos y no participan en casos de uso (el validador lo exige). Hoy hay dos: Usuario de Obra (Ingeniero de Obra, Responsable Técnico, Administrador; RNF-01) y Motor de Obra Studio (los dos motores; D-15), según D-20.
- **Cada transición de estado pertenece a un caso de uso.** El campo `cu` de la transición y `creado_en` de la máquina ubican la máquina de estados en «Otros diagramas»; el validador rechaza una transición sin caso.
- **Lo que depende del estudiante o del docente se deja marcado, no se inventa:** portada (grupo, alumnos), conteos de requisitos agregados, eliminados y redefinidos, y la validación del diagrama con los actores.
- **Un solo estilo de numeración** (RF-01) en tabla, matriz y fichas.
- **Los generadores no se tocan para arreglar un dato.** Si un diagrama sale mal por un dato, se corrige en el YAML; si sale mal por la forma de dibujarlo, se corrige el generador y se avisa.

## Referencias

- `references/formato-modelo-yaml.md`: secciones del YAML, la regla id/nombre y qué valida cada chequeo.
- `references/plantilla-manual-analisis.md`: orden de la plantilla y de dónde sale cada parte.
- `references/checklist-semantico.md`: revisión que requiere razonar sobre los textos.
- `references/ejemplo-obra-studio-guia.md`: guía de ejemplo de la plantilla completa (nivel de detalle y redacción de Pendientes). Es una foto del contenido en su momento: ante cualquier diferencia, mandan los datos de `modelo/modelo.yaml`.
