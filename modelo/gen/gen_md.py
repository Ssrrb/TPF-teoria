#!/usr/bin/env python3
"""modelo.yaml -> modelo-de-analisis.md (archivo de apoyo referenciado por el catálogo)."""
import pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PROY = RAIZ.parent
from modelo import cargar
import plan
M = cargar()
actores = {a["id"]: a for a in M["actores"]}
L = []
w = L.append

w("# Modelo de Análisis — Obra Studio")
w("")
w(f'*{M["meta"]["materia"]} · {M["meta"]["trabajo"]} · {M["meta"]["docente"]}*  ')
w(f'*Autores: {" · ".join(a["nombre"] for a in M["meta"]["autores"])}*')
w("")
w("Este archivo acompaña a [requerimientos-consolidados.md](requerimientos-consolidados.md) y al "
  "entregable `TPF-Obra-Studio.docx`. Reúne lo que no entra en la plantilla de la cátedra: el "
  "catálogo de casos de uso, las máquinas de estado, las decisiones de modelado, las vistas de "
  "arquitectura y la trazabilidad con la implementación.")
w("")
w("Todo su contenido y todos los diagramas se generan desde `modelo/modelo.yaml`, que es la única "
  "fuente de verdad. Para reproducirlos, ejecutar `modelo/build.sh`.")
w("")

w("## 1. Alcance")
w("")
w("| Módulo | Nombre | Situación |")
w("|---|---|---|")
for m in M["alcance"]["incluidos"]:
    w(f'| `{m["codigo"]}` | {m["nombre"]} | Desarrollado |')
for m in M["alcance"]["excluidos"]:
    w(f'| `{m["codigo"]}` | — | Excluido: {m["motivo"]} |')
w("")

w("## 2. Vocabulario")
w("")
w("La columna «Clase» nombra la clase del modelo; «Implementación» indica su contraparte en el "
  "código, cuando existe.")
w("")
w("| Término | Inglés | Clase | Implementación |")
w("|---|---|---|---|")
for v_ in M["vocabulario"]:
    w(f'| {v_["termino"]} | {v_["gloss"]} | `{v_["clase"]}` | {v_["implementacion"]} |')
w("")

w("## 3. Catálogo de casos de uso")
w("")
w("| ID | Caso de uso | Subsistema | Actores | Requisitos |")
w("|---|---|---|---|---|")
for c in M["casos_uso"]:
    rs = [r["id"] for r in M["requisitos"] if c["id"] in (r.get("casos_uso") or [])]
    rs_rf = [x for x in rs if x.startswith("RF")]
    sub = M["subsistemas"][c["subsistema"]]["nombre"]
    marca = " **(detallado)**" if c.get("detallado") else ""
    w(f'| {c["id"]} | {c["nombre"]}{marca} | {sub} | '
      f'{", ".join(actores[a]["nombre"] for a in c["actores"])} | {", ".join(rs_rf) or "—"} |')
w("")
w("Relaciones entre casos de uso:")
w("")
for r in M["relaciones_cu"]:
    w(f'- `{r["origen"]}` **«{r["tipo"]}»** `{r["destino"]}`')
w("")
w("Generalización de actores (los padres son abstractos y no tienen casos de uso propios):")
w("")
for g in M.get("generalizacion_actores", []):
    hijos = ", ".join(actores[h]["nombre"] for h in g["hijos"])
    w(f'- **{g["nombre"]}** ← {hijos}. {" ".join(g["descripcion"].split())}')
w("")

w("## 4. Máquinas de estado")
w("")
for ent, maq in M["estados"].items():
    w(f"### {ent}")
    w("")
    w(f'![Estados de {ent}](modelo/out/{plan.estado(ent)}.png)')
    w("")
    w("| Estado | Significado |")
    w("|---|---|")
    for e in maq["estados"]:
        w(f'| {e["n"]} | {e["d"]} |')
    w("")
    w("| Desde | Evento | Guarda | Hacia | Caso de uso |")
    w("|---|---|---|---|---|")
    for t_ in maq["transiciones"]:
        w(f'| {t_["de"]} | {t_["evento"]} | {t_.get("guarda", "—")} | {t_["a"]} | {", ".join(plan.cus(t_))} |')
    w("")

w("## 5. Decisiones de modelado")
w("")
w("Cada fila es una discrepancia hallada entre el catálogo de requerimientos y la documentación de "
  "dominio, con la resolución adoptada.")
w("")
for d in M["decisiones"]:
    w(f'### {d["id"]} — {d["tema"]}')
    w("")
    w(f'**Hallazgo.** {" ".join(d["hallazgo"].split())}')
    w("")
    w(f'**Resolución.** {" ".join(d["resolucion"].split())}')
    w("")

w("## 6. Arquitectura")
w("")
w("El Motor ECMS aplica Clean Architecture en cuatro anillos; las dependencias apuntan siempre "
  "hacia adentro. Los estereotipos de análisis son su proyección en UML:")
w("")
w("| Estereotipo UML | Anillo | Responsabilidad |")
w("|---|---|---|")
w("| `«Boundary»` | Adaptadores de interfaz | Traduce la petición y presenta el resultado. |")
w("| `«Control»` | Casos de uso | Orquesta entidades y puertos. |")
w("| `«Entity»` | Dominio | Concentra la regla de negocio y sus invariantes. |")
w("| `«Interface»` | Dominio (puertos) | Invierte la dependencia hacia la infraestructura. |")
w("")
w("Puertos declarados por el dominio:")
w("")
w("| Puerto | Operaciones | Adaptador |")
w("|---|---|---|")
for p_ in M["puertos"]:
    w(f'| `{p_["nombre"]}` | {", ".join("`"+x+"`" for x in p_["metodos"])} | `{p_["adaptador"]}` |')
w("")
w("Vistas C4 generadas con C4-PlantUML (`modelo/gen/gen_c4.py`, salida en `modelo/out/c4/`):")
w("")
w("")
for n, d in [("Contexto", "Obra Studio y su entorno."),
             ("Contenedores", "Estructura interna de Obra Studio."),
             ("Componentes", "Los cuatro anillos de Clean Architecture dentro del Motor ECMS.")]:
    w(f'**{n}.** {d}')
    w("")
    w(f'![{n}](modelo/out/c4/C4-{n}.png)')
    w("")
w("Cada caso de uso tiene además su contexto, sus contenedores y su vista dinámica C4; el "
  "documento los ubica en la sección de cada caso (ver la tabla siguiente).")
w("")
w("")

w("Figuras del entregable en el orden de la plantilla (`modelo/gen/plan.py`). El modelo "
  f"conceptual (`modelo/out/{plan.conceptual()}.png`) se genera como apoyo y no integra el documento.")
w("")
w("| Figura | Archivo | Diagrama |")
w("|---|---|---|")
for i, f in enumerate(plan.figuras(M), start=1):
    ruta = "/".join(x for x in ("modelo/out", f["carpeta"], f'{f["archivo"]}.png') if x)
    w(f'| {i} | `{ruta}` | {f["pie"]} |')
w("")

w("## 7. Trazabilidad con la implementación")
w("")
w("El motor de presupuesto está implementado; certificaciones y subcontratos están especificados "
  "en la documentación de dominio pero no implementados. Los diagramas de este trabajo son modelo "
  "de diseño, no transcripción del código.")
w("")
w("| Clase del modelo | Situación | Contraparte |")
w("|---|---|---|")
for tr in M["trazabilidad"]:
    sit = "Implementado" if tr["estado"] == "implementado" else "Especificado"
    w(f'| `{tr["clase"]}` | {sit} | {tr["nota"]} |')
w("")

w("## 8. Reproducibilidad")
w("")
w("```")
w("modelo/")
w("  modelo.yaml      fuente única: actores, requisitos, casos de uso, entidades, estados, tablas")
w("  gen/validar.py   chequeos de consistencia; el build falla si algo no cierra")
w("  gen/plan.py      qué diagrama va en cada sección de la plantilla y cómo se llama su archivo")
w("  gen/gen_puml.py  genera los diagramas UML")
w("  gen/gen_c4.py    genera las vistas C4-PlantUML\n  gen/gen_dsl.py   genera el workspace de Structurizr\n  gen/modelo.py    carga el YAML y resuelve ids a nombres")
w("  gen/gen_docx.py  genera el documento con el formato de la cátedra")
w("  gen/gen_md.py    genera este archivo")
w("  build.sh         ejecuta todo lo anterior de punta a punta")
w("```")
w("")
w("`validar.py` comprueba, entre otras cosas, que los 48 identificadores del catálogo estén "
  "presentes sin duplicados, que cada requisito mapee a un caso de uso existente, que ningún caso "
  "de uso quede sin requisito, que toda clase citada en un diagrama exista en el modelo, que cada "
  "mensaje dirigido a un puerto sea uno de sus métodos declarados y que ningún estado sea "
  "inalcanzable.")
w("")

(PROY / "modelo-de-analisis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"modelo-de-analisis.md generado ({len(L)} líneas)")
