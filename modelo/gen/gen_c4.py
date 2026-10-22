#!/usr/bin/env python3
"""modelo.yaml -> modelo/c4/*.puml con la librería C4-PlantUML (stdlib de PlantUML)."""
import pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
from modelo import cargar
M = cargar()
C4 = RAIZ / "c4"; C4.mkdir(exist_ok=True)
SIS = M["meta"]["sistema"]
actores = {a["id"]: a for a in M["actores"]}
casos   = {c["id"]: c for c in M["casos_uso"]}
puertos = {p["nombre"]: p for p in M["puertos"]}

def vid(s):
    return "".join(ch if ch.isalnum() else "_" for ch in s)

def q(s):
    return s.replace('"', "'")

def escribir(nombre, lineas):
    (C4 / nombre).write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"  {nombre}")

def corta(a):
    d = a["descripcion"].strip().replace("\n", " ")
    return d.split(". ")[0].rstrip(".") + "."

PERSONAS = [a for a in M["actores"] if a["tipo"] != "sistema"]
# Relaciones persona -> sistema (misma semántica que el workspace Structurizr previo)
USO = {"ING": "Carga el presupuesto y registra la medición oficial",
       "SUP": "Aprueba mediciones y otorga la conformidad técnica",
       "ADM": "Autoriza la emisión y aprueba movimientos presupuestarios",
       "SUB": "Presenta las mediciones de su contrato"}
USO = {k: v for k, v in USO.items() if k in actores}

def cabecera(inc, titulo):
    return ["@startuml", f"!include <C4/{inc}>", "LAYOUT_WITH_LEGEND()", f"title {titulo}", ""]

def personas(destino, relacion):
    L = []
    for a in PERSONAS:
        L.append(f'Person({a["id"]}, "{a["nombre"]}", "{q(corta(a))}")')
    L.append("")
    return L

def rel_personas(destino):
    return [f'Rel({k}, {destino}, "{v}", "HTTPS")' for k, v in USO.items()]

# ---------------------------------------------------------------- contexto
def gen_contexto():
    L = cabecera("C4_Context", f"Contexto — {SIS} y su entorno")
    L += personas(None, None)
    L.append(f'System(obra, "{SIS}", "Gestiona presupuesto, medición, certificación y costos de obra.")')
    L.append('System_Ext(erp, "Sistema ERP", "Motor financiero y documental. Registra lo que el ECMS midió y certificó.")')
    L.append("")
    L += rel_personas("obra")
    L.append('Rel(obra, erp, "Publica el certificado aprobado", "Evento de dominio")')
    L.append('Rel(erp, CLI, "Emite la factura del certificado", "Documento")') if "CLI" in actores else None
    L.append('Rel(erp, TES, "Registra el cobro o el pago", "Documento")') if "TES" in actores else None
    L.append("@enduml")
    escribir("C4-Contexto.puml", [x for x in L if x is not None])

# -------------------------------------------------------------- contenedores
def gen_contenedores():
    L = cabecera("C4_Container", f"Contenedores — {SIS}")
    L += personas(None, None)
    L.append('System_Ext(erp, "Sistema ERP", "Motor financiero y documental.")')
    L.append(f'System_Boundary(obra, "{SIS}") {{')
    L.append('  Container(web, "Aplicación Web", "React + TypeScript", "Formularios de carga, medición y certificación.")')
    L.append('  Container(ecms, "Motor ECMS", "TypeScript", "Reglas de obra, presupuesto, medición y certificación.")')
    L.append('  ContainerDb(bd, "Base de Datos", "PostgreSQL", "Obras, presupuestos, mediciones y certificados.")')
    L.append('  ContainerDb(archivos, "Almacén de Archivos", "Almacenamiento de objetos", "Planillas de origen, evidencias y certificados exportados.")')
    L.append("}")
    L.append("")
    L += rel_personas("web")
    L += ['Rel(web, ecms, "Invoca los casos de uso", "HTTPS/JSON")',
          'Rel(ecms, bd, "Lee y escribe", "SQL")',
          'Rel(ecms, archivos, "Conserva planillas, evidencias y exportaciones", "API de objetos")',
          'Rel(ecms, erp, "Publica el certificado aprobado", "Evento de dominio")',
          "@enduml"]
    escribir("C4-Contenedores.puml", L)

# --------------------------------------------------------------- componentes
GRUPO = {"boundary": ("Adaptadores de interfaz", "Controller / Presenter"),
         "control": ("Casos de uso", "Interactor"),
         "entity": ("Dominio: entidades", "Entidad de dominio"),
         "puertos": ("Dominio: puertos", "Interfaz"),
         "adapter": ("Infraestructura", "Adaptador")}
capas = {k: [] for k in GRUPO}
for cid, c in M["clases_cu"].items():
    for k in ("boundary", "control", "entity", "puertos"):
        for n in c[k]:
            if n not in capas[k]:
                capas[k].append(n)
for n in capas["puertos"]:
    a = puertos[n]["adaptador"]
    if a not in capas["adapter"]:
        capas["adapter"].append(a)

def relaciones_componentes(solo_cu=None):
    """Pares (origen, destino, mensaje) derivados de las secuencias; únicos para la vista estática."""
    pares, vistos = [], set()
    for cid, s in M["secuencias"].items():
        if solo_cu and cid != solo_cu:
            continue
        porid = {p["id"]: p for p in s["participantes"]}
        for m in s["mensajes"]:
            if "frag" in m or m.get("tipo") == "return":
                continue
            o, d = porid[m["de"]], porid[m["a"]]
            od = "web" if o["tipo"] == "actor" else vid(o["nombre"])
            dd = "web" if d["tipo"] == "actor" else vid(d["nombre"])
            if od == dd or (solo_cu is None and (od, dd) in vistos):
                continue
            vistos.add((od, dd)); pares.append((od, dd, m["msg"]))
    return pares

def gen_componentes():
    L = cabecera("C4_Component", "Componentes — capas de Clean Architecture en el Motor ECMS")
    L.append('Container(web, "Aplicación Web", "React + TypeScript", "Interfaz de usuario.")')
    L.append('ContainerDb(bd, "Base de Datos", "PostgreSQL", "Datos del sistema.")')
    L.append('ContainerDb(archivos, "Almacén de Archivos", "Almacenamiento de objetos", "Planillas y evidencias.")')
    L.append('System_Ext(erp, "Sistema ERP", "Motor financiero y documental.")')
    L.append('Container_Boundary(ecms, "Motor ECMS") {')
    for capa, (titulo, tec) in GRUPO.items():
        L.append(f'  Boundary({vid(capa)}_b, "{titulo}") {{')
        for n in capas[capa]:
            L.append(f'    Component({vid(n)}, "{n}", "{tec}")')
        L.append("  }")
    L.append("}")
    L.append("")
    comp = {vid(n) for k in capas for n in capas[k]} | {"web"}
    for od, dd, msg in relaciones_componentes():
        if od in comp and dd in comp:
            L.append(f'Rel({od}, {dd}, "{q(msg)}")')
    for n in capas["puertos"]:
        L.append(f'Rel({vid(puertos[n]["adaptador"])}, {vid(n)}, "Implementa")')
    L += ['Rel(web, ecms, "Invoca los casos de uso", "HTTPS/JSON")' if False else "",
          "@enduml"]
    escribir("C4-Componentes.puml", [x for x in L if x != ""] )

# ------------------------------------------------------------ vistas dinámicas
def gen_dinamicas():
    for cid, c in casos.items():
        if cid not in M["secuencias"]:
            continue
        pasos = relaciones_componentes(cid)
        usados = {x for p in pasos for x in p[:2]}
        L = cabecera("C4_Dynamic", f"{cid} — {c['nombre']}")
        L.append('Container(web, "Aplicación Web", "React + TypeScript", "Interfaz de usuario.")')
        for capa, (titulo, tec) in GRUPO.items():
            for n in capas[capa]:
                if vid(n) in usados:
                    L.append(f'Component({vid(n)}, "{n}", "{tec}")')
        L.append("")
        for i, (od, dd, msg) in enumerate(pasos, 1):
            L.append(f'Rel({od}, {dd}, "{i}. {q(msg)}")')
        L.append("@enduml")
        escribir(f"C4-{cid.replace('-', '')}.puml", L)

# ------------------------------------------------- introducción por caso de uso
CONTENEDOR = {"bd": 'ContainerDb(bd, "Base de Datos", "PostgreSQL", "Obras, presupuestos, mediciones y certificados.")',
              "archivos": 'ContainerDb(archivos, "Almacén de Archivos", "Almacenamiento de objetos", "Planillas, evidencias y certificados exportados.")'}
ROL = {"bd": ("Lee y escribe", "SQL"), "archivos": ("Conserva archivos", "API de objetos"),
       "erp": ("Publica el certificado aprobado", "Evento de dominio")}

def _actores_cu(c):
    return [actores[a] for a in c["actores"]]

def gen_intro_cu():
    """Dos vistas que abren la ficha de cada caso de uso: contexto (todos) y contenedores
    (solo los detallados, donde el modelo sabe qué adaptadores usa el caso)."""
    for cid, c in casos.items():
        n = cid.replace("-", "")
        acts = _actores_cu(c)
        humanos = [a for a in acts if a["tipo"] != "sistema"]
        externos = [a for a in acts if a["tipo"] == "sistema" and a["id"] != "ECMS"]
        L = cabecera("C4_Context", f"{cid} — {c['nombre']}: contexto")
        for a in humanos:
            L.append(f'Person({a["id"]}, "{a["nombre"]}", "{q(corta(a))}")')
        L.append(f'System(obra, "{SIS}", "Gestiona presupuesto, medición, certificación y costos de obra.")')
        for a in externos:
            L.append(f'System_Ext({a["id"]}, "{a["nombre"]}", "{q(corta(a))}")')
        L.append("")
        for a in humanos:
            L.append(f'Rel({a["id"]}, obra, "{q(c["nombre"])}")')
        for a in externos:
            L.append(f'Rel(obra, {a["id"]}, "Entrega el resultado del caso de uso")')
        L.append("@enduml")
        escribir(f"C4-{n}-contexto.puml", L)

        if cid not in M["clases_cu"]:
            continue
        cc = M["clases_cu"][cid]
        usa = {puertos[p]["contenedor"] for p in cc["puertos"]}
        L = cabecera("C4_Container", f"{cid} — {c['nombre']}: contenedores")
        for a in humanos:
            L.append(f'Person({a["id"]}, "{a["nombre"]}", "{q(corta(a))}")')
        L.append(f'System_Boundary(obra, "{SIS}") {{')
        L.append('  Container(web, "Aplicación Web", "React + TypeScript", "Formularios del caso de uso.")')
        L.append('  Container(ecms, "Motor ECMS", "TypeScript", "Reglas del caso de uso.")')
        for k in ("bd", "archivos"):
            if k in usa:
                L.append("  " + CONTENEDOR[k])
        L.append("}")
        if "erp" in usa:
            L.append('System_Ext(erp, "Sistema ERP", "Motor financiero y documental.")')
        L.append("")
        for a in humanos:
            L.append(f'Rel({a["id"]}, web, "{q(c["nombre"])}", "HTTPS")')
        L.append(f'Rel(web, ecms, "Invoca el caso de uso", "HTTPS/JSON")')
        for k in ("bd", "archivos", "erp"):
            if k in usa:
                L.append(f'Rel(ecms, {k}, "{ROL[k][0]}", "{ROL[k][1]}")')
        L.append("@enduml")
        escribir(f"C4-{n}-contenedores.puml", L)

if __name__ == "__main__":
    print("Generando vistas C4-PlantUML desde modelo.yaml:")
    gen_contexto(); gen_contenedores(); gen_componentes(); gen_dinamicas(); gen_intro_cu()
