# 2. El certificado tiene dos estados y se corrige con una revisión nueva

Date: 2026-06-01

## Status

Accepted (revisado el 2026-10-21)

## Context

La documentación describe el ciclo del certificado con tres, cuatro y cinco estados según el
documento consultado, y trata el rechazo unas veces como estado y otras como transición. Una
versión anterior de este modelo agregaba revisión por dos personas, cierre por período y
reapertura autorizada, más de lo que exige un certificado de avance.

## Decision

El certificado es un registro de avance (interno, de subcontratista o de adenda) con dos estados:
Borrador y Emitido. No se cierra por período. Corregir un certificado emitido crea una revisión
nueva en Borrador vinculada a la anterior, que se conserva sin cambios. La emisión la realiza un
usuario con rol admin o miembro con acceso al ECMS, y queda registrado quién emitió y cuándo.

## Consequences

El historial queda completo sin estados redundantes y ninguna corrección sobrescribe una revisión
emitida, con lo que se cumple la exigencia de conservar los certificados y sus fuentes. El camino
propio del certificado de adenda queda pendiente de definir (D-17).
