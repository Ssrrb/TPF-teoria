# Formato de `modelo/modelo.yaml`

Fuente única de verdad. Los generadores no leen el archivo directo: `modelo/gen/modelo.py` lo carga, resuelve los ids a nombres y entrega el modelo ya resuelto.

## Regla central: un id estable, un nombre visible

Cada **entidad**, **componente** (clase Boundary, Control o adaptador) y **puerto** se declara una vez:

```yaml
- id: certificado        # estable, snake_case; lo que referencia el resto del modelo
  nombre: Certificado    # visible; se cambia en este único lugar
```

Todo lo demás referencia por **id**. Dentro de un texto (mensajes de secuencia, prosa) se escribe `{id}`, por ejemplo `"{archivo_origen}(hashSHA256)"`. El cargador falla si:

- un id no existe, está duplicado o es de otro tipo (una entidad donde va un puerto);
- dos ids comparten nombre;
- un texto nombra una clase CamelCase a mano en vez de `{id}`;
- el adaptador de un puerto no es un componente `capa: adapter` con `contenedor` válido.

**Renombrar una clase = cambiar su `nombre:`.** Después, `validar.py` y los generadores propagan el cambio a UML, C4, documento y archivo de apoyo.

## Secciones

| Sección | Qué contiene | Referencia por |
|---|---|---|
| `meta`, `alcance` | Portada del documento y módulos incluidos o excluidos | texto |
| `actores` | `id`, `nombre`, `tipo` (primario, secundario, sistema), `externo`, `descripcion`, `uso` (relación con el sistema en C4 y Structurizr) | id de actor (`ING`, `SUP`…) |
| `generalizacion_actores` | Padres abstractos: `id`, `nombre`, `descripcion`, `hijos` (ids de actores). No participan en casos de uso; cada hijo tiene un solo padre | ids de actor |
| `requisitos` | `id` (RF-01…), `tipo` (RF, RNF, PR), `enunciado`, `casos_uso`, `redefinido: true` si cambió respecto del catálogo original | id de requisito y de caso de uso |
| `subsistemas`, `casos_uso`, `relaciones_cu` | Catálogo; `detallado: true` exige ficha completa; `include` y `extend` solo dentro de un subsistema. En la ficha, `alternativos` y `excepciones` son listas de `{ id, paso?, requisito?, continua?, texto }`: `paso` es el paso del flujo normal donde se bifurca (después de la respuesta del sistema), `continua: true` (solo alternativas) indica que el camino vuelve al flujo normal y `texto` sigue la forma «Condición: consecuencia» | id de caso de uso |
| `entidades` | `id`, `nombre`, `paquete`, `tabla`, `atributos`; sin `tabla` es objeto de valor | `id` |
| `relaciones` | `a`, `b` (ids de entidad), `tipo`, multiplicidades, `fk_en` (id de la entidad que lleva la clave), `fk_col`; `detalle: true` las omite del modelo conceptual | ids |
| `puertos` | `id`, `nombre`, `metodos`, `adaptador` (id de componente) | `id` |
| `componentes` | Clases boundary y control y adaptadores; los adaptadores llevan `contenedor` (bd, archivos, erp, ecms) | `id` |
| `clases_cu` | Por caso detallado: listas `boundary`, `control`, `entity`, `puertos` | ids |
| `estados` | Máquina de estados por entidad (la clave es el id de la entidad); `creado_en` lista los casos que crean la entidad y cada transición lleva `cu` (un caso o una lista) | id |
| `secuencias` | Por caso detallado: `participantes` (`id` local, `tipo`, `ref` al id de la clase, `objeto` opcional para distinguir dos instancias de la misma clase) y `mensajes` | `ref` y `{id}` |
| `decisiones`, `trazabilidad`, `vocabulario` | Discrepancias resueltas, estado de implementación y glosario | ids de entidad |

## Qué valida `validar.py`

Los 48 requisitos y su reparto, la trazabilidad en ambos sentidos, los actores sin uso, la generalización de actores (padres abstractos sin casos, hijos existentes, un padre por hijo), las relaciones include y extend, la ficha completa de los casos detallados (y avisa de cada caso sin detallar), que cada requisito citado en una alternativa o excepción esté marcado para ese CU, que su `paso` exista en el flujo y que `continua` solo aparezca en alternativas con `paso`, las clases por caso, las claves primarias y foráneas, las máquinas de estado (estados inalcanzables, transiciones a estados inexistentes, toda transición con un `cu` existente), las secuencias (participantes declarados, fragmentos balanceados, cada mensaje a un puerto debe ser uno de sus métodos declarados) y las referencias por id.

## Diagramas que salen de este modelo

`gen/plan.py` fija el orden de la plantilla y los nombres de archivo; ver la tabla de `SKILL.md`. `gen/gen_puml.py` genera en `modelo/uml/` y `modelo/out/` el alto nivel, la generalización de actores, un diagrama refinado por subsistema y, por caso detallado, clases, secuencia y actividades (si el flujo se ramifica), además de las máquinas de estado, las clases persistentes, el entidad relación y el modelo conceptual. En las clases de un caso, cada puerto muestra solo los métodos que su secuencia invoca.

`gen/gen_c4.py` genera, en `modelo/c4/` y `modelo/out/c4/`: `C4-Contexto`, `C4-Contenedores`, `C4-Componentes` (los anillos y la realización de cada puerto; la colaboración de cada caso está en su vista dinámica); por cada caso de uso, `C4-CUxx-contexto`; por cada caso detallado, además `C4-CUxx-contenedores` y la vista dinámica `C4-CUxx`.
