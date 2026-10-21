# Arquitectura de referencia

Obra Studio separa dos motores sobre un núcleo común. El ECMS mide: posee la obra, el
presupuesto, la medición oficial y el certificado. El ERP registra lo que el ECMS midió: posee la
factura, el cobro y el pago. Un certificado aprobado publica un evento; el ERP deriva de él el
documento financiero y conserva el vínculo con su certificado de origen.

## Regla de dependencia

El Motor ECMS aplica Clean Architecture en cuatro anillos. Las dependencias apuntan siempre hacia
adentro:

1. **Adaptadores de interfaz** traducen la petición y presentan el resultado.
2. **Casos de uso** orquestan entidades y puertos; no conocen la tecnología.
3. **Dominio** concentra las entidades, sus invariantes y los puertos que declara.
4. **Infraestructura** implementa esos puertos contra la base de datos, el almacén y el puente ERP.

La inversión ocurre en el tercer anillo: el dominio declara la interfaz y la infraestructura la
implementa, de modo que el sentido de la dependencia se opone al sentido del flujo de control.

## Proyección en notación UML

Los estereotipos de análisis de Jacobson son la proyección de estos anillos sobre el diagrama de
clases: «Boundary» corresponde a los adaptadores de interfaz, «Control» al interactor del caso de
uso y «Entity» al dominio. Los puertos aparecen como «Interface» y sus adaptadores los realizan.
