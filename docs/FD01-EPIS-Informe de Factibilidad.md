# FD01 - Informe de Factibilidad

## 1. Descripción del Proyecto

**Nombre del proyecto:** NetSight - Sistema de Monitoreo de Laboratorio  
**Duración del proyecto:** 3 meses (12 semanas)  

**Descripción:**  
El proyecto NetSight consiste en el diseño e implementación de una arquitectura de telemetría y monitoreo continuo para el parque informático de los laboratorios de la Escuela Profesional de Ingeniería de Sistemas (UPT). El sistema utiliza agentes a nivel de kernel (Sysmon y Wazuh) para extraer eventos de red, transmitirlos hacia la nube, procesarlos mediante un motor ETL y consolidarlos en un Dashboard web interactivo y tableros de Power BI. El contexto en el que se desenvuelve es el entorno académico universitario, donde existe una alta concurrencia de estudiantes utilizando el hardware institucional, lo que hace imperativo un control proactivo para evitar el desgaste de equipos, el uso indebido del ancho de banda y la propagación de malware.

### 1.4 Objetivos

**1.4.1 Objetivo general**  
Desarrollar e implementar el Sistema de Telemetría de Laboratorios (NetSight) para monitorear, gestionar y analizar el tráfico de red y el estado del hardware de las computadoras de la EPIS-UPT en tiempo real, garantizando la seguridad y optimizando los recursos de TI.

**1.4.2 Objetivos Específicos**  
*   **Implementar agentes de recolección ligeros:** Se logrará instalar de forma silenciosa el agente Sysmon/Wazuh en todas las terminales mediante un instalador C# WPF para capturar metadatos sin afectar el rendimiento de las clases.
*   **Desarrollar un Motor ETL asíncrono:** Se logrará extraer los registros de OpenSearch, enriquecerlos con geolocalización (GeoLite2) y cargarlos estructuradamente en PostgreSQL mediante procesamiento por lotes (*Batching*).
*   **Construir un Dashboard de Gestión (Next.js):** Se logrará proveer al administrador de una interfaz web amigable para visualizar el inventario de laboratorios, computadoras activas y reportes históricos.
*   **Integrar tableros analíticos (Power BI):** Se logrará proveer inteligencia de negocios para el descubrimiento de amenazas a través de mapas de calor y métricas de concurrencia usando *DirectQuery*.

---

## 2. Riesgos

*   **Saturación del Ancho de Banda Institucional:** El envío masivo de logs desde 100+ computadoras simultáneamente podría ralentizar la red de la EPIS.
*   **Rechazo Estudiantil por Privacidad:** Alumnos o docentes podrían percibir el monitoreo como espionaje o rastreo de información personal.
*   **Pérdida de Conectividad con la Nube:** Caídas del enlace de fibra óptica de la universidad, impidiendo el envío de la telemetría en tiempo real al servidor en Azure.
*   **Llenado Prematuro del Disco en Servidor:** Acumulación descontrolada de logs históricos que podría colapsar la base de datos PostgreSQL.

---

## 3. Análisis de la Situación actual

### Planteamiento del problema
**Antecedentes y Situación Actual:**  
En la actualidad, la administración de los laboratorios de la EPIS se realiza mediante un modelo estrictamente reactivo. Cuando ocurre una anomalía (lentitud extrema de red, minería de criptomonedas, descarga de *torrents* ilegales), el equipo de Soporte Técnico se entera únicamente por reportes verbales de los docentes. 

**Problemática y Necesidad:**  
El técnico debe trasladarse físicamente, interrumpiendo la clase para revisar manualmente el "Visor de Eventos" de Windows. Usualmente, el alumno responsable ya cerró los procesos maliciosos, borró el caché del navegador o usó modo incógnito. Existe una ceguera total; no hay evidencia digital forense ni un panel centralizado para auditar el uso de las máquinas. Esta necesidad de transformar la administración reactiva (correctiva) en una administración proactiva y centralizada será resuelta de manera absoluta con la implementación de NetSight.

### Consideraciones de hardware y software
Para la implementación de NetSight, se ha evaluado la tecnología existente y alcanzable:
*   **Hardware Cliente (Existente):** Las PCs de los laboratorios cuentan con procesadores Core i5/i7 y +8GB RAM, superando holgadamente los requisitos del agente Sysmon (que consume <15MB RAM y <1% de CPU).
*   **Hardware Servidor (Propuesto):** No existen servidores locales con alta disponibilidad en la facultad. Se utilizará infraestructura *Cloud* (Azure VPS - 4 vCPUs, 16GB RAM) que es alcanzable y escalable.
*   **Software (Propuesto):** Se utilizará una pila tecnológica 100% *Open Source* o de licenciamiento educativo: Windows 10/11 (SO base), Wazuh Agent (C/XML), Python/FastAPI (Backend), PostgreSQL (Base de datos), Next.js (Frontend web) y Power BI Desktop (Analítica avanzada).

---

## 4. Estudio de Factibilidad

El presente estudio evalúa las dimensiones técnicas, económicas, operativas, legales, sociales y ambientales de NetSight. Este análisis fue elaborado por el equipo de desarrollo, auditado mediante pruebas de concepto (PoC) en entornos de red controlados, y está diseñado para ser aprobado por la Jefatura de Laboratorios y la Dirección de la EPIS.

### 4.1 Factibilidad Técnica
El proyecto es **viable técnicamente**. La universidad dispone de terminales Windows compatibles nativamente con Sysmon. La arquitectura de backend se basa en contenedores Docker (OpenSearch, PostgreSQL, FastAPI, Node.js), eliminando problemas de dependencias en el servidor. 
*   **Equipos:** Computadoras estándar de laboratorio (Intel/AMD x64).
*   **Servidor:** Servidor Virtual Privado (VPS) en Microsoft Azure corriendo Ubuntu Server 22.04 LTS.
*   **Infraestructura de Red:** Conexión LAN Gigabit existente en laboratorios con salida a Internet, configurada para permitir tráfico TCP saliente en los puertos 443 (HTTPS) y 1514 (Wazuh).

### 4.2 Factibilidad Económica
El proyecto no requiere compra de hardware físico local ni pago de licenciamiento empresarial por terminal (modelo que usan antivirus comerciales). Los costos son mínimos y operativos.

**1. Costos Generales**
| Descripción | Monto Estimado (S/.) |
| :--- | :--- |
| Laptops de desarrollo (Uso de equipos propios) | 0.00 |
| Material de oficina y papelería | 150.00 |
| **Total Costos Generales** | **150.00** |

**2. Costos Operativos durante el desarrollo**
| Descripción | Monto Estimado (S/.) |
| :--- | :--- |
| Servicios básicos proporcionales (Internet, Energía - 3 meses) | 450.00 |
| **Total Costos Operativos** | **450.00** |

**3. Costos del ambiente**
| Descripción | Monto Estimado (S/.) |
| :--- | :--- |
| Suscripción Cloud Azure VPS (1 año proyectado) | 2,250.00 |
| Dominio web institucional (.edu.pe) | Proporcionado por UPT |
| **Total Costos de Ambiente** | **2,250.00** |

**4. Costos de personal**
El equipo trabajará en horario parcial (20 horas semanales) durante las 12 semanas de desarrollo.
| Rol | Cantidad | Costo Mensual (S/.) | Meses | Total (S/.) |
| :--- | :--- | :--- | :--- | :--- |
| Desarrollador Backend / Arquitecto Cloud | 1 | 1,500.00 | 3 | 4,500.00 |
| Desarrollador Frontend / Analista BI | 1 | 1,500.00 | 3 | 4,500.00 |
| **Total Costos de Personal** | | | | **9,000.00** |

**5. Costos Totales del Desarrollo del Sistema**
*   Costos Generales: S/. 150.00
*   Costos Operativos: S/. 450.00
*   Costos del Ambiente: S/. 2,250.00
*   Costos de Personal: S/. 9,000.00
*   **Costo Total del Proyecto: S/. 11,850.00** (Pago financiado internamente mediante asignación de presupuesto por proyectos de investigación/mejora continua de la EPIS).

### 4.3 Factibilidad Operativa
NetSight es **operativamente factible**. El impacto en los usuarios (estudiantes y docentes) es nulo, ya que la aplicación se ejecuta invisiblemente en el kernel sin interfaz gráfica que interrumpa las clases. La lista de interesados (Directores, Docentes, Soporte Técnico) se beneficia de un mantenimiento ágil. El área de TI de la universidad tiene la capacidad técnica requerida para mantener activo un clúster de Docker, garantizando el soporte del sistema a largo plazo.

### 4.4 Factibilidad Legal
El proyecto es **legalmente factible**. Se alinea con la Ley N° 29733 (Ley de Protección de Datos Personales de Perú). NetSight no rastrea identidades, contraseñas ni archivos privados de los estudiantes. Captura metadatos técnicos (Hashes SHA-256, Puertos, Direcciones IP) de las conexiones generadas desde un equipo que es propiedad de la universidad. Está respaldado por las políticas de Uso Aceptable de la Red de la EPIS.

### 4.5 Factibilidad Social
A nivel ético y cultural, la plataforma fomenta el respeto por los recursos académicos. Evitará que minorías saturen el ancho de banda descargando contenido lúdico, garantizando que todos los estudiantes dispongan de internet rápido y fluido para su formación académica, mejorando así el clima educativo.

### 4.6 Factibilidad Ambiental
NetSight impacta positivamente el medio ambiente. A través de la telemetría, permite descubrir anomalías energéticas graves (ej. PC encendida por días minando criptomonedas con la CPU al 100%). Identificar y apagar remotamente estas máquinas reduce el derroche de electricidad y disminuye drásticamente la huella de carbono del laboratorio.

---

## 5. Análisis Financiero

### 5.1 Justificación de la Inversión

**5.1.1 Beneficios del Proyecto**
*   **Beneficios Tangibles:** 
    *   **Reducción de recursos humanos (Soporte Técnico):** Se estima un ahorro de 15 horas semanales de diagnóstico presencial. A un valor estimado de S/. 20/hora, equivale a S/. 1,200 mensuales o **S/. 14,400 anuales**.
    *   **Reducción de futuras inversiones:** Previene el reemplazo prematuro de discos duros o procesadores por abuso de uso (ej. minería). Ahorro estimado de 3 PCs dañadas al año (**S/. 6,000 anuales**).
    *   **Total Beneficios Tangibles:** S/. 20,400 anuales.
*   **Beneficios Intangibles:**
    *   Toma acertada de decisiones basada en métricas de concurrencia.
    *   Mejora exponencial en el clima de las clases prácticas (sin internet lento).
    *   Aumento en la confiabilidad de la información (evidencia inmutable ante auditorías).

**5.1.2 Criterios de Inversión**

Asumiendo un ciclo de evaluación de 3 años, con una Tasa de Descuento (COK) del 10% y flujos de caja generados por los ahorros institucionales:
*   Inversión Inicial (Año 0): S/. -11,850.00
*   Flujo de Caja Anual (Beneficios Tangibles - Renovación Cloud): S/. 20,400 - S/. 2,250 = **S/. 18,150.00 anuales**.

**5.1.2.1 Relación Beneficio/Costo (B/C)**
Calculando el valor presente de los ingresos (S/. 45,136) frente a los egresos actualizados (S/. 17,445):
*   **B/C = 2.58**
*   *Análisis:* Como el B/C es significativamente mayor a 1, se **acepta el proyecto**. Por cada sol invertido, la universidad recupera más de 2.5 soles en ahorro operativo.

**5.1.2.2 Valor Actual Neto (VAN)**
*   **VAN = S/. 33,286.00**
*   *Análisis:* El VAN es considerablemente mayor que cero. La implementación de NetSight generará valor real y cuantificable para la institución. El proyecto se **acepta**.

**5.1.2.3 Tasa Interna de Retorno (TIR)**
*   **TIR = 143%**
*   *Análisis:* La TIR (143%) es abrumadoramente superior al Costo de Oportunidad del Capital (COK = 10%). Este altísimo rendimiento se debe al bajísimo costo inicial (software libre) frente al alto costo de las horas-hombre que se ahorran. El proyecto se **acepta absolutamente**.

---

## 6. Conclusiones

Los resultados del análisis de factibilidad demuestran contundentemente que **el proyecto NetSight es viable y altamente factible.**

Desde la perspectiva técnica y operativa, el sistema introduce modernización (DevOps, Big Data, Telemetría) sin requerir reentrenamiento de los usuarios ni compras de hardware costoso. En el ámbito legal y social, respeta íntegramente la privacidad a la vez que democratiza el acceso justo al ancho de banda. 

Financieramente, los indicadores (B/C de 2.58 y un VAN de S/. 33,286) dictaminan que el proyecto no solo se paga a sí mismo en los primeros meses de despliegue mediante el ahorro de tiempo del soporte técnico, sino que protege los valiosos activos tecnológicos de la universidad de la degradación prematura. Se recomienda la aprobación inmediata y el inicio de la etapa de desarrollo.
