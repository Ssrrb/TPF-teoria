#!/usr/bin/env python3
"""modelo.yaml -> modelo/uml/*.puml. No editar los .puml: se sobrescriben."""
import pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
M = yaml.safe_load((RAIZ / "modelo.yaml").read_text(encoding="utf-8"))
UML = RAIZ / "uml"; UML.mkdir(exist_ok=True)

actores   = {a["id"]: a for a in M["actores"]}
casos     = {c["id"]: c for c in M["casos_uso"]}
entidades = {e["nombre"]: e for e in M["entidades"]}
puertos   = {p["nombre"]: p for p in M["puertos"]}
tablas    = {e["tabla"]: e for e in M["entidades"] if e.get("tabla")}

# Sin skinparam de color: la plantilla de la cátedra usa el skin por defecto de PlantUML.
CAB = "skinparam dpi 150\nskinparam shadowing false\nskinparam defaultFontName Liberation Sans\n"

def escribir(nombre, cuerpo):
    (UML / nombre).write_text(cuerpo, encoding="utf-8")
    print(f"  {nombre}")

def ident(s):
    return "".join(ch if ch.isalnum() else "_" for ch in s)

# ---------------------------------------------------------------- casos de uso
def gen_casos_uso():
    """Un diagrama por subsistema: 16 casos en un solo lienzo resultan ilegibles."""
    for i, (sid, sub) in enumerate(sorted(M["subsistemas"].items()), start=1):
        miembros = [c for c in M["casos_uso"] if c["subsistema"] == sid]
        participan = {a for c in miembros for a in c["actores"]}
        prim = [a for a in M["actores"] if a["id"] in participan and a["tipo"] == "primario"]
        sec  = [a for a in M["actores"] if a["id"] in participan and a["tipo"] != "primario"]
        L = ["@startuml", "left to right direction", CAB.rstrip(),
             "skinparam packageStyle rectangle", "skinparam nodesep 12", "skinparam ranksep 60",
             f'title Sistema {M["meta"]["sistema"]} — Subsistema {sub["nombre"]}', ""]
        for a in prim:
            L.append(f'actor "{a["nombre"]}" as {a["id"]}')
        L.append("")
        L.append(f'rectangle "{sub["nombre"]}" {{')
        for c in miembros:
            L.append(f'  usecase "{c["id"]}\\n{c["nombre"]}" as {ident(c["id"])}')
        L.append("}")
        L.append("")
        for a in sec:
            L.append(f'actor "{a["nombre"]}" as {a["id"]}')
        L.append("")
        for c in miembros:
            for aid in c["actores"]:
                if actores[aid]["tipo"] == "primario":
                    L.append(f'{aid} --> {ident(c["id"])}')
                else:
                    L.append(f'{ident(c["id"])} --> {aid}')
        L.append("")
        for r in M["relaciones_cu"]:
            if casos[r["origen"]]["subsistema"] == sid:
                L.append(f'{ident(r["origen"])} ..> {ident(r["destino"])} : <<{r["tipo"]}>>')
        L.append("@enduml")
        escribir(f'0{i}-casos-de-uso-{sid}.puml', "\n".join(L))

# ------------------------------------------------- clases por caso de uso (CA)
def attr_resumen(e, maximo=3):
    """Identidad, los primeros atributos significativos y todos los derivados.
    El resto se elide con '...', como en los ejemplos de la cátedra: el detalle
    completo de columnas vive en el diagrama de entidad relación."""
    pk      = [a for a in e["atributos"] if a.get("pk")]
    simples = [a for a in e["atributos"] if not a.get("pk") and not a.get("derivado")]
    deriv   = [a for a in e["atributos"] if a.get("derivado")]
    elegidos = pk + simples[:maximo] + deriv
    lineas = [attr_uml(a) for a in elegidos]
    if len(simples) > maximo:
        lineas.append("  -...")
    return "\n".join(lineas)

def attr_uml(a):
    vis = "+" if a.get("pk") else "-"
    marca = "/" if a.get("derivado") else ""
    return f"  {vis}{marca}{a['n']} : {a['t']}"

def operaciones_desde_secuencia(cid):
    """La operación de una clase es el mensaje que recibe en el diagrama de interacción.
    Así la clase y la secuencia no pueden contradecirse."""
    ops = {}
    s = M["secuencias"].get(cid)
    if not s:
        return ops
    por_id = {p_["id"]: p_ for p_ in s["participantes"]}
    for m in s["mensajes"]:
        if "frag" in m or m.get("tipo") == "return":
            continue
        destino = por_id[m["a"]]
        if destino["tipo"] == "actor":
            continue
        ops.setdefault(destino["nombre"], [])
        if m["msg"] not in ops[destino["nombre"]]:
            ops[destino["nombre"]].append(m["msg"])
    return ops

def gen_clases_cu():
    """Tres capas y una sola arista por responsabilidad.
    La infraestructura no se dibuja aquí: la realización de cada puerto se ve en la vista de
    componentes C4. Así el diagrama muestra la regla de dependencia sin cruces innecesarios."""
    orden = {"CU-02": "03", "CU-05": "04", "CU-09": "05"}
    for cid, capas in M["clases_cu"].items():
        c = casos[cid]
        ops = operaciones_desde_secuencia(cid)
        def cuerpo_ops(n):
            return "\n".join(f"    +{o}" for o in ops.get(n, [])) or "    "
        L = ["@startuml", CAB.rstrip(), "skinparam classAttributeIconSize 0",
             "skinparam linetype ortho", "skinparam nodesep 25", "skinparam ranksep 45",
             "hide circle", f'title Caso de Uso {cid} — {c["nombre"]}', ""]
        L.append('package "Adaptadores de interfaz" <<Rectangle>> {')
        for n in capas["boundary"]:
            L.append(f'  class {n} <<Boundary>> {{\n{cuerpo_ops(n)}\n  }}')
        L.append("}")
        L.append('package "Casos de uso" <<Rectangle>> {')
        for n in capas["control"]:
            L.append(f'  class {n} <<Control>> {{\n{cuerpo_ops(n)}\n  }}')
        L.append("}")
        L.append('package "Dominio" <<Rectangle>> {')
        for n in capas["entity"]:
            e = entidades[n]
            cuerpo = attr_resumen(e)
            if ops.get(n):
                cuerpo += "\n    --\n" + "\n".join(f"    +{o}" for o in ops[n])
            est = "<<Entity>>" if not e.get("objeto_valor") else "<<ValueObject>>"
            L.append(f'  class {n} {est} {{\n{cuerpo}\n  }}')
        for n in capas["puertos"]:
            ms = "\n".join(f"  +{m}" for m in puertos[n]["metodos"])
            L.append(f'  interface {n} <<Interface>> {{\n{ms}\n  }}')
        L.append("}")
        L.append("")
        ctrl, pres = capas["boundary"][0], (capas["boundary"][1:] or [None])[0]
        interactor, servicios = capas["control"][0], capas["control"][1:]
        L.append(f'{ctrl} --> {interactor}')
        for s in servicios:
            L.append(f'{interactor} --> {s}')
        if pres:
            L.append(f'{interactor} ..> {pres}')
        for n in capas["puertos"]:
            L.append(f'{interactor} ..> {n}')
        if capas["entity"]:
            L.append(f'{interactor} ..> {capas["entity"][0]}')
        presentes = set(capas["entity"])
        for r in M["relaciones"]:
            if r.get("detalle"):
                continue
            if r["a"] in presentes and r["b"] in presentes:
                flecha = {"composicion": "*--", "agregacion": "o--", "asociacion": "--"}[r["tipo"]]
                L.append(f'{r["a"]} "{r["ca"]}" {flecha} "{r["cb"]}" {r["b"]}')
        L.append("")
        L.append("note as NInfra")
        L.append("  La infraestructura implementa cada puerto del dominio.")
        L.append("  Esa realización se documenta en la vista de componentes C4.")
        L.append("end note")
        L.append("@enduml")
        escribir(f'{orden[cid]}-{cid}-clases.puml', "\n".join(L))

# ------------------------------------------------------------------ secuencias
EST = {"boundary": "<<Boundary>>", "control": "<<Control>>",
       "entity": "<<Entity>>", "interface": "<<Interface>>"}

def gen_secuencias():
    orden = {"CU-02": "06", "CU-05": "07", "CU-09": "08"}
    for cid, s in M["secuencias"].items():
        c = casos[cid]
        L = ["@startuml", CAB.rstrip(), "skinparam sequenceMessageAlign left",
             f'title Caso de Uso {cid} — {c["nombre"]}', ""]
        for p in s["participantes"]:
            if p["tipo"] == "actor":
                L.append(f'actor "{p["nombre"]}" as {p["id"]}')
            else:
                L.append(f'participant "{EST[p["tipo"]]}\\n{p["nombre"]}" as {p["id"]}')
        L.append("")
        prof = 0
        pila = []          # (llamador, llamado) con activación abierta
        marcas = []        # profundidad de pila al abrir cada fragmento

        def cerrar_hasta(n, sangria):
            while len(pila) > n:
                _, llamado = pila.pop()
                L.append(f'{sangria}deactivate {llamado}')

        for m in s["mensajes"]:
            sangria = "  " * prof
            if "frag" in m:
                f = m["frag"]
                if f == "end":
                    cerrar_hasta(marcas.pop() if marcas else 0, sangria)
                    prof -= 1
                    L.append("  " * max(prof, 0) + "end")
                elif f == "else":
                    cerrar_hasta(marcas[-1] if marcas else 0, sangria)
                    L.append("  " * max(prof - 1, 0) + f'else {m.get("etiqueta", "")}')
                else:
                    L.append(sangria + f'{f} {m.get("etiqueta", "")}')
                    prof += 1
                    marcas.append(len(pila))
                continue
            tipo = m.get("tipo")
            if tipo == "return":
                # cierra las activaciones anidadas que quedaron abiertas bajo esta
                for i in range(len(pila) - 1, -1, -1):
                    if pila[i][1] == m["de"] and pila[i][0] == m["a"]:
                        cerrar_hasta(i + 1, sangria)
                        break
                L.append(f'{sangria}{m["de"]} --> {m["a"]} : {m["msg"]}')
                if pila and pila[-1] == (m["a"], m["de"]):
                    pila.pop()
                    L.append(f'{sangria}deactivate {m["de"]}')
            elif tipo == "create":
                L.append(f'{sangria}{m["de"]} -> {m["a"]} ** : {m["msg"]}')
            elif tipo == "async":
                L.append(f'{sangria}{m["de"]} ->> {m["a"]} : {m["msg"]}')
            else:
                L.append(f'{sangria}{m["de"]} -> {m["a"]} : {m["msg"]}')
                L.append(f'{sangria}activate {m["a"]}')
                pila.append((m["de"], m["a"]))
        cerrar_hasta(0, "")
        L.append("@enduml")
        escribir(f'{orden[cid]}-{cid}-secuencia.puml', "\n".join(L))

# -------------------------------------------------------- clases persistentes
GRUPOS = [
    ("09", "A", "Obra y presupuesto",
     ["Organización y seguridad", "Partes", "Obra y configuración", "Presupuesto"]),
    ("10", "B", "Medición y certificación",
     ["Medición", "Certificación", "Subcontratos e integración ERP"]),
]

def gen_clases_persistentes():
    """Dos figuras complementarias. Reunir las 28 clases con todos sus atributos en un solo
    lienzo resulta ilegible; el detalle completo de columnas está en el diagrama de entidad
    relación, que es el modelo físico."""
    persistentes = [e for e in M["entidades"] if e.get("tabla")]
    rels = [r for r in M["relaciones"] if not r.get("detalle")
            and entidades[r["a"]].get("tabla") and entidades[r["b"]].get("tabla")]
    for num, sid, nombre, paquetes in GRUPOS:
        propias = [e for e in persistentes if e["paquete"] in paquetes]
        nom_propias = {e["nombre"] for e in propias}
        # cada relación se dibuja una sola vez: en la figura que contiene el extremo hijo
        mias = [r for r in rels if r["b"] in nom_propias]
        refs = []
        for r in mias:
            if r["a"] not in nom_propias and r["a"] not in refs:
                refs.append(r["a"])
        L = ["@startuml", CAB.rstrip(), "skinparam classAttributeIconSize 0",
             "skinparam linetype ortho", "skinparam nodesep 22", "skinparam ranksep 50",
             "hide circle", f'title Clases Persistentes ({sid}) — {nombre}', ""]
        por_paquete = {}
        for e in propias:
            por_paquete.setdefault(e["paquete"], []).append(e)
        for paq, ents in por_paquete.items():
            L.append(f'package "{paq}" <<Rectangle>> {{')
            for e in ents:
                L.append(f'  class {e["nombre"]} <<persistent>> {{\n{attr_resumen(e)}\n  }}')
            L.append("}")
        if refs:
            L.append('package "De otra figura" <<Rectangle>> {')
            for n in refs:
                L.append(f'  class {n} <<referencia>>')
            L.append("}")
        for r in mias:
            flecha = {"composicion": "*--", "agregacion": "o--", "asociacion": "--"}[r["tipo"]]
            L.append(f'{r["a"]} "{r["ca"]}" {flecha} "{r["cb"]}" {r["b"]}')
        L.append("")
        L.append("note as NDeriv")
        L.append("  Los atributos con / son derivados: se calculan desde")
        L.append("  los registros aprobados y no se almacenan.")
        L.append("  Los puntos suspensivos indican atributos elididos; el")
        L.append("  detalle completo de columnas está en el diagrama de")
        L.append("  entidad relación.")
        L.append("  Las clases <<referencia>> se detallan en la otra figura.")
        L.append("end note")
        L.append("@enduml")
        escribir(f'{num}-clases-persistentes-{sid}.puml', "\n".join(L))

# ------------------------------------------------------------ entidad-relación
PATA = {("1", "0..*"): "||--o{", ("1", "1..*"): "||--|{", ("1", "1"): "||--||",
        ("1", "0..1"): "||--o|", ("0..1", "0..*"): "|o--o{", ("0..1", "0..1"): "|o--o|",
        ("0..1", "1..*"): "|o--|{"}

def gen_der():
    L = ["@startuml", CAB.rstrip(), "left to right direction",
         "title Diagrama de Entidad Relación", "", "hide circle",
         "skinparam linetype ortho", ""]
    fks = {}
    for r in M["relaciones"]:
        fks.setdefault(r["fk_en"], []).append(r)
    for e in M["entidades"]:
        t = e.get("tabla")
        if not t:
            continue
        comp = e.get("pk_compuesta") or []
        L.append(f'entity "{t}" as {t} {{')
        for a in e["atributos"]:
            if a.get("derivado"):
                continue
            if a.get("pk"):
                L.append(f'  * {a["n"]} : {a["sql"]} <<PK>>')
        for col in comp:
            L.append(f'  * {col} : UUID <<PK, FK>>')
        L.append("  --")
        for a in e["atributos"]:
            if a.get("derivado") or a.get("pk"):
                continue
            marca = "  " if a.get("null") else "* "
            L.append(f'  {marca}{a["n"]} : {a["sql"]}')
        for r in fks.get(t, []):
            if r["fk_col"] in comp:
                continue
            opcional = r["ca"].startswith("0")
            marca = "  " if opcional else "* "
            L.append(f'  {marca}{r["fk_col"]} : UUID <<FK>>')
        L.append("}")
    L.append("")
    for r in M["relaciones"]:
        ta, tb = entidades[r["a"]].get("tabla"), entidades[r["b"]].get("tabla")
        if not (ta and tb):
            continue
        pata = PATA.get((r["ca"], r["cb"]), "||--o{")
        etiqueta = f' : {r["rol"]}' if r.get("rol") else ""
        L.append(f'{ta} {pata} {tb}{etiqueta}')
    L.append("@enduml")
    escribir("11-entidad-relacion.puml", "\n".join(L))

# --------------------------------------------------------------------- estados
def gen_estados():
    for i, (ent, maq) in enumerate(M["estados"].items(), start=12):
        L = ["@startuml", CAB.rstrip(), f'title Estados de {ent}', ""]
        for e in maq["estados"]:
            L.append(f'state "{e["n"]}" as {ident(e["n"])}')
            L.append(f'{ident(e["n"])} : {e["d"]}')
        L.append("")
        L.append(f'[*] --> {ident(maq["inicial"])}')
        for t in maq["transiciones"]:
            g = f' [{t["guarda"]}]' if t.get("guarda") else ""
            L.append(f'{ident(t["de"])} --> {ident(t["a"])} : {t["evento"]}{g}')
        for f in maq.get("finales", []):
            L.append(f'{ident(f)} --> [*]')
        L.append("@enduml")
        escribir(f'{i}-estado-{ent}.puml', "\n".join(L))

if __name__ == "__main__":
    print("Generando diagramas desde modelo.yaml:")
    gen_casos_uso(); gen_clases_cu(); gen_secuencias()
    gen_clases_persistentes(); gen_der(); gen_estados()
    print(f"\n{len(list(UML.glob('*.puml')))} diagramas generados en modelo/uml/")
