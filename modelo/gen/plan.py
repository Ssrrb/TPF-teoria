"""Qué diagrama va en cada sección de la plantilla «Manual de Análisis» y cómo se llama su archivo.

La plantilla fija el orden: Diagrama de Casos de Uso (Alto Nivel), Diagrama de Generalización de
Actores, Diagramas de Casos de Uso (refinados) y, por cada caso de uso, Descripción, Modelo
Estructural, Modelo Dinámico y Otros diagramas. Ese orden se declara solo aquí; gen_puml, gen_c4,
gen_docx, gen_md y verificar_salida lo leen. Los archivos se nombran por su contenido (caso de uso,
subsistema, entidad) y no por un número de orden: agregar un caso de uso no renombra los demás.
"""

# ------------------------------------------------------------------ nombres de archivo
def alto_nivel():            return "casos-de-uso-alto-nivel"
def generalizacion():        return "generalizacion-actores"
def casos_uso(sid):          return f"casos-de-uso-{sid}"
def clases(cid):             return f"{cid}-clases"
def secuencia(cid):          return f"{cid}-secuencia"
def actividades(cid):        return f"{cid}-actividades"
def estado(ent):             return f"estado-{ent}"
def persistentes(sid):       return f"clases-persistentes-{sid}"
def der():                   return "entidad-relacion"
def conceptual():            return "modelo-conceptual"
def c4_contexto(cid):        return f"C4-{cid.replace('-', '')}-contexto"
def c4_contenedores(cid):    return f"C4-{cid.replace('-', '')}-contenedores"
def c4_dinamica(cid):        return f"C4-{cid.replace('-', '')}"

# Dos figuras de clases persistentes: 28 clases en un solo lienzo resultan ilegibles.
GRUPOS_PERSISTENTES = [
    ("A", "Obra y presupuesto", ["Organización y seguridad", "Partes", "Obra y configuración", "Presupuesto"]),
    ("B", "Medición y certificación", ["Medición", "Certificación", "Subcontratos e integración ERP"]),
]


def fig(archivo, pie, c4=False, titulo=None, intro=None):
    return {"archivo": archivo, "carpeta": "c4" if c4 else "", "pie": pie, "titulo": titulo, "intro": intro}


# ------------------------------------------------------------------ estados por caso de uso
def cus(t):
    v = t.get("cu") or []
    return [v] if isinstance(v, str) else list(v)


def transiciones_de(M, cid):
    """{entidad: [eventos]} que el caso de uso dispara, según 'creado_en' de la máquina y el campo
    'cu' de cada transición."""
    r = {}
    for ent, maq in M["estados"].items():
        if cid in maq.get("creado_en", []):
            r.setdefault(ent, []).append(f'crear en {maq["inicial"]}')
        for t in maq["transiciones"]:
            if cid in cus(t):
                r.setdefault(ent, []).append(t["evento"])
    return r


def dueno_maquina(M):
    """Cada máquina de estados se dibuja completa una sola vez, porque la plantilla pide evitar
    redundancias: en el caso de uso que dispara más transiciones (crear la entidad no cuenta);
    ante empate, en el que lleva a un estado final y, si sigue el empate, en el primero del catálogo."""
    orden = {c["id"]: i for i, c in enumerate(M["casos_uso"])}
    dueno = {}
    for ent, maq in M["estados"].items():
        puntaje = {}
        for t in maq["transiciones"]:
            for cid in cus(t):
                n, final = puntaje.get(cid, (0, False))
                puntaje[cid] = (n + 1, final or t["a"] in maq.get("finales", []))
        if puntaje:
            dueno[ent] = min(puntaje, key=lambda c: (-puntaje[c][0], not puntaje[c][1], orden[c]))
    return dueno


def ramifica(c):
    """El flujo tiene caminos alternativos o de excepción anclados a un paso."""
    return any(x.get("paso") for x in (c.get("alternativos") or []) + (c.get("excepciones") or []))


# ------------------------------------------------------------------ plan del documento
def globales(M):
    """Secciones de diagramas previas a los casos de uso, en el orden de la plantilla."""
    sis = M["meta"]["sistema"]
    return [
        ("Diagrama de Casos de Uso (Alto Nivel)",
         [fig(alto_nivel(), f"Casos de uso de alto nivel de {sis}, agrupados por procesos.")]),
        ("Diagrama de Generalización de Actores",
         [fig(generalizacion(), "Generalización de actores.")]),
        ("Diagramas de Casos de Uso",
         [fig(casos_uso(sid), f'Casos de uso del subsistema {s["nombre"]}.',
              titulo=f'Sistema {sis} — Subsistema {s["nombre"]}', intro=s["descripcion"])
          for sid, s in sorted(M["subsistemas"].items())]),
    ]


def por_caso(M, c):
    """Las cuatro subsecciones de un caso de uso. Cada una es (título, figuras, referencias);
    las referencias apuntan a una máquina de estados dibujada en otro caso de uso."""
    cid = c["id"]
    detallado = cid in M["clases_cu"]
    desc = [fig(c4_contexto(cid), f"Contexto C4 del caso de uso {cid}.", c4=True)]
    if detallado:
        desc.append(fig(c4_contenedores(cid), f"Contenedores C4 que intervienen en {cid}.", c4=True))
    estructural = [fig(clases(cid), f"Clases del caso de uso {cid}.")] if detallado else []
    dinamico = []
    if cid in M["secuencias"]:
        dinamico = [fig(secuencia(cid), f"Interacción del caso de uso {cid}."),
                    fig(c4_dinamica(cid), f"Vista dinámica C4 de {cid} entre componentes.", c4=True)]
    otros, refs = [], []
    if c.get("flujo") and ramifica(c):
        otros.append(fig(actividades(cid), f"Actividades del caso de uso {cid}, con sus caminos alternativos y de excepción."))
    dueno = dueno_maquina(M)
    for ent, eventos in transiciones_de(M, cid).items():
        if dueno.get(ent) == cid:
            otros.append(fig(estado(ent), f"Estados de {ent}."))
        else:
            refs.append((ent, dueno[ent], eventos))
    return [("Descripción", desc, []), ("Modelo Estructural", estructural, []),
            ("Modelo Dinámico", dinamico, []), ("Otros diagramas", otros, refs)]


def diseno(M):
    return [
        ("Diagrama de Clases Persistentes",
         [fig(persistentes(sid), f"Clases persistentes ({sid}): {nombre.lower()}.")
          for sid, nombre, _ in GRUPOS_PERSISTENTES]),
        ("Diagrama de Entidad Relación", [fig(der(), "Diagrama de entidad relación.")]),
    ]


def figuras(M):
    """Todas las figuras del documento en orden; el índice + 1 es su número de figura."""
    r = [f for _, fs in globales(M) for f in fs]
    for c in M["casos_uso"]:
        r += [f for _, fs, _ in por_caso(M, c) for f in fs]
    r += [f for _, fs in diseno(M) for f in fs]
    return r


def numeros(M):
    return {f["archivo"]: i for i, f in enumerate(figuras(M), start=1)}
