#!/usr/bin/env python3
"""modelo.yaml -> modelo-de-analisis.md (archivo de apoyo referenciado por el catálogo)."""
import pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PROY = RAIZ.parent
M = yaml.safe_load((RAIZ / "modelo.yaml").read_text(encoding="utf-8"))
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

w("## 4. Máquinas de estado")
w("")
for idx, (ent, maq) in enumerate(M["estados"].items(), start=12):
    w(f"### {ent}")
    w("")
    w(f'![Estados de {ent}](modelo/out/{idx}-estado-{ent}.png)')
    w("")
    w("| Estado | Significado |")
    w("|---|---|")
    for e in maq["estados"]:
        w(f'| {e["n"]} | {e["d"]} |')
    w("")
    w("| Desde | Evento | Guarda | Hacia |")
    w("|---|---|---|---|")
    for t_ in maq["transiciones"]:
        w(f'| {t_["de"]} | {t_["evento"]} | {t_.get("guarda", "—")} | {t_["a"]} |')
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
w("Vistas C4 generadas con Structurizr (`modelo/workspace.dsl`, salida en `modelo/out/c4/`):")
w("")
w("")
for n, d in [("Paisaje", "Obra Studio, el ERP y las personas que intervienen."),
             ("Contexto", "Obra Studio y su entorno."),
             ("Contenedores", "Estructura interna de Obra Studio."),
             ("Componentes", "Los cuatro anillos de Clean Architecture dentro del Motor ECMS."),
             ("CU02", "Interacción de componentes al importar el presupuesto."),
             ("CU05", "Interacción de componentes al aprobar una medición."),
             ("CU09", "Interacción de componentes al emitir un certificado.")]:
    w(f'**{n}.** {d}')
    w("")
    w(f'![{n}](modelo/out/c4/structurizr-{n}.png)')
    w("")
w("")

w("Diagramas UML del entregable (`modelo/out/`):")
w("")
w("| Archivo | Diagrama |")
w("|---|---|")
for png in sorted((RAIZ / "out").glob("*.png")):
    w(f'| `{png.name}` | {png.stem.split("-", 1)[1].replace("-", " ")} |')
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
w("  gen/gen_puml.py  genera los diagramas UML")
w("  gen/gen_dsl.py   genera el workspace de Structurizr")
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
