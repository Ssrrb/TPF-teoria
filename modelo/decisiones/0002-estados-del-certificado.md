# 2. El certificado tiene cuatro estados y el rechazo es una transición

Date: 2026-06-01

## Status

Accepted

## Context

La documentación describe el ciclo del certificado con tres, cuatro y cinco estados según el
documento consultado, y trata el rechazo unas veces como estado y otras como transición.

## Decision

Se unifica en cuatro estados: Borrador, Emitido, Aprobado y Cerrado. El rechazo no es un estado
sino la transición de Emitido a Borrador, que conserva el motivo, el actor y la fecha. La
corrección de un certificado cerrado exige reapertura autorizada y auditada, que crea una revisión
vinculada y preserva el original.

## Consequences

El historial queda completo sin estados redundantes y la reapertura nunca sobrescribe el documento
emitido, lo que satisface la exigencia de conservar los certificados cerrados y sus fuentes.
