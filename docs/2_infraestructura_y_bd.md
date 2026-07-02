# Documentación Técnica de Infraestructura

Este documento provee un análisis a profundidad sobre los componentes de infraestructura, despliegue y esquema de datos para el proyecto **NetSight - Sistema de Monitoreo de Laboratorio**. Todos los diagramas de este documento están modelados usando código PlantUML.

## 1. Topología de Despliegue (Terraform en Azure)

La infraestructura en la nube está completamente automatizada utilizando Infrastructure as Code (IaC) con Terraform. El código de Terraform (`main.tf`, `variables.tf`) aprovisiona una Máquina Virtual en Microsoft Azure que aloja todo el backend y los contenedores de datos.

```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle

cloud "Microsoft Azure" {
    package "Resource Group (Sysmon-RG)" {
        package "Virtual Network (VNet)" {
            
            node "Ubuntu 22.04 LTS VPS\n(Wazuh + Backend)" as vps {
                component "Wazuh Manager\n(Puerto 1514)" as wmanager
                component "Wazuh Dashboard\n(Puerto 443)" as wdashboard
                component "OpenSearch / Wazuh Indexer" as indexer
                
                component "FastAPI Server\n(Puerto 8000)" as fastapi
                database "PostgreSQL 13\n(Puerto 5432)" as postgres
            }
            
            package "Network Security Group (NSG)" {
                [Regla: Allow 1514 (Sysmon)]
                [Regla: Allow 443 (Dashboard)]
                [Regla: Allow 8000 (API)]
                [Regla: Allow 22 (SSH)]
                [Regla: Allow 5432 (Postgres)]
            }
        }
    }
}

actor "Administrador (SSH / Web)" as admin
node "PCs Laboratorios (Wazuh Agent)" as agents

agents --> [Regla: Allow 1514 (Sysmon)]
admin --> [Regla: Allow 22 (SSH)]
admin --> [Regla: Allow 443 (Dashboard)]

[Regla: Allow 1514 (Sysmon)] --> wmanager
[Regla: Allow 443 (Dashboard)] --> wdashboard

@enduml
```

### Proceso de Aprovisionamiento
1. **Terraform Apply**: Se crea la máquina virtual y se abren los puertos requeridos en el Security Group de Azure.
2. **`deploy_wazuh.sh`**: Script de inicialización de shell que se ejecuta tras el aprovisionamiento. Sus tareas son:
   - Instalar el Wazuh Manager, Wazuh Indexer y Wazuh Dashboard.
   - Instalar PostgreSQL e importar el esquema inicial desde `schema.sql`.
   - Preparar el entorno Python y correr en background la API FastAPI.

---

## 2. Esquema de Base de Datos Relacional (PostgreSQL)

La capa de persistencia ha sido diseñada con un esquema estrella ("Star Schema") modificado para el modelado en Power BI, y cuenta con llaves foráneas y eliminación en cascada para facilitar la gestión del estado de los agentes.

### Diagrama Entidad-Relación (ERD)

```plantuml
@startuml
!theme plain
hide circle
skinparam linetype ortho

entity "laboratorios" as labs {
  * **id** : UUID <<PK>>
  --
  * nombre : VARCHAR(255) <<UNIQUE>>
  descripcion : TEXT
  * creado_en : TIMESTAMP
}

entity "computadoras" as pcs {
  * **id** : UUID <<PK>>
  --
  * hostname : VARCHAR(255)
  * laboratorio_id : UUID <<FK>>
  ip_local : VARCHAR(45)
  * activo : BOOLEAN
  * registrado_en : TIMESTAMP
}

entity "trafico_red" as net {
  * **id** : BIGSERIAL <<PK>>
  --
  * computadora_id : UUID <<FK>>
  * timestamp_evento : TIMESTAMP
  ip_origen : VARCHAR(45)
  ip_destino : VARCHAR(45)
  pais_destino : VARCHAR(100)
  ciudad_destino : VARCHAR(100)
  puerto_destino : INT
  protocolo : VARCHAR(10)
  proceso : VARCHAR(500)
}

entity "trafico_dns" as dns {
  * **id** : BIGSERIAL <<PK>>
  --
  * computadora_id : UUID <<FK>>
  * timestamp_evento : TIMESTAMP
  dominio : VARCHAR(500)
  proceso : VARCHAR(500)
}

entity "etl_estado" as etl {
  * **id** : SERIAL <<PK>>
  --
  * ultimo_timestamp : TIMESTAMP
  registros_procesados : BIGINT
  * actualizado_en : TIMESTAMP
}

labs ||--o{ pcs : "1 : N"
pcs ||--o{ net : "1 : N\n(ON DELETE CASCADE)"
pcs ||--o{ dns : "1 : N\n(ON DELETE CASCADE)"

note right of etl
  Tabla de control de
  carga incremental ETL.
end note

@enduml
```

### Detalles Técnicos del Esquema
- **Gestión del Historial:** La tabla `computadoras` usa el campo `activo` para evitar borrar la PC si se desconecta, previniendo que el `ON DELETE CASCADE` borre el historial valioso de `trafico_red` y `trafico_dns`.
- **Enriquecimiento ETL:** Los campos `pais_destino`, `ciudad_destino` y `proceso` en `trafico_red` no son capturados como tal desde el log original Sysmon, sino que son inyectados y correlacionados asíncronamente en vuelo por el worker ETL `engine.py`.
- **Rendimiento e Índices:** Se han creado índices tipo B-Tree (`idx_trafico_red_timestamp`, `idx_trafico_red_computadora`) que optimizan enormemente las vistas lógicas como `v_trafico_resumen` al ser consultadas por el modo DirectQuery de Power BI.

---

## 3. Flujo de Sincronización de Agentes (Wazuh <-> Postgres)

Para mantener actualizado el estado booleano de `activo` en las computadoras sin intervención manual, el sistema utiliza el script `sync_agents.py` ejecutado en cronjob (cada 5 minutos).

```plantuml
@startuml
!theme plain

participant "Cronjob\n(Linux)" as cron
participant "FastAPI\n(sync_agents.py)" as api
participant "API Wazuh Manager" as wazuh
database "PostgreSQL\n(computadoras)" as db

cron -> api : POST /api/etl/sync-agents
activate api

api -> wazuh : GET /security/user/authenticate
wazuh --> api : JWT Token

api -> wazuh : GET /agents?status=active
wazuh --> api : Lista JSON de agentes activos\n(ej. [{"name":"Pallar"}])

api -> db : UPDATE computadoras SET activo = TRUE \nWHERE LOWER(TRIM(hostname)) IN (Lista Wazuh)
db --> api : OK

api -> db : UPDATE computadoras SET activo = FALSE \nWHERE LOWER(TRIM(hostname)) NOT IN (Lista Wazuh)
db --> api : OK

api --> cron : 200 OK (Estadísticas Sincronización)
deactivate api
@enduml
```

Este proceso unifica el inventario real del antivirus/HIDS (Wazuh) con el inventario administrativo (PostgreSQL) y automáticamente se refleja en tiempo real dentro del portal en Next.js y los reportes de IT.
