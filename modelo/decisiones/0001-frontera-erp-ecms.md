# 1. El ECMS posee la medición; el ERP posee el documento financiero

Date: 2026-06-01

## Status

Accepted

## Context

La documentación de Obra Studio asigna el contrato de subcontrato al ERP en un documento y al
ECMS en otro. Sin una regla única, el mismo hecho podría registrarse dos veces y los importes
dejarían de coincidir entre ambos motores.

## Decision

Se adopta la regla de propiedad por naturaleza del registro: si es un hecho de campo (medición,
parte de máquina) pertenece al ECMS; si es un documento legal (contrato, factura, pago) pertenece
al ERP. El certificado aprobado publica un evento y el ERP deriva de él la factura o el pago,
conservando el vínculo con su certificado de origen.

## Consequences

El ERP no recalcula costo de obra y el ECMS no emite documentos legales. Un certificado tiene a lo
sumo un documento financiero derivado, de modo que no se puede facturar más de lo certificado.
