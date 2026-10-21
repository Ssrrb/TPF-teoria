# 3. El movimiento presupuestario requiere aprobación interna y contractual

Date: 2026-06-01

## Status

Accepted

## Context

El catálogo de requerimientos exige registrar por separado la aprobación interna y la contractual
de un movimiento presupuestario, y activar la versión solo entonces. La documentación de dominio
no define una máquina de estados para el movimiento.

## Decision

Se diseña el ciclo Propuesto, AprobadoInterno, AprobadoContractual y Vigente, más Rechazado. Solo
la transición a Vigente genera una versión de presupuesto nueva; la anterior pasa a Reemplazada y
permanece consultable.

## Consequences

Una sola aprobación no modifica el presupuesto vigente. La cantidad medida que excedía el saldo
queda como propuesta pendiente y se vuelve certificable únicamente cuando un movimiento vigente la
cubre.
