"""Carga modelo.yaml y resuelve las referencias por id a nombres.

En el YAML cada clase, componente y puerto se declara UNA vez con `id` (estable) y `nombre`
(visible). Todo lo demás lo referencia por id. Renombrar una clase es cambiar su `nombre`:
los generadores reciben el modelo ya resuelto y no ven ids.

Una referencia a un id inexistente es un error de carga, no un diagrama con un nombre roto.
"""
import pathlib, re, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INTERPOLA = re.compile(r"\{([a-z][a-z0-9_]*)\}")


class ModeloError(Exception):
    def __init__(self, errores):
        super().__init__("\n".join(errores))
        self.errores = errores


def _interpolar(valor, nombres, err, donde):
    """Reemplaza {id} por el nombre en cualquier cadena del modelo."""
    if isinstance(valor, str):
        def sub(m):
            if m.group(1) not in nombres:
                err(f"{donde}: '{{{m.group(1)}}}' no es un id declarado.")
                return m.group(0)
            return nombres[m.group(1)]
        return INTERPOLA.sub(sub, valor)
    if isinstance(valor, list):
        return [_interpolar(v, nombres, err, donde) for v in valor]
    if isinstance(valor, dict):
        return {k: _interpolar(v, nombres, err, donde) for k, v in valor.items()}
    return valor


def cargar(ruta=None):
    M = yaml.safe_load((pathlib.Path(ruta) if ruta else RAIZ / "modelo.yaml").read_text(encoding="utf-8"))
    errores = []
    err = errores.append

    # 1. Registro de ids: entidades, componentes, puertos. Un id, un nombre.
    nombres, tipo_de = {}, {}
    for seccion, tipo in (("entidades", "entidad"), ("componentes", "componente"), ("puertos", "puerto")):
        for x in M.get(seccion, []):
            i = x.get("id")
            if not i:
                err(f"{seccion}: '{x.get('nombre')}' no declara id.")
                continue
            if i in nombres:
                err(f"{seccion}: el id '{i}' está duplicado.")
            nombres[i] = x["nombre"]
            tipo_de[i] = tipo
    # los nombres visibles tampoco pueden repetirse: serían la misma clase en dos diagramas
    vistos = {}
    for i, n in nombres.items():
        if n in vistos:
            err(f"el nombre '{n}' lo usan dos ids: '{vistos[n]}' y '{i}'.")
        vistos[n] = i
    tabla_de = {e["id"]: e["tabla"] for e in M.get("entidades", []) if e.get("tabla") and e.get("id")}

    def ref(i, tipo, donde):
        if i not in nombres:
            err(f"{donde}: el id '{i}' no existe.")
            return str(i)
        if tipo_de[i] != tipo:
            err(f"{donde}: '{i}' es {tipo_de[i]}, se esperaba {tipo}.")
        return nombres[i]

    # 1b. Ningún texto puede nombrar una clase a mano: debe usar {id}, o el renombre la dejaría atrás
    camel = [n for n in nombres.values() if len(re.findall("[A-Z]", n)) >= 2]
    patron = re.compile(r"(?<![A-Za-z0-9_{])(" + "|".join(sorted(map(re.escape, camel), key=len, reverse=True)) + r")(?![A-Za-z0-9_}])")

    def literales(v, donde):
        if isinstance(v, str):
            for m in patron.finditer(v):
                i = next(k for k, n in nombres.items() if n == m.group(1))
                err(f"{donde}: '{m.group(1)}' escrito a mano; usar {{{i}}}.")
        elif isinstance(v, list):
            for x in v:
                literales(x, donde)
        elif isinstance(v, dict):
            for k, x in v.items():
                if k not in ("nombre", "ref"):
                    literales(x, f"{donde}.{k}")
    literales({k: v for k, v in M.items() if k not in ("entidades", "componentes", "puertos")}, "texto")

    # 2. Referencias estructurales
    for r in M.get("relaciones", []):
        d = f"relaciones {r.get('a')}->{r.get('b')}"
        r["a"] = ref(r["a"], "entidad", d)
        r["b"] = ref(r["b"], "entidad", d)
        if r["fk_en"] not in tabla_de:
            err(f"{d}: fk_en '{r['fk_en']}' no es una entidad persistente.")
        else:
            r["fk_en"] = tabla_de[r["fk_en"]]

    for p in M.get("puertos", []):
        comp = next((x for x in M.get("componentes", []) if x.get("id") == p["adaptador"]), {})
        if comp.get("capa") != "adapter" or comp.get("contenedor") not in ("bd", "archivos", "erp", "ecms"):
            err(f"puertos[{p['id']}]: el adaptador '{p['adaptador']}' debe ser un componente capa adapter con contenedor bd|archivos|erp|ecms.")
        p["contenedor"] = comp.get("contenedor")
        p["adaptador"] = ref(p["adaptador"], "componente", f"puertos[{p['id']}].adaptador")

    for cid, c in M.get("clases_cu", {}).items():
        for capa, tipo in (("boundary", "componente"), ("control", "componente"),
                           ("entity", "entidad"), ("puertos", "puerto")):
            c[capa] = [ref(i, tipo, f"clases_cu[{cid}].{capa}") for i in c.get(capa, [])]

    M["estados"] = {ref(i, "entidad", "estados"): maq for i, maq in M.get("estados", {}).items()}

    for cid, s in M.get("secuencias", {}).items():
        actores = {a["id"]: a["nombre"] for a in M["actores"]}
        for p in s["participantes"]:
            if p["tipo"] == "actor":
                p.setdefault("nombre", actores.get(p["id"], p["id"]))
            elif "ref" in p:
                p["nombre"] = nombres.get(p["ref"]) or (err(f"secuencias[{cid}]: ref '{p['ref']}' no existe.") or p["ref"])
            else:
                err(f"secuencias[{cid}]: el participante '{p['id']}' no declara ref.")

    for t in M.get("trazabilidad", []):
        t["clase"] = ref(t["clase"], "entidad", "trazabilidad")

    for v in M.get("vocabulario", []):
        if v["clase"] != "—":
            v["clase"] = ref(v["clase"], "entidad", f"vocabulario[{v['termino']}]")
        v["derivado_de"] = [ref(i, "entidad", f"vocabulario[{v['termino']}].derivado_de")
                            for i in v.get("derivado_de", [])] or v.get("derivado_de", [])

    # 3. {id} en cualquier texto del modelo (mensajes de secuencia, prosa)
    M = _interpolar(M, nombres, err, "texto")
    if errores:
        raise ModeloError(errores)
    return M
