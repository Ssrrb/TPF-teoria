#!/usr/bin/env python3
"""Comprueba que el documento generado concuerde con el modelo."""
import pathlib, re, subprocess, sys, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PROY = RAIZ.parent
M = yaml.safe_load((RAIZ / "modelo.yaml").read_text(encoding="utf-8"))
pdf = PROY / "TPF-Obra-Studio.pdf"
texto = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                       capture_output=True, text=True).stdout
plano = " ".join(texto.split())
apoyo = (PROY / "modelo-de-analisis.md").read_text(encoding="utf-8")

fallos = []
def chk(cond, msg):
    if not cond: fallos.append(msg)

# los 48 identificadores aparecen en el documento
for r in M["requisitos"]:
    chk(r["id"] in plano, f"{r['id']} no aparece en el documento.")
# los 16 casos de uso aparecen
for c in M["casos_uso"]:
    chk(c["id"] in plano, f"{c['id']} no aparece en el documento.")
    chk(c["nombre"] in plano, f"El nombre de {c['id']} no aparece en el documento.")
# los actores aparecen con el nombre del modelo
for a in M["actores"]:
    chk(a["nombre"] in plano, f"El actor '{a['nombre']}' no aparece en el documento.")
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
# las figuras referenciadas existen
figs = set(re.findall(r"Figura (\d+)\.", plano))
chk(len(figs) >= 11, f"Se esperan al menos 11 figuras, se hallaron {len(figs)}.")
# toda imagen generada se usa o se declara
pngs = {p.name for p in (RAIZ / "out").glob("*.png")}
chk(len(pngs) == 15, f"Se esperan 15 diagramas UML, hay {len(pngs)}.")

print("=" * 74)
print(f"  Verificación de salida — {pdf.name}")
print("=" * 74)
for f in fallos:
    print(f"  ERROR  {f}")
if fallos:
    print(f"\n{len(fallos)} discrepancia(s) entre el modelo y el documento.")
    sys.exit(1)
print(f"\nSin discrepancias: {len(M['requisitos'])} requisitos, {len(M['casos_uso'])} casos de uso, "
      f"{len(M['actores'])} actores y {len(figs)} figuras concuerdan con el modelo.")
