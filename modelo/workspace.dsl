workspace "Obra Studio" "Modelo de arquitectura del Trabajo Práctico Final — Ingeniería del Software 2." {

    model {
        ing = person "Ingeniero de Obra" "Carga el presupuesto y el cronograma de la obra, registra la medición oficial de cada ítem del período con su evidencia, genera y emite los certificados de avance y los corrige."
        sup = person "Responsable Técnico" "Supervisor de la obra."
        adm = person "Administrador" "Gerente de la obra."
        sub = person "Subcontratista" "Presenta las mediciones correspondientes a su contrato y consulta el estado de sus mediciones, certificados y saldos."
        cli = person "Cliente" "Comitente de la obra."
        tes = person "Finanzas y Tesorería" "Opera dentro del ERP."

        erpExterno = softwareSystem "Sistema ERP" "Motor financiero y documental. Registra lo que el ECMS midió y certificó." "Externo"

        obraStudio = softwareSystem "Obra Studio" "Gestiona presupuesto, medición, certificación y costos de obra." {
            web = container "Aplicación Web" "Presenta los formularios de carga, medición y certificación." "React + TypeScript"
            ecms = container "Motor ECMS" "Reglas de obra, presupuesto, medición y certificación." "TypeScript" {
                group "Adaptadores de interfaz" {
                    importarPresupuestoControlador = component "ImportarPresupuestoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    importacionPresentador = component "ImportacionPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    aprobarMedicionControlador = component "AprobarMedicionControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    medicionPresentador = component "MedicionPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    emitirCertificadoControlador = component "EmitirCertificadoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    certificadoPresentador = component "CertificadoPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                }
                group "Casos de uso" {
                    importarPresupuestoInteractor = component "ImportarPresupuestoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    validarEstructuraServicio = component "ValidarEstructuraServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    contrastarTotalesServicio = component "ContrastarTotalesServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    aprobarMedicionInteractor = component "AprobarMedicionInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    evaluarSaldoServicio = component "EvaluarSaldoServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    emitirCertificadoInteractor = component "EmitirCertificadoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    calcularValorizacionServicio = component "CalcularValorizacionServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                }
                group "Dominio: entidades" {
                    obra = component "Obra" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    presupuesto = component "Presupuesto" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    versionPresupuesto = component "VersionPresupuesto" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    lineaPresupuesto = component "LineaPresupuesto" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    archivoOrigen = component "ArchivoOrigen" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    informeImportacion = component "InformeImportacion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    periodo = component "Periodo" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    medicionOficial = component "MedicionOficial" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    evidencia = component "Evidencia" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    propuestaPendiente = component "PropuestaPendiente" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    certificado = component "Certificado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    revisionCertificado = component "RevisionCertificado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    lineaCertificado = component "LineaCertificado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    retencionAplicada = component "RetencionAplicada" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    configuracionObra = component "ConfiguracionObra" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    fondoRetencion = component "FondoRetencion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    valorizacion = component "Valorizacion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                }
                group "Dominio: puertos" {
                    iPresupuestoRepositorio = component "IPresupuestoRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iAlmacenArchivos = component "IAlmacenArchivos" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iLectorPlanilla = component "ILectorPlanilla" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iAuditoriaRepositorio = component "IAuditoriaRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iMedicionRepositorio = component "IMedicionRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iReloj = component "IReloj" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iCertificadoRepositorio = component "ICertificadoRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iGeneradorDocumento = component "IGeneradorDocumento" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iPublicadorEventos = component "IPublicadorEventos" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                }
                group "Infraestructura" {
                    presupuestoRepositorioSQL = component "PresupuestoRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    almacenArchivosS3 = component "AlmacenArchivosS3" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    lectorPlanillaXLSX = component "LectorPlanillaXLSX" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    auditoriaRepositorioSQL = component "AuditoriaRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    medicionRepositorioSQL = component "MedicionRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    relojSistema = component "RelojSistema" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    certificadoRepositorioSQL = component "CertificadoRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    generadorDocumentoXLSXPDF = component "GeneradorDocumentoXLSXPDF" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    puenteERP = component "PuenteERP" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                }
            }
            bd = container "Base de Datos" "Obras, presupuestos, mediciones y certificados." "PostgreSQL" "Almacen"
            archivos = container "Almacén de Archivos" "Planillas de origen, evidencias y certificados exportados." "Almacenamiento de objetos" "Almacen"

            !docs docs
            !adrs decisiones
        }

        ing -> web "Carga el presupuesto, registra la medición oficial y emite certificados" "HTTPS"
        sup -> web "Aprueba mediciones y cierra el período" "HTTPS"
        adm -> web "Activa versiones, emite certificados y aprueba movimientos presupuestarios" "HTTPS"
        sub -> web "Presenta las mediciones de su contrato" "HTTPS"
        ecms -> erpExterno "Publica el certificado emitido para su documento financiero" "Evento de dominio"
        web -> ecms "Invoca los casos de uso" "HTTPS/JSON"
        ecms -> bd "Lee y escribe" "SQL"
        ecms -> archivos "Conserva planillas, evidencias y exportaciones" "API de objetos"
        erpExterno -> cli "Emite la factura del certificado" "Documento"
        erpExterno -> tes "Registra el cobro o el pago" "Documento"

        web -> importarPresupuestoControlador "importarPresupuesto(obraId, archivo)" "Llamada interna"
        importarPresupuestoControlador -> importarPresupuestoInteractor "ejecutar(solicitudImportacion)" "Llamada interna"
        importarPresupuestoInteractor -> iAlmacenArchivos "guardar(archivo)" "Llamada interna"
        importarPresupuestoInteractor -> iPresupuestoRepositorio "buscarPorHash(hashSHA256)" "Llamada interna"
        importarPresupuestoInteractor -> iLectorPlanilla "leer(archivo)" "Llamada interna"
        importarPresupuestoInteractor -> lineaPresupuesto "crear(codigo, unidad, cantidad, precioUnitario)" "Llamada interna"
        importarPresupuestoInteractor -> validarEstructuraServicio "validar(lineas)" "Llamada interna"
        importarPresupuestoInteractor -> contrastarTotalesServicio "contrastar(totalDeclarado, totalRecalculado)" "Llamada interna"
        importarPresupuestoInteractor -> versionPresupuesto "crear(numero, estado = Propuesta)" "Llamada interna"
        web -> aprobarMedicionControlador "listarMediciones(obraId, periodoId)" "Llamada interna"
        aprobarMedicionControlador -> aprobarMedicionInteractor "obtenerPendientes(periodoId)" "Llamada interna"
        aprobarMedicionInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)" "Llamada interna"
        aprobarMedicionInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        aprobarMedicionInteractor -> lineaPresupuesto "saldo(cantidadAcumulada)" "Llamada interna"
        aprobarMedicionInteractor -> evaluarSaldoServicio "evaluar(cantidadMedida, saldo)" "Llamada interna"
        aprobarMedicionInteractor -> propuestaPendiente "crear(exceso, estado = Pendiente)" "Llamada interna"
        aprobarMedicionInteractor -> medicionOficial "aprobar(cantidadCertificable, actorId, fecha)" "Llamada interna"
        aprobarMedicionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, decisión)" "Llamada interna"
        web -> emitirCertificadoControlador "abrirRevision(revisionId)" "Llamada interna"
        emitirCertificadoControlador -> emitirCertificadoInteractor "obtenerRevision(revisionId)" "Llamada interna"
        emitirCertificadoInteractor -> iCertificadoRepositorio "buscarRevision(revisionId)" "Llamada interna"
        emitirCertificadoInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)" "Llamada interna"
        emitirCertificadoInteractor -> certificado "emitir(numero, fecha, destinatario, actorId)" "Llamada interna"
        emitirCertificadoInteractor -> iGeneradorDocumento "exportar(revision, formato)" "Llamada interna"
        emitirCertificadoInteractor -> iPublicadorEventos "publicar(CertificadoEmitido(certificadoId))" "Llamada interna"
        presupuestoRepositorioSQL -> iPresupuestoRepositorio "Implementa" "Inyección de dependencias"
        almacenArchivosS3 -> iAlmacenArchivos "Implementa" "Inyección de dependencias"
        lectorPlanillaXLSX -> iLectorPlanilla "Implementa" "Inyección de dependencias"
        auditoriaRepositorioSQL -> iAuditoriaRepositorio "Implementa" "Inyección de dependencias"
        medicionRepositorioSQL -> iMedicionRepositorio "Implementa" "Inyección de dependencias"
        relojSistema -> iReloj "Implementa" "Inyección de dependencias"
        certificadoRepositorioSQL -> iCertificadoRepositorio "Implementa" "Inyección de dependencias"
        generadorDocumentoXLSXPDF -> iGeneradorDocumento "Implementa" "Inyección de dependencias"
        puenteERP -> iPublicadorEventos "Implementa" "Inyección de dependencias"
        obra -> configuracionObra "Se compone de (1 a 1)" "Referencia de dominio"
        configuracionObra -> fondoRetencion "Se compone de (1 a 0..*)" "Referencia de dominio"
        obra -> presupuesto "Se compone de (1 a 1..*)" "Referencia de dominio"
        presupuesto -> versionPresupuesto "Se compone de (1 a 1..*)" "Referencia de dominio"
        versionPresupuesto -> lineaPresupuesto "Se compone de (1 a 1..*)" "Referencia de dominio"
        lineaPresupuesto -> lineaPresupuesto "jerarquía rubro/subrubro/ítem (0..1 a 0..*)" "Referencia de dominio"
        versionPresupuesto -> archivoOrigen "Se compone de (1 a 0..1)" "Referencia de dominio"
        versionPresupuesto -> informeImportacion "Se compone de (1 a 0..1)" "Referencia de dominio"
        obra -> periodo "Se compone de (1 a 0..*)" "Referencia de dominio"
        periodo -> medicionOficial "Se compone de (1 a 0..*)" "Referencia de dominio"
        lineaPresupuesto -> medicionOficial "Se asocia con (1 a 0..*)" "Referencia de dominio"
        versionPresupuesto -> medicionOficial "medida contra (1 a 0..*)" "Referencia de dominio"
        medicionOficial -> evidencia "Se compone de (1 a 0..*)" "Referencia de dominio"
        medicionOficial -> propuestaPendiente "Se compone de (1 a 0..1)" "Referencia de dominio"
        periodo -> certificado "Se asocia con (1 a 0..*)" "Referencia de dominio"
        certificado -> revisionCertificado "Se compone de (1 a 1..*)" "Referencia de dominio"
        revisionCertificado -> lineaCertificado "Se compone de (1 a 1..*)" "Referencia de dominio"
        medicionOficial -> lineaCertificado "Se asocia con (1 a 0..1)" "Referencia de dominio"
        lineaPresupuesto -> lineaCertificado "Se asocia con (1 a 0..*)" "Referencia de dominio"
        revisionCertificado -> retencionAplicada "Se compone de (1 a 0..*)" "Referencia de dominio"
        fondoRetencion -> retencionAplicada "Se asocia con (1 a 0..*)" "Referencia de dominio"
        importarPresupuestoInteractor -> importacionPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        aprobarMedicionInteractor -> medicionPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        emitirCertificadoInteractor -> certificadoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        calcularValorizacionServicio -> valorizacion "Produce" "Llamada interna"
    }

    views {
        systemLandscape "Paisaje" "Obra Studio, el ERP y las personas que intervienen." {
            include *
            autolayout lr
        }
        systemContext obraStudio "Contexto" "Obra Studio y su entorno." {
            include *
            autolayout lr
        }
        container obraStudio "Contenedores" "Estructura interna de Obra Studio." {
            include *
            autolayout lr
        }
        component ecms "Componentes" "Capas de Clean Architecture dentro del Motor ECMS." {
            include *
            autolayout lr
        }
        dynamic ecms "CU02" "CU-02 — Importar presupuesto y cronograma." {
            web -> importarPresupuestoControlador "importarPresupuesto(obraId, archivo)"
            importarPresupuestoControlador -> importarPresupuestoInteractor "ejecutar(solicitudImportacion)"
            importarPresupuestoInteractor -> iAlmacenArchivos "guardar(archivo)"
            importarPresupuestoInteractor -> iPresupuestoRepositorio "buscarPorHash(hashSHA256)"
            importarPresupuestoInteractor -> iLectorPlanilla "leer(archivo)"
            importarPresupuestoInteractor -> lineaPresupuesto "crear(codigo, unidad, cantidad, precioUnitario)"
            importarPresupuestoInteractor -> validarEstructuraServicio "validar(lineas)"
            importarPresupuestoInteractor -> contrastarTotalesServicio "contrastar(totalDeclarado, totalRecalculado)"
            importarPresupuestoInteractor -> versionPresupuesto "crear(numero, estado = Propuesta)"
            autolayout lr
        }
        dynamic ecms "CU05" "CU-05 — Aprobar o rechazar medición oficial." {
            web -> aprobarMedicionControlador "listarMediciones(obraId, periodoId)"
            aprobarMedicionControlador -> aprobarMedicionInteractor "obtenerPendientes(periodoId)"
            aprobarMedicionInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)"
            aprobarMedicionInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            aprobarMedicionInteractor -> lineaPresupuesto "saldo(cantidadAcumulada)"
            aprobarMedicionInteractor -> evaluarSaldoServicio "evaluar(cantidadMedida, saldo)"
            aprobarMedicionInteractor -> propuestaPendiente "crear(exceso, estado = Pendiente)"
            aprobarMedicionInteractor -> medicionOficial "aprobar(cantidadCertificable, actorId, fecha)"
            aprobarMedicionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, decisión)"
            autolayout lr
        }
        dynamic ecms "CU09" "CU-09 — Emitir certificado de avance." {
            web -> emitirCertificadoControlador "abrirRevision(revisionId)"
            emitirCertificadoControlador -> emitirCertificadoInteractor "obtenerRevision(revisionId)"
            emitirCertificadoInteractor -> iCertificadoRepositorio "buscarRevision(revisionId)"
            emitirCertificadoInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)"
            emitirCertificadoInteractor -> certificado "emitir(numero, fecha, destinatario, actorId)"
            emitirCertificadoInteractor -> iGeneradorDocumento "exportar(revision, formato)"
            emitirCertificadoInteractor -> iPublicadorEventos "publicar(CertificadoEmitido(certificadoId))"
            autolayout lr
        }
        image * "uml01casosdeusoA" {
            image out/01-casos-de-uso-A.png
            title "UML — 01-casos-de-uso-A"
        }
        image * "uml02casosdeusoB" {
            image out/02-casos-de-uso-B.png
            title "UML — 02-casos-de-uso-B"
        }
        image * "uml03CU02clases" {
            image out/03-CU-02-clases.png
            title "UML — 03-CU-02-clases"
        }
        image * "uml04CU05clases" {
            image out/04-CU-05-clases.png
            title "UML — 04-CU-05-clases"
        }
        image * "uml05CU09clases" {
            image out/05-CU-09-clases.png
            title "UML — 05-CU-09-clases"
        }
        image * "uml06CU02secuencia" {
            image out/06-CU-02-secuencia.png
            title "UML — 06-CU-02-secuencia"
        }
        image * "uml07CU05secuencia" {
            image out/07-CU-05-secuencia.png
            title "UML — 07-CU-05-secuencia"
        }
        image * "uml08CU09secuencia" {
            image out/08-CU-09-secuencia.png
            title "UML — 08-CU-09-secuencia"
        }
        image * "uml09clasespersistentesA" {
            image out/09-clases-persistentes-A.png
            title "UML — 09-clases-persistentes-A"
        }
        image * "uml10clasespersistentesB" {
            image out/10-clases-persistentes-B.png
            title "UML — 10-clases-persistentes-B"
        }
        image * "uml11entidadrelacion" {
            image out/11-entidad-relacion.png
            title "UML — 11-entidad-relacion"
        }
        image * "uml12estadoVersionPresupuesto" {
            image out/12-estado-VersionPresupuesto.png
            title "UML — 12-estado-VersionPresupuesto"
        }
        image * "uml13estadoMedicionOficial" {
            image out/13-estado-MedicionOficial.png
            title "UML — 13-estado-MedicionOficial"
        }
        image * "uml14estadoCertificado" {
            image out/14-estado-Certificado.png
            title "UML — 14-estado-Certificado"
        }
        image * "uml15estadoMovimientoPresupuestario" {
            image out/15-estado-MovimientoPresupuestario.png
            title "UML — 15-estado-MovimientoPresupuestario"
        }

        styles {
            element "Person" {
                shape person
                background #0b5394
                color #ffffff
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Externo" {
                background #8c8c8c
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Almacen" {
                shape cylinder
                background #438dd5
                color #ffffff
            }
            element "Component" {
                background #85bbf0
                color #000000
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
