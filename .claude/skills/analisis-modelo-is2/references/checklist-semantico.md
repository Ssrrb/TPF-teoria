# Revisión semántica de coherencia

`modelo/gen/validar.py` detecta lo que se puede comprobar con reglas (requisitos y casos huérfanos, actores no declarados, referencias por id rotas, fichas incompletas, transiciones imposibles). Lo que sigue requiere leer los textos y razonar; revisarlo a mano sobre las fichas, las especificaciones detalladas y los estados. Cada hallazgo va a la lista de pendientes con la forma «qué dice A / qué dice B / qué decisión falta».

1. **Actor del catálogo vs. actor en el flujo.** Cada CU debe tener el mismo actor principal en el catálogo, en el diagrama y en el flujo de su especificación. (Ejemplo real: CU-03 figuraba con Administrador, pero la especificación de CU-02 decía que el Ingeniero de Obra solicita la activación.)
2. **Precondiciones vs. máquina de estados.** Los estados que exige la precondición de un CU deben ser alcanzables en la máquina de estados antes de ese CU. (Ejemplo: CU-09 pedía período cerrado, pero el certificado pasaba a Cerrado después de Aprobado.)
3. **Estados sin CU.** Toda transición de la máquina de estados debe pertenecer a un CU. (Ejemplo: la transición Borrador → Emitido no tenía CU claro.)
4. **Requerimientos citados en excepciones y notas.** Si una excepción o nota cita un RF/RNF/PR que no está marcado para ese CU en la matriz, agregar la marca o quitar la cita.
5. **Requerimientos con un solo CU.** Un RNF que, por su texto, aplica a varios CU (p. ej. atomicidad a todo cierre o aprobación) pero figura en uno solo es sospechoso; contrastar con la matriz del documento original del TPF.
6. **Generalización de actores.** El hijo hereda todos los CU del padre; no usarla si rompe una separación de funciones (quien conforma no autoriza, quien registra no aprueba).
7. **Separación de funciones.** Si los requerimientos exigen personas distintas (p. ej. RF-17), comprobar que ningún actor figure en ambos lados de esa regla dentro del mismo CU.
8. **Flujo alternativo.** La plantilla lo pide como sección aparte; si la especificación solo tiene *Excepciones*, anotarlo como pendiente.
9. **Numeración.** Si la plantilla usa RF001/NF001 y el catálogo RF-01/RNF-01, decidir uno solo y convertir tabla, matriz y fichas de una vez.
10. **Portada y conteos.** Grupo Nº, alumnos y conteos de requerimientos agregados, eliminados y redefinidos.
