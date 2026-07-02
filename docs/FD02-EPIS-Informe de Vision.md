# FD02 - Informe de Visión (NetSight)

## 1. Introducción

### 1.1 Propósito
El propósito de este documento es recopilar, analizar y definir las necesidades de alto nivel y las características del producto **NetSight** (Sistema de Telemetría de Laboratorios de la EPIS). Se enfoca en las capacidades que necesita la Escuela Profesional de Ingeniería de Sistemas y los motivos por los que se requieren. Sirve como base para el alineamiento entre los desarrolladores, los administradores de TI y la jefatura académica respecto a *qué* construirá el equipo de desarrollo.

### 1.2 Alcance
Este Informe de Visión aplica a la plataforma integral de telemetría **NetSight**, la cual abarca:
*   El despliegue de agentes silenciosos en las computadoras de laboratorio.
*   La transmisión, limpieza y almacenamiento en la nube (Azure) de eventos forenses.
*   La interfaz de gestión (Next.js) y visualización analítica (Power BI) para la toma de decisiones institucionales.
No incluye la modificación física del hardware de red (switches o routers) de la universidad, operando exclusivamente a nivel de software de aplicación (Endpoint).

### 1.3 Definiciones, Siglas y Abreviaturas
*   **Stakeholders:** Interesados o involucrados clave del proyecto (Docentes, Estudiantes, Administradores, Jefatura).
*   **SIEM:** *Security Information and Event Management*. Sistemas que proporcionan análisis en tiempo real de alertas de seguridad generadas por el hardware de red.
*   **Telemetría:** Medición automática y transmisión de datos a distancia desde el equipo origen hasta un punto de recepción (Nube) para su monitorización.
*   **WPF:** *Windows Presentation Foundation*, tecnología usada para el desarrollo del instalador gráfico en Windows.

### 1.4 Referencias
*   **[FD01]** Informe de Factibilidad (NetSight).
*   **[FD03]** Especificación de Requerimientos de Software (NetSight).
*   **[FD04]** Informe de Arquitectura de Software (NetSight).
*   Metodología RUP (*Rational Unified Process*) - Documento de Visión.

### 1.5 Visión General
El resto del presente Informe de Visión aborda el Posicionamiento del producto y la Definición del Problema (Sección 2). En futuras secciones se desarrollarán los Perfiles de los Usuarios (*Stakeholders*), las Capacidades del Producto y las Restricciones de Diseño que enmarcan los límites del sistema NetSight.

---

## 2. Posicionamiento

### 2.1 Oportunidad de negocio (Oportunidad Institucional)
La Escuela Profesional de Ingeniería de Sistemas (EPIS) cuenta con múltiples laboratorios especializados y un parque informático considerable. Actualmente, la universidad invierte presupuestos significativos en hardware de alto rendimiento y ancho de banda, sin embargo, carece de métricas exactas sobre su utilización real. 

La oportunidad institucional radica en **introducir metodologías corporativas de Ciberseguridad y Monitoreo (Big Data / SIEM)** dentro del ámbito académico a una fracción del costo tradicional, apalancándose en herramientas *Open Source*. Esto permitirá a la Jefatura prolongar la vida útil del hardware, reducir drásticamente los gastos operativos asociados al Soporte Técnico, y garantizar un entorno de enseñanza fluido y equitativo para los estudiantes.

### 2.2 Definición del problema

Para establecer claramente la razón de ser de NetSight, se enuncia la problemática bajo el formato estándar:

| Elemento | Descripción de la Problemática |
| :--- | :--- |
| **El problema de...** | La falta de monitoreo proactivo, diagnóstico tardío y abuso indiscriminado de la red por parte de los usuarios en los laboratorios de cómputo. |
| **Afecta a...** | Los Docentes (que pierden tiempo de enseñanza), los Estudiantes (que sufren de internet lento), el equipo de Soporte Técnico (saturado con tareas manuales) y la Dirección de la EPIS (sin datos para justificar presupuestos). |
| **El impacto del cual es...** | Degradación prematura del hardware (debido a ejecución de malware oculto o criptominería), clases prácticas interrumpidas por lentitud de la red, y la absoluta incapacidad de rastrear o sancionar a los estudiantes que cometen infracciones informáticas (ausencia de evidencia inmutable). |
| **Una buena solución sería...** | Una plataforma de telemetría centralizada, asíncrona y transparente (invisible para el alumno), que recolecte huellas digitales de red de manera inmutable desde el *Kernel*, centralice el análisis en la nube, y presente tableros visuales interactivos que notifiquen automáticamente anomalías al administrador. |


## 3. Descripción de los interesados y usuarios

### 3.1 Resumen de los interesados
Los interesados (*Stakeholders*) son las personas u organizaciones que respaldan, patrocinan o se ven impactadas indirectamente por el proyecto, aunque no necesariamente utilizan el sistema en su día a día.
*   **Dirección de la EPIS:** Patrocinador principal. Interesado en que el proyecto prevenga daños patrimoniales y mejore la calidad del servicio educativo.
*   **Jefatura de Laboratorios:** Interesado en contar con reportes estadísticos para justificar la necesidad de nuevos equipos o mayor ancho de banda.
*   **Docentes y Estudiantes:** Impactados positivamente. No interactúan con el sistema, pero se benefician de una red libre de cuellos de botella generados por usuarios irregulares.

### 3.2 Resumen de los usuarios
Los usuarios son quienes interactuarán directamente con el software NetSight a través de sus interfaces.
*   **Analista de Seguridad / Administrador TI:** Usuario principal del Dashboard web y los tableros de Power BI. Encargado de monitorear alertas y gestionar el inventario de máquinas.
*   **Técnico de Soporte:** Usuario operativo de campo. Encargado de utilizar el Instalador Cliente (C# WPF) en cada computadora física de los laboratorios.

### 3.3 Entorno de usuario
El sistema se utiliza en dos entornos físicos y lógicos distintos:
*   **Entorno Administrativo (Nube/Web):** El Analista de Seguridad accede al sistema desde cualquier computadora de la universidad o mediante VPN remota, utilizando navegadores modernos (Chrome, Edge, Firefox) para ingresar al Dashboard y Power BI.
*   **Entorno Operativo (Laboratorios EPIS):** El Técnico de Soporte interactúa con computadoras físicas (arquitectura x64, SO Windows 10/11) dentro de las subredes de la universidad (LAN). La instalación se realiza físicamente vía USB o remotamente vía Políticas de Grupo (GPO).

### 3.4 Perfiles de los interesados
*   **Director EPIS:** Toma decisiones ejecutivas. Requiere reportes de alto nivel (mensuales/semestrales) sobre el porcentaje de uso de los laboratorios y el Retorno de Inversión (ROI) del hardware adquirido.
*   **Jefe de Laboratorios:** Coordina la operatividad. Necesita saber qué computadoras fallan frecuentemente y si la infraestructura actual soporta el software moderno que demandan los cursos.

### 3.5 Perfiles de los Usuarios
*   **Administrador TI:** Perfil técnico avanzado. Capaz de interpretar direcciones IP, puertos lógicos y hashes criptográficos. Su labor es filtrar "ruido" e identificar verdaderas amenazas en el tráfico recolectado.
*   **Técnico de Soporte:** Perfil técnico intermedio. Su enfoque es la eficiencia; necesita que el proceso de afiliar una nueva computadora al sistema tome menos de 1 minuto y no requiera configuraciones complejas por consola de comandos.

### 3.6 Necesidades de los interesados y usuarios
| Interesado / Usuario | Necesidad | Solución Actual | Solución Propuesta (NetSight) |
| :--- | :--- | :--- | :--- |
| **Administrador TI** | Centralizar el monitoreo de cientos de PCs sin revisar una por una. | Inspección manual (Visor de Eventos). | Un único tablero web analítico en Power BI actualizado en tiempo real. |
| **Técnico Soporte** | Instalar el agente de recolección rápidamente y sin errores humanos. | Ejecución manual de decenas de *scripts* .BAT. | Un instalador unificado (`.exe`) empaquetado en C# con validaciones gráficas. |
| **Jefatura** | Reportes de uso inmutables para aplicar sanciones a infractores de red. | Reportes verbales (sin evidencia física). | Trazabilidad forense firmada con *hashes SHA-256* desde el Kernel. |

---

## 4. Vista General del Producto

### 4.1 Perspectiva del producto
NetSight no es un simple programa de escritorio, sino una **Arquitectura Distribuida**. Es un producto independiente desarrollado *In-House* para la UPT, pero que se apoya e interactúa fuertemente con subsistemas externos probados en la industria:
*   **Nivel SO:** Depende del driver oficial de *Microsoft Sysinternals (Sysmon)*.
*   **Nivel Transporte:** Depende del agente *Wazuh* para el cifrado y ruteo TCP.
*   **Nivel Enriquecimiento:** Se apoya en la base de datos *GeoLite2* para resolución geográfica (offline).

### 4.2 Resumen de capacidades
1.  **Recolección Silenciosa e Inmutable:** Captura conexiones de red y creación de procesos a nivel de sistema operativo (Ring 0), imposible de ser burlado por un alumno en modo incógnito.
2.  **ETL Asíncrono e Inteligente:** Un motor Python que procesa picos de miles de registros por minuto usando colas, resolviendo la IP a un país/ciudad, para luego insertarlo masivamente en PostgreSQL (*Bulk Insert*).
3.  **Visualización Analítica Híbrida:** Presenta un CRUD clásico web para gestión básica (Next.js) y un lienzo de inteligencia de negocios avanzado (Power BI) vía *DirectQuery* para mapas de calor.
4.  **Autonomía de Almacenamiento (Housekeeping):** El sistema se auto-purga cronológicamente para evitar llenar el disco duro del servidor en Azure.

### 4.3 Suposiciones y dependencias
*   **Suposiciones:** Se asume que todas las computadoras objetivo utilizarán el sistema operativo Windows 10 o superior (no hay cobertura Linux/Mac para el Endpoint). Se asume que el puerto TCP 1514 de salida no está bloqueado por el firewall perimetral de la universidad.
*   **Dependencias:** El motor de búsqueda rápida (*buffer*) depende absolutamente de que el contenedor de OpenSearch cuente con al menos 8GB de RAM libres en Azure.

### 4.4 Costos y precios
Al ser un desarrollo interno (tesis o proyecto institucional), NetSight **no tiene un precio de comercialización (Venta al público = $0)**. 
Los costos operativos recaen enteramente bajo el modelo OPEX (Gasto Operativo Cloud). La universidad solo debe financiar la suscripción a Microsoft Azure (VPS Standard_D4s_v3), con un costo aproximado de entre $40 y $80 USD mensuales, lo cual incluye el tráfico de datos entrante (Ingress) gratuito.

### 4.5 Licenciamiento e instalación
*   **Licenciamiento del Código Propio:** El software desarrollado (Dashboard, Motor ETL, Instalador C#) será entregado a la EPIS bajo una licencia permisiva (ej. MIT) para uso interno.
*   **Licenciamiento de Terceros:** Wazuh opera bajo licencia *GPLv2*, PostgreSQL bajo *PostgreSQL License* y Next.js bajo *MIT*. Todas permiten su uso sin pagos corporativos.
*   **Instalación:** 
    *   **Servidor:** Despliegue totalmente automatizado basado en Infraestructura como Código (*Terraform*).
    *   **Endpoint (Laboratorio):** Instalación *"One-Click"* mediante un autoejecutable (`Setup.exe`) que inscribe la máquina, configura los XML de Sysmon y arranca el servicio automáticamente sin requerir reinicio del equipo.


## 5. Características del producto

NetSight se distingue por las siguientes características de alto nivel que dictan su desarrollo técnico:
*   **Monitoreo Transparente (Zero-Touch):** El agente cliente se instala y ejecuta sin mostrar ninguna interfaz al usuario final (estudiante). Se inicia automáticamente con el arranque de Windows como un servicio del sistema.
*   **Filtrado Heurístico en el Origen:** El sistema no recolecta "todo" el tráfico. Solo filtra y encola eventos deterministas de alto riesgo (Event ID 3: Conexiones de red, Event ID 22: Consultas DNS) generados por procesos detectados por Sysmon.
*   **Enriquecimiento Geográfico Asíncrono:** Antes de ser almacenada, cada dirección IP foránea es interceptada por el motor ETL en Python e identificada con un país y ciudad utilizando la base de datos *GeoLite2*.
*   **Analítica Visual Dinámica:** En lugar de exportar hojas de cálculo muertas, el sistema se conecta por *DirectQuery* a Power BI, ofreciendo "Mapas de Calor" interactivos donde el Administrador puede filtrar picos de red por fecha, laboratorio o programa ejecutable.

## 6. Restricciones

El diseño y desarrollo de NetSight está condicionado por las siguientes restricciones ineludibles:
*   **Restricciones de Hardware Cliente:** El agente de telemetría (Sysmon/Wazuh) está estrictamente diseñado para entornos **Windows (Arquitectura x64)**. Computadoras con Linux o macOS en los laboratorios quedan fuera del alcance del proyecto actual.
*   **Restricciones de Hardware Servidor:** Para garantizar la ingesta masiva de logs en tiempo real, el contenedor de indexación (OpenSearch) exige un entorno virtualizado (Azure) con al menos **16 GiB de Memoria RAM** dedicados.
*   **Restricciones Legales/Éticas:** Por cumplimiento normativo de la privacidad estudiantil, el sistema tiene terminantemente **prohibido capturar pulsaciones de teclado (Keyloggers), realizar capturas de pantalla, interceptar tráfico HTTPS desencriptado (Capa 7) o recopilar datos biométricos**.

## 7. Rangos de calidad

Para que el producto sea considerado exitoso y operativo en el entorno de producción de la universidad, debe cumplir con los siguientes atributos y métricas de calidad:
*   **Tolerancia a Caídas (Resiliencia):** Si la PC cliente pierde conexión a internet, el agente debe cachear la telemetría localmente (hasta 1GB). La pérdida de datos (*Data Loss*) permitida es de **0%** ante cortes de red de hasta 72 horas.
*   **Latencia Analítica:** El tiempo transcurrido desde que un estudiante genera una conexión anómala hasta que el evento aparece estructurado en la base de datos de PostgreSQL no debe exceder los **5 minutos** (frecuencia máxima del motor Batch ETL).
*   **Rendimiento Visual (Performance):** Los tableros de Power BI deben renderizar millones de registros históricos en menos de **3 segundos**, gracias a la pre-agregación y creación de Vistas Materializadas en la base de datos.
*   **Disponibilidad del Servicio Web (Uptime):** La API REST y el sistema de ingesta (Wazuh Manager) deben ostentar una disponibilidad del **99.9%** (arquitectura orientada a Alta Disponibilidad).

## 8. Precedencia y Prioridad

Dado el volumen del sistema, la liberación de las características se organiza según la criticidad para la EPIS.

**Prioridad Alta (Núcleo Crítico):**
1.  Desarrollo del **Instalador Autoejecutable en C# (WPF)** y configuración del agente *Sysmon*. Sin esto, no hay recolección de datos.
2.  Implementación del contenedor **OpenSearch** en Azure y desarrollo del **Motor ETL en Python**. Sin esto, los datos crudos no pueden ser procesados ni almacenados estructuralmente.

**Prioridad Media (Explotación de Datos):**
3.  Desarrollo de las Vistas Materializadas en PostgreSQL e integración mediante *DirectQuery* con **Power BI**. Esto provee el retorno de inversión visual para la Jefatura.
4.  Creación del script de **Housekeeping**. Crítico a mediano plazo para evitar la saturación del disco duro del servidor.

**Prioridad Baja (Gestión Administrativa):**
5.  Desarrollo del **Dashboard Web en Next.js**. Aunque útil para el inventario, los administradores de TI pueden, en primera instancia, gestionar la base de datos directamente vía SQL o a través de las herramientas internas de Wazuh si es estrictamente necesario, por lo que su desarrollo puede aplazarse a la última fase del ciclo de vida.


## 9. Otros requerimientos del producto

Además de las capacidades funcionales, el sistema debe alinearse a marcos normativos y tecnológicos específicos para garantizar su legitimidad y robustez.

### a) Estándares legales
*   **Ley N° 29733 (Ley de Protección de Datos Personales - Perú):** El sistema debe garantizar que toda recolección se limite a telemetría técnica (Direcciones IP, Hostnames, hashes de procesos) y no recopile datos biométricos, credenciales bancarias ni historiales de navegación privada desencriptada, asegurando el estricto cumplimiento de la normativa nacional.
*   **Políticas Universitarias (EPIS-UPT):** El despliegue del sistema debe estar amparado por los términos de "Uso Aceptable de la Red Institucional" que los estudiantes aceptan implícitamente al matricularse.

### b) Estándares de comunicación
*   **Protocolos Seguros en Tránsito:** Toda la telemetría que viaja desde los laboratorios (LAN) hacia la nube (Azure) debe estar encapsulada utilizando el protocolo **TCP sobre TLS (Transport Layer Security) v1.2 o v1.3**.
*   **Gestión Web:** El acceso de los administradores al Dashboard y a la API REST debe forzarse mediante **HTTPS** utilizando certificados SSL válidos, mitigando ataques de intermediario (*Man-In-The-Middle*).

### c) Estándares de cumplimiento de la plataforma
*   **Norma ISO/IEC 27001 (Referencial):** Aunque la universidad no busque una certificación formal inmediata para este proyecto, el tratamiento de los *logs* de red (su retención, inmutabilidad y acceso restringido) debe basarse en las mejores prácticas del anexo A de esta norma internacional para Sistemas de Gestión de Seguridad de la Información (SGSI).

### d) Estándares de calidad y seguridad
*   **Autenticación y Autorización:** El backend en FastAPI debe implementar seguridad basada en **JWT (JSON Web Tokens)** para el acceso a las rutas administrativas.
*   **Almacenamiento de Credenciales:** Todas las contraseñas de los administradores almacenadas en PostgreSQL deben ser *hasheadas* irreversiblemente utilizando el algoritmo **Bcrypt**, garantizando que una brecha de base de datos no exponga accesos en texto plano.
*   **Prevención de Inyección:** Integración obligatoria de un ORM (como *SQLAlchemy*) para la sanitización de consultas, impidiendo ataques de Inyección SQL (SQLi).

---

## CONCLUSIONES

1.  El Informe de Visión consolida la justificación estratégica del sistema **NetSight**, dictaminando que la administración de los laboratorios debe abandonar de manera urgente el modelo reactivo.
2.  La visión del producto es clara: proveer una plataforma de monitoreo *Zero-Touch* (invisible para el alumno), que descentraliza el esfuerzo técnico mediante un motor ETL y centraliza la toma de decisiones a través de tableros de inteligencia de negocios (Power BI).
3.  Al delimitar estrictamente las capacidades y, sobre todo, las **restricciones legales y tecnológicas**, garantizamos que el equipo de desarrollo se enfoque en la extracción de metadatos forenses inmutables, maximizando el rendimiento (Búfer de 1GB) y evitando sobreingeniería que comprometa la viabilidad del proyecto.

## RECOMENDACIONES

1.  **Despliegue Centralizado:** Para evitar cuellos de botella operativos en la fase de implementación, se recomienda encarecidamente utilizar las Políticas de Grupo (GPO) del *Active Directory* (si existe) o herramientas de clonación de discos (ej. *Clonezilla*) para inyectar el instalador `.exe` del agente en todas las computadoras simultáneamente.
2.  **Capacitación Analítica:** Se recomienda impartir un taller básico de interpretación de *Dashboards* (Power BI) al Director de la EPIS y Jefatura de Laboratorios, asegurando que las métricas extraídas se conviertan efectivamente en decisiones institucionales y justificación de presupuestos.
3.  **Auditorías Periódicas de Red:** Revisar semestralmente que el Firewall perimetral de la universidad no bloquee el tráfico de salida TCP por el puerto 1514, vital para la sincronización con la nube.

## BIBLIOGRAFIA

*   **Microsoft Corporation.** (2023). *Sysmon (System Monitor) - Windows Sysinternals*. Recuperado de la documentación oficial de Microsoft.
*   **Wazuh Inc.** (2024). *Wazuh Documentation: Architecture and Deployment*. Recuperado de docs.wazuh.com.
*   **Kruchten, P.** (2003). *The Rational Unified Process: An Introduction* (3ra Edición). Addison-Wesley Professional. (Referencia metodológica para la estructuración de la Visión).
*   **Congreso de la República del Perú.** (2011). *Ley N° 29733, Ley de Protección de Datos Personales*. Diario Oficial El Peruano.
