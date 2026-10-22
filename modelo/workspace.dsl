workspace "Obra Studio" "Modelo de arquitectura del Trabajo Práctico Final — Ingeniería del Software 2." {

    model {
        ing = person "Ingeniero de Obra" "Carga el presupuesto y el cronograma de la obra, registra la medición oficial de cada ítem del período con su evidencia, genera y emite los certificados de avance y los corrige."
        sup = person "Responsable Técnico" "Supervisor de la obra."
        adm = person "Administrador" "Gerente de la obra."
        sub = person "Subcontratista" "Consulta el estado de sus mediciones, certificados, valorizaciones y saldos."
        cli = person "Cliente" "Comitente de la obra."
        tes = person "Finanzas y Tesorería" "Opera dentro del ERP."

        obraStudio = softwareSystem "Obra Studio" "Gestiona presupuesto, medición, certificación, costos, facturas y pagos de obra." {
            web = container "Aplicación Web" "Presenta los formularios de carga, medición y certificación." "React + TypeScript"
            ecms = container "Motor ECMS" "Reglas de obra, presupuesto, medición y certificación." "TypeScript" {
                group "Adaptadores de interfaz" {
                    crearObraControlador = component "CrearObraControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    obraPresentador = component "ObraPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    importarPresupuestoControlador = component "ImportarPresupuestoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    importacionPresentador = component "ImportacionPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    activarVersionControlador = component "ActivarVersionControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    versionPresentador = component "VersionPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    registrarMedicionControlador = component "RegistrarMedicionControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    medicionPresentador = component "MedicionPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    aprobarMedicionControlador = component "AprobarMedicionControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    cerrarPeriodoControlador = component "CerrarPeriodoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    periodoPresentador = component "PeriodoPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    generarBorradorControlador = component "GenerarBorradorControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    certificadoPresentador = component "CertificadoPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    corregirCertificadoControlador = component "CorregirCertificadoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    emitirCertificadoControlador = component "EmitirCertificadoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    documentoFinancieroControlador = component "DocumentoFinancieroControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    documentoFinancieroPresentador = component "DocumentoFinancieroPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    movimientoControlador = component "MovimientoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    movimientoPresentador = component "MovimientoPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    registrarSubcontratoControlador = component "RegistrarSubcontratoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    subcontratoPresentador = component "SubcontratoPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    consultarSubcontratoControlador = component "ConsultarSubcontratoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    certificarSubcontratoControlador = component "CertificarSubcontratoControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    calcularCostosControlador = component "CalcularCostosControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    costosPresentador = component "CostosPresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    consultarReportesControlador = component "ConsultarReportesControlador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                    reportePresentador = component "ReportePresentador" "Traduce la petición de la interfaz y presenta el resultado. No contiene reglas de negocio." "Controller / Presenter"
                }
                group "Casos de uso" {
                    crearObraInteractor = component "CrearObraInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    importarPresupuestoInteractor = component "ImportarPresupuestoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    validarEstructuraServicio = component "ValidarEstructuraServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    contrastarTotalesServicio = component "ContrastarTotalesServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    activarVersionInteractor = component "ActivarVersionInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    registrarMedicionInteractor = component "RegistrarMedicionInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    aprobarMedicionInteractor = component "AprobarMedicionInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    evaluarSaldoServicio = component "EvaluarSaldoServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    cerrarPeriodoInteractor = component "CerrarPeriodoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    generarBorradorInteractor = component "GenerarBorradorInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    calcularValorizacionServicio = component "CalcularValorizacionServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    detectarAlertasServicio = component "DetectarAlertasServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    corregirCertificadoInteractor = component "CorregirCertificadoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    emitirCertificadoInteractor = component "EmitirCertificadoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    derivarDocumentoInteractor = component "DerivarDocumentoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    movimientoInteractor = component "MovimientoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    evaluarLimiteServicio = component "EvaluarLimiteServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    registrarSubcontratoInteractor = component "RegistrarSubcontratoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    consultarSubcontratoInteractor = component "ConsultarSubcontratoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    certificarSubcontratoInteractor = component "CertificarSubcontratoInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    calcularCostosInteractor = component "CalcularCostosInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    calcularCostoViaServicio = component "CalcularCostoViaServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    consultarReportesInteractor = component "ConsultarReportesInteractor" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                    generarCurvaSServicio = component "GenerarCurvaSServicio" "Orquesta el caso de uso sobre las entidades y los puertos. No conoce la infraestructura." "Interactor"
                }
                group "Dominio: entidades" {
                    obra = component "Obra" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    configuracionObra = component "ConfiguracionObra" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    rolAsignado = component "RolAsignado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    usuario = component "Usuario" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    organizacion = component "Organizacion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    cliente = component "Cliente" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    presupuesto = component "Presupuesto" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    versionPresupuesto = component "VersionPresupuesto" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    lineaPresupuesto = component "LineaPresupuesto" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    archivoOrigen = component "ArchivoOrigen" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    informeImportacion = component "InformeImportacion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    medicionOficial = component "MedicionOficial" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    evidencia = component "Evidencia" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    periodo = component "Periodo" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    propuestaPendiente = component "PropuestaPendiente" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    certificado = component "Certificado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    revisionCertificado = component "RevisionCertificado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    lineaCertificado = component "LineaCertificado" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    valorizacion = component "Valorizacion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    retencionAplicada = component "RetencionAplicada" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    fondoRetencion = component "FondoRetencion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    documentoFinancieroERP = component "DocumentoFinancieroERP" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    movimientoPresupuestario = component "MovimientoPresupuestario" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    aprobacion = component "Aprobacion" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    subcontrato = component "Subcontrato" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    socio = component "Socio" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    analisisCostoUnitario = component "AnalisisCostoUnitario" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                    componenteACU = component "ComponenteACU" "Entidad del dominio: concentra la regla de negocio y sus invariantes." "Entidad de dominio"
                }
                group "Dominio: puertos" {
                    iObraRepositorio = component "IObraRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iUsuarioRepositorio = component "IUsuarioRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iAuditoriaRepositorio = component "IAuditoriaRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iPresupuestoRepositorio = component "IPresupuestoRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iAlmacenArchivos = component "IAlmacenArchivos" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iLectorPlanilla = component "ILectorPlanilla" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iReloj = component "IReloj" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iMedicionRepositorio = component "IMedicionRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iCertificadoRepositorio = component "ICertificadoRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iGeneradorDocumento = component "IGeneradorDocumento" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iPublicadorEventos = component "IPublicadorEventos" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iDocumentoFinancieroRepositorio = component "IDocumentoFinancieroRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iMovimientoRepositorio = component "IMovimientoRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iSubcontratoRepositorio = component "ISubcontratoRepositorio" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                    iConsultaReportes = component "IConsultaReportes" "Puerto declarado por el dominio. Invierte la dependencia hacia la infraestructura." "Interfaz"
                }
                group "Infraestructura" {
                    obraRepositorioSQL = component "ObraRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    usuarioRepositorioSQL = component "UsuarioRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    auditoriaRepositorioSQL = component "AuditoriaRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    presupuestoRepositorioSQL = component "PresupuestoRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    almacenArchivosS3 = component "AlmacenArchivosS3" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    lectorPlanillaXLSX = component "LectorPlanillaXLSX" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    relojSistema = component "RelojSistema" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    medicionRepositorioSQL = component "MedicionRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    certificadoRepositorioSQL = component "CertificadoRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    generadorDocumentoXLSXPDF = component "GeneradorDocumentoXLSXPDF" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    puenteERP = component "PuenteERP" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    documentoFinancieroRepositorioERP = component "DocumentoFinancieroRepositorioERP" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    movimientoRepositorioSQL = component "MovimientoRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    subcontratoRepositorioSQL = component "SubcontratoRepositorioSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                    consultaReportesSQL = component "ConsultaReportesSQL" "Implementa el puerto contra una tecnología concreta." "Adaptador"
                }
            }
            bd = container "Base de Datos" "Obras, presupuestos, mediciones y certificados." "PostgreSQL" "Almacen"
            archivos = container "Almacén de Archivos" "Planillas de origen, evidencias y certificados exportados." "Almacenamiento de objetos" "Almacen"
            erp = container "Motor ERP" "Facturas, pagos y avance físico-financiero de la obra."

            !docs docs
            !adrs decisiones
        }

        ing -> web "Carga el presupuesto, registra la medición oficial y emite certificados" "HTTPS"
        sup -> web "Aprueba mediciones y cierra el período" "HTTPS"
        adm -> web "Activa versiones, emite certificados y aprueba movimientos presupuestarios" "HTTPS"
        sub -> web "Consulta el estado de su contrato" "HTTPS"
        tes -> web "Aprueba y ejecuta pagos y registra cobros" "HTTPS"
        ecms -> erp "Publica el certificado emitido para su documento financiero" "Evento de dominio"
        web -> ecms "Invoca los casos de uso" "HTTPS/JSON"
        ecms -> bd "Lee y escribe" "SQL"
        ecms -> archivos "Conserva planillas, evidencias y exportaciones" "API de objetos"
        erp -> cli "Emite la factura del certificado interno" "Documento"

        web -> crearObraControlador "nuevaObra(organizacionId)" "Llamada interna"
        crearObraControlador -> crearObraInteractor "prepararAlta(organizacionId)" "Llamada interna"
        crearObraInteractor -> iUsuarioRepositorio "listarMiembros(organizacionId)" "Llamada interna"
        crearObraInteractor -> iObraRepositorio "existeCodigo(codigo)" "Llamada interna"
        crearObraInteractor -> obra "crear(codigo, nombre, direccion, fechas, clienteId)" "Llamada interna"
        crearObraInteractor -> rolAsignado "crear(usuarioId, rol, vigenteDesde)" "Llamada interna"
        crearObraInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, alta)" "Llamada interna"
        web -> importarPresupuestoControlador "importarPresupuesto(obraId, archivo)" "Llamada interna"
        importarPresupuestoControlador -> importarPresupuestoInteractor "ejecutar(solicitudImportacion)" "Llamada interna"
        importarPresupuestoInteractor -> iAlmacenArchivos "guardar(archivo)" "Llamada interna"
        importarPresupuestoInteractor -> iPresupuestoRepositorio "buscarPorHash(hashSHA256)" "Llamada interna"
        importarPresupuestoInteractor -> iLectorPlanilla "leer(archivo)" "Llamada interna"
        importarPresupuestoInteractor -> lineaPresupuesto "crear(codigo, unidad, cantidad, precioUnitario)" "Llamada interna"
        importarPresupuestoInteractor -> validarEstructuraServicio "validar(lineas)" "Llamada interna"
        importarPresupuestoInteractor -> contrastarTotalesServicio "contrastar(totalDeclarado, totalRecalculado)" "Llamada interna"
        importarPresupuestoInteractor -> versionPresupuesto "crear(numero, estado = Propuesta)" "Llamada interna"
        web -> activarVersionControlador "abrirVersion(versionId)" "Llamada interna"
        activarVersionControlador -> activarVersionInteractor "obtenerVersion(versionId)" "Llamada interna"
        activarVersionInteractor -> iPresupuestoRepositorio "buscarVersion(versionId)" "Llamada interna"
        activarVersionInteractor -> iReloj "ahora()" "Llamada interna"
        activarVersionInteractor -> versionPresupuesto "confirmarEstructura()" "Llamada interna"
        activarVersionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, activación)" "Llamada interna"
        web -> registrarMedicionControlador "abrirMedicion(obraId, periodoId, lineaId)" "Llamada interna"
        registrarMedicionControlador -> registrarMedicionInteractor "prepararMedicion(periodoId, lineaId)" "Llamada interna"
        registrarMedicionInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        registrarMedicionInteractor -> iMedicionRepositorio "acumuladoAprobado(lineaId)" "Llamada interna"
        registrarMedicionInteractor -> medicionOficial "corregir(cantidad, ejecutor)" "Llamada interna"
        registrarMedicionInteractor -> iAlmacenArchivos "guardar(evidencia)" "Llamada interna"
        registrarMedicionInteractor -> evidencia "crear(nombre, tipo, ruta)" "Llamada interna"
        registrarMedicionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, medición)" "Llamada interna"
        web -> aprobarMedicionControlador "listarMediciones(obraId, periodoId)" "Llamada interna"
        aprobarMedicionControlador -> aprobarMedicionInteractor "obtenerPendientes(periodoId)" "Llamada interna"
        aprobarMedicionInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)" "Llamada interna"
        aprobarMedicionInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        aprobarMedicionInteractor -> lineaPresupuesto "saldo(cantidadAcumulada)" "Llamada interna"
        aprobarMedicionInteractor -> evaluarSaldoServicio "evaluar(cantidadMedida, saldo)" "Llamada interna"
        aprobarMedicionInteractor -> propuestaPendiente "crear(exceso, estado = Pendiente)" "Llamada interna"
        aprobarMedicionInteractor -> medicionOficial "aprobar(cantidadCertificable, actorId, fecha)" "Llamada interna"
        aprobarMedicionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, decisión)" "Llamada interna"
        web -> cerrarPeriodoControlador "abrirPeriodo(obraId, periodoId)" "Llamada interna"
        cerrarPeriodoControlador -> cerrarPeriodoInteractor "obtenerEstado(periodoId)" "Llamada interna"
        cerrarPeriodoInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)" "Llamada interna"
        cerrarPeriodoInteractor -> periodo "puedeCerrarse()" "Llamada interna"
        cerrarPeriodoInteractor -> iReloj "ahora()" "Llamada interna"
        cerrarPeriodoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, período, cierre)" "Llamada interna"
        web -> generarBorradorControlador "generarBorrador(obraId, periodoId)" "Llamada interna"
        generarBorradorControlador -> generarBorradorInteractor "ejecutar(periodoId, actorId)" "Llamada interna"
        generarBorradorInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)" "Llamada interna"
        generarBorradorInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        generarBorradorInteractor -> certificado "crear(tipo = interno, estado = Borrador, revisión 1)" "Llamada interna"
        generarBorradorInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)" "Llamada interna"
        generarBorradorInteractor -> detectarAlertasServicio "detectar(lineas, versionVigente)" "Llamada interna"
        generarBorradorInteractor -> iCertificadoRepositorio "guardar(certificado)" "Llamada interna"
        generarBorradorInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, borrador)" "Llamada interna"
        web -> corregirCertificadoControlador "corregirCertificado(certificadoId)" "Llamada interna"
        corregirCertificadoControlador -> corregirCertificadoInteractor "obtenerEmitido(certificadoId)" "Llamada interna"
        corregirCertificadoInteractor -> iCertificadoRepositorio "buscarRevision(revisionId)" "Llamada interna"
        corregirCertificadoInteractor -> revisionCertificado "crear(numero = anterior + 1, revisionAnterior)" "Llamada interna"
        corregirCertificadoInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)" "Llamada interna"
        corregirCertificadoInteractor -> certificado "corregir(revisionNueva)" "Llamada interna"
        corregirCertificadoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, revisión, corrección)" "Llamada interna"
        web -> emitirCertificadoControlador "abrirRevision(revisionId)" "Llamada interna"
        emitirCertificadoControlador -> emitirCertificadoInteractor "obtenerRevision(revisionId)" "Llamada interna"
        emitirCertificadoInteractor -> iCertificadoRepositorio "buscarRevision(revisionId)" "Llamada interna"
        emitirCertificadoInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)" "Llamada interna"
        emitirCertificadoInteractor -> certificado "emitir(numero, fecha, destinatario, actorId)" "Llamada interna"
        emitirCertificadoInteractor -> iGeneradorDocumento "exportar(revision, formato)" "Llamada interna"
        emitirCertificadoInteractor -> iPublicadorEventos "publicar(CertificadoEmitido(certificadoId))" "Llamada interna"
        web -> documentoFinancieroControlador "certificadoEmitido(certificadoId, tipo, monto)" "Llamada interna"
        documentoFinancieroControlador -> derivarDocumentoInteractor "derivar(certificadoId, tipo, monto)" "Llamada interna"
        derivarDocumentoInteractor -> iDocumentoFinancieroRepositorio "buscarPorCertificado(certificadoId)" "Llamada interna"
        derivarDocumentoInteractor -> documentoFinancieroERP "crear(tipo, numero, fecha, monto, estado = Registrado)" "Llamada interna"
        derivarDocumentoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, certificado, documento)" "Llamada interna"
        documentoFinancieroControlador -> web "entrega la factura del certificado" "Llamada interna"
        web -> movimientoControlador "proponerMovimiento(obraId, objetivoId)" "Llamada interna"
        movimientoControlador -> movimientoInteractor "prepararPropuesta(objetivoId)" "Llamada interna"
        movimientoInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        movimientoInteractor -> iAlmacenArchivos "guardar(respaldo)" "Llamada interna"
        movimientoInteractor -> evaluarLimiteServicio "evaluar(tipo, cantidad, precio, saldoVigente)" "Llamada interna"
        movimientoInteractor -> movimientoPresupuestario "crear(tipo, motivo, montoEfecto, limite, estado = Propuesto)" "Llamada interna"
        movimientoInteractor -> iMovimientoRepositorio "guardar(movimiento)" "Llamada interna"
        movimientoInteractor -> versionPresupuesto "crear(numero siguiente, líneas con el movimiento)" "Llamada interna"
        movimientoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, movimiento)" "Llamada interna"
        web -> registrarSubcontratoControlador "nuevoSubcontrato(obraId)" "Llamada interna"
        registrarSubcontratoControlador -> registrarSubcontratoInteractor "prepararAlta(obraId)" "Llamada interna"
        registrarSubcontratoInteractor -> iSubcontratoRepositorio "listarSocios(organizacionId)" "Llamada interna"
        registrarSubcontratoInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        registrarSubcontratoInteractor -> subcontrato "crear(numero, montoContrato, modalidad, alcance)" "Llamada interna"
        registrarSubcontratoInteractor -> iPublicadorEventos "publicar(SubcontratoRegistrado(subcontratoId))" "Llamada interna"
        registrarSubcontratoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, subcontrato, alta)" "Llamada interna"
        web -> consultarSubcontratoControlador "consultarContrato(subcontratoId)" "Llamada interna"
        consultarSubcontratoControlador -> consultarSubcontratoInteractor "ejecutar(subcontratoId, actorId)" "Llamada interna"
        consultarSubcontratoInteractor -> iSubcontratoRepositorio "buscar(subcontratoId)" "Llamada interna"
        consultarSubcontratoInteractor -> subcontrato "perteneceA(socioId)" "Llamada interna"
        consultarSubcontratoInteractor -> iMedicionRepositorio "listarPorSubcontrato(subcontratoId)" "Llamada interna"
        consultarSubcontratoInteractor -> iCertificadoRepositorio "listarPorSubcontrato(subcontratoId)" "Llamada interna"
        consultarSubcontratoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, subcontrato, acceso denegado)" "Llamada interna"
        web -> certificarSubcontratoControlador "certificarSubcontrato(subcontratoId, periodoId)" "Llamada interna"
        certificarSubcontratoControlador -> certificarSubcontratoInteractor "ejecutar(subcontratoId, periodoId, actorId)" "Llamada interna"
        certificarSubcontratoInteractor -> iSubcontratoRepositorio "buscar(subcontratoId)" "Llamada interna"
        certificarSubcontratoInteractor -> iMedicionRepositorio "listarPorSubcontrato(subcontratoId)" "Llamada interna"
        certificarSubcontratoInteractor -> certificado "crear(tipo = subcontrato, estado = Borrador)" "Llamada interna"
        certificarSubcontratoInteractor -> calcularValorizacionServicio "calcular(lineas, preciosContrato)" "Llamada interna"
        certificarSubcontratoInteractor -> iCertificadoRepositorio "siguienteNumero(obraId)" "Llamada interna"
        certificarSubcontratoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, certificado, emisión)" "Llamada interna"
        certificarSubcontratoInteractor -> iPublicadorEventos "publicar(CertificadoEmitido(certificadoId))" "Llamada interna"
        web -> calcularCostosControlador "analizarCostos(obraId, fechaCorte)" "Llamada interna"
        calcularCostosControlador -> calcularCostosInteractor "ejecutar(obraId, fechaCorte, actorId)" "Llamada interna"
        calcularCostosInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        calcularCostosInteractor -> calcularCostoViaServicio "calcular(acu, via)" "Llamada interna"
        calcularCostoViaServicio -> analisisCostoUnitario "componentesPorVia(via)" "Llamada interna"
        web -> consultarReportesControlador "consultarCurvaS(obraId, fechaCorte)" "Llamada interna"
        consultarReportesControlador -> consultarReportesInteractor "curvaS(obraId, fechaCorte, actorId)" "Llamada interna"
        consultarReportesInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)" "Llamada interna"
        consultarReportesInteractor -> iConsultaReportes "avanceFisico(obraId, fechaCorte)" "Llamada interna"
        consultarReportesInteractor -> generarCurvaSServicio "componer(series, fechaCorte)" "Llamada interna"
        obraRepositorioSQL -> iObraRepositorio "Implementa" "Inyección de dependencias"
        usuarioRepositorioSQL -> iUsuarioRepositorio "Implementa" "Inyección de dependencias"
        auditoriaRepositorioSQL -> iAuditoriaRepositorio "Implementa" "Inyección de dependencias"
        presupuestoRepositorioSQL -> iPresupuestoRepositorio "Implementa" "Inyección de dependencias"
        almacenArchivosS3 -> iAlmacenArchivos "Implementa" "Inyección de dependencias"
        lectorPlanillaXLSX -> iLectorPlanilla "Implementa" "Inyección de dependencias"
        relojSistema -> iReloj "Implementa" "Inyección de dependencias"
        medicionRepositorioSQL -> iMedicionRepositorio "Implementa" "Inyección de dependencias"
        certificadoRepositorioSQL -> iCertificadoRepositorio "Implementa" "Inyección de dependencias"
        generadorDocumentoXLSXPDF -> iGeneradorDocumento "Implementa" "Inyección de dependencias"
        puenteERP -> iPublicadorEventos "Implementa" "Inyección de dependencias"
        documentoFinancieroRepositorioERP -> iDocumentoFinancieroRepositorio "Implementa" "Inyección de dependencias"
        movimientoRepositorioSQL -> iMovimientoRepositorio "Implementa" "Inyección de dependencias"
        subcontratoRepositorioSQL -> iSubcontratoRepositorio "Implementa" "Inyección de dependencias"
        consultaReportesSQL -> iConsultaReportes "Implementa" "Inyección de dependencias"
        organizacion -> obra "Agrupa (1 a 0..*)" "Referencia de dominio"
        organizacion -> usuario "Agrupa (1 a 1..*)" "Referencia de dominio"
        usuario -> rolAsignado "Se compone de (1 a 0..*)" "Referencia de dominio"
        obra -> rolAsignado "Se asocia con (1 a 0..*)" "Referencia de dominio"
        cliente -> obra "comitente (1 a 0..*)" "Referencia de dominio"
        obra -> configuracionObra "Se compone de (1 a 1)" "Referencia de dominio"
        configuracionObra -> fondoRetencion "Se compone de (1 a 0..*)" "Referencia de dominio"
        obra -> presupuesto "Se compone de (1 a 1..*)" "Referencia de dominio"
        presupuesto -> versionPresupuesto "Se compone de (1 a 1..*)" "Referencia de dominio"
        versionPresupuesto -> lineaPresupuesto "Se compone de (1 a 1..*)" "Referencia de dominio"
        lineaPresupuesto -> lineaPresupuesto "jerarquía rubro/subrubro/ítem (0..1 a 0..*)" "Referencia de dominio"
        versionPresupuesto -> archivoOrigen "Se compone de (1 a 0..1)" "Referencia de dominio"
        versionPresupuesto -> informeImportacion "Se compone de (1 a 0..1)" "Referencia de dominio"
        analisisCostoUnitario -> lineaPresupuesto "Se asocia con (0..1 a 0..*)" "Referencia de dominio"
        analisisCostoUnitario -> componenteACU "Se compone de (1 a 1..*)" "Referencia de dominio"
        obra -> analisisCostoUnitario "Agrupa (1 a 0..*)" "Referencia de dominio"
        obra -> periodo "Se compone de (1 a 0..*)" "Referencia de dominio"
        periodo -> medicionOficial "Se compone de (1 a 0..*)" "Referencia de dominio"
        lineaPresupuesto -> medicionOficial "Se asocia con (1 a 0..*)" "Referencia de dominio"
        versionPresupuesto -> medicionOficial "medida contra (1 a 0..*)" "Referencia de dominio"
        usuario -> medicionOficial "registra (1 a 0..*)" "Referencia de dominio"
        medicionOficial -> evidencia "Se compone de (1 a 0..*)" "Referencia de dominio"
        medicionOficial -> propuestaPendiente "Se compone de (1 a 0..1)" "Referencia de dominio"
        movimientoPresupuestario -> propuestaPendiente "cubre (0..1 a 0..*)" "Referencia de dominio"
        lineaPresupuesto -> movimientoPresupuestario "objetivo (1 a 0..*)" "Referencia de dominio"
        versionPresupuesto -> movimientoPresupuestario "genera (0..1 a 0..*)" "Referencia de dominio"
        periodo -> certificado "Se asocia con (1 a 0..*)" "Referencia de dominio"
        subcontrato -> certificado "Se asocia con (0..1 a 0..*)" "Referencia de dominio"
        certificado -> revisionCertificado "Se compone de (1 a 1..*)" "Referencia de dominio"
        revisionCertificado -> lineaCertificado "Se compone de (1 a 1..*)" "Referencia de dominio"
        medicionOficial -> lineaCertificado "Se asocia con (1 a 0..1)" "Referencia de dominio"
        lineaPresupuesto -> lineaCertificado "Se asocia con (1 a 0..*)" "Referencia de dominio"
        usuario -> certificado "emite (0..1 a 0..*)" "Referencia de dominio"
        movimientoPresupuestario -> aprobacion "Se compone de (0..1 a 0..*)" "Referencia de dominio"
        usuario -> aprobacion "Se asocia con (1 a 0..*)" "Referencia de dominio"
        revisionCertificado -> retencionAplicada "Se compone de (1 a 0..*)" "Referencia de dominio"
        fondoRetencion -> retencionAplicada "Se asocia con (1 a 0..*)" "Referencia de dominio"
        certificado -> documentoFinancieroERP "Se asocia con (1 a 0..1)" "Referencia de dominio"
        obra -> subcontrato "Agrupa (1 a 0..*)" "Referencia de dominio"
        socio -> subcontrato "Se asocia con (1 a 0..*)" "Referencia de dominio"
        crearObraInteractor -> obraPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        importarPresupuestoInteractor -> importacionPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        activarVersionInteractor -> versionPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        registrarMedicionInteractor -> medicionPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        aprobarMedicionInteractor -> medicionPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        cerrarPeriodoInteractor -> periodoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        generarBorradorInteractor -> certificadoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        corregirCertificadoInteractor -> certificadoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        emitirCertificadoInteractor -> certificadoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        derivarDocumentoInteractor -> documentoFinancieroPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        movimientoInteractor -> movimientoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        registrarSubcontratoInteractor -> subcontratoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        consultarSubcontratoInteractor -> subcontratoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        certificarSubcontratoInteractor -> certificadoPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        calcularCostosInteractor -> costosPresentador "Entrega el resultado del caso de uso" "Llamada interna"
        consultarReportesInteractor -> reportePresentador "Entrega el resultado del caso de uso" "Llamada interna"
        calcularValorizacionServicio -> valorizacion "Produce" "Llamada interna"
    }

    views {
        systemLandscape "Paisaje" "Obra Studio y las personas que intervienen." {
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
        dynamic ecms "CU01" "CU-01 — Crear obra y asignar responsables." {
            web -> crearObraControlador "nuevaObra(organizacionId)"
            crearObraControlador -> crearObraInteractor "prepararAlta(organizacionId)"
            crearObraInteractor -> iUsuarioRepositorio "listarMiembros(organizacionId)"
            crearObraInteractor -> iObraRepositorio "existeCodigo(codigo)"
            crearObraInteractor -> obra "crear(codigo, nombre, direccion, fechas, clienteId)"
            crearObraInteractor -> rolAsignado "crear(usuarioId, rol, vigenteDesde)"
            crearObraInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, alta)"
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
        dynamic ecms "CU03" "CU-03 — Confirmar estructura y activar versión vigente." {
            web -> activarVersionControlador "abrirVersion(versionId)"
            activarVersionControlador -> activarVersionInteractor "obtenerVersion(versionId)"
            activarVersionInteractor -> iPresupuestoRepositorio "buscarVersion(versionId)"
            activarVersionInteractor -> iReloj "ahora()"
            activarVersionInteractor -> versionPresupuesto "confirmarEstructura()"
            activarVersionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, activación)"
            autolayout lr
        }
        dynamic ecms "CU04" "CU-04 — Registrar medición oficial." {
            web -> registrarMedicionControlador "abrirMedicion(obraId, periodoId, lineaId)"
            registrarMedicionControlador -> registrarMedicionInteractor "prepararMedicion(periodoId, lineaId)"
            registrarMedicionInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            registrarMedicionInteractor -> iMedicionRepositorio "acumuladoAprobado(lineaId)"
            registrarMedicionInteractor -> medicionOficial "corregir(cantidad, ejecutor)"
            registrarMedicionInteractor -> iAlmacenArchivos "guardar(evidencia)"
            registrarMedicionInteractor -> evidencia "crear(nombre, tipo, ruta)"
            registrarMedicionInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, medición)"
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
        dynamic ecms "CU06" "CU-06 — Cerrar período de medición." {
            web -> cerrarPeriodoControlador "abrirPeriodo(obraId, periodoId)"
            cerrarPeriodoControlador -> cerrarPeriodoInteractor "obtenerEstado(periodoId)"
            cerrarPeriodoInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)"
            cerrarPeriodoInteractor -> periodo "puedeCerrarse()"
            cerrarPeriodoInteractor -> iReloj "ahora()"
            cerrarPeriodoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, período, cierre)"
            autolayout lr
        }
        dynamic ecms "CU07" "CU-07 — Generar borrador de certificado." {
            web -> generarBorradorControlador "generarBorrador(obraId, periodoId)"
            generarBorradorControlador -> generarBorradorInteractor "ejecutar(periodoId, actorId)"
            generarBorradorInteractor -> iMedicionRepositorio "listarPorPeriodo(periodoId)"
            generarBorradorInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            generarBorradorInteractor -> certificado "crear(tipo = interno, estado = Borrador, revisión 1)"
            generarBorradorInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)"
            generarBorradorInteractor -> detectarAlertasServicio "detectar(lineas, versionVigente)"
            generarBorradorInteractor -> iCertificadoRepositorio "guardar(certificado)"
            generarBorradorInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, borrador)"
            autolayout lr
        }
        dynamic ecms "CU08" "CU-08 — Corregir certificado emitido." {
            web -> corregirCertificadoControlador "corregirCertificado(certificadoId)"
            corregirCertificadoControlador -> corregirCertificadoInteractor "obtenerEmitido(certificadoId)"
            corregirCertificadoInteractor -> iCertificadoRepositorio "buscarRevision(revisionId)"
            corregirCertificadoInteractor -> revisionCertificado "crear(numero = anterior + 1, revisionAnterior)"
            corregirCertificadoInteractor -> calcularValorizacionServicio "calcular(lineas, configuracionObra)"
            corregirCertificadoInteractor -> certificado "corregir(revisionNueva)"
            corregirCertificadoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, revisión, corrección)"
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
        dynamic ecms "CU10" "CU-10 — Derivar documento financiero en ERP." {
            web -> documentoFinancieroControlador "certificadoEmitido(certificadoId, tipo, monto)"
            documentoFinancieroControlador -> derivarDocumentoInteractor "derivar(certificadoId, tipo, monto)"
            derivarDocumentoInteractor -> iDocumentoFinancieroRepositorio "buscarPorCertificado(certificadoId)"
            derivarDocumentoInteractor -> documentoFinancieroERP "crear(tipo, numero, fecha, monto, estado = Registrado)"
            derivarDocumentoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, certificado, documento)"
            documentoFinancieroControlador -> web "entrega la factura del certificado"
            autolayout lr
        }
        dynamic ecms "CU11" "CU-11 — Proponer y aprobar movimiento presupuestario." {
            web -> movimientoControlador "proponerMovimiento(obraId, objetivoId)"
            movimientoControlador -> movimientoInteractor "prepararPropuesta(objetivoId)"
            movimientoInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            movimientoInteractor -> iAlmacenArchivos "guardar(respaldo)"
            movimientoInteractor -> evaluarLimiteServicio "evaluar(tipo, cantidad, precio, saldoVigente)"
            movimientoInteractor -> movimientoPresupuestario "crear(tipo, motivo, montoEfecto, limite, estado = Propuesto)"
            movimientoInteractor -> iMovimientoRepositorio "guardar(movimiento)"
            movimientoInteractor -> versionPresupuesto "crear(numero siguiente, líneas con el movimiento)"
            movimientoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, version, movimiento)"
            autolayout lr
        }
        dynamic ecms "CU12" "CU-12 — Registrar contrato de subcontrato." {
            web -> registrarSubcontratoControlador "nuevoSubcontrato(obraId)"
            registrarSubcontratoControlador -> registrarSubcontratoInteractor "prepararAlta(obraId)"
            registrarSubcontratoInteractor -> iSubcontratoRepositorio "listarSocios(organizacionId)"
            registrarSubcontratoInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            registrarSubcontratoInteractor -> subcontrato "crear(numero, montoContrato, modalidad, alcance)"
            registrarSubcontratoInteractor -> iPublicadorEventos "publicar(SubcontratoRegistrado(subcontratoId))"
            registrarSubcontratoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, subcontrato, alta)"
            autolayout lr
        }
        dynamic ecms "CU13" "CU-13 — Consultar estado del subcontrato." {
            web -> consultarSubcontratoControlador "consultarContrato(subcontratoId)"
            consultarSubcontratoControlador -> consultarSubcontratoInteractor "ejecutar(subcontratoId, actorId)"
            consultarSubcontratoInteractor -> iSubcontratoRepositorio "buscar(subcontratoId)"
            consultarSubcontratoInteractor -> subcontrato "perteneceA(socioId)"
            consultarSubcontratoInteractor -> iMedicionRepositorio "listarPorSubcontrato(subcontratoId)"
            consultarSubcontratoInteractor -> iCertificadoRepositorio "listarPorSubcontrato(subcontratoId)"
            consultarSubcontratoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, subcontrato, acceso denegado)"
            autolayout lr
        }
        dynamic ecms "CU14" "CU-14 — Certificar y valorizar subcontrato." {
            web -> certificarSubcontratoControlador "certificarSubcontrato(subcontratoId, periodoId)"
            certificarSubcontratoControlador -> certificarSubcontratoInteractor "ejecutar(subcontratoId, periodoId, actorId)"
            certificarSubcontratoInteractor -> iSubcontratoRepositorio "buscar(subcontratoId)"
            certificarSubcontratoInteractor -> iMedicionRepositorio "listarPorSubcontrato(subcontratoId)"
            certificarSubcontratoInteractor -> certificado "crear(tipo = subcontrato, estado = Borrador)"
            certificarSubcontratoInteractor -> calcularValorizacionServicio "calcular(lineas, preciosContrato)"
            certificarSubcontratoInteractor -> iCertificadoRepositorio "siguienteNumero(obraId)"
            certificarSubcontratoInteractor -> iAuditoriaRepositorio "registrar(actor, fecha, obra, certificado, emisión)"
            certificarSubcontratoInteractor -> iPublicadorEventos "publicar(CertificadoEmitido(certificadoId))"
            autolayout lr
        }
        dynamic ecms "CU15" "CU-15 — Calcular costos por vía." {
            web -> calcularCostosControlador "analizarCostos(obraId, fechaCorte)"
            calcularCostosControlador -> calcularCostosInteractor "ejecutar(obraId, fechaCorte, actorId)"
            calcularCostosInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            calcularCostosInteractor -> calcularCostoViaServicio "calcular(acu, via)"
            calcularCostoViaServicio -> analisisCostoUnitario "componentesPorVia(via)"
            autolayout lr
        }
        dynamic ecms "CU16" "CU-16 — Consultar reportes y Curva S." {
            web -> consultarReportesControlador "consultarCurvaS(obraId, fechaCorte)"
            consultarReportesControlador -> consultarReportesInteractor "curvaS(obraId, fechaCorte, actorId)"
            consultarReportesInteractor -> iPresupuestoRepositorio "buscarVersionVigente(obraId)"
            consultarReportesInteractor -> iConsultaReportes "avanceFisico(obraId, fechaCorte)"
            consultarReportesInteractor -> generarCurvaSServicio "componer(series, fechaCorte)"
            autolayout lr
        }
        image * "umlCU01actividades" {
            image out/CU-01-actividades.png
            title "UML — CU-01-actividades"
        }
        image * "umlCU01clases" {
            image out/CU-01-clases.png
            title "UML — CU-01-clases"
        }
        image * "umlCU01secuencia" {
            image out/CU-01-secuencia.png
            title "UML — CU-01-secuencia"
        }
        image * "umlCU02actividades" {
            image out/CU-02-actividades.png
            title "UML — CU-02-actividades"
        }
        image * "umlCU02clases" {
            image out/CU-02-clases.png
            title "UML — CU-02-clases"
        }
        image * "umlCU02secuencia" {
            image out/CU-02-secuencia.png
            title "UML — CU-02-secuencia"
        }
        image * "umlCU03actividades" {
            image out/CU-03-actividades.png
            title "UML — CU-03-actividades"
        }
        image * "umlCU03clases" {
            image out/CU-03-clases.png
            title "UML — CU-03-clases"
        }
        image * "umlCU03secuencia" {
            image out/CU-03-secuencia.png
            title "UML — CU-03-secuencia"
        }
        image * "umlCU04actividades" {
            image out/CU-04-actividades.png
            title "UML — CU-04-actividades"
        }
        image * "umlCU04clases" {
            image out/CU-04-clases.png
            title "UML — CU-04-clases"
        }
        image * "umlCU04secuencia" {
            image out/CU-04-secuencia.png
            title "UML — CU-04-secuencia"
        }
        image * "umlCU05actividades" {
            image out/CU-05-actividades.png
            title "UML — CU-05-actividades"
        }
        image * "umlCU05clases" {
            image out/CU-05-clases.png
            title "UML — CU-05-clases"
        }
        image * "umlCU05secuencia" {
            image out/CU-05-secuencia.png
            title "UML — CU-05-secuencia"
        }
        image * "umlCU06actividades" {
            image out/CU-06-actividades.png
            title "UML — CU-06-actividades"
        }
        image * "umlCU06clases" {
            image out/CU-06-clases.png
            title "UML — CU-06-clases"
        }
        image * "umlCU06secuencia" {
            image out/CU-06-secuencia.png
            title "UML — CU-06-secuencia"
        }
        image * "umlCU07actividades" {
            image out/CU-07-actividades.png
            title "UML — CU-07-actividades"
        }
        image * "umlCU07clases" {
            image out/CU-07-clases.png
            title "UML — CU-07-clases"
        }
        image * "umlCU07secuencia" {
            image out/CU-07-secuencia.png
            title "UML — CU-07-secuencia"
        }
        image * "umlCU08actividades" {
            image out/CU-08-actividades.png
            title "UML — CU-08-actividades"
        }
        image * "umlCU08clases" {
            image out/CU-08-clases.png
            title "UML — CU-08-clases"
        }
        image * "umlCU08secuencia" {
            image out/CU-08-secuencia.png
            title "UML — CU-08-secuencia"
        }
        image * "umlCU09clases" {
            image out/CU-09-clases.png
            title "UML — CU-09-clases"
        }
        image * "umlCU09secuencia" {
            image out/CU-09-secuencia.png
            title "UML — CU-09-secuencia"
        }
        image * "umlCU10actividades" {
            image out/CU-10-actividades.png
            title "UML — CU-10-actividades"
        }
        image * "umlCU10clases" {
            image out/CU-10-clases.png
            title "UML — CU-10-clases"
        }
        image * "umlCU10secuencia" {
            image out/CU-10-secuencia.png
            title "UML — CU-10-secuencia"
        }
        image * "umlCU11actividades" {
            image out/CU-11-actividades.png
            title "UML — CU-11-actividades"
        }
        image * "umlCU11clases" {
            image out/CU-11-clases.png
            title "UML — CU-11-clases"
        }
        image * "umlCU11secuencia" {
            image out/CU-11-secuencia.png
            title "UML — CU-11-secuencia"
        }
        image * "umlCU12actividades" {
            image out/CU-12-actividades.png
            title "UML — CU-12-actividades"
        }
        image * "umlCU12clases" {
            image out/CU-12-clases.png
            title "UML — CU-12-clases"
        }
        image * "umlCU12secuencia" {
            image out/CU-12-secuencia.png
            title "UML — CU-12-secuencia"
        }
        image * "umlCU13actividades" {
            image out/CU-13-actividades.png
            title "UML — CU-13-actividades"
        }
        image * "umlCU13clases" {
            image out/CU-13-clases.png
            title "UML — CU-13-clases"
        }
        image * "umlCU13secuencia" {
            image out/CU-13-secuencia.png
            title "UML — CU-13-secuencia"
        }
        image * "umlCU14actividades" {
            image out/CU-14-actividades.png
            title "UML — CU-14-actividades"
        }
        image * "umlCU14clases" {
            image out/CU-14-clases.png
            title "UML — CU-14-clases"
        }
        image * "umlCU14secuencia" {
            image out/CU-14-secuencia.png
            title "UML — CU-14-secuencia"
        }
        image * "umlCU15actividades" {
            image out/CU-15-actividades.png
            title "UML — CU-15-actividades"
        }
        image * "umlCU15clases" {
            image out/CU-15-clases.png
            title "UML — CU-15-clases"
        }
        image * "umlCU15secuencia" {
            image out/CU-15-secuencia.png
            title "UML — CU-15-secuencia"
        }
        image * "umlCU16actividades" {
            image out/CU-16-actividades.png
            title "UML — CU-16-actividades"
        }
        image * "umlCU16clases" {
            image out/CU-16-clases.png
            title "UML — CU-16-clases"
        }
        image * "umlCU16secuencia" {
            image out/CU-16-secuencia.png
            title "UML — CU-16-secuencia"
        }
        image * "umlcasosdeusoA" {
            image out/casos-de-uso-A.png
            title "UML — casos-de-uso-A"
        }
        image * "umlcasosdeusoB" {
            image out/casos-de-uso-B.png
            title "UML — casos-de-uso-B"
        }
        image * "umlcasosdeusoaltonivel" {
            image out/casos-de-uso-alto-nivel.png
            title "UML — casos-de-uso-alto-nivel"
        }
        image * "umlclasespersistentesA" {
            image out/clases-persistentes-A.png
            title "UML — clases-persistentes-A"
        }
        image * "umlclasespersistentesB" {
            image out/clases-persistentes-B.png
            title "UML — clases-persistentes-B"
        }
        image * "umlentidadrelacion" {
            image out/entidad-relacion.png
            title "UML — entidad-relacion"
        }
        image * "umlestadoCertificado" {
            image out/estado-Certificado.png
            title "UML — estado-Certificado"
        }
        image * "umlestadoDocumentoFinancieroERP" {
            image out/estado-DocumentoFinancieroERP.png
            title "UML — estado-DocumentoFinancieroERP"
        }
        image * "umlestadoMedicionOficial" {
            image out/estado-MedicionOficial.png
            title "UML — estado-MedicionOficial"
        }
        image * "umlestadoMovimientoPresupuestario" {
            image out/estado-MovimientoPresupuestario.png
            title "UML — estado-MovimientoPresupuestario"
        }
        image * "umlestadoPeriodo" {
            image out/estado-Periodo.png
            title "UML — estado-Periodo"
        }
        image * "umlestadoVersionPresupuesto" {
            image out/estado-VersionPresupuesto.png
            title "UML — estado-VersionPresupuesto"
        }
        image * "umlgeneralizacionactores" {
            image out/generalizacion-actores.png
            title "UML — generalizacion-actores"
        }
        image * "umlmodeloconceptual" {
            image out/modelo-conceptual.png
            title "UML — modelo-conceptual"
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
