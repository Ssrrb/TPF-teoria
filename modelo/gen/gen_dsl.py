#!/usr/bin/env python3
"""modelo.yaml -> modelo/workspace.dsl (Structurizr, modelo C4 + vistas de imagen)."""
import pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
M = yaml.safe_load((RAIZ / "modelo.yaml").read_text(encoding="utf-8"))
actores = {a["id"]: a for a in M["actores"]}
casos   = {c["id"]: c for c in M["casos_uso"]}
puertos = {p["nombre"]: p for p in M["puertos"]}

def vid(s):
    if s.isupper():
        return s.lower()
    s = "".join(ch if ch.isalnum() else "_" for ch in s)
    return (s[0].lower() + s[1:]) if s else s

# componentes = unión de las capas de los casos detallados
capas = {"boundary": [], "control": [], "entity": [], "puertos": [], "adapter": []}
for cid, c in M["clases_cu"].items():
    for k in ("boundary", "control", "entity", "puertos"):
        for n in c[k]:
            if n not in capas[k]:
                capas[k].append(n)
for n in capas["puertos"]:
    a = puertos[n]["adaptador"]
    if a not in capas["adapter"]:
        capas["adapter"].append(a)

GRUPO = {"boundary": "Adaptadores de interfaz", "control": "Casos de uso",
         "entity": "Dominio: entidades", "puertos": "Dominio: puertos",
         "adapter": "Infraestructura"}
TEC = {"boundary": "Controller / Presenter", "control": "Interactor",
       "entity": "Entidad de dominio", "puertos": "Interfaz", "adapter": "Adaptador"}
DESC = {"boundary": "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio.",
        "control": "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura.",
        "entity": "Entidad del dominio: concentra la regla de negocio y sus invariantes.",
        "puertos": "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura.",
        "adapter": "Implementa el puerto contra una tecnología concreta."}

L = []
w = L.append
w(f'workspace "{M["meta"]["sistema"]}" "Modelo de arquitectura del Trabajo Práctico Final — {M["meta"]["materia"]}." {{')
w("")
w("    model {")
for aid, a in actores.items():
    if a["tipo"] == "sistema":
        continue
    corta = a["descripcion"].strip().replace("\n", " ")
    corta = corta.split(". ")[0].rstrip(".") + "."
    w(f'        {vid(aid)} = person "{a["nombre"]}" "{corta}"')
w("")
w('        erpExterno = softwareSystem "Sistema ERP" "Motor financiero y documental. Registra lo que el ECMS midió y certificó." "Externo"')
w("")
w(f'        obraStudio = softwareSystem "{M["meta"]["sistema"]}" "Gestiona presupuesto, medición, certificación y costos de obra." {{')
w('            web = container "Aplicación Web" "Presenta los formularios de carga, medición y certificación." "React + TypeScript"')
w('            ecms = container "Motor ECMS" "Reglas de obra, presupuesto, medición y certificación." "TypeScript" {')
for capa in ("boundary", "control", "entity", "puertos", "adapter"):
    w(f'                group "{GRUPO[capa]}" {{')
    for n in capas[capa]:
        w(f'                    {vid(n)} = component "{n}" "{DESC[capa]}" "{TEC[capa]}"')
    w("                }")
w("            }")
w('            bd = container "Base de Datos" "Obras, presupuestos, mediciones y certificados." "PostgreSQL" "Almacen"')
w('            archivos = container "Almacén de Archivos" "Planillas de origen, evidencias y certificados exportados." "Almacenamiento de objetos" "Almacen"')
w("")
w("            !docs docs")
w("            !adrs decisiones")
w("        }")
w("")
# relaciones de contexto
for cid, c in casos.items():
    pass
w('        ing -> web "Carga el presupuesto y registra la medición oficial" "HTTPS"')
w('        sup -> web "Aprueba mediciones y otorga la conformidad técnica" "HTTPS"')
w('        adm -> web "Autoriza la emisión y aprueba movimientos presupuestarios" "HTTPS"')
w('        sub -> web "Presenta las mediciones de su contrato" "HTTPS"')
w('        ecms -> erpExterno "Publica el certificado aprobado para su documento financiero" "Evento de dominio"')
w('        web -> ecms "Invoca los casos de uso" "HTTPS/JSON"')
w('        ecms -> bd "Lee y escribe" "SQL"')
w('        ecms -> archivos "Conserva planillas, evidencias y exportaciones" "API de objetos"')
w('        erpExterno -> cli "Emite la factura del certificado" "Documento"')
w('        erpExterno -> tes "Registra el cobro o el pago" "Documento"')
w("")
# relaciones entre componentes, derivadas de las secuencias
vistas = set()
dinamicas = {}
for cid, s in M["secuencias"].items():
    porid = {p["id"]: p for p in s["participantes"]}
    pasos = []
    for m in s["mensajes"]:
        if "frag" in m or m.get("tipo") == "return":
            continue
        o, d = porid[m["de"]], porid[m["a"]]
        od = vid(o["nombre"]) if o["tipo"] != "actor" else "web"
        dd = vid(d["nombre"]) if d["tipo"] != "actor" else "web"
        if od == dd:
            continue
        pasos.append((od, dd, m["msg"]))
        if (od, dd) not in vistas:
            vistas.add((od, dd))
            w(f'        {od} -> {dd} "{m["msg"]}" "Llamada interna"')
    dinamicas[cid] = pasos
for n in capas["puertos"]:
    w(f'        {vid(puertos[n]["adaptador"])} -> {vid(n)} "Implementa" "Inyección de dependencias"')
# relaciones del modelo de dominio entre las entidades que son componentes
ents = set(capas["entity"])
for r in M["relaciones"]:
    if r["a"] in ents and r["b"] in ents and (vid(r["a"]), vid(r["b"])) not in vistas:
        vistas.add((vid(r["a"]), vid(r["b"])))
        etiqueta = r.get("rol") or {"composicion": "Se compone de",
                                    "agregacion": "Agrupa", "asociacion": "Se asocia con"}[r["tipo"]]
        w(f'        {vid(r["a"])} -> {vid(r["b"])} "{etiqueta} ({r["ca"]} a {r["cb"]})" "Referencia de dominio"')
# el interactor entrega su resultado al presentador del mismo caso de uso
for cid, c in M["clases_cu"].items():
    presentadores = [n for n in c["boundary"] if "Presentador" in n]
    for pr in presentadores:
        w(f'        {vid(c["control"][0])} -> {vid(pr)} "Entrega el resultado del caso de uso" "Llamada interna"')
# objetos de valor: los produce el caso de uso que los calcula
conectados = {x for par in vistas for x in par}
for cid, c in M["clases_cu"].items():
    for n in c["entity"]:
        if vid(n) in conectados:
            continue
        productor = next((x for x in c["control"] if n.lower() in x.lower()), c["control"][0])
        vistas.add((vid(productor), vid(n)))
        conectados.add(vid(n))
        w(f'        {vid(productor)} -> {vid(n)} "Produce" "Llamada interna"')
w("    }")
w("")
w("    views {")
w('        systemLandscape "Paisaje" "Obra Studio, el ERP y las personas que intervienen." {')
w("            include *"); w("            autolayout lr"); w("        }")
w('        systemContext obraStudio "Contexto" "Obra Studio y su entorno." {')
w("            include *"); w("            autolayout lr"); w("        }")
w('        container obraStudio "Contenedores" "Estructura interna de Obra Studio." {')
w("            include *"); w("            autolayout lr"); w("        }")
w('        component ecms "Componentes" "Capas de Clean Architecture dentro del Motor ECMS." {')
w("            include *"); w("            autolayout lr"); w("        }")
for cid, pasos in dinamicas.items():
    c = casos[cid]
    w(f'        dynamic ecms "{cid.replace("-", "")}" "{cid} — {c["nombre"]}." {{')
    emitidos = set()
    for od, dd, msg in pasos:
        if (od, dd) in emitidos:
            continue
        emitidos.add((od, dd))
        w(f'            {od} -> {dd} "{msg}"')
    w("            autolayout lr"); w("        }")
# vistas de imagen: los diagramas UML, para que el workspace los reúna
for png in sorted((RAIZ / "out").glob("*.png")):
    clave = "uml" + png.stem.replace("-", "").replace("_", "")
    w(f'        image * "{clave}" {{')
    w(f"            image out/{png.name}")
    w(f'            title "UML — {png.stem}"')
    w("        }")
w("")
w("        styles {")
for etiqueta, props in [
    ("Person", [("shape", "person"), ("background", "#0b5394"), ("color", "#ffffff")]),
    ("Software System", [("background", "#1168bd"), ("color", "#ffffff")]),
    ("Externo", [("background", "#8c8c8c"), ("color", "#ffffff")]),
    ("Container", [("background", "#438dd5"), ("color", "#ffffff")]),
    ("Almacen", [("shape", "cylinder"), ("background", "#438dd5"), ("color", "#ffffff")]),
    ("Component", [("background", "#85bbf0"), ("color", "#000000")]),
]:
    w(f'            element "{etiqueta}" {{')
    for k, v in props:
        w(f"                {k} {v}")
    w("            }")
w("        }")
w("    }")
w("")
w("    configuration {")
w("        scope softwaresystem")
w("    }")
w("}")

(RAIZ / "workspace.dsl").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"workspace.dsl generado: {len(capas['boundary'])+len(capas['control'])+len(capas['entity'])+len(capas['puertos'])+len(capas['adapter'])} componentes, "
      f"{len(dinamicas)} vistas dinámicas, {len(list((RAIZ/'out').glob('*.png')))} vistas de imagen")
