# INFORME FINAL DEL PROYECTO: NETSIGHT

---

### Resumen
El proyecto NetSight implementa una plataforma distribuida de telemetría y ciberseguridad para la red de laboratorios de la Escuela Profesional de Ingeniería de Sistemas (EPIS) de la Universidad Privada de Tacna. Ante la falta de visibilidad en el tráfico de red local y los constantes incidentes que merman el rendimiento de los equipos y degradan la calidad del servicio educativo, esta propuesta recolecta y procesa metadatos a nivel de kernel utilizando Sysmon y Wazuh Agent. Estos datos son transmitidos de forma segura a una nube en Azure, donde un motor ETL en Python limpia y geolocaliza las conexiones antes de almacenarlas en PostgreSQL. Finalmente, la analítica es consumida mediante un portal en Next.js y tableros interactivos en Power BI (DirectQuery). El estudio demostró que esta solución open source no requiere costos de licenciamiento por equipo, operando con un presupuesto de S/ 11,850.00, una Tasa Interna de Retorno (TIR) del 143% y un Ratio Beneficio/Costo de 2.58.

### Abstract
The NetSight project implements a distributed telemetry and cybersecurity platform for the computer laboratories network at the School of Systems Engineering (EPIS) of the Private University of Tacna. Addressing the lack of visibility in local network traffic and constant incidents that degrade computer performance and academic quality, this proposal collects and processes metadata at the kernel level using Sysmon and Wazuh Agent. These data are securely transmitted to an Azure cloud instance, where a Python ETL engine cleanses and geolocalizes connections before storing them in PostgreSQL. Finally, the analytics are accessed through a Next.js portal and interactive Power BI dashboards via DirectQuery. The study demonstrated that this open-source solution requires no endpoint licensing fees, operating with a budget of S/ 11,850.00, an Internal Rate of Return (IRR) of 143%, and a Benefit/Cost Ratio of 2.58.

---

## 1. Antecedentes o introducción
La Escuela Profesional de Ingeniería de Sistemas (EPIS) de la Universidad Privada de Tacna (UPT) administra una infraestructura compuesta por múltiples laboratorios especializados (Redes, Desarrollo de Software, Sistemas Operativos, etc.). Estos espacios son utilizados intensivamente de forma diaria por cientos de estudiantes y docentes de diferentes ciclos académicos.

Históricamente, la administración y mantenimiento de este parque informático ha operado bajo un modelo estrictamente manual y reactivo. La Jefatura de Laboratorios y el equipo de Soporte Técnico dependían exclusivamente de reportes manuales respecto a anomalías como "internet excesivamente lento", "computadoras congeladas" o "pantallas azules". Esta carencia de un sistema de telemetría o auditoría técnica automatizada ha derivado sistemáticamente en el desgaste prematuro de los equipos de cómputo, el abuso del ancho de banda institucional para fines no académicos, y una carga operativa insostenible para el personal técnico, quienes debían trasladarse físicamente a diagnosticar cada máquina de manera individual.

---

## 2. Título
**NetSight: Sistema de Telemetría y Ciberseguridad para Laboratorios de Cómputo**

---

## 3. Autores
*   **Renzo Antayhua** (Estudiante de Ingeniería de Sistemas - EPIS)
*   **Joan Cristian Medina Quispe** (Estudiante de Ingeniería de Sistemas - EPIS - Código: 2022074255)

---

## 4. Planteamiento del problema

### 4.1. Problema
El problema nuclear radica en la **ausencia absoluta de visibilidad proactiva y trazabilidad digital** dentro de la red de laboratorios de la EPIS. Cuando ocurre un incidente cibernético (como un ataque de denegación de servicio interno) o un abuso de recursos (ej. ejecución de software de minería de criptomonedas o descargas de *torrents* P2P), el estudiante infractor suele borrar su historial de navegación y procesos. Al no existir un repositorio centralizado de *logs* (SIEM), el técnico de soporte se ve forzado a revisar localmente el "Visor de Eventos" de Windows, incurriendo en un Tiempo Medio de Resolución (MTTR) de horas o días, y usualmente sin lograr recolectar evidencia inmutable. Esto genera impunidad ante infracciones a la red universitaria y ceguera para la toma de decisiones directivas.

### 4.2. Justificación
La implementación de una solución tecnológica moderna es imperativa y se justifica en tres ejes fundamentales:
*   **Eje Tecnológico y Patrimonial:** Prolongar la vida útil del hardware (procesadores y discos SSD) previniendo el estrés térmico ocasionado por *malware* o procesos no autorizados que corren en segundo plano.
*   **Eje Económico y Operativo:** El proyecto demuestra que la prevención de daños y la reducción del 60% del tiempo invertido por el personal de TI en diagnósticos manuales, supera ampliamente y justifica con creces el bajo costo operativo mensual del servidor en la nube.
*   **Eje Académico:** Garantizar a la plana docente un entorno de red robusto, rápido y estable, permitiendo que las sesiones prácticas se desarrollen sin interrupciones técnicas.

### 4.3. Alcance
El proyecto abarca el ciclo de vida completo del procesamiento de datos de telemetría.
*   **Incluye:** La extracción de metadatos desde el Kernel de Windows en las PCs locales (usando Sysmon y Wazuh Agent), su transmisión cifrada (TLS 1.2+) hacia la nube de Azure, su procesamiento y enriquecimiento geográfico mediante un motor ETL en Python, y su consolidación final en PostgreSQL. Culmina con la capa de presentación mediante un Dashboard web de gestión (Next.js) y lienzos de inteligencia de negocios interactivos (Power BI).
*   **No incluye:** El desarrollo de hardware propietario, la provisión de servicio de internet, ni la intervención o reconfiguración física de los enrutadores/switches perimetrales de la UPT.

---

## 5. Objetivos

### 5.1. General
Desarrollar, integrar y desplegar el Sistema de Telemetría de Laboratorios (NetSight) para transformar la administración reactiva de TI en un modelo predictivo y proactivo, centralizando el análisis forense de la red y optimizando la gobernanza de la infraestructura de la EPIS.

### 5.2. Específicos
1.  **Implementar un agente recolector silencioso (*Zero-Touch*):** Desplegar Sysmon y Wazuh en las terminales mediante un autoinstalador para capturar metadatos sin impacto en el rendimiento (< 1% CPU).
2.  **Desarrollar un motor ETL asíncrono:** Construir una tubería de datos en Python que extraiga registros crudos de OpenSearch, resuelva las IPs a ubicaciones geográficas y ejecute inserciones masivas (*Bulk Inserts*) en PostgreSQL.
3.  **Diseñar tableros visuales interactivos (*Dashboards*):** Proveer a la Jefatura y Administradores de herramientas de inteligencia de negocios para el descubrimiento interactivo de amenazas.
4.  **Garantizar la inmutabilidad forense:** Asegurar que la evidencia recolectada esté firmada con Hashes criptográficos (SHA-256) directamente desde el origen, impidiendo la falsificación de datos por parte de los alumnos.

---

## 6. Marco Teórico

El desarrollo del proyecto NetSight se fundamenta en la convergencia de la ciberseguridad defensiva, la ingeniería de datos y la inteligencia de negocios. A continuación, se detallan los pilares teóricos y tecnológicos que sustentan la arquitectura del sistema:

### 6.1. EDR (Endpoint Detection and Response) y HIDS (Host-based Intrusion Detection System)
En el ámbito de la seguridad de la información, el monitoreo tradicional basado en redes (NIDS) ha perdido efectividad debido al uso masivo del cifrado de tráfico (SSL/TLS). Por ello, la ciberseguridad defensiva moderna se desplaza hacia los **Endpoints** (terminales de usuario).
*   **HIDS:** Es una herramienta residente en el host que monitorea y analiza las partes internas de un sistema informático, tales como llamadas al sistema, cambios en el registro y modificaciones de archivos críticos (FIM).
*   **EDR:** Evoluciona el concepto del HIDS al no solo monitorear, sino también registrar de forma continua las actividades del dispositivo (procesos y conexiones de red) y aplicar reglas analíticas complejas para responder ante comportamientos sospechosos o malware persistente.
En este proyecto, **Wazuh** actúa como el núcleo HIDS/EDR distribuido. Utiliza agentes ligeros que establecen canales seguros (TLS 1.2) con un servidor manager central para transmitir de forma ininterrumpida la telemetría del sistema operativo cliente.

### 6.2. Auditoría Forense y Monitoreo a nivel Kernel (Sysmon)
Para lograr una trazabilidad digital inmutable y detallada, es necesario interceptar los eventos directamente desde el kernel del sistema operativo.
*   **Microsoft Sysmon (System Monitor):** Es un servicio del sistema y controlador de dispositivo (*device driver*) de la suite Sysinternals que se instala en el anillo 0 (*Ring 0*) de Windows. Permite registrar en el registro de eventos de Windows (Application and Services Logs/Microsoft/Windows/Sysmon/Operational) detalles forenses críticos de la actividad del host.
NetSight depende heurísticamente de dos identificadores de evento específicos de Sysmon:
*   **Event ID 3 (NetworkConnect):** Captura todas las conexiones de red TCP/UDP salientes y entrantes, registrando la dirección IP de origen, puerto, IP de destino, protocolo y la ruta completa del proceso ejecutable (`image`) que inició la llamada.
*   **Event ID 22 (DnsQuery):** Registra las consultas de resolución de nombres de dominio realizadas por cualquier proceso, lo cual es vital para auditar la comunicación con servidores de comando y control (C2) o el desvío de tráfico a través de proxies.

### 6.3. SIEM y Almacenamiento NoSQL de Alta Velocidad (OpenSearch)
El volumen de logs generados por cientos de computadoras en tiempo real es extremadamente alto, catalogándolo como un escenario de **Big Data**. La gestión y consulta de esta información requiere un enfoque **SIEM** (*Security Information and Event Management*).
*   **SIEM:** Centraliza la ingesta de telemetría de múltiples agentes, normaliza los datos y provee capacidades de búsqueda heurística y correlación de alertas.
*   **OpenSearch (Wazuh Indexer):** Es un motor de búsqueda y analítica NoSQL distribuido, derivado de Elasticsearch. Almacena la telemetría en documentos JSON indexados mediante estructuras invertidas (*inverted indexes*). Esto permite la indexación en milisegundos de millones de logs crudos y consultas de búsqueda complejas, actuando como un búfer o *Data Lake* amortiguador de alta velocidad.

### 6.4. Pipelines de Datos e Integración ETL (Python)
Aunque un SIEM (como OpenSearch) es excelente para almacenar logs crudos y realizar búsquedas de texto plano, carece de la estructura relacional necesaria para auditorías cruzadas complejas, inventariado de TI o modelados rápidos de Inteligencia de Negocios (BI). Por tanto, se requiere un flujo **ETL** (*Extract, Transform, Load*):
1.  **Extracción:** El pipeline lee de forma incremental (usando cursores temporales almacenados en una tabla de control `etl_estado`) los eventos JSON crudos desde OpenSearch a través de su REST API.
2.  **Transformación:** Se limpian los nombres de los hostnames y procesos (`LOWER(TRIM())`) para evitar fallos de llaves foráneas. Asimismo, se inyecta geolocalización física para tráfico externo consultando localmente la base de datos de ciudad/país de **MaxMind GeoIP**, reduciendo la necesidad de APIs externas que ralenticen el flujo.
3.  **Carga:** Los registros enriquecidos se insertan en PostgreSQL utilizando la técnica de inserción masiva por bloques (*Bulk Inserts*), minimizando el overhead de red y los bloqueos de base de datos.

### 6.5. Inteligencia de Negocios (BI) y Consultas DirectQuery
La toma de decisiones gerenciales y técnicas requiere una interfaz analítica que no sufra de latencias y presente datos actualizados al instante.
*   **Modelo en Estrella (Star Schema):** Es un enfoque de modelado de datos que separa la información en Tablas de Hechos (transacciones o eventos como `trafico_red`) y Tablas de Dimensiones (entidades como `computadoras` o `laboratorios`).
*   **DirectQuery (Power BI):** A diferencia de la importación tradicional que copia los datos a la memoria de Power BI de forma programada, DirectQuery realiza consultas SQL inmediatas a la base de datos PostgreSQL cada vez que el usuario interactúa con un visual. Esto garantiza que las alertas de ciberseguridad y el monitoreo de laboratorios ocurran en tiempo real sin requerir refrescos programados o consumo innecesario de almacenamiento local.


---

## 7. Desarrollo de la propuesta

### 7.1. Análisis de Factibilidad

*   **Factibilidad Técnica:** El software se integra con librerías nativas de Windows a través de Sysmon (desarrollado por Microsoft) y el agente de Wazuh, herramientas consolidadas a nivel global. El backend utiliza Python 3.10+ y PostgreSQL, plataformas altamente compatibles con el parque de hardware actual.
*   **Factibilidad Económica:** Se descartan licencias comerciales (CrowdStrike, Splunk) que cobran por dispositivo. El costo de desarrollo fue de S/ 11,850.00 y el costo en la nube es de S/ 2,250.00 anuales. El análisis financiero proyectado a 3 años arrojó un Valor Actual Neto (VAN) de **S/ 33,286.00**, una Tasa Interna de Retorno (TIR) del **143%**, y un Ratio Beneficio/Costo (B/C) de **2.58**, garantizando el retorno rápido de la inversión.
*   **Factibilidad Operativa:** El instalador C# WPF automatiza la inscripción de la computadora en un solo clic, sin requerir conocimientos técnicos avanzados por parte del personal de soporte. El dashboard en Next.js unifica el control en una interfaz amigable.
*   **Factibilidad Social:** Asegura un entorno académico de alta velocidad y libre de malware para los estudiantes de la EPIS. Además, promueve la cultura de análisis de datos y transparencia entre la plana docente y los directivos.
*   **Factibilidad Legal:** Cumple estrictamente con la Ley N° 29733 (Ley de Protección de Datos Personales en el Perú) ya que recolecta exclusivamente metadatos técnicos de red (IPs, puertos, protocolos) y hashes del sistema, excluyendo de forma nativa datos personales, historial de teclas (keyloggers) o chats privados.
*   **Factibilidad Ambiental:** Al alertar procesos maliciosos en segundo plano (ej. minería de criptomonedas), previene el sobrecalentamiento del hardware. Esto extiende la vida útil de los procesadores y componentes en un 30%, disminuyendo la huella de carbono y la generación de chatarra electrónica (e-waste) en la universidad.

### 7.2. Tecnología de desarrollo
La selección tecnológica se basó en el alto rendimiento y soporte comunitario:
*   **Capa Cliente (Endpoints):** Microsoft Sysinternals (Sysmon) para captura en Kernel de Windows; Wazuh Agent para ruteo de eventos; C# (WPF) para el instalador automático.
*   **Capa Lógica y ETL:** Wazuh Manager y OpenSearch (NoSQL); Python 3.10+ (FastAPI, psycopg2) por su eficiencia en tareas asíncronas y procesamiento por lotes.
*   **Capa de Datos:** PostgreSQL 15, brindando soporte relacional e indexación B-Tree robusta para análisis interactivo.
*   **Capa Visual:** Next.js (React) para el portal de control administrativo; Microsoft Power BI conectado vía DirectQuery para visualización en tiempo real.

### 7.3. Metodología de implementación
El desarrollo se basó en el Proceso Unificado (RUP) y la arquitectura C4 (Contexto, Contenedor, Componente). Para el despliegue formal del software en los laboratorios, los siguientes documentos de ingeniería se generaron e incluyeron en los anexos correspondientes:
*   **Documento de VISIÓN:** Define el alcance, los interesados del sistema y los criterios de aceptación técnicos.
*   **Documento SRS (Especificación de Requerimientos de Software):** Detalla los requerimientos funcionales, no funcionales y los diagramas de casos de uso (auto-registro, recolección, sincronización de Wazuh).
*   **Documento SAD (Documento de Arquitectura de Software):** Explica las vistas físicas, lógicas y el modelo C4 de contenedores de datos.

---

## 8. Cronograma (personas, tiempo, otros recursos)
El proyecto se ejecutó en un periodo estricto de 12 semanas (3 meses), liderado por dos (02) Desarrolladores/Analistas de la EPIS (Renzo Antayhua y Joan Cristian Medina).

*   **Fase 1: Inicio (Semana 1-2):** Levantamiento de información técnica en los laboratorios de cómputo. Redacción del análisis de factibilidad y documento de Visión.
*   **Fase 2: Elaboración (Semana 3-4):** Redacción del SRS y estructuración del diseño arquitectónico C4. Aprovisionamiento de la nube de Azure de prueba.
*   **Fase 3: Construcción I (Semana 5-7):** Configuración de PostgreSQL y dockerización del backend. Programación de la ETL incremental en Python.
*   **Fase 4: Construcción II (Semana 8-9):** Desarrollo del instalador Windows en C# (WPF) y diseño de la plantilla heurística de Sysmon.
*   **Fase 5: Construcción III (Semana 10-11):** Creación de la API REST en FastAPI, desarrollo del Dashboard (Next.js) e integración de los tableros analíticos de Power BI.
*   **Fase 6: Transición (Semana 12):** Pruebas de estrés de red (anti-inundación), carga incremental en producción y firma del acta de entrega.

---

## 9. Presupuesto
La estructura de costos del proyecto NetSight se centró en un modelo OPEX (gastos operativos), maximizando el uso de software libre y evitando el pago por terminales:

| Categoría de Costo | Detalle del Concepto | Monto Proyectado (S/.) |
| :--- | :--- | :---: |
| **Costos Generales** | Material ofimático, papelería y consumibles varios. | 150.00 |
| **Costos Operativos** | Servicios básicos (Internet, Energía) proporcionales a 3 meses. | 450.00 |
| **Infraestructura Cloud** | Suscripción Azure VPS (Standard_D4s_v3) proyectada a 12 meses. | 2,250.00 |
| **Costos de Personal** | Dos (02) Analistas/Desarrolladores part-time durante 3 meses. | 9,000.00 |
| **Total del Proyecto** | **Inversión Total Financiada** | **11,850.00** |

---

## 10. Conclusiones y Recomendaciones

### Conclusiones y Retos Enfrentados
1.  **Erradicación de la Ceguera Operativa:** El sistema provee visibilidad total en tiempo real de las conexiones sospechosas de los laboratorios y genera evidencias inmutables (hashes) para aplicar el reglamento de soporte institucional.
2.  **Desafío del Bucle de CPU en la ETL:** Durante el desarrollo, se enfrentó un bug lógico crítico en la paginación del ETL. Cuando el script encontraba conexiones de una PC no registrada (`Pallar`), ignoraba el evento pero no actualizaba el cursor de tiempo. Esto creaba un bucle infinito que saturaba la CPU del servidor. Se resolvió actualizando el timestamp del cursor al inicio de cada evaluación de log, permitiendo saltar registros no válidos sin quedarse atascado.
3.  **Preservación de Historial Técnico:** El uso inicial de la propiedad `ON DELETE CASCADE` de PostgreSQL eliminaba todo el historial de tráfico de una PC si esta se eliminaba de Wazuh. Se solucionó agregando la columna `activo` (BOOLEAN) y programando un script sincronizador (`sync_agents.py`) que altera el flag mediante consultas de API sin borrar la data acumulada, resolviendo el reto de retención forense solicitado por el cliente.
4.  **Rentabilidad Demostrada:** Se demostró la viabilidad de implementar infraestructuras complejas tipo SIEM/Big Data con costos operativos muy bajos mediante la integración inteligente de herramientas de software libre.

### Recomendaciones
1.  **Despliegue vía GPO:** Integrar el instalador `.exe` compilado dentro de las Políticas de Grupo de Active Directory de la universidad para automatizar la inscripción al momento de formatear laboratorios.
2.  **Monitoreo del Almacenamiento:** Evaluar semestralmente el crecimiento de PostgreSQL. Aunque se cuenta con una rutina de purga (`housekeeping.py`), el crecimiento exponencial del tráfico al incorporar más aulas requerirá escalamiento del disco SSD.
3.  **Cultura de Datos:** Capacitar a la jefatura de TI sobre la interpretación de los reportes interactivos para fundamentar presupuestos futuros de ancho de banda ante el Rectorado.

---

## 11. Bibliografía
*   **Kruchten, P.** (1995). *The 4+1 View Model of Architecture*. IEEE Software.
*   **Microsoft Corporation.** (2024). *Windows Sysinternals: Sysmon Documentation & Advanced Filtering*. Microsoft Docs.
*   **Wazuh Inc.** (2024). *Wazuh Open Source Security Platform: Architecture and Deployment Guide*. Recuperado de docs.wazuh.com.
*   **FastAPI / Tiangolo.** (2024). *FastAPI Documentation: Async, Concurrency, and Pydantic validation*.
