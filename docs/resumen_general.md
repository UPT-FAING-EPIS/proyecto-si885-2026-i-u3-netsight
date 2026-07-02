# 🛡️ NetSight - Resumen General del Proyecto y Auditoría de Documentación

Este documento contiene un análisis exhaustivo y resumen general del proyecto **NetSight - Sistema de Monitoreo de Laboratorio** y su suite de documentación. Ha sido estructurado para proporcionar una comprensión clara del estado del arte de la plataforma, su arquitectura técnica, el diseño del modelo de datos, la lógica del backend/ETL, el comportamiento del agente cliente, el frontend y la inteligencia de negocios con Power BI.

---

## 1. Visión General del Proyecto

**NetSight** es una solución distribuida de telemetría y monitoreo de tráfico de red a nivel de terminales (*endpoints*) diseñada específicamente para los laboratorios de cómputo de la **Escuela Profesional de Ingeniería de Sistemas (EPIS) de la Universidad Privada de Tacna (UPT)**. 

### 1.1 Problemática de Negocio
Actualmente, la administración del parque informático académico opera de forma **reactiva**. Ante incidencias de red, degradación de rendimiento por uso no autorizado (como descargas P2P/Torrent o minería de criptomonedas) o intrusiones de seguridad, el equipo de soporte técnico se entera mediante reportes tardíos y debe realizar revisiones físicas e históricas manuales en el *Visor de Eventos* de Windows de cada PC. NetSight cambia este paradigma hacia una **gestión proactiva y centralizada**.

### 1.2 Objetivos del Sistema
*   **Monitoreo Continuo y Silencioso:** Captura de telemetría de red a nivel de kernel utilizando agentes livianos.
*   **Procesamiento y Enriquecimiento de Datos:** Ingesta incremental de logs, geolocalización e identificación de procesos en tiempo real.
*   **Observabilidad Centralizada:** Visualización en un Dashboard Web y análisis analítico avanzado en Power BI.
*   **Control de Cumplimiento:** Identificación de patrones anómalos de tráfico, conexiones internacionales de riesgo y software indebido.

---

## 2. Estructura del Repositorio de Código

La organización física del proyecto refleja fielmente la separación de responsabilidades y la modularidad de su arquitectura distribuida:

*   [**`/infrastructure`**](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/infrastructure): Contiene el esquema SQL relacional ([`schema.sql`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/infrastructure/schema.sql)), los scripts para levantar la infraestructura de servidores mediante Terraform (`/terraform`) y el despliegue automático del clúster wazuh ([`deploy_wazuh.sh`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/infrastructure/deploy_wazuh.sh)).
*   [**`/server`**](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/server): El backend en Python. Implementado con **FastAPI** ([`main.py`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/server/app/main.py)), cuenta con modelos relacionales ORM (SQLAlchemy) y la lógica de negocio de los procesos ETL (`/app/etl`):
    *   [`engine.py`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/server/app/etl/engine.py): Pipeline de extracción e inserción incremental en lote cruzando logs de OpenSearch y geolocalización MaxMind.
    *   [`sync_agents.py`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/server/app/etl/sync_agents.py): Sincronización del estado "Activo/Inactivo" de los agentes Wazuh.
    *   [`housekeeping.py`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/server/app/etl/housekeeping.py): Purga periódica para mantener bajo control el tamaño físico de la BD.
*   [**`/dashboard`**](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/dashboard): El portal web administrativo construido en **Next.js 15 (App Router)** y **React 19**.
*   [**`/installer`**](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/installer): Instalador cliente nativo para Windows desarrollado en **C# con WPF (.NET)** ([`NetworkMonitorInstaller.sln`](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/installer/NetworkMonitorInstaller.sln)), diseñado para un despliegue silencioso en un clic.
*   [**`/docs`**](file:///c:/Users/Admin/Desktop/LabsNegocios/proyecto-si885-2026-i-u3-netsight/docs): Documentación del proyecto, incluyendo manuales técnicos detallados y los informes académicos de fases (FD01-FD05).

---

## 3. Arquitectura General y Flujo de Datos

NetSight utiliza una **arquitectura orientada a eventos** de extremo a extremo, detallada en el diagrama lógico a continuación:

```mermaid
flowchart TD
    subgraph Laboratorios EPIS [Laboratorios Locales (Windows)]
        PC1[PC Laboratorio 1] -->|Sysmon Logs ID 3 & 22| W_Agent1(Wazuh Agent 1)
        PCN[PC Laboratorio N] -->|Sysmon Logs ID 3 & 22| W_AgentN(Wazuh Agent N)
    end

    subgraph Azure Cloud [Azure VPS - Servidor Central]
        W_Agent1 -.->|Puerto Encripción 1514| W_Manager(Wazuh Manager)
        W_AgentN -.->|Puerto Encripción 1514| W_Manager
        
        W_Manager -->|Indexación JSON| O_Search[(OpenSearch / Wazuh Indexer)]
        
        subgraph Motor ETL (Python FastAPI)
            ETL_Eng[engine.py] -->|1. Pull incremental 500-10000| O_Search
            ETL_Eng -->|2. Resuelve Pais/Ciudad| MaxMind[(MaxMind GeoIP)]
            ETL_Eng -->|3. Filtra hostnames válidos| DB_PG
        end

        DB_PG[(PostgreSQL 13)]
        
        API_Fast[FastAPI Backend] -->|Consulta telemetría| DB_PG
        
        Cron[Cronjobs / Linux] -->|POST /api/etl/*| API_Fast
        API_Fast -->|Ejecuta| ETL_Eng
        API_Fast -->|Ejecuta| Sync[sync_agents.py]
        API_Fast -->|Ejecuta| HK[housekeeping.py]
    end

    subgraph Capa Consumo [Visualización e Inteligencia]
        Admin((Administrador TI)) -->|HTTPS 443| Dash_Next[Dashboard Next.js 15]
        Dash_Next -->|Consume API REST| API_Fast
        
        P_BI(Power BI Service) -->|Conexión DirectQuery| DB_PG
        Dash_Next -->|Renderiza iframe| P_BI
    end
```

### 3.1 Flujo de Ingesta y Procesamiento
1.  **Captura en Endpoint:** El agente cliente de **Sysmon** intercepta la actividad a nivel de Kernel y genera eventos **ID 3 (NetworkConnect)** y **ID 22 (DnsQuery)**.
2.  **Reenvío de Logs:** El **Wazuh Agent** recopila los logs de Sysmon desde el canal de eventos de Windows (`eventchannel`) y los transmite de forma segura al **Wazuh Manager** en Azure.
3.  **Indexación:** El Manager envía los registros a **OpenSearch** para su almacenamiento crudo.
4.  **Extracción Incremental (ETL):** El script `engine.py` se ejecuta asíncronamente. Consulta OpenSearch buscando nuevos registros desde la última marca de tiempo guardada en `etl_estado`.
5.  **Transformación y Enriquecimiento:**
    *   Filtra los registros asegurándose de que la PC origen ya está registrada en la base de datos PostgreSQL.
    *   Extrae el nombre básico del proceso (limpiando rutas largas).
    *   Geolocaliza la IP destino mediante la base local **MaxMind GeoLite2**. Para IPs locales/privadas inyecta la etiqueta `"LAN"`.
6.  **Carga Relacional:** Escribe los datos procesados en `trafico_red` y `trafico_dns` mediante una inserción masiva en lotes (*Bulk Insert*).
7.  **Consumo Analítico:** Power BI Desktop/Service consulta directamente las vistas PostgreSQL en modo **DirectQuery** para reflejar la actividad casi en tiempo real.

---

## 4. Diseño del Esquema de Datos (PostgreSQL)

La base de datos relacional utiliza un esquema híbrido optimizado para análisis analíticos rápidos (diseño estrella):

*   **`laboratorios`:** UUID identificador, nombre único del laboratorio y descripción física.
*   **`computadoras`:** Mantiene la relación física entre las terminales y los laboratorios. Almacena el `hostname`, `ip_local` y un flag booleano `activo`. 
    *   *Nota de Diseño:* Si una PC se desconecta o desinstala, `activo` cambia a `FALSE` pero el registro se mantiene para evitar que una eliminación en cascada (`ON DELETE CASCADE`) destruya el histórico de tráfico acumulado.
*   **`trafico_red`:** Contiene los registros de telemetría de red. Registra `computadora_id`, timestamp del evento (basado en la hora real del host de Windows), IPs origen/destino, puerto y protocolo de destino, localización (`pais_destino`, `ciudad_destino`) y el nombre de la aplicación ejecutora (`proceso`).
*   **`trafico_dns`:** Almacena el historial de solicitudes de dominios, cruzando `computadora_id`, `dominio` y el `proceso` que originó la petición.
*   **`etl_estado`:** Tabla de una única fila que almacena el cursor temporal (`ultimo_timestamp`) de la ingesta de OpenSearch para asegurar transacciones libres de duplicidad.

### Vistas de Explotación Analítica (BI)
*   **`v_trafico_resumen`:** Une `trafico_red`, `computadoras` y `laboratorios`. Evita que Power BI tenga que realizar múltiples `JOIN` en caliente, mejorando la velocidad de DirectQuery en el servidor.
*   **`v_trafico_dns_resumen`:** Vista consolidada para consultas DNS históricas.

---

## 5. Arquitectura del Backend y Pipeline de Datos (Python FastAPI)

Ubicado en `/server/app`, el motor backend proporciona robustez mediante programación moderna basada en FastAPI y SQLAlchemy Async.

### 5.1 Endpoints CRUD e Integración
*   **Endpoints Administrativos:** Listado y creación de laboratorios (`/api/laboratorios/`) y registro automático de equipos (`/api/computadoras/`).
*   **Endpoints de Ejecución de Tareas (Jobs):**
    *   `/api/etl/sync`: Despacha el motor ETL de tráfico (`engine.py`).
    *   `/api/etl/sync-agents`: Valida los hostnames inscritos contra la API de Wazuh Manager para apagar o encender el flag `activo` (`sync_agents.py`).
    *   `/api/etl/housekeeping`: Invocación de la purga de base de datos (`housekeeping.py`).
*   **`/api/stats/`:** Proporciona los totales cuantitativos de infraestructura y tráfico para las tarjetas de control del Dashboard.
*   **`/api/download-installer`:** Sirve el ejecutable del agente C# precompilado en el VPS Azure.

### 5.2 Optimización de Rendimiento en Ingesta
El pipeline de `engine.py` utiliza patrones de optimización de datos:
1.  **Bulk Load con execute_values:** En lugar de ejecutar miles de sentencias `INSERT` individuales, recopila la data en listas de Python y usa `psycopg2.extras.execute_values` para mandar bloques de 500 registros.
2.  **Validaciones Flexibles:** El Mapeo del hostname se hace de forma insensible a mayúsculas/minúsculas y libre de espacios (`LOWER(TRIM(hostname))`) para evitar discordancias entre los nombres devueltos por Windows OS y Wazuh.

---

## 6. Agente Cliente (C# WPF)

Para simplificar al administrador de red el aprovisionamiento de las terminales, se desarrolló un instalador de escritorio en C# con arquitectura orientada a servicios.

### 6.1 Secuencia Lógica de Instalación (Un Solo Clic)
1.  **Elevación UAC:** El instalador verifica privilegios de administrador del sistema. Si no los tiene, se relanza automáticamente requiriendo permisos (`runas`).
2.  **Descarga Automática:** Trae en segundo plano el binario MSI del Wazuh Agent y el motor de Sysmon64 desde la API del servidor NetSight.
3.  **Despliegue de Sysmon:**
    *   Genera un archivo de configuración XML personalizado (`sysmon_config.xml`) que filtra específicamente el tráfico saliente y consultas de red, silenciando eventos ruidosos innecesarios.
    *   Ejecuta `Sysmon64.exe -i -accepteula` para montarlo como servicio del sistema operativo.
4.  **Despliegue de Wazuh:** Instala el agente Wazuh de forma silenciosa, enlazándolo con la IP pública del Wazuh Manager de Azure.
5.  **Inyección de Metadatos (`ossec.conf`):** Modifica el XML del agente local para añadirle etiquetas que identifiquen el laboratorio asignado y optimiza los búferes de memoria del agente local (`client_buffer`) para evitar pérdida de logs ante ráfagas altas de tráfico.
6.  **Registro de Hostname:** Consume el endpoint `POST /api/computadoras/` de FastAPI para dar de alta el equipo en la base de datos de PostgreSQL y finalmente reinicia el servicio de Wazuh para iniciar la monitorización.

---

## 7. Frontend Dashboard (Next.js)

El panel web ubicado en `/dashboard` está concebido para ser un portal administrativo ágil y ligero.

*   **Tecnologías:** Next.js 15 (App Router), React 19, TypeScript y Tailwind CSS.
*   **Funciones Principales:**
    *   **Monitoreo del Inventario:** Muestra gráficamente el listado de laboratorios y computadoras, con indicadores de color que revelan si una PC está enviando logs en tiempo real o está inactiva.
    *   **Métricas Rápidas:** Consumo de la API `/api/stats/` para reflejar el volumen de red procesado.
    *   **Acciones a Demanda:** Inclusión del componente `SyncButton` para que un operador de TI pueda invocar la sincronización manual del flujo de datos con un clic.
    *   **Integración Power BI:** Embebido directo mediante Iframe del reporte institucional de Power BI.

---

## 8. Análisis Avanzado e Inteligencia de Negocios (Power BI)

Power BI constituye la capa analítica de visualización de datos de NetSight, alimentada desde PostgreSQL a través de la vista desnormalizada `v_trafico_resumen` en modo **DirectQuery** para velocidad e inmediatez.

### 8.1 Fórmulas DAX Implementadas
*   **Volumen de Conexiones:**
    ```dax
    Eventos Totales = COUNT('v_trafico_resumen'[id])
    ```
*   **Filtro de Tráfico Externo (Movimiento Lateral vs Tráfico Web):**
    ```dax
    Es Externa = 
    IF(
        LEFT('v_trafico_resumen'[ip_destino], 3) = "192" || 
        LEFT('v_trafico_resumen'[ip_destino], 2) = "10" || 
        LEFT('v_trafico_resumen'[ip_destino], 3) = "172", 
        "Interna", 
        "Externa"
    )
    ```
*   **Categorización de Amenazas en Puertos:**
    ```dax
    Nivel Riesgo = 
    SWITCH( TRUE(),
        'v_trafico_resumen'[puerto_destino] IN {21, 22, 23, 3389, 445}, "Crítico",
        'v_trafico_resumen'[puerto_destino] > 1024, "Dinámico/Alto",
        "Estándar"
    )
    ```

### 8.2 Tableros Diseñados (Blueprint)
1.  **Ciberseguridad & Threat Hunting:** Enfocado en alertar sobre el uso de protocolos inseguros (como Telnet o RDP sin tunelizar) y geolocalización de IPs de destino a través de mapas mundiales para identificar exfiltraciones de datos a zonas de riesgo.
2.  **Control Académico y Productividad:** Mapea los procesos activos en las PCs durante clases. Permite identificar de manera forense si los estudiantes están jugando (ej. `discord.exe`, ejecutables de Steam) o utilizando proxys/VPNs para evadir los controles.
3.  **Operaciones y Gestión de Capacidad:** Permite ver picos de consumo de red y horas de uso máximo de los laboratorios para planificar actualizaciones de hardware y optimizar el ancho de banda contratado.

---

## 9. Análisis de Entregables Formales (Fases FD01 - FD05)

La documentación formal se encuentra redactada en formato Markdown en `/docs`. Una revisión minuciosa nos da el siguiente resumen de cada informe técnico:

### FD01: Informe de Factibilidad
*   **Factibilidad Técnica:** Viable debido a la compatibilidad nativa de Sysmon con la infraestructura Windows local y el uso de tecnologías estándar de contenedores en Azure.
*   **Factibilidad Económica:** Altamente rentable. El costo total estimado de desarrollo y despliegue inicial es de **S/. 11,850.00**, usando herramientas de código abierto que eliminan costosas licencias de EDR (Endpoint Detection and Response) tradicionales.
*   **Riesgos Mapeados:**
    *   Saturación de red institucional por volumen de logs.
    *   Llenado precoz del disco del servidor (resuelto con `housekeeping.py`).
    *   Privacidad de los datos de los estudiantes (resuelto monitoreando estrictamente metadatos de red del sistema y no contenido del tráfico).

### FD02: Informe de Visión
*   Establece el alcance del producto. Identifica los principales involucrados: el Director de la EPIS (UPT), Jefes de Laboratorio, personal de soporte técnico y el alumnado.
*   Presenta los casos de uso principales a alto nivel: Registro de Equipos, Extracción de Logs de Tráfico, Consultas Analíticas, Notificación de Alertas y Purga de Historial.

### FD03: Requerimientos
*   Detalla requerimientos funcionales y no funcionales. 
*   **Funcionales:** Registro automatizado de terminales, extracción incremental por lotes, geolocalización de destinos, vistas enriquecidas para BI y dashboard administrativo web.
*   **No Funcionales:** Latencia de sincronización <5 minutos, consumo del agente local de Windows <15MB RAM y <1% de CPU, interfaz de Next.js responsiva con carga <2 segundos, y persistencia segura en base de datos cifrada.

### FD04: Informe de Arquitectura de Software
*   Define el estilo de la arquitectura: **Arquitectura Orientada a Eventos (EDA)** y **Patrón Arquitectónico en Capas** (Presentación, Aplicación/Negocio, Ingesta/ETL y Persistencia).
*   Describe las vistas del modelo de arquitectura (Vistas lógica, de implementación, de procesos y de despliegue).
*   Especifica las tácticas de arquitectura: disponibilidad (reinicio automático de contenedores en Azure VM), rendimiento (inserciones masivas Postgres y consultas DirectQuery) y seguridad (comunicaciones HTTPS y túnel seguro SSL de Wazuh en puerto 1514).

### FD05: Informe de Proyecto Final
*   Evalúa el cumplimiento de las metas del proyecto.
*   Documenta las pruebas unitarias y de integración del flujo de datos completas, la estabilidad del agente local de Windows en clases piloto y las lecciones aprendidas sobre el manejo de altos volúmenes de logs a través de tuning de bases de datos.

---

## 10. Conclusiones y Diagnóstico General de NetSight

Tras una minuciosa revisión general del repositorio y de toda la suite de documentación, se emite el siguiente veredicto técnico:

### 🌟 Fortalezas del Proyecto
1.  **Gran Diseño de Arquitectura (Bajo Acoplamiento):** El uso de Wazuh como intermediario de ingesta evita sobrecargar el backend de FastAPI con conexiones TCP crudas de cientos de agentes. FastAPI solo consulta el almacén intermedio (OpenSearch).
2.  **Optimización Relacional:** El uso de vistas desnormalizadas y una tabla dedicada a gestionar el cursor incremental de la ETL (`etl_estado`) demuestra un excelente entendimiento del diseño de bases de datos relacionales y de rendimiento de BI.
3.  **Simplicidad de Despliegue en Clientes:** El instalador C# WPF es sumamente robusto al integrar la elevación UAC automatizada y la inyección XML directa a archivos de configuración de Wazuh.

### ⚠️ Oportunidades de Mejora / Recomendaciones
1.  **Seguridad en el Endpoint de Registro:** El endpoint `/api/computadoras/` (`POST`) es expuesto de manera pública para permitir que el instalador C# registre equipos nuevos. Se recomienda añadir una clave API simple (API Key) o token compartido embebido en el instalador para evitar el registro malicioso de PCs ficticias en el sistema.
2.  **Indexación y Particionado de Base de Datos:** A largo plazo, el volumen en la tabla `trafico_red` puede crecer exponencialmente si se aumentan las computadoras. Se sugiere implementar particionamiento por rangos de fecha en PostgreSQL para optimizar los `DELETE` del housekeeper y las búsquedas de DirectQuery.
3.  **Monitoreo del Estado del Worker:** Actualmente, el motor ETL depende de un Cronjob en el servidor VPS de Azure. Implementar un monitoreo de salud (*Heartbeat*) de esta tarea programada aseguraría que fallos silenciosos de la ETL sean alertados de inmediato al administrador.
