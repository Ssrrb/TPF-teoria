# Requerimientos Consolidados — Obra Studio

*Universidad Católica Nuestra Señora de la Asunción · Facultad de Ciencias y Tecnología · Carrera de Análisis de Sistemas*  
*Trabajo Práctico Final · Ingeniería del Software 2*  
*Autores: Rojas, Taveira y Scotover · Docente: Dr. Emilio Gutiérrez Rodríguez · Año 2026*  
*Organización de referencia: Cuatro Projects S.R.L.*

## 1. Propósito y autoridad de las fuentes

Este catálogo establece los requerimientos consolidados para Obra Studio. El wiki gobierna el vocabulario, las entidades, las reglas de negocio, la propiedad de la información y los flujos ERP–ECMS. La captura de Cuatro Projects se usa para necesidades específicas cuando el wiki no define el tema y la necesidad no contradice las reglas del producto.

La base teórica de Análisis de Requerimientos — Objetivos Avanzados aporta trazabilidad entre captura, análisis, diseño y validación; modelado UML; modularidad; validación participativa; análisis de riesgos y gestión del cambio.

El alcance cubre presupuesto y movimientos, medición oficial, certificación de avance, subcontratos, cálculo de costos y reportes. Compras, almacén detallado, contabilidad y tesorería se incluyen como contexto de interacción ERP, sin desarrollar sus flujos completos.

El modelo conceptual, los casos de uso, los estados y los diagramas se encuentran en [modelo-de-analisis.md](modelo-de-analisis.md).

## 2. Fuentes consultadas

- Captura: [TPC 04 - Captura de Requerimientos - Rojas,Taveira,Scotover.pdf](<TPC 04 - Captura de Requerimientos - Rojas,Taveira,Scotover.pdf>).
- Gobierno y vocabulario: wiki/AGENTS.md.
- Dominio: docs/foundations/erp-ecms-architecture.mdx; docs/domain/budgets.mdx; docs/domain/acu.mdx; docs/domain/cost-engine.mdx; docs/domain/certifications.mdx; docs/domain/module-hierarchy.mdx.
- Arquitectura e integración: docs/system/architecture-overview.mdx; docs/system/erp-ecms-bridge.mdx.
- Flujo de interfaz compatible: docs/product/certification-workflow.mdx.
- Base teórica: [Análisis de Requerimientos — Objetivos Avanzados](https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingeniería+del+Software+2/2025/Clase+20+Análisis+de+Requerimientos/Zk+Análisis+de+Requerimientos+-+Objetivos+Avanzados).

## 3. Convenciones

- Cada identificador original se conserva como referencia estable.
- El enunciado de cada fila es el requerimiento consolidado para este modelo.
- ERP refiere al motor financiero y documental; ECMS, al motor de obra, medición y costos.
- El certificado de ECMS y la factura o el pago de ERP son registros distintos pero relacionados.
- **Wiki** identifica reglas del producto; **Complemento** identifica necesidades de Cuatro Projects compatibles con el wiki; **Wiki + Complemento** indica que el requisito combina ambos aportes.
- Este catálogo mantiene trazabilidad y criterios de aceptación; no compara documentos entre sí.
- **Movimiento presupuestario** es el término unificado para aditivo, deductivo y variación de precio; sus tipos son `AMPLIACION`, `DEDUCCION` y `VARIACION_PRECIO`.
- **Valorización** (importe calculado de un certificado) y **Curva S** no pertenecen al vocabulario del wiki: son alcance nuevo que este trabajo incorpora, y así se declaran en el modelo.
- **Responsable técnico** se corresponde con el rol de supervisor de obra; el ingeniero de obra registra, el responsable técnico aprueba y el administrador autoriza la emisión.

## 4. Requerimientos funcionales

| ID | Requerimiento consolidado | Origen | Caso / criterio de aceptación |
|---|---|---|---|
| RF-01 | El sistema permitirá crear una obra con datos identificatorios y asignar sus responsables. | Wiki | CU-01: cada obra queda asociada a responsables y organización. |
| RF-02 | El sistema permitirá cargar el XLSX de presupuesto y cronograma y conservar el archivo original asociado a su versión. | Complemento | CU-02: se recupera el archivo de origen de una versión. |
| RF-03 | El sistema identificará hojas, columnas y relaciones entre rubros e ítems e informará cada dato obligatorio inválido con su ubicación. | Complemento | CU-02: el error señala hoja, fila y columna. |
| RF-04 | El sistema mostrará diferencias entre totales declarados en el XLSX y totales recalculados, sin modificar el archivo original. | Complemento | CU-02: el usuario revisa ambos totales antes de confirmar. |
| RF-05 | El sistema permitirá confirmar rubros, unidades y agrupaciones antes de activar el presupuesto de una obra. | Wiki | CU-03: la versión no se activa sin confirmación de estructura. |
| RF-06 | El sistema conservará versiones del presupuesto y cronograma; cada modificación aprobada generará una versión nueva sin alterar anteriores. | Wiki + Complemento | CU-02/CU-11: se consulta la versión anterior y la nueva vigente. |
| RF-07 | El sistema permitirá registrar por período una medición oficial por ítem con cantidad, unidad, ejecutor propio o subcontratado y evidencia. | Wiki | CU-04: el registro conserva todos esos datos y su respaldo. |
| RF-08 | El sistema permitirá al responsable técnico aprobar o rechazar cada medición y conservar decisión, actor y fecha. | Wiki | CU-05: la decisión queda en el historial. |
| RF-09 | El sistema comparará la cantidad medida con el saldo del presupuesto vigente; el exceso quedará como propuesta pendiente y no formará parte de la medición oficial ni del certificado hasta que un movimiento aprobado lo cubra. | Complemento | CU-05/CU-07/CU-11: solo una cantidad cubierta por la versión vigente integra la medición oficial certificable. |
| RF-10 | El sistema impedirá contabilizar dos veces una misma cantidad de trabajo físico aunque la ejecute un subcontratista. | Complemento | CU-04/CU-14: el acumulado físico se incrementa una sola vez. |
| RF-11 | El sistema permitirá cerrar un período cuando sus mediciones estén resueltas y aprobadas. | Wiki | CU-06: un período con mediciones pendientes no se cierra. |
| RF-12 | El sistema generará el borrador de certificado con cantidades medidas y aprobadas que sean elegibles según el presupuesto vigente. | Wiki | CU-07: el borrador excluye cantidades sin aprobación o sin saldo. |
| RF-13 | El sistema calculará la valorización con cantidad certificable y precio de venta vigente, y aplicará impuestos y fondos según la configuración de la obra. | Wiki | CU-07: subtotal, impuestos y retenciones se reproducen desde su configuración. |
| RF-14 | El sistema mostrará la cantidad medida del período, las mediciones oficiales aprobadas acumuladas y el saldo del presupuesto vigente; cada certificado conservará el vínculo con su documento financiero ERP derivado. | Wiki | CU-07/CU-10: el acumulado físico coincide con las mediciones aprobadas y cada factura refiere a su certificado sin duplicarlo. |
| RF-15 | El sistema señalará en el borrador excesos, mediciones faltantes, precios sin movimiento vigente y diferencias de totales con sus datos de origen. | Complemento | CU-07: cada alerta identifica rubro/ítem y fuente. |
| RF-16 | El sistema permitirá corregir un certificado emitido creando una revisión nueva vinculada y conservando las revisiones anteriores. *(Redefinido.)* | Wiki | CU-08: la corrección mantiene vínculo con el antecedente y no lo sobrescribe. |
| RF-17 | El sistema permitirá emitir el certificado de avance solo a usuarios con rol admin o miembro con acceso al ECMS, y registrará quién lo emitió y cuándo. *(Redefinido.)* | Complemento | CU-09: un visualizador no puede emitir; cada emisión identifica a su actor y su fecha. |
| RF-18 | El sistema permitirá registrar número, fecha, destinatario y revisión del certificado, y exportar un archivo nuevo XLSX o PDF. | Wiki | CU-09/CU-10: el archivo corresponde a la revisión emitida y no sobrescribe sus fuentes. |
| RF-19 | El sistema permitirá proponer ampliaciones, deducciones y variaciones de precio asociadas a rubros o ítems, con motivo y respaldo. | Wiki | CU-11: el movimiento identifica tipo, objetivo, motivo y documento. |
| RF-20 | El sistema mostrará efecto monetario, límite, importe utilizado y saldo de cada propuesta, e impedirá aprobar datos incompletos o un exceso sin excepción registrada. | Complemento | CU-11: datos faltantes o exceso no autorizado impiden aprobar. |
| RF-21 | El sistema registrará por separado las aprobaciones interna y contractual de un movimiento presupuestario y solo entonces actualizará la versión vigente. | Complemento | CU-11: una sola aprobación no activa la versión. |
| RF-22 | El sistema certificará cantidades pendientes solo después de que un movimiento aprobado las cubra. *(Redefinido.)* | Wiki | CU-07/CU-11: la nueva cantidad certificable usa la versión vigente que refleja el movimiento. |
| RF-23 | El sistema permitirá registrar en ERP el contrato legal y vincularlo con el alcance técnico, rubros, precios, límites, impuestos y retenciones de la obra. | Wiki | CU-12: contrato ERP y alcance ECMS permanecen relacionados. |
| RF-24 | El sistema permitirá al subcontratista consultar solo el estado de sus mediciones, certificados, valorizaciones y saldos; las mediciones de su trabajo las registra el Ingeniero de Obra. *(Redefinido.)* | Wiki | CU-13: no puede registrar mediciones ni consultar otro contrato. |
| RF-25 | El sistema valorizará el certificado de subcontratista según el contrato, registrará esa valorización en el control de costos de ECMS y enviará el resultado aprobado a ERP para el proceso de pago, sin cambiar el precio de venta al cliente. | Wiki | CU-14: costo analítico, valorización contractual, precio de venta y pago se presentan por separado. |
| RF-26 | El sistema calculará costos por obra, rubro e ítem mediante materiales, mano de obra y equipos, y comparará los resultados con el presupuesto vigente, que refleja los movimientos aprobados. | Wiki | CU-15: cada importe identifica vía, período, fuente y naturaleza; el movimiento modifica el plan y no se registra como costo incurrido. |
| RF-27 | El sistema mostrará Curva S a una misma fecha de corte y separará avance físico, financiero y físico pendiente de movimiento presupuestario vigente. | Complemento | CU-16: las tres series comparten fecha y explican unidad/ponderación. |
| RF-28 | El sistema permitirá consultar presupuesto vigente, costos propios y subcontratados, certificaciones y saldos por obra/rubro, con acceso a cada respaldo. | Wiki | CU-16: cada cifra conduce a su registro o documento fuente. |

## 5. Requerimientos no funcionales

| ID | Requerimiento consolidado | Origen | Vínculo a caso / criterio de aceptación |
|---|---|---|---|
| RNF-01 | El sistema comprobará organización, pertenencia a la obra y rol antes de permitir leer o modificar información. | Wiki | CU-01 a CU-16: una cuenta sin permiso vigente no accede al registro. |
| RNF-02 | La vista del subcontratista se limitará a su contrato; no mostrará presupuestos internos, márgenes, salarios ni otros contratos. | Wiki | CU-13/CU-14: consultas fuera del contrato se deniegan. |
| RNF-03 | Una operación interrumpida no dejará un período parcialmente cerrado ni una modificación activa sin las aprobaciones requeridas. | Wiki | CU-06/CU-11: la operación queda en estado íntegro anterior o completo. |
| RNF-04 | El sistema conservará actor, fecha, obra, versión y evidencia para cada medición, revisión, aprobación, emisión y cambio relevante. | Wiki | CU-04 a CU-14: el historial permite reconstruir quién hizo qué y sobre qué versión. |
| RNF-05 | Los certificados emitidos y las versiones que los originaron permanecerán consultables; una corrección crea una revisión nueva. *(Redefinido.)* | Wiki | CU-08/CU-09: la revisión anterior no se sobrescribe y la corrección queda enlazada. |
| RNF-06 | Los cálculos monetarios usarán aritmética decimal y producirán el mismo resultado para iguales entradas, parámetros y versiones. | Wiki | CU-07/CU-09/CU-14/CU-15: repetir el cálculo con la misma instantánea devuelve el mismo importe. |
| RNF-07 | Volver a cargar el mismo XLSX sin cambios no creará otra versión de presupuesto o cronograma. | Complemento | CU-02: la repetición refiere la versión existente. |
| RNF-08 | Las copias de seguridad permitirán restaurar conjuntamente registros, adjuntos y versiones de una obra. | Complemento | CU-02/CU-07/CU-14: la restauración recupera relaciones y archivos. |
| RNF-09 | Los formularios de medición podrán utilizarse desde un teléfono e identificar campos requeridos y errores de carga. | Complemento | CU-04: el escenario de medición puede completarse desde vista móvil. |
| RNF-10 | Las operaciones principales podrán completarse con teclado, foco visible y mensajes de error identificables. | Complemento | CU-02/CU-04/CU-05/CU-07: el recorrido de teclado completa y comunica el flujo principal. |
| RNF-11 | Los reportes indicarán fecha de corte, unidad, moneda y procedencia de cada total. | Wiki | CU-10/CU-15/CU-16: ningún total carece de contexto de lectura. |
| RNF-12 | Toda certificación o valorización consultable permitirá recuperar presupuesto, mediciones y documentos usados para calcularla. | Wiki | CU-07/CU-09/CU-14: desde el registro se llega a sus fuentes y adjuntos. |

## 6. Restricciones de plataforma y alcance

| ID | Restricción consolidada | Origen | Vínculo a caso / criterio de aceptación |
|---|---|---|---|
| PR-01 | La primera versión será una aplicación web en español. | Complemento | CU-01 a CU-16: interfaz, mensajes y documentos de usuario se presentan en español. |
| PR-02 | La solución servirá inicialmente a una constructora y respetará la organización por empresa, workspace/proyecto y obra de Obra Studio. | Wiki | CU-01/CU-16: los datos se consultan dentro de la organización y las obras pertenecen a su agrupador. |
| PR-03 | La moneda operativa inicial será guaraní paraguayo (PYG). | Complemento | CU-07/CU-14/CU-15: los importes se rotulan y calculan en PYG. |
| PR-04 | El presupuesto y el cronograma podrán ingresar por XLSX; las exportaciones se generarán como archivos nuevos. | Wiki + Complemento | CU-02/CU-09: el origen permanece preservado y cada exportación es independiente. |
| PR-05 | La integración entre ECMS y ERP seguirá el puente y eventos definidos en Obra Studio; no se añadirán conectores externos fuera del alcance de módulos. | Wiki | CU-10/CU-14: certificados aprobados originan registros ERP relacionados. |
| PR-06 | ERP mantendrá facturas y pagos derivados de certificados aprobados; ECMS no será dueño de los documentos financieros ni de la ejecución de pagos. | Wiki | CU-10/CU-14: el documento financiero queda en ERP y refiere al certificado ECMS. |
| PR-07 | El análisis de costo utilizará las vías de materiales, mano de obra y equipos de ACU y motor; este trabajo no desarrolla la operación completa de inventario/almacén. | Wiki | CU-15: los costos muestran sus componentes y fuente sin simular movimientos de stock fuera de alcance. |
| PR-08 | Toda asistencia de IA para redactar o explicar requerirá verificación y decisión humana; los importes procederán de reglas deterministas. | Complemento | CU-07/CU-09/CU-11: la IA no aprueba, registra mediciones ni fija importes oficiales. |

## 7. Trazabilidad y control de cambios

La trazabilidad se mantiene mediante el identificador original, el caso de uso indicado en cada fila, el origen normativo y el criterio de aceptación. El modelo relacionado expone las entidades, interacciones y estados correspondientes.

El modelo de análisis correspondiente está en [modelo-de-analisis.md](modelo-de-analisis.md) y el entregable en `TPF-Obra-Studio.docx`. Ambos, junto con todos los diagramas, se generan desde `modelo/modelo.yaml` ejecutando `modelo/build.sh`, de modo que ningún nombre, estado o identificador pueda discrepar entre el catálogo y los diagramas.

Todo cambio posterior actualiza el enunciado, su fuente, el caso de uso y el criterio asociado. Los cambios de regla presupuestaria, estados de certificación, cálculo o propiedad ERP/ECMS requieren revisar también los diagramas del modelo para preservar consistencia.

## 8. Validación de aceptación

- Confirmar que el catálogo contiene los 48 identificadores originales, sin duplicados ni omisiones.
- Verificar la trazabilidad de cada requisito hacia un caso de uso, una fuente y un criterio observable.
- Comprobar importación inválida, diferencias de totales y carga XLSX repetida.
- Comprobar cantidad superior al saldo, acumulado decreciente, medición rechazada y doble conteo físico.
- Comprobar certificado de avance, certificado de subcontratista, corrección mediante revisión nueva y vínculo con ERP.
- Comprobar que un movimiento aprobado crea nueva versión y mantiene la anterior.
- Recalcular ejemplos de certificados, subcontratos y vías de costo con aritmética decimal.
- Comprobar que el subcontratista no consulta otros contratos ni información interna.
- Comprobar que cada reporte identifica fecha de corte, unidad, moneda, fuente y naturaleza del importe.
- Revisar que los diagramas del modelo usen los estados y nombres de este catálogo.

## 9. Referencias

- egrpy.org. (2025). *Análisis de Requerimientos — Objetivos Avanzados*. https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingeniería+del+Software+2/2025/Clase+20+Análisis+de+Requerimientos/Zk+Análisis+de+Requerimientos+-+Objetivos+Avanzados
- Cuatro Projects S.R.L. (2026). [*TPC 04 - Captura de Requerimientos - Rojas,Taveira,Scotover*](<TPC 04 - Captura de Requerimientos - Rojas,Taveira,Scotover.pdf>) [Documento PDF].
- Obra Studio. (s. f.). *Wiki de dominio, arquitectura e integración*. Documentación interna, carpeta wiki/docs/.
- Bruegge, B. y Dutoit, A. H. (2002). *Ingeniería de software orientado a objetos*. Pearson Educación. [Registro bibliográfico de Dialnet](https://dialnet.unirioja.es/servlet/libro?codigo=369091).
- Pressman, R. S. (2010). *Ingeniería del software: un enfoque práctico* (7.ª ed.). McGraw-Hill Interamericana. [Registro bibliográfico de la Universidad Central del Este](https://koha.uce.edu.do/cgi-bin/koha/opac-detail.pl?biblionumber=210765).
- Sommerville, I. (2011). *Ingeniería de software* (9.ª ed.). Pearson Educación. [Catálogo de Bibliotecas de la Universidad Nacional del Nordeste](https://redbiblio.unne.edu.ar/pergamo/documento.php?id=ROCA.10.60665&recno=60665&ui=10).
- Rumbaugh, J., Jacobson, I. y Booch, G. (2007). *El lenguaje unificado de modelado: manual de referencia* (2.ª ed.). Pearson Educación. [Catálogo de la Universidad de Montevideo](https://opac.um.edu.uy/index.php?id=10693&lvl=notice_display).
