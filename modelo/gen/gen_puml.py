#!/usr/bin/env python3
"""modelo.yaml -> modelo/uml/*.puml. No editar los .puml: se sobrescriben.
Los nombres de archivo y el orden en el documento los fija gen/plan.py."""
import pathlib, textwrap, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
from modelo import cargar
import plan
M = cargar()
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

# ------------------------------------------------------ casos de uso de alto nivel
def gen_alto_nivel():
    """Por procesos: cada subsistema es un caso de uso de alto nivel y cada actor se une a los
    subsistemas donde participa. Se deriva del catálogo; no repite los 16 casos."""
    L = ["@startuml", "left to right direction", CAB.rstrip(), "skinparam nodesep 20",
         "skinparam ranksep 80", f'title Sistema {M["meta"]["sistema"]} — Casos de Uso de Alto Nivel', ""]
    subs = sorted(M["subsistemas"].items())
    participa = {sid: {a for c in M["casos_uso"] if c["subsistema"] == sid for a in c["actores"]}
                 for sid, _ in subs}
    for a in M["actores"]:
        if a["tipo"] == "primario":
            L.append(f'actor "{a["nombre"]}" as {a["id"]}')
    L.append("")
    L.append(f'rectangle "{M["meta"]["sistema"]}" {{')
    for sid, s in subs:
        L.append(f'  usecase "{s["nombre"]}" as SUB_{ident(sid)}')
    L.append("}")
    L.append("")
    for a in M["actores"]:
        if a["tipo"] != "primario":
            L.append(f'actor "{a["nombre"]}" as {a["id"]}')
    L.append("")
    for sid, _ in subs:
        for a in M["actores"]:
            if a["id"] in participa[sid]:
                L.append(f'{a["id"]} --> SUB_{ident(sid)}' if a["tipo"] == "primario"
                         else f'SUB_{ident(sid)} --> {a["id"]}')
    L.append("@enduml")
    escribir(f"{plan.alto_nivel()}.puml", "\n".join(L))

# ---------------------------------------------------- generalización de actores
def gen_generalizacion():
    """Jerarquía declarada en generalizacion_actores. Los padres son abstractos: agrupan el acceso
    común y no agregan casos de uso propios. Se dibujan todos los actores para que la figura muestre
    también a los que no generalizan."""
    # sin la dirección explícita, un lienzo con solo actores se dibuja como secuencia
    L = ["@startuml", "top to bottom direction", CAB.rstrip(), "skinparam nodesep 30",
         "skinparam ranksep 60", "title Generalización de Actores", ""]
    for g in M.get("generalizacion_actores", []):
        L.append(f'actor "{g["nombre"]}" as {g["id"]} <<abstracto>>')
    for a in M["actores"]:
        L.append(f'actor "{a["nombre"]}" as {a["id"]}')
    L.append("")
    for g in M.get("generalizacion_actores", []):
        for h in g["hijos"]:
            L.append(f'{g["id"]} <|-- {h}')
    L.append("@enduml")
    escribir(f"{plan.generalizacion()}.puml", "\n".join(L))

# ---------------------------------------------------------------- casos de uso
def gen_casos_uso():
    """Un diagrama por subsistema: 16 casos en un solo lienzo resultan ilegibles."""
    for sid, sub in sorted(M["subsistemas"].items()):
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
        escribir(f"{plan.casos_uso(sid)}.puml", "\n".join(L))

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
            # solo los métodos del puerto que este caso de uso invoca; sin uso en la secuencia, todos
            usados = [m for m in puertos[n]["metodos"]
                      if any(o.split("(")[0] == m.split("(")[0] for o in ops.get(n, []))]
            ms = "\n".join(f"  +{m}" for m in usados or puertos[n]["metodos"])
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
        escribir(f"{plan.clases(cid)}.puml", "\n".join(L))

# ------------------------------------------------------------------ secuencias
EST = {"boundary": "<<Boundary>>", "control": "<<Control>>",
       "entity": "<<Entity>>", "interface": "<<Interface>>"}

def gen_secuencias():
    for cid, s in M["secuencias"].items():
        c = casos[cid]
        L = ["@startuml", CAB.rstrip(), "skinparam sequenceMessageAlign left",
             f'title Caso de Uso {cid} — {c["nombre"]}', ""]
        for p in s["participantes"]:
            if p["tipo"] == "actor":
                L.append(f'actor "{p["nombre"]}" as {p["id"]}')
            else:
                # 'objeto' distingue dos instancias de la misma clase (versión nueva y anterior)
                rotulo = f'{p["objeto"]} : {p["nombre"]}' if p.get("objeto") else p["nombre"]
                L.append(f'participant "{EST[p["tipo"]]}\\n{rotulo}" as {p["id"]}')
        L.append("")
        prof = 0
        pila = []          # (llamador, llamado) con activación abierta
        marcas = []        # por fragmento abierto: la menor profundidad de pila desde que se abrió

        def sacar():
            # si dentro del fragmento se cierra una activación de afuera, lo que se abra después
            # también es del fragmento: la marca baja con la pila
            r = pila.pop()
            for mk in marcas:
                mk[0] = min(mk[0], len(pila))
            return r

        def cerrar_hasta(n, sangria):
            while len(pila) > n:
                _, llamado = sacar()
                L.append(f'{sangria}deactivate {llamado}')

        for m in s["mensajes"]:
            sangria = "  " * prof
            if "frag" in m:
                f = m["frag"]
                if f == "end":
                    cerrar_hasta(marcas.pop()[0] if marcas else 0, sangria)
                    prof -= 1
                    L.append("  " * max(prof, 0) + "end")
                elif f == "else":
                    cerrar_hasta(marcas[-1][0] if marcas else 0, sangria)
                    L.append("  " * max(prof - 1, 0) + f'else {m.get("etiqueta", "")}')
                else:
                    L.append(sangria + f'{f} {m.get("etiqueta", "")}')
                    prof += 1
                    marcas.append([len(pila)])
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
                    sacar()
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
        escribir(f"{plan.secuencia(cid)}.puml", "\n".join(L))

# ------------------------------------------------------------------ actividades
def envolver(texto, ancho=46):
    return "\\n".join(textwrap.wrap(" ".join(texto.split()), ancho))

def partir(x):
    """'Condición: consecuencia.' -> (condición, consecuencia). Sin dos puntos, todo es consecuencia."""
    cond, sep, resto = x["texto"].partition(": ")
    cond, resto = (cond, resto) if sep else (x["id"], x["texto"])
    return cond, resto[:1].upper() + resto[1:]

def gen_actividades():
    """Flujo de la ficha con un carril por actor y otro para el sistema. Cada alternativa o
    excepción anclada a un paso se dibuja como decisión después de la respuesta de ese paso:
    la alternativa marcada 'continua' vuelve al flujo normal; las demás lo terminan. Las
    excepciones sin paso pueden ocurrir en cualquier momento y van en una nota."""
    sis = M["meta"]["sistema"]
    for c in M["casos_uso"]:
        if not (c.get("flujo") and plan.ramifica(c)):
            continue
        carril = lambda aid: actores[aid]["nombre"] if aid in actores else sis
        L = ["@startuml", CAB.rstrip(), f'title Caso de Uso {c["id"]} — {c["nombre"]}: actividades', ""]
        # en un mismo paso, primero las validaciones que impiden el objetivo y después las variantes
        desvios = [("exc", x) for x in c.get("excepciones") or []] + \
                  [("alt", x) for x in c.get("alternativos") or []]
        L.append(f'|{carril(c["flujo"][0]["actor"])}|')
        L.append("start")
        for n, paso in enumerate(c["flujo"], 1):
            if paso["actor"] in actores:
                L.append(f'|{carril(paso["actor"])}|')
                L.append(f':{envolver(paso["accion"])};')
            L.append(f"|{sis}|")
            L.append(f':{envolver(paso["respuesta"])};')
            for tipo, x in desvios:
                if x.get("paso") != n:
                    continue
                cond, efecto = partir(x)
                L.append(f'if ({x["id"]}. ¿{envolver(cond, 34)}?) then (sí)')
                L.append(f'  :{envolver(efecto)};')
                if not (tipo == "alt" and x.get("continua")):
                    L.append("  stop" if tipo == "alt" else "  end")
                L.append("else (no)")
                L.append("endif")
        sueltas = [x for t, x in desvios if not x.get("paso")]
        if sueltas:
            L.append("note right")
            L.append("  En cualquier paso:")
            for x in sueltas:
                ref = f' ({x["requisito"]})' if x.get("requisito") else ""
                L.append(f'  {x["id"]}{ref}. {envolver(partir(x)[0], 50)}'.replace("\\n", "\n    "))
            L.append("end note")
        L.append("stop")
        L.append("@enduml")
        escribir(f'{plan.actividades(c["id"])}.puml', "\n".join(L))

# -------------------------------------------------------- clases persistentes
def gen_clases_persistentes():
    """Dos figuras complementarias. Reunir las 28 clases con todos sus atributos en un solo
    lienzo resulta ilegible; el detalle completo de columnas está en el diagrama de entidad
    relación, que es el modelo físico."""
    persistentes = [e for e in M["entidades"] if e.get("tabla")]
    rels = [r for r in M["relaciones"] if not r.get("detalle")
            and entidades[r["a"]].get("tabla") and entidades[r["b"]].get("tabla")]
    for sid, nombre, paquetes in plan.GRUPOS_PERSISTENTES:
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
        escribir(f"{plan.persistentes(sid)}.puml", "\n".join(L))

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
    escribir(f"{plan.der()}.puml", "\n".join(L))

# ------------------------------------------------------------ modelo conceptual
def gen_conceptual():
    """Modelo de dominio: solo conceptos y asociaciones con multiplicidad, sin atributos ni capas.
    Solo entran las entidades marcadas 'conceptual' en el YAML y las relaciones entre ellas."""
    L = ["@startuml", CAB.rstrip(), "skinparam nodesep 40", "skinparam ranksep 70",
         "hide circle", "hide members", "left to right direction", "skinparam classBackgroundColor #FFFFFF",
         f'title Modelo Conceptual — {M["meta"]["sistema"]}', ""]
    rels = [r for r in M["relaciones"] if not r.get("detalle")
            and entidades[r["a"]].get("conceptual") and entidades[r["b"]].get("conceptual")]
    usadas = {x for r in rels for x in (r["a"], r["b"])}
    for e in M["entidades"]:
        if e.get("conceptual") and e["nombre"] in usadas:
            L.append(f'class {e["nombre"]}')
    L.append("")
    for r in rels:
        flecha = {"composicion": "*--", "agregacion": "o--", "asociacion": "--"}[r["tipo"]]
        rol = f' : {r["rol"]}' if r.get("rol") else ""
        L.append(f'{r["a"]} "{r["ca"]}" {flecha} "{r["cb"]}" {r["b"]}{rol}')
    L.append("@enduml")
    escribir(f"{plan.conceptual()}.puml", "\n".join(L))

# --------------------------------------------------------------------- estados
def gen_estados():
    """Cada transición lleva el caso de uso que la dispara; así la figura se lee junto al caso
    de uso donde se ubica (gen/plan.py elige uno, para no repetirla)."""
    for ent, maq in M["estados"].items():
        L = ["@startuml", CAB.rstrip(), f'title Estados de {ent}', ""]
        for e in maq["estados"]:
            L.append(f'state "{e["n"]}" as {ident(e["n"])}')
            L.append(f'{ident(e["n"])} : {e["d"]}')
        L.append("")
        crea = f' : ({", ".join(maq["creado_en"])})' if maq.get("creado_en") else ""
        L.append(f'[*] --> {ident(maq["inicial"])}{crea}')
        for t in maq["transiciones"]:
            g = f' [{t["guarda"]}]' if t.get("guarda") else ""
            L.append(f'{ident(t["de"])} --> {ident(t["a"])} : {t["evento"]}{g}\\n({", ".join(plan.cus(t))})')
        for f in maq.get("finales", []):
            L.append(f'{ident(f)} --> [*]')
        L.append("@enduml")
        escribir(f"{plan.estado(ent)}.puml", "\n".join(L))

if __name__ == "__main__":
    print("Generando diagramas desde modelo.yaml:")
    gen_alto_nivel(); gen_generalizacion(); gen_casos_uso()
    gen_clases_cu(); gen_secuencias(); gen_actividades(); gen_estados()
    gen_clases_persistentes(); gen_der(); gen_conceptual()
    print(f"\n{len(list(UML.glob('*.puml')))} diagramas generados en modelo/uml/")
