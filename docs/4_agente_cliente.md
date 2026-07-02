# Documentación Técnica: Agente Cliente (Instalador WPF)

El Agente Cliente está contenido en la solución `NetworkMonitorInstaller` desarrollada en **C# con WPF (.NET)**. Su propósito es reducir a un solo clic (despliegue silencioso) la configuración compleja de los endpoints Windows de los laboratorios, integrando Sysmon, Wazuh Agent y la API Central.

## 1. Arquitectura del Agente

El código está estructurado mediante un patrón de UI y Servicios, donde la vista (`MainWindow.xaml`) orquesta las llamadas a tres servicios principales:
- `SysmonService.cs`: Generación de perfiles XML y ejecución de Sysmon.
- `WazuhService.cs`: Instalación vía MSI, edición XML (`ossec.conf`) y gestión de Windows Services (UAC).
- `ApiService.cs`: Comunicación HTTP con el backend de FastAPI.

---

## 2. Flujo de Instalación

Al hacer clic en el botón "Instalar", el software ejecuta una secuencia determinista para aprovisionar el host.

```plantuml
@startuml
!theme plain
skinparam activityShape octagon

start
:Usuario selecciona **Laboratorio** y
presiona "Instalar";

:Paso A: Descargar Instaladores;
note right
  Descarga `Sysmon64.exe` y `wazuh-agent.msi`
  desde el servidor de descargas del VPS.
end note

:Paso B: Generar configuración Sysmon;
note right
  Crea `sysmon_config.xml` estrictamente para
  capturar Event ID 3 (NetworkConnect)
  y silenciar los demás (ruido).
end note

:Paso C: Instalar Sysmon64.exe;
if (¿Ya está instalado?) then (Sí)
  :Ejecutar actualización (-c);
else (No)
  :Ejecutar instalación (-i -accepteula);
endif

:Paso D: Instalar Wazuh Agent (msiexec);
note right
  Instalación silenciosa inyectando la
  IP del WAZUH_MANAGER como parámetro.
end note

:Paso E: Etiquetado en ossec.conf;
note right
  Inyecta `<labels><label key="laboratorio">ID</label></labels>`
  para que OpenSearch sepa de dónde viene el tráfico.
end note

:Paso F: Registro de Hostname en Backend;

:Paso G: Optimizar ossec.conf;
note right
  - Asegurar lectura de `eventchannel` para Sysmon.
  - Aumentar `client_buffer` a 100,000 eventos.
end note

:Reiniciar Servicio (WazuhSvc);
stop
@enduml
```

---

## 3. Diagrama de Secuencia de Comunicación

El instalador no solo despliega software de terceros, sino que debe mantener al backend informado de su existencia para no romper la llave foránea del motor ETL.

```plantuml
@startuml
!theme plain
autonumber

actor "Técnico TI" as user
participant "App WPF\n(MainWindow)" as app
participant "ApiService" as api
participant "Backend\n(FastAPI)" as server
participant "Windows OS" as win
participant "Wazuh Agent" as wazuh

user -> app : Iniciar Instalador
app -> win : Solicitar Elevación UAC (RunAs)
win --> app : Proceso Ejecutándose como Administrador

user -> app : Clic en "Refrescar Laboratorios"
app -> api : GetLaboratoriosAsync()
api -> server : GET /api/laboratorios/
server --> api : 200 OK (JSON List)
api --> app : Actualiza ComboBox

user -> app : Clic en "Instalar"
app -> win : Instalar Sysmon & Wazuh
win --> app : Listo

app -> win : Leer Environment.MachineName\ny NetworkInterfaces
win --> app : "PC-LAB-01" y "192.168.1.15"

app -> api : RegistrarComputadoraAsync()
api -> server : POST /api/computadoras/\n{hostname, laboratorio_id, ip_local}
server --> api : 201 Created
api --> app : Éxito

app -> wazuh : Reiniciar Servicio
wazuh --> server : [A partir de ahora, manda logs a través del Manager]
@enduml
```

---

## 4. Resoluciones Técnicas Clave

### Elevación de Privilegios Automática
El instalador usa el método `WazuhService.ReroutearSiNoEsAdmin()`, el cual verifica el token de `WindowsPrincipal`. Si el usuario no es administrador, la aplicación se reinicia a sí misma solicitando explícitamente el prompt UAC (`Verb = "runas"`).

### XML Parsing de `ossec.conf`
Dado que el archivo de configuración de Wazuh (`ossec.conf`) es altamente estricto, el `WazuhService` utiliza `System.Xml.Linq` para analizar y modificar los nodos `<labels>` y `<client_buffer>` y lo guarda usando una configuración especial (`OmitXmlDeclaration = true` y sin BOM UTF-8) para evitar que el servicio de Wazuh falle al intentar leerlo.

### Filtros de Sysmon
El `sysmon_config.xml` ha sido optimizado para evitar ahogar la red. Usa el enfoque:
- `<NetworkConnect onmatch="exclude" />`: Significa "Si la regla excluye nada, **incluye absolutamente todo**".
- Todo lo demás (ej. `ProcessCreate`, `FileDelete`) utiliza `<... onmatch="include" />` vacío, lo que silencia el evento completamente para el Event Viewer.
