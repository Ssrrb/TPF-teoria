---
name: analisis-modelo-is2
description: Trabaja el modelo de análisis del TPF de Ingeniería del Software 2 (Obra Studio, plantilla «Manual de Análisis») sobre modelo/modelo.yaml, que es la única fuente de verdad. Edita el YAML, valida, regenera diagramas UML, vistas C4-PlantUML, documento y archivo de apoyo, y arma cada caso de uso con una introducción C4 seguida de la ficha, el modelo estructural y el dinámico. Usar siempre que el usuario mencione TPF, Modelo de Análisis, Manual de Análisis, casos de uso, actores, requerimientos (RF/RNF/PR), matriz de requerimientos vs casos de uso, diagramas UML o C4 del proyecto, o pida renombrar una clase, agregar un caso de uso o revisar la coherencia del análisis, aunque no nombre la skill.
---

# Modelo de análisis del TPF (Obra Studio)

**`modelo/modelo.yaml` manda.** Actores, requisitos, casos de uso, entidades, estados, secuencias y decisiones viven ahí. Todo lo demás (diagramas UML, vistas C4, documento, archivo de apoyo) se genera y se sobrescribe en cada build. No se edita ningún archivo generado, y no se crea un segundo modelo paralelo (ni JSON ni otro formato).

Esquema y reglas del YAML: `references/formato-modelo-yaml.md`. Leerlo antes de tocar el modelo.

## Flujo de trabajo

1. **Editar solo `modelo/modelo.yaml`.** Para un renombre, cambiar el `nombre:` de la entidad, componente o puerto; nada más repite el nombre. Para agregar algo, declararlo con `id` y `nombre` y referenciarlo por id.
2. **Validar:** `cd modelo && uv run --quiet --with pyyaml python3 gen/validar.py`. Los errores se corrigen en el YAML. Un id inexistente, un nombre de clase escrito a mano en un texto o un requisito sin caso de uso hacen fallar la validación.
3. **Regenerar:** `./build.sh` ejecuta validación, UML, C4, workspace de Structurizr, archivo de apoyo, documento y verificación del documento contra el modelo. Si faltan herramientas (`plantuml`, `pandoc`, `soffice`), correr los generadores individuales (`gen/gen_puml.py`, `gen/gen_c4.py`, `gen/gen_md.py`) y decirle al usuario qué parte del build no se ejecutó.
4. **Revisar la coherencia semántica** con `references/checklist-semantico.md`. El validador comprueba reglas; el checklist cubre lo que exige leer los textos (actor del catálogo vs. del flujo, precondiciones vs. estados, separación de funciones).
5. **Registrar lo que no se pueda decidir** en `decisiones:` del YAML o en la lista de pendientes, con la forma «qué dice A / qué dice B / qué decisión falta». No inventar requerimientos, casos de uso ni textos de flujo que el material no sustente.

## Cómo se arma cada caso de uso

Cada caso de uso abre con el modelo C4 como explicación introductoria, de lo general a lo particular, y recién después viene la ficha:

| Orden | Contenido | Archivo generado | Alcance |
|---|---|---|---|
| 1 | **Contexto C4**: quién usa el caso y con qué sistemas externos interactúa | `modelo/out/c4/C4-CUxx-contexto.png` | los 16 casos |
| 2 | **Contenedores C4**: qué contenedores (web, motor, base de datos, archivos, ERP) intervienen, deducido de los puertos que usa el caso | `modelo/out/c4/C4-CUxx-contenedores.png` | solo casos detallados |
| 3 | Ficha: descripción, precondiciones, poscondiciones, flujo normal, excepciones | `casos_uso[]` del YAML | todos; los detallados llevan flujo completo |
| 4 | **Modelo estructural**: clases por capa (Boundary, Control, Entity) | `modelo/out/NN-CU-xx-clases.png` | solo detallados |
| 5 | **Modelo dinámico**: secuencia UML y vista C4 dinámica entre componentes | `modelo/out/NN-CU-xx-secuencia.png`, `modelo/out/c4/C4-CUxx.png` | solo detallados |

Los casos no detallados tienen solo el contexto C4; el modelo no sabe qué adaptadores usan, y la skill no debe inventarlos. Para promover un caso a detallado hay que completar en el YAML su `clases_cu`, su `secuencias` y los campos de la ficha (el validador exige cuáles); con eso aparecen solos sus contenedores, clases, secuencia y vista dinámica.

Las vistas C4 del sistema completo (`C4-Contexto`, `C4-Contenedores`, `C4-Componentes`) van antes de los casos de uso, como introducción general del documento. Todas se generan con `gen/gen_c4.py` usando la librería C4-PlantUML (stdlib de PlantUML, sin descargas).

## Criterios que conviene respetar

- **Cada requisito en al menos un caso de uso y cada caso de uso con al menos un requisito.** El validador lo exige; la matriz cierra en ambos sentidos.
- **Los requisitos transversales** (control de acceso, idioma) aparecen en todos los casos; está bien, pero no confundirlos con falta de análisis.
- **La generalización de actores es opcional.** El hijo hereda todos los casos del padre; solo se justifica para acceso común y nunca si rompe una separación de funciones (RF-17, CU-05). Hoy el YAML no declara jerarquía de actores ni hay generador para ese diagrama ni para el de alto nivel: si se piden, agregar la jerarquía al YAML y el generador a `gen/gen_puml.py`, y avisar de la decisión.
- **Lo que depende del estudiante o del docente se deja marcado, no se inventa:** portada (grupo, alumnos), conteos de requisitos agregados, eliminados y redefinidos, y la validación del diagrama con los actores.
- **Un solo estilo de numeración** (RF-01) en tabla, matriz y fichas.
- **Los generadores no se tocan para arreglar un dato.** Si un diagrama sale mal por un dato, se corrige en el YAML; si sale mal por la forma de dibujarlo, se corrige el generador y se avisa.

## Referencias

- `references/formato-modelo-yaml.md`: secciones del YAML, la regla id/nombre y qué valida cada chequeo.
- `references/plantilla-manual-analisis.md`: orden de la plantilla y de dónde sale cada parte.
- `references/checklist-semantico.md`: revisión que requiere razonar sobre los textos.
- `references/ejemplo-obra-studio-guia.md`: guía de ejemplo de la plantilla completa (nivel de detalle y redacción de Pendientes). Es una foto del contenido en su momento: ante cualquier diferencia, mandan los datos de `modelo/modelo.yaml`.
