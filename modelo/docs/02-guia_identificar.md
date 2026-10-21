# Guia para identificar posibles casos de usos "Derivación de Casos de Uso a partir de Requerimientos"

https://www.egrpy.org/050+Base+de+Conocimientos/200++Mi+Zettelkasten/100+Docencia/Ingeniería+del+Software+1/Clase+12+Caso+Práctico+de+Aplicando+SDLC/Sistema+de+Biblioteca/40+Análisis+de+Requerimientos/Zk+Derivación+de+Casos+de+Uso+a+partir+de+Requerimientos

Este apartado describe un procedimiento metodológico y reusable para derivar casos de uso a partir de requerimientos de software, en el marco de un enfoque orientado a objetivos del usuario (Jacobson et al., 1992; Cockburn, 2001).

1. **Punto de Partida: Tipos de Requerimientos** 
Se asume que la fase de ingeniería de requerimientos ha producido, como mínimo:

Un conjunto de requerimientos funcionales (RF) que describen capacidades observables del sistema.
Un conjunto de requerimientos no funcionales (RNF) y reglas de negocio, que condicionan calidad, rendimiento, seguridad, etc.
Restricciones de dominio y decisiones de entorno (plataforma, navegadores, integración, etc.).
Los casos de uso se derivan principalmente de los RF y de las reglas de negocio asociadas a ellos, pero deben redactarse de manera coherente con RNF y restricciones (Wiegers y Beatty, 2013).

2. **Identificación de Actores a partir de Requerimientos** 
El primer paso consiste en pasar de “usuarios genéricos” a actores bien definidos (Jacobson et al., 1992).

Pasos:

Revisar RF, RNF y documentación de contexto buscando referencias a roles, perfiles, clases de usuario y sistemas externos (por ejemplo, “cliente”, “bibliotecario”, “sistema de pagos”, “API externa”).
Consolidar estos roles en una lista de actores candidatos, distinguiendo actores humanos vs sistemas externos, actores primarios (los que inician casos de uso) vs secundarios.
Identificar relaciones de generalización/especialización entre actores (por ejemplo, Usuario general, UsuarioRegistrado, Administrador), manteniendo los casos de uso en el nivel de abstracción adecuado.
Esta identificación de actores proporciona la base para formular metas de usuario y, en consecuencia, casos de uso significativos (Jacobson et al., 1992).

3. **De Requerimientos Funcionales a Objetivos de Usuario** 
Cada requerimiento funcional debe analizarse desde la perspectiva de objetivo del actor (Cockburn, 2001).

Heurística:

Para cada RF, preguntarse explícitamente:
“¿Qué objetivo concreto intenta alcanzar un actor cuando este requerimiento se cumple?”.
Verificar si ese objetivo puede describirse como un escenario de interacción completo:
inicio (disparador),
serie de pasos entre actor y sistema,
resultado observable para el actor (postcondición con valor).
Cuando varios RF describen variaciones estrechamente relacionadas de un mismo objetivo, agruparlos en un caso de uso principal, con escenarios alternativos o casos de uso de extensión (Cockburn, 2001).
El resultado de este paso es un conjunto preliminar de “metas de usuario”, que se convierten en candidatos a casos de uso (Jacobson et al., 1992).

4. **Clasificar Casos de Uso: Principales, Incluidos, de Extensión y Generalizados** 
No todos los RF se convierten en casos de uso independientes; algunos representan pasos recurrentes u opciones condicionales (Cockburn, 2001).

Criterios prácticos:

Caso de uso principal (nivel meta de usuario): representa un objetivo significativo y completo para un actor (por ejemplo, “Registrar pedido”, “Realizar préstamo”) (Cockburn, 2001).
Caso de uso incluido (<<include>>): representa un subobjetivo común, que aparece sistemáticamente como parte de varios casos de uso (por ejemplo, “Autenticar usuario”, “Calcular impuestos”). Suele derivarse de RF que describen funcionalidades reutilizables que rara vez tienen sentido por sí solas para el actor. Ver Dependencia Include (Cockburn, 2001).
Caso de uso de extensión (<<extend>>): captura variantes opcionales o condicionales de un flujo principal (por ejemplo, “Renovar pedido”, “Aplicar descuento especial dentro de Registrar pedido”). Suele corresponder a RF que añaden comportamiento bajo condiciones especiales. Ver Dependencia Extend (Cockburn, 2001).
Generalización entre casos de uso: se utiliza cuando existen varios casos de uso que comparten un comportamiento base significativo, pero cada uno añade pasos propios o reglas diferentes. En esos casos:
se define un caso de uso general que recoge el comportamiento común,
y uno o más casos de uso especializados que heredan ese comportamiento y lo refinan o amplían.
Ver también Generalización entre Casos de Uso (Jacobson et al., 1992; Cockburn, 2001).
La generalización resulta útil cuando las variaciones son múltiples y relativamente simétricas (por ejemplo, “Registrar Venta en Tienda Física”, “Registrar Venta Online” como especializaciones de “Registrar Venta”), mientras que <<extend>> resulta más adecuada para añadir una variante opcional puntual sobre un único caso base (Cockburn, 2001).

Esta clasificación ayuda a modularizar el modelo de casos de uso sin perder legibilidad.

5. **Incorporar Reglas de Negocio y RNF en los Casos de Uso** 
Los RNF y las reglas de negocio no se transforman en casos de uso independientes, pero influyen en la redacción y priorización de los mismos (Wiegers y Beatty, 2013).

Algunos RNF se explicitan como condiciones de calidad en los casos de uso (tiempo máximo de respuesta, volumen máximo de datos, concurrencia esperada, etc.).
Las reglas de negocio se documentan como precondiciones, garantías y restricciones del caso de uso (por ejemplo, “solo usuarios con rol X pueden ejecutar este caso”, “no se puede renovar si la fecha de devolución ha expirado”).
Así, el caso de uso actúa como “contrato de comportamiento” entre actores y sistema (Jacobson et al., 1992; Wiegers y Beatty, 2013).

6. **Construir la Matriz de Trazabilidad Requerimientos ↔ Casos de Uso** 
Una vez estabilizada la lista de casos de uso (en una primera aproximación razonable), se construye una matriz de trazabilidad que vincula cada requerimiento (RF, y eventualmente reglas de negocio) con uno o más casos de uso que lo satisfacen (Wiegers y Beatty, 2013).

Se verifica que:

Todo RF tiene al menos un caso de uso asociado (trazabilidad hacia adelante).
Todo caso de uso tiene respaldo en uno o varios requerimientos (trazabilidad hacia atrás), evitando funcionalidad huérfana.
Es importante enfatizar que esta “estabilización” es heurística e iterativa:

La identificación y estructuración de casos de uso no es un proceso lineal que se haga “de una sola vez”.
La matriz de trazabilidad suele revelar lagunas, redundancias o casos mal estructurados, lo que conduce a nuevas rondas de revisión: se refinan casos de uso (por ejemplo, descomponiendo uno muy grande, introduciendo un <<include>> o un <<extend>>, o reestructurando una generalización), se ajustan RF, o se actualizan reglas de negocio.
Cada iteración mejora la alineación entre la Lista de Requerimientos y el modelo de casos de uso, hasta alcanzar un nivel de estabilidad suficiente para pasar a actividades de diseño y prueba (Wiegers y Beatty, 2013).