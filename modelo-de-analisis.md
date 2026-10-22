# Modelo de Análisis — Obra Studio

*Ingeniería del Software 2 · Trabajo Práctico Final · Dr. Emilio Gutiérrez Rodríguez*  
*Autores: Rojas, Sebastián · Taveira, Baltazar · Scotover, Leandro*

Este archivo acompaña a [requerimientos-consolidados.md](requerimientos-consolidados.md) y al entregable `TPF-Obra-Studio.docx`. Reúne lo que no entra en la plantilla de la cátedra: el catálogo de casos de uso, las máquinas de estado, las decisiones de modelado, las vistas de arquitectura y la trazabilidad con la implementación.

Todo su contenido y todos los diagramas se generan desde `modelo/modelo.yaml`, que es la única fuente de verdad. Para reproducirlos, ejecutar `modelo/build.sh`.

## 1. Alcance

| Módulo | Nombre | Situación |
|---|---|---|
| `ecms.budgets` | Presupuestos | Desarrollado |
| `ecms.acu` | Análisis de Costo Unitario | Desarrollado |
| `ecms.certifications` | Certificaciones | Desarrollado |
| `ecms.subcontracts` | Subcontratos | Desarrollado |
| `erp.invoices` | Facturas | Desarrollado |
| `erp.payments` | Pagos | Desarrollado |
| `ecms.stock` | — | Excluido: PR-07 excluye la operación de inventario y almacén. |
| `ecms.rrhh` | — | Excluido: Fuera del alcance de presupuesto, medición y certificación. |
| `ecms.partes` | — | Excluido: La vía C del motor de costos se documenta sin desarrollar partes diarios. |
| `erp.petty-cash` | — | Excluido: Compras menores no intervienen en la cadena de certificación. |
| `erp.finance` | — | Excluido: Contabilidad y tesorería se tratan como contexto de interacción ERP. |

## 2. Vocabulario

La columna «Clase» nombra la clase del modelo; «Implementación» indica su contraparte en el código, cuando existe.

| Término | Inglés | Clase | Implementación |
|---|---|---|---|
| Obra | work site | `Obra` | projects (fila) |
| Presupuesto | budget | `Presupuesto` | ProjectFile / budgets |
| Versión de presupuesto | budget version | `VersionPresupuesto` | budgets.revision + budget_operations |
| Rubro | chapter | `LineaPresupuesto` | CostItem.rowType='chapter' |
| Ítem | budget line | `LineaPresupuesto` | CostItem.rowType='begrotingspost' |
| ACU | unit cost analysis | `AnalisisCostoUnitario` | CostItem.acu + calculateAcu() |
| Medición oficial | official measurement | `MedicionOficial` | no implementado (especificado) |
| Período | period | `Periodo` | no implementado (especificado) |
| Certificado de avance | advance certificate | `Certificado` | no implementado (especificado) |
| Valorización | valuation | `Valorizacion` | extiende el wiki: importe calculado del certificado |
| Movimiento presupuestario | budget movement | `MovimientoPresupuestario` | budgets kind='adendas', capítulo AD-N |
| Subcontrato | subcontract | `Subcontrato` | no implementado (especificado) |
| Socio | partner | `Socio` | no implementado (especificado) |
| Curva S | S-curve | `—` | extiende el wiki: reporte derivado, sin tabla propia |
| Fondo de reparo | retention fund | `RetencionAplicada` | no implementado (especificado) |

## 3. Catálogo de casos de uso

| ID | Caso de uso | Subsistema | Actores | Requisitos |
|---|---|---|---|---|
| CU-01 | Crear obra y asignar responsables | Presupuesto y Medición | Administrador | RF-01 |
| CU-02 | Importar presupuesto y cronograma **(detallado)** | Presupuesto y Medición | Ingeniero de Obra | RF-02, RF-03, RF-04, RF-06 |
| CU-03 | Confirmar estructura y activar versión vigente | Presupuesto y Medición | Administrador | RF-05 |
| CU-04 | Registrar medición oficial | Presupuesto y Medición | Ingeniero de Obra | RF-07, RF-10 |
| CU-05 | Aprobar o rechazar medición oficial **(detallado)** | Presupuesto y Medición | Responsable Técnico | RF-08, RF-09 |
| CU-06 | Cerrar período de medición | Presupuesto y Medición | Responsable Técnico | RF-11 |
| CU-07 | Generar borrador de certificado | Certificación y Subcontratos | Ingeniero de Obra | RF-09, RF-12, RF-13, RF-14, RF-15, RF-22 |
| CU-08 | Corregir certificado emitido | Certificación y Subcontratos | Ingeniero de Obra | RF-16 |
| CU-09 | Emitir certificado de avance **(detallado)** | Certificación y Subcontratos | Ingeniero de Obra, Administrador | RF-17, RF-18 |
| CU-10 | Derivar documento financiero en ERP | Certificación y Subcontratos | Motor de Ingeniería, Sistema ERP, Finanzas y Tesorería | RF-14, RF-18 |
| CU-11 | Proponer y aprobar movimiento presupuestario | Presupuesto y Medición | Administrador, Responsable Técnico, Cliente | RF-06, RF-09, RF-19, RF-20, RF-21, RF-22 |
| CU-12 | Registrar contrato de subcontrato | Certificación y Subcontratos | Administrador | RF-23 |
| CU-13 | Presentar medición de subcontrato | Certificación y Subcontratos | Subcontratista | RF-24 |
| CU-14 | Certificar y valorizar subcontrato | Certificación y Subcontratos | Responsable Técnico, Subcontratista, Sistema ERP | RF-10, RF-25 |
| CU-15 | Calcular costos por vía | Presupuesto y Medición | Ingeniero de Obra, Motor de Ingeniería | RF-26 |
| CU-16 | Consultar reportes y Curva S | Certificación y Subcontratos | Administrador, Responsable Técnico | RF-27, RF-28 |

Relaciones entre casos de uso:

- `CU-09` **«include»** `CU-10`
- `CU-14` **«include»** `CU-10`
- `CU-11` **«extend»** `CU-05`

## 4. Máquinas de estado

### VersionPresupuesto

![Estados de VersionPresupuesto](modelo/out/12-estado-VersionPresupuesto.png)

| Estado | Significado |
|---|---|
| Propuesta | Importada y registrada; espera la confirmación de estructura y la activación. |
| Vigente | Rige para medición, certificación y control de saldo. |
| Reemplazada | Un movimiento aprobado generó una versión posterior; permanece consultable. |
| Descartada | El Administrador no confirmó su estructura; no llegó a regir. |

| Desde | Evento | Guarda | Hacia |
|---|---|---|---|
| Propuesta | confirmar estructura y activar | estructura confirmada | Vigente |
| Propuesta | descartar | — | Descartada |
| Vigente | activar versión posterior | — | Reemplazada |

### MedicionOficial

![Estados de MedicionOficial](modelo/out/13-estado-MedicionOficial.png)

| Estado | Significado |
|---|---|
| Registrada | Cargada por el Ingeniero de Obra con su evidencia; espera decisión. |
| Aprobada | El Responsable Técnico la validó; su cantidad cubierta es certificable. |
| Rechazada | Devuelta con motivo; no integra el acumulado físico. |

| Desde | Evento | Guarda | Hacia |
|---|---|---|---|
| Registrada | aprobar | — | Aprobada |
| Registrada | rechazar | motivo informado | Rechazada |
| Rechazada | corregir y reenviar | — | Registrada |

### Certificado

![Estados de Certificado](modelo/out/14-estado-Certificado.png)

| Estado | Significado |
|---|---|
| Borrador | En preparación o corrección; todavía no se emitió. Editable. |
| Emitido | Con número, fecha y actor; visible en el avance físico-financiero de la obra y publicado al ERP. |

| Desde | Evento | Guarda | Hacia |
|---|---|---|---|
| Borrador | emitir | — | Emitido |
| Emitido | corregir / crea revisión nueva y conserva la anterior | — | Borrador |

### MovimientoPresupuestario

![Estados de MovimientoPresupuestario](modelo/out/15-estado-MovimientoPresupuestario.png)

| Estado | Significado |
|---|---|
| Propuesto | Registrado con tipo, objetivo, motivo y respaldo documental. |
| AprobadoInterno | La organización lo aprobó; todavía no modifica el presupuesto. |
| AprobadoContractual | El comitente lo aceptó; habilita la nueva versión. |
| Vigente | Generó una versión de presupuesto nueva que ya rige. |
| Rechazado | No prosperó; el presupuesto vigente no cambia. |

| Desde | Evento | Guarda | Hacia |
|---|---|---|---|
| Propuesto | aprobar internamente | datos completos y dentro del límite | AprobadoInterno |
| Propuesto | rechazar | — | Rechazado |
| AprobadoInterno | aprobar contractualmente | — | AprobadoContractual |
| AprobadoInterno | rechazar | — | Rechazado |
| AprobadoContractual | activar versión | — | Vigente |

## 5. Decisiones de modelado

Cada fila es una discrepancia hallada entre el catálogo de requerimientos y la documentación de dominio, con la resolución adoptada.

### D-01 — Términos ausentes en la documentación de dominio

**Hallazgo.** «Valorización» y «Curva S» no aparecen en ninguna versión de la documentación de Obra Studio.

**Resolución.** Se conservan como requisitos (RF-13, RF-25 y RF-27) y se declaran en la tabla de vocabulario como alcance que extiende el dominio documentado. Valorización designa el importe calculado del certificado; Curva S es un reporte derivado que no agrega tabla propia.

### D-02 — Aditivos y deductivos

**Hallazgo.** El catálogo habla de aditivos y deductivos; la documentación de dominio no usa esos términos.

**Resolución.** Se unifican en MovimientoPresupuestario con tipo AMPLIACION, DEDUCCION o VARIACION_PRECIO, que es el vocabulario del dominio.

### D-03 — Rol de responsable técnico

**Hallazgo.** El catálogo nombra un «responsable técnico» que no existe como rol en el dominio.

**Resolución.** Se asimila al Supervisor de la obra: es el actor que aprueba o rechaza las mediciones y cierra el período. Es un actor, no un rol: en el sistema opera como miembro o admin (D-08).

### D-04 — Idempotencia de la importación

**Hallazgo.** RNF-07 exige que recargar el mismo XLSX no cree otra versión, pero la implementación actual calcula el hash sobre el documento ya confirmado y no sobre el archivo.

**Resolución.** ArchivoOrigen declara hashSHA256 sobre el contenido del archivo y la importación lo consulta antes de crear una versión, de modo que el requisito se cumple tal como está enunciado.

### D-05 — Doble conteo de trabajo físico

**Hallazgo.** RF-10 exige impedir que una misma cantidad se contabilice dos veces, sin indicar el mecanismo.

**Resolución.** Existe una sola MedicionOficial por ítem y período, con el ejecutor como atributo en lugar de un registro separado para el subcontratista. El acumulado se incrementa una sola vez por construcción del modelo, no por una validación añadida.

### D-06 — Estados del movimiento presupuestario

**Hallazgo.** RF-21 exige aprobación interna y contractual separadas; el dominio no define estados para el movimiento.

**Resolución.** Se diseña el ciclo Propuesto, AprobadoInterno, AprobadoContractual y Vigente, más Rechazado. Solo la transición a Vigente genera una versión de presupuesto nueva.

### D-07 — Estados del certificado

**Hallazgo.** La documentación describe el certificado con tres, cuatro y cinco estados según el documento, y trata el rechazo unas veces como estado y otras como transición. El modelo anterior además cerraba el certificado al cerrar el período, aunque la emisión exigía el período ya cerrado.

**Resolución.** El certificado es un registro de avance, no un trámite: tiene dos estados, Borrador y Emitido, y no se cierra por período. Corregir un certificado emitido crea una revisión nueva en Borrador vinculada a la anterior, que se conserva. Su tipo es interno, subcontrato o adenda; el interno se refleja en el avance físico-financiero de la obra en el ERP o en el ECMS.

### D-08 — Modelo de permisos

**Hallazgo.** Una parte de la documentación define una matriz de roles y otra afirma que la aplicación no debe definir ningún rol.

**Resolución.** Se adopta un conjunto mínimo de roles, porque RNF-01 exige comprobar el rol: admin, miembro y visualizador, más miembro ERP (contadores) y miembro ECMS (asistente o fiscalizador de campo). Un actor no es un rol: el Ingeniero de Obra opera como miembro, el Responsable Técnico como miembro o admin, el Administrador (gerente) como admin, un auditor como visualizador y Finanzas y Tesorería como miembro ERP. El Subcontratista accede solo a su contrato (RNF-02). No se impone separación de funciones entre roles.

### D-09 — Propiedad del contrato de subcontrato

**Hallazgo.** Un documento asigna el contrato al ERP y otro al ECMS.

**Resolución.** Se aplica la regla de propiedad por naturaleza del registro: el hecho de campo pertenece al ECMS y el documento legal al ERP. El contrato es del ERP; el certificado, del ECMS.

### D-10 — Persistencia del árbol de presupuesto

**Hallazgo.** La implementación guarda el presupuesto como documento JSON y no como tablas normalizadas.

**Resolución.** El diagrama de entidad relación presenta el modelo normalizado, que es lo que corresponde al modelo de diseño. El almacenamiento documental se documenta como decisión de implementación y no altera el modelo conceptual.

### D-11 — Atributos derivados

**Hallazgo.** Importes como el acumulado certificado o el saldo podrían almacenarse y quedar desfasados.

**Resolución.** Se marcan como derivados en el diagrama de clases y se omiten como columnas en el diagrama de entidad relación: se calculan desde los registros aprobados y no pueden discrepar de su origen.

### D-12 — Alcance del trabajo

**Hallazgo.** Obra Studio no tiene ningún módulo de taller ni de fabricación, ni en la documentación ni en el catálogo de módulos de la implementación.

**Resolución.** No hay nada que excluir por ese concepto. El alcance se acota explícitamente a seis módulos y se declaran los excluidos con su motivo.

### D-13 — Activación de la versión de presupuesto

**Hallazgo.** CU-03 figuraba con el Administrador, pero CU-02 lo incluía y su flujo hacía que el Ingeniero de Obra solicitara la activación.

**Resolución.** Se separan: CU-02 termina con la versión en Propuesta y CU-03, del Administrador, confirma la estructura (RF-05) y la activa o la descarta. Se quita el include CU-02 → CU-03, porque activar es una meta propia del Administrador y no un paso común de varios casos.

### D-14 — Relaciones entre casos de uso de certificación

**Hallazgo.** CU-09 incluía CU-07 aunque su precondición exige que el borrador ya exista, y CU-08 extendía CU-09 aunque la corrección ocurre después de la emisión.

**Resolución.** Se quitan ambas relaciones: generar el borrador (CU-07) y corregir un emitido (CU-08) son metas propias que preceden o siguen a la emisión. Se mantienen CU-09 y CU-14 incluyendo CU-10 (subobjetivo común sin actor humano propio) y CU-11 extendiendo CU-05 en el exceso sobre saldo.

### D-15 — Motor de Ingeniería como actor

**Hallazgo.** El modelo de casos de uso declara al Motor de Ingeniería como actor sistema de CU-10 y CU-15, mientras las vistas C4 lo ubican como contenedor interno de Obra Studio.

**Resolución.** Se mantiene como actor de tipo sistema para representar los procesos que el motor ejecuta sin intervención de un usuario: el cálculo por vía y la publicación del evento hacia el ERP. La vista C4 describe la estructura y no los objetivos, por eso lo ubica dentro del sistema.

### D-16 — Requisitos redefinidos respecto del catálogo

**Hallazgo.** RF-16, RF-17, RF-22 y RNF-05 suponían un certificado con revisión por dos personas, cierre y reapertura autorizada; las excepciones de CU-09 citaban RNF-06 sin que el catálogo lo marcara.

**Resolución.** Se redefinen los cuatro para el certificado de dos estados y los roles mínimos (D-07, D-08): RF-16 corrige mediante revisión nueva, RF-17 limita quién emite, RF-22 conserva solo la certificación de pendientes cubiertos y RNF-05 habla de certificados emitidos. RNF-06 se marca en CU-09, que calcula la valorización.

### D-17 — Pendiente: camino del certificado de adenda y facturación al cliente

**Hallazgo.** El certificado de adenda sigue un camino distinto al de los ítems presupuestados, pero el modelo tiene un solo flujo (CU-07 → CU-09). RF-14 y PR-06 hablan de factura derivada del certificado; el certificado interno se refleja en el avance físico-financiero.

**Resolución.** Pendiente: falta definir el camino del certificado de adenda (si exige el movimiento vigente, quién lo emite) y desde qué certificado factura el ERP al cliente.

### D-18 — Pendiente: medición presentada por el subcontratista

**Hallazgo.** CU-13 hace que el Subcontratista presente mediciones de su contrato, y D-05 establece una sola MedicionOficial por ítem y período, con el ejecutor como atributo.

**Resolución.** Pendiente: falta decidir si lo que presenta el Subcontratista es la medición oficial con ejecutor subcontratado o una presentación previa que el Ingeniero de Obra convierte en oficial, y quién la aprueba.

### D-19 — Pendiente: frontera del ERP

**Hallazgo.** El alcance incluye los módulos erp.invoices y erp.payments, pero las vistas C4 y el catálogo de actores tratan al ERP como sistema externo.

**Resolución.** Pendiente: falta decidir si facturas y pagos se desarrollan en este modelo o quedan como interacción con el ERP, y ajustar el alcance o el actor según corresponda.

## 6. Arquitectura

El Motor ECMS aplica Clean Architecture en cuatro anillos; las dependencias apuntan siempre hacia adentro. Los estereotipos de análisis son su proyección en UML:

| Estereotipo UML | Anillo | Responsabilidad |
|---|---|---|
| `«Boundary»` | Adaptadores de interfaz | Traduce la petición y presenta el resultado. |
| `«Control»` | Casos de uso | Orquesta entidades y puertos. |
| `«Entity»` | Dominio | Concentra la regla de negocio y sus invariantes. |
| `«Interface»` | Dominio (puertos) | Invierte la dependencia hacia la infraestructura. |

Puertos declarados por el dominio:

| Puerto | Operaciones | Adaptador |
|---|---|---|
| `IPresupuestoRepositorio` | `buscarVersionVigente(obraId)`, `buscarPorHash(hash)`, `guardarVersion(version)` | `PresupuestoRepositorioSQL` |
| `IAlmacenArchivos` | `guardar(archivo)`, `recuperar(ruta)` | `AlmacenArchivosS3` |
| `ILectorPlanilla` | `leer(archivo)`, `detectarEstructura(hojas)` | `LectorPlanillaXLSX` |
| `IMedicionRepositorio` | `listarPorPeriodo(periodoId)`, `guardar(medicion)`, `acumuladoAprobado(lineaId)` | `MedicionRepositorioSQL` |
| `ICertificadoRepositorio` | `buscarRevision(revisionId)`, `guardar(certificado)`, `siguienteNumero(obraId)` | `CertificadoRepositorioSQL` |
| `IGeneradorDocumento` | `exportar(revision, formato)` | `GeneradorDocumentoXLSXPDF` |
| `IPublicadorEventos` | `publicar(evento)` | `PuenteERP` |
| `IAuditoriaRepositorio` | `registrar(entrada)` | `AuditoriaRepositorioSQL` |
| `IReloj` | `ahora()` | `RelojSistema` |

Vistas C4 generadas con C4-PlantUML (`modelo/gen/gen_c4.py`, salida en `modelo/out/c4/`):


**Contexto.** Obra Studio y su entorno.

![Contexto](modelo/out/c4/C4-Contexto.png)

**Contenedores.** Estructura interna de Obra Studio.

![Contenedores](modelo/out/c4/C4-Contenedores.png)

**Componentes.** Los cuatro anillos de Clean Architecture dentro del Motor ECMS.

![Componentes](modelo/out/c4/C4-Componentes.png)

**CU02.** Interacción de componentes al importar el presupuesto.

![CU02](modelo/out/c4/C4-CU02.png)

**CU05.** Interacción de componentes al aprobar una medición.

![CU05](modelo/out/c4/C4-CU05.png)

**CU09.** Interacción de componentes al emitir un certificado.

![CU09](modelo/out/c4/C4-CU09.png)


Diagramas UML del entregable (`modelo/out/`):

| Archivo | Diagrama |
|---|---|
| `01-casos-de-uso-A.png` | casos de uso A |
| `02-casos-de-uso-B.png` | casos de uso B |
| `03-CU-02-clases.png` | CU 02 clases |
| `04-CU-05-clases.png` | CU 05 clases |
| `05-CU-09-clases.png` | CU 09 clases |
| `06-CU-02-secuencia.png` | CU 02 secuencia |
| `07-CU-05-secuencia.png` | CU 05 secuencia |
| `08-CU-09-secuencia.png` | CU 09 secuencia |
| `09-clases-persistentes-A.png` | clases persistentes A |
| `10-clases-persistentes-B.png` | clases persistentes B |
| `11-entidad-relacion.png` | entidad relacion |
| `12-estado-VersionPresupuesto.png` | estado VersionPresupuesto |
| `13-estado-MedicionOficial.png` | estado MedicionOficial |
| `14-estado-Certificado.png` | estado Certificado |
| `15-estado-MovimientoPresupuestario.png` | estado MovimientoPresupuestario |

## 7. Trazabilidad con la implementación

El motor de presupuesto está implementado; certificaciones y subcontratos están especificados en la documentación de dominio pero no implementados. Los diagramas de este trabajo son modelo de diseño, no transcripción del código.

| Clase del modelo | Situación | Contraparte |
|---|---|---|
| `Obra` | Implementado | Fila de la tabla projects. |
| `Presupuesto` | Implementado | Tabla budgets, con tipo cliente, costo o adendas. |
| `VersionPresupuesto` | Implementado | Columna revision más el diario inmutable budget_operations. |
| `LineaPresupuesto` | Implementado | CostItem dentro del documento del presupuesto. |
| `AnalisisCostoUnitario` | Implementado | Partida marcada como ACU y su cálculo. |
| `ArchivoOrigen` | Implementado | Importación con hash del contenido. |
| `InformeImportacion` | Implementado | Informe de importación con totales declarado y recalculado. |
| `MedicionOficial` | Especificado | Documentada en el dominio; sin implementación. |
| `Periodo` | Especificado | Documentada en el dominio; sin implementación. |
| `Certificado` | Especificado | Módulo de certificaciones presente en el catálogo, sin implementación. |
| `Subcontrato` | Especificado | Módulo de subcontratos presente en el catálogo, sin implementación. |
| `DocumentoFinancieroERP` | Especificado | Factura y pago del ERP; fuera del alcance implementado. |

## 8. Reproducibilidad

```
modelo/
  modelo.yaml      fuente única: actores, requisitos, casos de uso, entidades, estados, tablas
  gen/validar.py   chequeos de consistencia; el build falla si algo no cierra
  gen/gen_puml.py  genera los diagramas UML
  gen/gen_c4.py    genera las vistas C4-PlantUML
  gen/gen_dsl.py   genera el workspace de Structurizr
  gen/modelo.py    carga el YAML y resuelve ids a nombres
  gen/gen_docx.py  genera el documento con el formato de la cátedra
  gen/gen_md.py    genera este archivo
  build.sh         ejecuta todo lo anterior de punta a punta
```

`validar.py` comprueba, entre otras cosas, que los 48 identificadores del catálogo estén presentes sin duplicados, que cada requisito mapee a un caso de uso existente, que ningún caso de uso quede sin requisito, que toda clase citada en un diagrama exista en el modelo, que cada mensaje dirigido a un puerto sea uno de sus métodos declarados y que ningún estado sea inalcanzable.

