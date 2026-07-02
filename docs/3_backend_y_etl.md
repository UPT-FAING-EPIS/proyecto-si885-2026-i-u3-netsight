# Documentación Técnica: Backend y Proceso ETL

El servidor Backend del proyecto **NetSight - Sistema de Monitoreo de Laboratorio** está construido utilizando **FastAPI** en Python. Tiene una doble función: por un lado, sirve como API REST para el Dashboard y para el proceso de registro del instalador; por otro, encapsula la lógica de los motores de extracción, transformación y carga (ETL), sincronización y purga de datos.

## 1. Arquitectura de Endpoints (FastAPI)

El archivo `main.py` define la interfaz REST y la interacción con PostgreSQL mediante SQLAlchemy (de forma asíncrona).

### Endpoints Principales
- **CRUD Laboratorios (`/api/laboratorios/`)**: Permite listar, crear, actualizar y eliminar (con cascada) laboratorios físicos.
- **Registro Computadoras (`/api/computadoras/`)**:
  - `GET`: Lista todas las PC junto a su estado activo y laboratorio asignado.
  - `POST`: Expuesto para que el instalador C# registre automáticamente el host (mediante su hostname y dirección IP) durante la instalación de Sysmon/Wazuh.
- **Acciones Administrativas ETL (`/api/etl/*`)**:
  - `/api/etl/sync`: Dispara manualmente la ejecución del motor ETL de tráfico.
  - `/api/etl/sync-agents`: Dispara la validación de actividad entre Wazuh y Postgres.
  - `/api/etl/housekeeping`: Inicia la limpieza de datos antiguos.

---

## 2. Motor ETL de Tráfico de Red (`engine.py`)

Es el componente crítico (Data Pipeline) que asegura que los logs crudos que llegan de Sysmon (mediante Wazuh y almacenados en OpenSearch) se enriquezcan y pasen a la estructura relacional (PostgreSQL) para Power BI. 

### Diagrama de Flujo del ETL

```plantuml
@startuml
!theme plain
skinparam activityShape octagon

start
:Obtener **ultimo_timestamp** de tabla ""etl_estado"";
:Cargar Base de Datos **MaxMind GeoIP**;

repeat
  :Consultar **OpenSearch**
  (Índice: wazuh-alerts-*, EventID: 3 y 22
  > ultimo_timestamp, Batch: 500);
  
  if (¿Hay resultados?) then (No)
    break
  else (Sí)
    :Procesar cada evento del lote;
    note right
      Extraer IP origen, IP destino, puertos,
      protocolos, dominio DNS, ruta del proceso.
    end note
    
    :Verificar hostname en PostgreSQL;
    if (¿Hostname existe?) then (Sí)
      :Resolver GeoIP
      (Obtener País y Ciudad para IP Destino);
      :Añadir a lista temporal;
    else (No)
      :Ignorar Evento
      (Previene error llave foránea);
    endif
    
    :Avanzar contador temporal de iteración;
  endif
  
  :Bulk Insert (execute_values)
  a tablas ""trafico_red"" y ""trafico_dns"";
repeat while (¿Total de la página = 500?)

:Actualizar tabla ""etl_estado""
con el último timestamp leído
y total de registros procesados;
stop
@enduml
```

### Principios del `engine.py`:
1. **Incrementalidad**: Evita procesar la misma data dos veces al recordar el último `timestamp` en `etl_estado`.
2. **Eficiencia por Lotes (Bulk Insert)**: Usa `psycopg2.extras.execute_values` para insertar registros de a 500 de golpe, bajando drásticamente el costo computacional sobre Postgres.
3. **Resiliencia Textual**: Implementa normalización `LOWER(TRIM(hostname))` para evitar rechazos por espacios ocultos o diferencias de mayúsculas desde Sysmon Windows.

---

## 3. Sincronización de Agentes (`sync_agents.py`)

Para que el Dashboard muestre métricas fiables de computadoras conectadas (y no incluya terminales que han sido desmanteladas o perdieron su agente), se creó un sincronizador que conversa mediante API nativa con el Wazuh Manager.

### Diagrama de Secuencia de Sincronización

```plantuml
@startuml
!theme plain
autonumber

participant "Cronjob\n(FastAPI)" as api
participant "Wazuh API\n(Puerto 55000)" as wazuh
database "PostgreSQL" as db

api -> wazuh : Petición POST /security/user/authenticate
wazuh --> api : JWT Auth Token

api -> wazuh : Petición GET /agents?status=active\n(Header: Bearer Token)
wazuh --> api : Respuesta JSON (Lista de Hostnames Activos)

api -> api : Limpieza de strings\n(TRIM y LOWER)

api -> db : UPDATE computadoras SET activo = TRUE\nWHERE hostname IN (Lista) AND activo = FALSE
db --> api : OK (Filas Afectadas)

api -> db : UPDATE computadoras SET activo = FALSE\nWHERE hostname NOT IN (Lista) AND activo = TRUE
db --> api : OK (Filas Afectadas)

api -> api : Retornar estadísticas
@enduml
```

---

## 4. Retención y Limpieza de Datos (`housekeeping.py`)

Debido a que el Event ID 3 de Sysmon genera gran volumen de datos (una PC puede generar miles de conexiones DNS o TCP/UDP por día), el crecimiento de la base de datos PostgreSQL debe controlarse.

- **Mecanismo**: El script elimina mediante una consulta `DELETE` todos aquellos eventos de red (en `trafico_red` y `trafico_dns` por su relación de FK en `computadoras` o mediante cascada si aplica, en este caso directo a `trafico_red`) que sean más antiguos a un límite de tiempo definido (variable de entorno `RETENTION_DAYS`, por defecto **30 días**).
- **Ejecución**: Generalmente configurado vía Crontab del sistema operativo para ejecutarse en horas de madrugada (`0 0 * * *`).

```plantuml
@startuml
!theme plain

start
:Leer variable RETENTION_DAYS (ej: 30);
:Ejecutar DELETE FROM trafico_red
WHERE timestamp_evento < NOW() - 30 days;
:Obtener cantidad de registros eliminados (cursor.rowcount);
:Hacer commit en la Base de Datos;
stop

@enduml
```
