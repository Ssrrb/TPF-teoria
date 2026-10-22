#!/usr/bin/env python3
"""Comprueba que el documento generado concuerde con el modelo y con el plan de la plantilla."""
import pathlib, re, shutil, subprocess, sys, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PROY = RAIZ.parent
from modelo import cargar
import plan
M = cargar()
pdf, docx = PROY / "TPF-Obra-Studio.pdf", PROY / "TPF-Obra-Studio.docx"

def texto_documento():
    """El PDF si está al día y hay pdftotext; si no, el texto del docx del que sale."""
    if shutil.which("pdftotext") and pdf.exists() and pdf.stat().st_mtime >= docx.stat().st_mtime:
        return pdf.name, subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                                        capture_output=True, text=True).stdout
    from docx import Document
    d = Document(str(docx))
    partes = [p.text for p in d.paragraphs]
    partes += [c.text for t in d.tables for f in t.rows for c in f.cells]
    return docx.name, "\n".join(partes)

fuente, texto = texto_documento()
plano = " ".join(texto.split())
apoyo = (PROY / "modelo-de-analisis.md").read_text(encoding="utf-8")

fallos = []
def chk(cond, msg):
    if not cond: fallos.append(msg)

# los 48 identificadores aparecen en el documento
for r in M["requisitos"]:
    chk(r["id"] in plano, f"{r['id']} no aparece en el documento.")
# los 16 casos de uso aparecen, cada uno con las cuatro subsecciones de la plantilla
for c in M["casos_uso"]:
    chk(c["id"] in plano, f"{c['id']} no aparece en el documento.")
    chk(c["nombre"] in plano, f"El nombre de {c['id']} no aparece en el documento.")
SUBS = ["Descripción", "Modelo Estructural", "Modelo Dinámico", "Otros diagramas"]
for sub in SUBS:
    n = len(re.findall(rf"^{sub}$", texto, flags=re.M)) if fuente.endswith(".docx") else plano.count(sub)
    chk(n >= len(M["casos_uso"]), f"La subsección «{sub}» aparece {n} veces; se esperan {len(M['casos_uso'])}.")
# las secciones de diagramas previas a los casos de uso, en el orden de la plantilla
pos = [plano.find(t) for t, _ in plan.globales(M)]
chk(all(p >= 0 for p in pos) and pos == sorted(pos),
    "Faltan o están fuera de orden las secciones de alto nivel, generalización y casos de uso.")
# los actores aparecen con el nombre del modelo
for a in M["actores"]:
    chk(a["nombre"] in plano, f"El actor '{a['nombre']}' no aparece en el documento.")
for g in M.get("generalizacion_actores", []):
    chk(g["nombre"] in plano, f"El actor abstracto '{g['nombre']}' no aparece en el documento.")
# cada estado declarado aparece en el archivo de apoyo
for ent, maq in M["estados"].items():
    for e in maq["estados"]:
        chk(e["n"] in apoyo, f"El estado {ent}.{e['n']} no aparece en modelo-de-analisis.md.")
# vocabulario descartado: no debe quedar rastro del término viejo
for viejo in ("aditivo", "Aditivo"):
    chk(viejo not in plano, f"El término descartado '{viejo}' sigue en el documento.")
# la matriz cubre los 48 y ninguna fila queda vacía
sin_cu = [r["id"] for r in M["requisitos"] if not (r.get("casos_uso") or [])]
chk(not sin_cu, f"Requisitos sin caso de uso: {sin_cu}")
# cada figura del plan está en el documento y su imagen existe
esperadas = plan.figuras(M)
figs = set(re.findall(r"Figura (\d+)\.", plano))
chk(len(figs) == len(esperadas), f"Se esperan {len(esperadas)} figuras, se hallaron {len(figs)}.")
for f in esperadas:
    ruta = RAIZ / "out" / f["carpeta"] / f'{f["archivo"]}.png'
    chk(ruta.exists(), f"Falta la imagen {ruta.relative_to(RAIZ)}.")
# no quedan imágenes UML de corridas anteriores: todo PNG es del plan o el modelo conceptual
uml = {f'{f["archivo"]}.png' for f in esperadas if not f["carpeta"]} | {f"{plan.conceptual()}.png"}
sobran = sorted(p.name for p in (RAIZ / "out").glob("*.png") if p.name not in uml)
chk(not sobran, f"Imágenes UML que ningún diagrama del plan usa: {sobran}")

print("=" * 74)
print(f"  Verificación de salida — {fuente}")
print("=" * 74)
for f in fallos:
    print(f"  ERROR  {f}")
if fallos:
    print(f"\n{len(fallos)} discrepancia(s) entre el modelo y el documento.")
    sys.exit(1)
print(f"\nSin discrepancias: {len(M['requisitos'])} requisitos, {len(M['casos_uso'])} casos de uso, "
      f"{len(M['actores'])} actores y {len(figs)} figuras concuerdan con el modelo.")
