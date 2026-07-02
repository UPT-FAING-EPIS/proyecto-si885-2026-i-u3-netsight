# Estructura de Presentación: NetSight (Opción 2 - Enfoque Directivo)

Este documento contiene la estructura visual, el texto sugerido para las diapositivas y el guion oral (*speech*) para tu sustentación del proyecto NetSight. Está diseñado para una duración aproximada de 10-15 minutos ante un jurado mixto (técnico y de negocios).

---

## Diapositiva 1: Portada y El Problema Institucional

*   **Título Visual:** NetSight: Sistema de Telemetría para Laboratorios
*   **Texto en pantalla (Viñetas breves):**
    *   **Contexto:** Parque informático crítico de la UPT sin auditoría automatizada.
    *   **El Problema:** Modelo reactivo. Diagnóstico manual de incidentes.
    *   **El Impacto:** Impunidad ante mal uso (ej. criptominería), desgaste de hardware y pérdida de tiempo de enseñanza.
*   **Prompt para imagen (opcional):** `A split screen illustration. Left side: a stressed IT technician looking at a broken computer in a university lab. Right side: A glowing, futuristic abstract network of computers connected to a central glowing node. Flat vector style, corporate blue and orange colors.`
*   **Guion Oral (Speech):** 
    > "Buenos días. Imaginen un laboratorio con 40 computadoras de alta gama donde, de pronto, el internet colapsa o las máquinas se congelan. Actualmente, en la EPIS, el técnico debe ir físicamente, revisar máquina por máquina y, usualmente, el estudiante infractor ya borró su historial. Presentamos NetSight, la solución para erradicar esta ceguera operativa y transformar el diagnóstico reactivo en inteligencia proactiva."

---

## Diapositiva 2: Objetivos y Restricciones del Proyecto

*   **Título Visual:** Objetivos y Delimitación Tecnológica
*   **Texto en pantalla:**
    *   **Objetivo:** Telemetría centralizada e inmutable sin intervenir el hardware de red.
    *   **Requerimientos Clave:**
        *   Agente invisible (Zero-Touch) en Windows.
        *   Análisis masivo de logs sin saturar la red local.
    *   **Restricciones Legales:** Cumplimiento estricto de la Ley N° 29733 (Privacidad de datos; cero keyloggers).
*   **Visual:** Íconos minimalistas (Un escudo de seguridad, un engranaje y un mazo legal).
*   **Guion Oral (Speech):** 
    > "Nuestro objetivo no era comprar aparatos costosos, sino crear un agente silencioso de software. La universidad exigió tres cosas: que la instalación fuera instantánea, que no se sature la red de los alumnos, y algo vital: el cumplimiento de la Ley de Protección de Datos Personales. NetSight no rastrea contraseñas ni pulsaciones, solo metadatos forenses como IPs y Hashes de sistema."

---

## Diapositiva 3: Arquitectura General del Sistema

*   **Título Visual:** Arquitectura Híbrida y Tubería de Datos (Data Pipeline)
*   **Visual Recomendado:** Coloca aquí el **Diagrama C4 de Contenedores** (El diagrama de la Sección 8.1 del FD04 que muestra la PC, Azure y el Administrador).
*   **Texto en pantalla:**
    *   **Endpoint (Laboratorio):** Sysmon + Wazuh Agent.
    *   **Ingesta (Azure Cloud):** OpenSearch (Buffer) + FastAPI.
    *   **ETL & Persistencia:** Python Batching + PostgreSQL.
    *   **Presentación:** Power BI y Next.js.
*   **Guion Oral (Speech):** 
    > "Esta es la radiografía del proyecto. Usamos una arquitectura de microservicios distribuida. En el laboratorio, Sysmon y Wazuh capturan la huella digital. Ese log viaja cifrado a la nube de Azure y cae en un amortiguador llamado OpenSearch. Para no colapsar la base de datos, usamos un motor ETL en Python que actúa como un puente: cruza las IPs para saber de qué país provienen y luego guarda los datos estructurados en PostgreSQL."

---

## Diapositiva 4: Explotación Analítica (El Resultado Final)

*   **Título Visual:** Inteligencia de Negocios y Monitoreo Web
*   **Visual Recomendado:** Un *Mockup* (montaje) de una laptop mostrando el Dashboard de Next.js y un monitor mostrando los Mapas de Calor de Power BI.
*   **Prompt para imagen (opcional):** `A sleek, modern dual-monitor desk setup. The left monitor shows a dark-mode web dashboard with lists of computers. The right monitor shows a bright Power BI data visualization with heatmaps and bar charts. Professional office lighting, photorealistic.`
*   **Texto en pantalla:**
    *   **Inventario en Tiempo Real:** Dashboard web seguro (autenticado con JWT).
    *   **Mapas de Calor (Power BI):** Consultas *DirectQuery* para cruzar fechas, aulas y amenazas.
    *   **Evidencia Inmutable:** Trazabilidad firmada criptográficamente (SHA-256).
*   **Guion Oral (Speech):** 
    > "Todo el trabajo arquitectónico desemboca aquí. El administrador ya no lee archivos de texto aburridos. Ingresa a un portal web rápido hecho en Next.js para gestionar el inventario, y utiliza tableros dinámicos en Power BI. Si hubo un ataque, el sistema muestra exactamente el Hash criptográfico del archivo malicioso, brindando evidencia inmutable para aplicar sanciones."

---

## Diapositiva 5: Factibilidad Financiera (Retorno de Inversión)

*   **Título Visual:** Viabilidad y Presupuesto (Modelo OPEX)
*   **Visual Recomendado:** Una tabla comparativa simple o un gráfico de barras (Costos vs Ahorros).
*   **Texto en pantalla:**
    *   **Inversión Inicial:** Basado 100% en *Open Source* (Cero licencias por PC).
    *   **Costo Cloud (Azure):** S/ 2,250.00 anuales.
    *   **Ahorro Institucional Estimado:** S/ 20,400.00 (Prevención de hardware y horas-hombre).
    *   **Indicadores de Éxito:** B/C = 2.58 | TIR = 143%.
*   **Guion Oral (Speech):** 
    > "Técnicamente es un éxito, pero comercialmente es aún mejor. Al rechazar opciones propietarias como CrowdStrike, ahorramos miles de dólares en licencias. Los únicos costos recaen en el pago del servidor virtual en Azure y el desarrollo interno (S/ 11,850 en total). El proyecto se paga solo en meses, logrando una altísima Tasa Interna de Retorno del 143% gracias al ahorro de horas de soporte técnico y prevención de daños a los procesadores."

---

## Diapositiva 6: Conclusiones y Cierre

*   **Título Visual:** Conclusiones y Trabajo Futuro
*   **Texto en pantalla:**
    *   **Misión Cumplida:** Ceguera operativa erradicada. La EPIS cuenta con visibilidad absoluta.
    *   **Escalabilidad Comprobada:** El búfer asíncrono soporta miles de eventos sin latencia.
    *   **Trabajo Futuro / Recomendaciones:** Despliegue masivo vía *Active Directory (GPO)* y capacitación docente en análisis de datos.
*   **Guion Oral (Speech):** 
    > "En conclusión, NetSight demuestra que la universidad puede implementar tecnologías corporativas de Big Data a costos muy bajos. Hemos reemplazado los rumores por evidencia científica, y las reparaciones de hardware por prevención inteligente. El siguiente paso es integrar la instalación silenciosa a las Políticas de Grupo de la red universitaria. Muchas gracias."
