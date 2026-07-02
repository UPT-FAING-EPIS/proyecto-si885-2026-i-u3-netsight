# Documentación Técnica: Frontend Dashboard

El portal administrativo de **NetSight - Sistema de Monitoreo de Laboratorio** ha sido desarrollado en **Next.js 15 (App Router)** y **React 19**, proporcionando una interfaz moderna, rápida y responsiva para la gestión de la infraestructura y visualización de telemetría.

## 1. Arquitectura de Componentes

La aplicación está diseñada usando una arquitectura de componentes funcionales e interactúa de manera asíncrona con el Backend FastAPI a través del servicio encapsulado en `lib/api.ts`.

```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle

package "Next.js App Router (/src/app)" {
    component "Layout Principal\n(layout.tsx)" as layout
    
    component "Dashboard General\n(page.tsx)" as page_dashboard
    component "Gestión Laboratorios\n(laboratorios/page.tsx)" as page_labs
    component "Gestión Computadoras\n(computadoras/page.tsx)" as page_pcs
}

package "Componentes UI (/src/components)" {
    component "Sidebar" as sidebar
    component "StatsCard" as statscard
    component "SyncButton" as syncbtn
    component "LabTable & PcTable" as tables
}

package "Capa de Datos (/src/lib)" {
    component "api.ts (Fetch Client)" as api
}

cloud "Backend REST (FastAPI)" as backend
cloud "Power BI Service" as pbi

layout --> sidebar
layout --> page_dashboard
layout --> page_labs
layout --> page_pcs

page_dashboard --> statscard
page_dashboard --> pbi : Iframe embebido
page_labs --> tables
page_pcs --> tables

sidebar --> syncbtn

page_dashboard --> api : fetchStats()
page_labs --> api : CRUD Laboratorios
page_pcs --> api : fetchComputadoras()
syncbtn --> api : triggerETLSync()

api --> backend : Peticiones HTTP/JSON
@enduml
```

---

## 2. Vistas Principales

### 2.1 Resumen General (`/`)
Es la vista de aterrizaje (Landing) del administrador. Presenta:
- **Tarjetas de Estadísticas (`StatsCard`)**: Muestra en tiempo real la cantidad de Laboratorios creados, Computadoras registradas y el volumen total de Registros de Tráfico procesados por la base de datos. Se auto-refresca cada 30 segundos.
- **Power BI Embebido**: Despliega un `<iframe allowFullScreen>` apuntando al reporte público en Power BI Service (`app.powerbi.com`), que consume los datos procesados.
- **Botón de Descarga**: Un acceso directo (`/api/download-installer`) para descargar el instalador compilado del agente cliente (C# WPF).

### 2.2 Gestión de Laboratorios (`/laboratorios`)
Permite definir los agrupamientos físicos o lógicos de la infraestructura.
- Se comunica vía `api.ts` para hacer `POST` o `PUT` de la entidad `LaboratorioCreate`.
- Esta vista es esencial ya que, sin laboratorios registrados, el Instalador del Agente Cliente no podrá culminar su instalación.

### 2.3 Inventario de Computadoras (`/computadoras`)
Un listado de solo-lectura (`fetchComputadoras`) que muestra todos los hosts inscritos en la plataforma.
- Visualiza el campo `hostname`, `ip_local`, fecha de registro y el estado de conexión (`activo`), ayudando al personal de soporte a detectar equipos desconectados.

---

## 3. Flujo de Sincronización Manual (SyncButton)

Dado que los flujos de ETL están automatizados por Cronjobs en Linux, se ha provisto un botón estratégico en la cabecera / menú lateral (`SyncButton.tsx`) que permite al administrador forzar la extracción de datos desde OpenSearch hacia PostgreSQL a demanda.

### Diagrama de Flujo y Estados de UI

```plantuml
@startuml
!theme plain
autonumber

actor "Usuario (Admin)" as user
participant "SyncButton.tsx" as btn
participant "api.ts" as api
participant "FastAPI\n(/api/etl/sync)" as server

user -> btn : Clic en "Forzar Sincronización"
btn -> btn : setState(loading: true)
btn -> btn : Render: Icono Spinner

btn -> api : triggerETLSync()
api -> server : POST /api/etl/sync

note right of server
  El servidor pausa hasta que
  el proceso engine.py extrae,
  transforma e inserta la data
  hacia Postgres.
end note

server --> api : 200 OK\n{registros_procesados: 1540}

api --> btn : Retorna objeto ETLSyncResult
btn -> btn : setState(loading: false)
btn -> btn : setState(result: success)

btn --> user : Toast Notification:\n"1540 registros procesados"

btn -> btn : setTimeout(4000ms)
btn -> btn : Ocultar Toast
@enduml
```

### Gestión de Errores
El frontend está protegido contra interrupciones en el backend. Si el endpoint de ETL falla (por caída de base de datos o timeout de OpenSearch), el bloque `catch` dentro de `triggerETLSync` capturará el error HTTP, devolviendo un objeto que activará un Toast con la clase `toast-error` notificando la falla sin colapsar la página entera.
