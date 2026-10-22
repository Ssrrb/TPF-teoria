#!/usr/bin/env python3
"""Chequeos de consistencia sobre modelo.yaml. Falla el build si algo no cierra."""
import sys, pathlib, yaml
from collections import Counter

RAIZ = pathlib.Path(__file__).resolve().parent.parent
from modelo import cargar, ModeloError
try:
    M = cargar()
except ModeloError as exc:
    print("=" * 74); print("  Referencias del modelo"); print("=" * 74)
    for e_ in exc.errores:
        print(f"  ERROR  {e_}")
    print(f"\n{len(exc.errores)} error(es). El modelo no es consistente.")
    sys.exit(1)

errores, avisos = [], []
def err(m): errores.append(m)
def avi(m): avisos.append(m)

actores    = {a["id"]: a for a in M["actores"]}
requisitos = {r["id"]: r for r in M["requisitos"]}
casos      = {c["id"]: c for c in M["casos_uso"]}
entidades  = {e["nombre"]: e for e in M["entidades"]}
puertos    = {p["nombre"]: p for p in M["puertos"]}
tablas     = {e["tabla"]: e for e in M["entidades"] if e.get("tabla")}

# 1. Catálogo de requisitos -----------------------------------------------------
if len(requisitos) != 48:
    err(f"Se esperan 48 identificadores, hay {len(requisitos)}.")
cuenta = Counter(r["tipo"] for r in M["requisitos"])
for tipo, n in (("RF", 28), ("RNF", 12), ("PR", 8)):
    if cuenta[tipo] != n:
        err(f"Se esperan {n} requisitos {tipo}, hay {cuenta[tipo]}.")
dups = [k for k, v in Counter(r["id"] for r in M["requisitos"]).items() if v > 1]
if dups:
    err(f"Identificadores duplicados: {dups}")

# 2. Trazabilidad requisito -> caso de uso --------------------------------------
for rid, r in requisitos.items():
    cus = r.get("casos_uso") or []
    if not cus:
        err(f"{rid} no mapea a ningún caso de uso.")
    for cu in cus:
        if cu not in casos:
            err(f"{rid} referencia el caso de uso inexistente {cu}.")

# 3. Ningún caso de uso huérfano ------------------------------------------------
cubiertos = {cu for r in M["requisitos"] for cu in (r.get("casos_uso") or [])}
for cid in casos:
    if cid not in cubiertos:
        err(f"{cid} no responde a ningún requisito.")

for c in M["casos_uso"]:
    if c.get("subsistema") not in M["subsistemas"]:
        err(f"{c['id']}: subsistema '{c.get('subsistema')}' no declarado.")

# 4/5. Actores -------------------------------------------------------------------
usados = set()
for cid, c in casos.items():
    for a in c["actores"]:
        if a not in actores:
            err(f"{cid} referencia el actor inexistente '{a}'.")
        usados.add(a)
for aid in actores:
    if aid not in usados:
        err(f"El actor '{aid}' ({actores[aid]['nombre']}) no participa en ningún caso de uso.")

# 5b. Generalización de actores: padres abstractos, sin casos propios, un padre por hijo
padre_de = {}
for g in M.get("generalizacion_actores", []):
    if g["id"] in actores:
        err(f"generalizacion_actores: '{g['id']}' ya es un actor concreto; el padre debe ser abstracto.")
    if g["nombre"] in {a["nombre"] for a in actores.values()}:
        err(f"generalizacion_actores: el nombre '{g['nombre']}' ya lo usa un actor concreto.")
    if not g.get("hijos"):
        err(f"generalizacion_actores[{g['id']}]: sin hijos.")
    for h in g.get("hijos", []):
        if h not in actores:
            err(f"generalizacion_actores[{g['id']}]: el hijo '{h}' no es un actor.")
        if h in padre_de:
            err(f"generalizacion_actores: '{h}' tiene dos padres ({padre_de[h]} y {g['id']}).")
        padre_de[h] = g["id"]
    if any(g["id"] in c["actores"] for c in M["casos_uso"]):
        err(f"generalizacion_actores[{g['id']}]: un padre abstracto no participa en casos de uso; sus hijos los heredarían.")

# 6. Relaciones entre casos de uso ----------------------------------------------
for rel in M["relaciones_cu"]:
    for extremo in ("origen", "destino"):
        if rel[extremo] not in casos:
            err(f"relaciones_cu: {rel[extremo]} no existe.")
    if casos.get(rel["origen"], {}).get("subsistema") != casos.get(rel["destino"], {}).get("subsistema"):
        err(f"relaciones_cu {rel['origen']}->{rel['destino']}: cruza subsistemas; el diagrama no la mostraría.")
    if rel["tipo"] not in ("include", "extend"):
        err(f"relaciones_cu: tipo '{rel['tipo']}' inválido.")

# 7/8. Casos de uso detallados ---------------------------------------------------
detallados = [c for c in M["casos_uso"] if c.get("detallado")]
# la plantilla pide Descripción, Modelo Estructural y Modelo Dinámico para cada caso de uso
for c in M["casos_uso"]:
    if not c.get("detallado"):
        avi(f"{c['id']} no está detallado: su sección queda sin ficha completa, clases ni secuencia.")
for c in detallados:
    cid = c["id"]
    for campo in ("descripcion", "precondiciones", "poscondiciones", "flujo", "excepciones",
                  "creado_por", "fecha_creacion", "modificado_por", "fecha_modificacion"):
        if not c.get(campo):
            err(f"{cid} detallado sin '{campo}'.")
    permitidos = set(c["actores"]) | {"Sistema"}
    for i, paso in enumerate(c.get("flujo") or [], 1):
        if paso["actor"] not in permitidos:
            err(f"{cid} paso {i}: el actor '{paso['actor']}' no está entre los actores del caso de uso.")
        if not paso.get("accion") or not paso.get("respuesta"):
            err(f"{cid} paso {i}: falta acción o respuesta del sistema.")
    for e in (c.get("alternativos") or []) + (c.get("excepciones") or []):
        r = e.get("requisito")
        if r and r not in requisitos:
            err(f"{cid} {e.get('id')}: requisito {r} inexistente.")
        elif r and cid not in (requisitos[r].get("casos_uso") or []):
            err(f"{cid} {e.get('id')}: cita {r}, que no está marcado para {cid} en la matriz.")
        if "paso" in e and not 1 <= e["paso"] <= len(c.get("flujo") or []):
            err(f"{cid} {e.get('id')}: el paso {e['paso']} no existe en el flujo normal.")
        if "continua" in e and e not in (c.get("alternativos") or []):
            err(f"{cid} {e.get('id')}: 'continua' solo vale en un flujo alternativo; una excepción termina el caso.")
        if e.get("continua") and "paso" not in e:
            err(f"{cid} {e.get('id')}: 'continua' necesita el 'paso' donde se bifurca.")
    # el caso detallado debe declarar sus clases
    if cid not in M["clases_cu"]:
        err(f"{cid} detallado sin entrada en clases_cu.")

# 9. Clases por caso de uso ------------------------------------------------------
for cid, capas in M["clases_cu"].items():
    if cid not in casos:
        err(f"clases_cu: {cid} no existe como caso de uso.")
    for e in capas.get("entity", []):
        if e not in entidades:
            err(f"clases_cu[{cid}]: la entidad '{e}' no está declarada en entidades.")
    for p in capas.get("puertos", []):
        if p not in puertos:
            err(f"clases_cu[{cid}]: el puerto '{p}' no está declarado en puertos.")
    for capa in ("boundary", "control"):
        if not capas.get(capa):
            err(f"clases_cu[{cid}]: capa '{capa}' vacía.")

# 10. Entidades y atributos ------------------------------------------------------
for nombre, e in entidades.items():
    pks = [a for a in e["atributos"] if a.get("pk")]
    compuesta = e.get("pk_compuesta")
    if e.get("tabla") and not compuesta and len(pks) != 1:
        err(f"{nombre}: una entidad persistente necesita exactamente una clave primaria (tiene {len(pks)}).")
    if compuesta:
        if pks:
            err(f"{nombre}: declara clave primaria compuesta y además un atributo pk.")
        foraneas = {r["fk_col"] for r in M["relaciones"] if r["fk_en"] == e["tabla"]}
        for c in compuesta:
            if c not in foraneas:
                err(f"{nombre}: la clave compuesta nombra '{c}', que no es una foránea de {e['tabla']}.")
    if e.get("objeto_valor") and e.get("tabla"):
        err(f"{nombre}: un objeto de valor no lleva tabla.")
    for a in e["atributos"]:
        if a.get("derivado") and a.get("sql"):
            err(f"{nombre}.{a['n']}: un atributo derivado no debe tener columna SQL.")
        if e.get("tabla") and not a.get("derivado") and not a.get("sql"):
            err(f"{nombre}.{a['n']}: atributo persistente sin tipo SQL.")

# 11. Relaciones entre entidades -------------------------------------------------
vistas = Counter()
for r in M["relaciones"]:
    for extremo in ("a", "b"):
        if r[extremo] not in entidades:
            err(f"relaciones: la entidad '{r[extremo]}' no existe.")
    if r["fk_en"] not in tablas:
        err(f"relaciones {r['a']}->{r['b']}: fk_en '{r['fk_en']}' no es una tabla declarada.")
    else:
        cols = {a["n"] for a in tablas[r["fk_en"]]["atributos"]}
        if r["fk_col"] in cols:
            err(f"relaciones {r['a']}->{r['b']}: fk_col '{r['fk_col']}' choca con un atributo de {r['fk_en']}.")
    vistas[(r["fk_en"], r["fk_col"])] += 1
for (t, c), n in vistas.items():
    if n > 1:
        err(f"La columna {t}.{c} se declara {n} veces como clave foránea.")

# 12. Máquinas de estado ---------------------------------------------------------
for ent, maq in M["estados"].items():
    if ent not in entidades:
        err(f"estados: la entidad '{ent}' no existe.")
        continue
    nombres = {e["n"] for e in maq["estados"]}
    if maq["inicial"] not in nombres:
        err(f"estados[{ent}]: estado inicial '{maq['inicial']}' no declarado.")
    for f in maq.get("finales", []):
        if f not in nombres:
            err(f"estados[{ent}]: estado final '{f}' no declarado.")
    alcanzables = {maq["inicial"]}
    for t in maq["transiciones"]:
        for extremo in ("de", "a"):
            if t[extremo] not in nombres:
                err(f"estados[{ent}]: transición hacia estado inexistente '{t[extremo]}'.")
        alcanzables.add(t["a"])
        # toda transición pertenece a un caso de uso (checklist semántico, punto 3)
        cus_t = t.get("cu") or []
        cus_t = [cus_t] if isinstance(cus_t, str) else cus_t
        if not cus_t:
            err(f"estados[{ent}] {t['de']} -> {t['a']}: la transición no declara el caso de uso que la dispara.")
        for cu in cus_t:
            if cu not in casos:
                err(f"estados[{ent}] {t['de']} -> {t['a']}: el caso de uso {cu} no existe.")
    for cu in maq.get("creado_en", []):
        if cu not in casos:
            err(f"estados[{ent}].creado_en: el caso de uso {cu} no existe.")
    for n in nombres - alcanzables:
        err(f"estados[{ent}]: el estado '{n}' es inalcanzable.")
    # la entidad debe tener un atributo 'estado' que lo soporte
    if not any(a["n"] == "estado" for a in entidades[ent]["atributos"]):
        err(f"estados[{ent}]: la entidad no declara el atributo 'estado'.")

# 12b. Secuencias -----------------------------------------------------------------
ABRE = {"alt", "loop", "opt"}
for cid, s in M.get("secuencias", {}).items():
    if cid not in casos:
        err(f"secuencias: {cid} no existe como caso de uso."); continue
    if not casos[cid].get("detallado"):
        err(f"secuencias[{cid}]: solo los casos detallados llevan diagrama de interacción.")
    ids = [p_["id"] for p_ in s["participantes"]]
    for d, n in Counter(ids).items():
        if n > 1:
            err(f"secuencias[{cid}]: participante '{d}' declarado {n} veces.")
    capas = M["clases_cu"].get(cid, {})
    declaradas = set(capas.get("boundary", [])) | set(capas.get("control", [])) | \
                 set(capas.get("entity", [])) | set(capas.get("puertos", []))
    nombres_actores = {actores[a]["nombre"] for a in casos[cid]["actores"]}
    for p_ in s["participantes"]:
        if p_["tipo"] == "actor":
            if p_["nombre"] not in nombres_actores:
                err(f"secuencias[{cid}]: el actor '{p_['nombre']}' no participa en {cid}.")
        elif p_["nombre"] not in declaradas:
            err(f"secuencias[{cid}]: '{p_['nombre']}' no está en clases_cu[{cid}].")
    pila = []
    for i, m in enumerate(s["mensajes"], 1):
        if "frag" in m:
            f = m["frag"]
            if f in ABRE:
                pila.append(f)
            elif f == "else":
                if not pila or pila[-1] != "alt":
                    err(f"secuencias[{cid}] msg {i}: 'else' fuera de un fragmento 'alt'.")
            elif f == "end":
                if not pila:
                    err(f"secuencias[{cid}] msg {i}: 'end' sin fragmento abierto.")
                else:
                    pila.pop()
            else:
                err(f"secuencias[{cid}] msg {i}: fragmento '{f}' desconocido.")
            continue
        for extremo in ("de", "a"):
            if m[extremo] not in ids:
                err(f"secuencias[{cid}] msg {i}: participante '{m[extremo]}' no declarado.")
        if not m.get("msg"):
            err(f"secuencias[{cid}] msg {i}: sin texto de mensaje.")
    if pila:
        err(f"secuencias[{cid}]: quedan {len(pila)} fragmento(s) sin cerrar: {pila}")
    porid = {p_["id"]: p_ for p_ in s["participantes"]}
    for i, m in enumerate(s["mensajes"], 1):
        if "frag" in m or m.get("tipo") == "return":
            continue
        d = porid.get(m["a"], {})
        if d.get("tipo") == "interface":
            firmas = {x.split("(")[0] for x in puertos[d["nombre"]]["metodos"]}
            if m["msg"].split("(")[0] not in firmas:
                err(f"secuencias[{cid}] msg {i}: '{m['msg']}' no es un método declarado de {d['nombre']} ({sorted(firmas)}).")
for c in detallados:
    if c["id"] not in M.get("secuencias", {}):
        err(f"{c['id']} detallado sin diagrama de interacción en secuencias.")

# 12c. Decisiones y trazabilidad --------------------------------------------------
vistos = set()
for d in M.get("decisiones", []):
    if d["id"] in vistos:
        err(f"decisiones: {d['id']} duplicado.")
    vistos.add(d["id"])
    for campo in ("tema", "hallazgo", "resolucion"):
        if not d.get(campo):
            err(f"decisiones[{d['id']}]: falta '{campo}'.")
for tr in M.get("trazabilidad", []):
    if tr["clase"] not in entidades:
        err(f"trazabilidad: la clase '{tr['clase']}' no existe en entidades.")
    if tr["estado"] not in ("implementado", "especificado"):
        err(f"trazabilidad[{tr['clase']}]: estado '{tr['estado']}' inválido.")

# 13. Vocabulario ----------------------------------------------------------------
for v in M["vocabulario"]:
    if v["clase"] == "—":
        for d in v.get("derivado_de", []):
            if d not in entidades:
                err(f"vocabulario: '{v['termino']}' se deriva de '{d}', que no existe.")
        continue
    if v["clase"] not in entidades:
        avi(f"vocabulario: '{v['termino']}' apunta a la clase '{v['clase']}', que no está en entidades.")

# ------------------------------------------------------------------------------
print("=" * 74)
print(f"  Validación del modelo — {len(requisitos)} requisitos · {len(casos)} casos de uso · "
      f"{len(entidades)} entidades · {len(tablas)} tablas · {len(M.get(chr(39)+chr(39), []) or M.get('secuencias', {}))} secuencias")
print("=" * 74)
for a in avisos:
    print(f"  aviso  {a}")
for e in errores:
    print(f"  ERROR  {e}")
if errores:
    print(f"\n{len(errores)} error(es). El modelo no es consistente.")
    sys.exit(1)
print(f"\nSin errores{' (' + str(len(avisos)) + ' aviso(s))' if avisos else ''}. El modelo es consistente.")
