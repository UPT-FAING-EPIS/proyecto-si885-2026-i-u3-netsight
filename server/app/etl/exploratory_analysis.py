"""
exploratory_analysis.py - Módulo de Análisis Exploratorio de Datos (EDA) y Predicción de Tráfico.

Este script realiza las siguientes acciones:
1. Conecta con PostgreSQL para extraer los datos de tráfico de red y DNS.
2. Si la base de datos no está disponible o está vacía, genera un dataset de simulación realista de Sysmon (Event ID 3 y 22).
3. Realiza un Análisis Exploratorio de Datos (EDA):
   - Distribución de protocolos (TCP/UDP/ICMP).
   - Aplicaciones más utilizadas (procesos).
   - Volumen de tráfico por hora.
4. Implementa un modelo predictivo (Regresión Lineal e Intervalo de Confianza) para proyectar
   el volumen de eventos de red diarios para los próximos 7 días, permitiendo estimar cuándo
   se llenará el almacenamiento.
5. Exporta un archivo de hoja de cálculo de Excel (.xlsx), gráficos visuales (.png) y un
   archivo consolidado en JSON (.json) con los resultados.
"""

import os
import json
import logging
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("exploratory_analysis")

# Rutas de salida para los artefactos generados
OUTPUT_DIR = r"c:\Users\Admin\Desktop\LabsNegocios\proyecto-si885-2026-i-u3-netsight\docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
PUBLIC_DIR = r"c:\Users\Admin\Desktop\LabsNegocios\proyecto-si885-2026-i-u3-netsight\dashboard\public"
os.makedirs(PUBLIC_DIR, exist_ok=True)

DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DATABASE", "network_monitor")
DB_USER = os.getenv("PG_USER", "netmon_user")
DB_PASS = os.getenv("PG_PASSWORD", "changeme")

def extract_data_from_db():
    """Intenta extraer datos reales de PostgreSQL."""
    try:
        import psycopg2
        logger.info("Intentando conectar a PostgreSQL para extraer datos...")
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASS
        )
        query_red = "SELECT * FROM v_trafico_resumen;"
        df_red = pd.read_sql_query(query_red, conn)
        
        query_dns = "SELECT * FROM v_trafico_dns_resumen;"
        df_dns = pd.read_sql_query(query_dns, conn)
        
        conn.close()
        
        if df_red.empty:
            logger.warning("La tabla de tráfico de red está vacía. Se usará simulación.")
            return None, None
            
        logger.info(f"Extraídos {len(df_red)} registros de red y {len(df_dns)} de DNS de la base de datos.")
        return df_red, df_dns
    except Exception as e:
        logger.warning(f"No se pudo conectar a la base de datos o falló la extracción: {e}. Se procederá a simular los datos.")
        return None, None

def generate_mock_data():
    """Genera datos de simulación realistas del tráfico Sysmon de laboratorios de la EPIS."""
    logger.info("Generando datos simulados con fines de modelado exploratorio y predictivo...")
    np.random.seed(42)
    
    # 1. Definir laboratorios y computadoras
    laboratorios = ["Laboratorio de Redes", "Laboratorio de Software", "Laboratorio de Sistemas"]
    computadoras = [f"PC-LAB{l[15:17]}-{i:02d}" for l in laboratorios for i in range(1, 11)]
    
    # 2. Generar marcas de tiempo para los últimos 30 días
    start_date = datetime.now() - timedelta(days=30)
    timestamps = [start_date + timedelta(minutes=int(x)) for x in np.random.exponential(10, 5000).cumsum()]
    timestamps = [ts for ts in timestamps if ts < datetime.now()]
    num_events = len(timestamps)
    
    # 3. Procesos comunes
    procesos = {
        "chrome.exe": 0.40,
        "msedge.exe": 0.15,
        "discord.exe": 0.10,
        "teams.exe": 0.08,
        "pycharm64.exe": 0.07,
        "Code.exe": 0.07,
        "spotify.exe": 0.05,
        "steam.exe": 0.04,
        "utorrent.exe": 0.03,
        "xmrig.exe": 0.01  # Minero de criptomonedas (Simulación de anomalía)
    }
    proc_list = list(procesos.keys())
    proc_weights = list(procesos.values())
    
    # 4. Puertos y Protocolos
    puertos = [80, 443, 8080, 53, 22, 3389, 445, 1514]
    p_weights = [0.15, 0.60, 0.08, 0.10, 0.02, 0.02, 0.01, 0.02]
    
    paises = ["Perú", "Estados Unidos", "Brasil", "Alemania", "Irlanda", "Rusia", "China", "LAN"]
    pais_weights = [0.10, 0.45, 0.05, 0.05, 0.05, 0.10, 0.10, 0.10]
    
    # 5. Llenar tráfico de red
    records_red = []
    for ts in timestamps:
        pc = np.random.choice(computadoras)
        lab = f"Laboratorio de {pc.split('-')[1][:3]}"
        if "RED" in pc:
            lab = "Laboratorio de Redes"
        elif "SOF" in pc:
            lab = "Laboratorio de Software"
        else:
            lab = "Laboratorio de Sistemas"
            
        proceso = np.random.choice(proc_list, p=proc_weights)
        puerto = int(np.random.choice(puertos, p=p_weights))
        protocolo = "TCP" if puerto != 53 else "UDP"
        pais = np.random.choice(paises, p=pais_weights)
        
        # Geolocalización mock
        ciudad = "Lima" if pais == "Perú" else ("New York" if pais == "Estados Unidos" else "Red Local" if pais == "LAN" else "Desconocida")
        
        records_red.append({
            "timestamp_evento": ts,
            "hostname": pc,
            "laboratorio_nombre": lab,
            "ip_origen": f"192.168.1.{np.random.randint(10, 200)}",
            "ip_destino": f"8.8.8.8" if puerto == 53 else f"104.244.42.{np.random.randint(1, 254)}",
            "pais_destino": pais,
            "ciudad_destino": ciudad,
            "puerto_destino": puerto,
            "protocolo": protocolo,
            "proceso": proceso
        })
        
    df_red = pd.DataFrame(records_red)
    
    # 6. Llenar tráfico DNS
    records_dns = []
    dominios = ["google.com", "github.com", "microsoft.com", "discord.gg", "spotify.com", "steamcommunity.com", "utorrent.com", "pool.minexmr.com"]
    d_weights = [0.25, 0.25, 0.15, 0.10, 0.08, 0.07, 0.07, 0.03]
    
    for _ in range(int(num_events * 0.8)):
        ts = np.random.choice(timestamps)
        pc = np.random.choice(computadoras)
        lab = "Laboratorio de Redes" if "RED" in pc else ("Laboratorio de Software" if "SOF" in pc else "Laboratorio de Sistemas")
        proceso = np.random.choice(proc_list, p=proc_weights)
        dominio = np.random.choice(dominios, p=d_weights)
        
        records_dns.append({
            "timestamp_evento": ts,
            "hostname": pc,
            "laboratorio_nombre": lab,
            "dominio": dominio,
            "proceso": proceso
        })
    df_dns = pd.DataFrame(records_dns)
    
    return df_red, df_dns

def perform_eda(df_red, df_dns):
    """Realiza análisis exploratorio y genera visualizaciones PNG."""
    logger.info("Realizando análisis exploratorio de datos (EDA)...")
    
    # Configurar estilo de los gráficos
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    
    # 1. Distribución de Protocolos
    plt.figure(figsize=(8, 5))
    protocolo_counts = df_red["protocolo"].value_counts()
    colors = ['#00FFFF', '#00E676', '#E040FB']
    protocolo_counts.plot(kind='bar', color=colors[:len(protocolo_counts)], edgecolor='black')
    plt.title("Distribución de Protocolos en el Tráfico de Red", fontsize=14, fontweight='bold', color='#1A237E')
    plt.xlabel("Protocolo", fontsize=12)
    plt.ylabel("Cantidad de Conexiones", fontsize=12)
    plt.tight_layout()
    plot_protocolo_path = os.path.join(OUTPUT_DIR, "plot_distribucion_protocolo.png")
    plt.savefig(plot_protocolo_path, dpi=150)
    plot_protocolo_public_path = os.path.join(PUBLIC_DIR, "plot_distribucion_protocolo.png")
    plt.savefig(plot_protocolo_public_path, dpi=150)
    plt.close()
    logger.info(f"Guardado gráfico de distribución de protocolos en: {plot_protocolo_path}")
    
    # 2. Top Procesos Generadores de Tráfico
    plt.figure(figsize=(10, 6))
    top_procesos = df_red["proceso"].value_counts().head(10)
    top_procesos.sort_values(ascending=True).plot(kind='barh', color='#29B6F6', edgecolor='black')
    plt.title("Top 10 Procesos con Mayor Tráfico de Red", fontsize=14, fontweight='bold', color='#1A237E')
    plt.xlabel("Número de Eventos Registrados", fontsize=12)
    plt.ylabel("Nombre del Proceso (.exe)", fontsize=12)
    plt.tight_layout()
    plot_procesos_path = os.path.join(OUTPUT_DIR, "plot_top_procesos.png")
    plt.savefig(plot_procesos_path, dpi=150)
    plot_procesos_public_path = os.path.join(PUBLIC_DIR, "plot_top_procesos.png")
    plt.savefig(plot_procesos_public_path, dpi=150)
    plt.close()
    logger.info(f"Guardado gráfico de procesos en: {plot_procesos_path}")

def perform_prediction(df_red):
    """Implementa proyección predictiva del volumen de tráfico."""
    logger.info("Calculando proyecciones de volumen de datos y tendencias diarias...")
    
    # Agrupar eventos por día
    df_red['fecha'] = pd.to_datetime(df_red['timestamp_evento']).dt.date
    daily_events = df_red.groupby('fecha').size().reset_index(name='eventos')
    daily_events = daily_events.sort_values('fecha').reset_index(drop=True)
    
    # Crear variable X (días numéricos desde el inicio)
    daily_events['dia_index'] = np.arange(len(daily_events))
    
    X = daily_events['dia_index']
    y = daily_events['eventos']
    
    # Ajuste de regresión lineal para predecir la tendencia del tráfico
    coef = np.polyfit(X, y, 1)
    poly1d_fn = np.poly1d(coef)
    
    # Proyección para los próximos 7 días
    future_days = np.arange(len(daily_events), len(daily_events) + 7)
    future_dates = [daily_events['fecha'].max() + timedelta(days=int(i)) for i in range(1, 8)]
    predictions = poly1d_fn(future_days)
    
    # Intervalo de Confianza simple (1.96 * Desviación Estándar de los residuos)
    residuos = y - poly1d_fn(X)
    std_error = np.std(residuos)
    margin = 1.96 * std_error
    
    # Graficar la serie temporal, la línea de tendencia y la proyección futura
    plt.figure(figsize=(12, 6))
    
    # Fechas completas para graficar
    all_dates = list(daily_events['fecha']) + future_dates
    all_x = np.concatenate([X, future_days])
    
    plt.plot(daily_events['fecha'], y, 'o-', color='#3F51B5', label='Tráfico Registrado', linewidth=2)
    plt.plot(daily_events['fecha'], poly1d_fn(X), '--', color='#FF5722', label='Tendencia Ajustada')
    
    # Graficar proyección
    plt.plot(future_dates, predictions, 'ro--', label='Proyección (Siguientes 7 Días)', linewidth=2)
    plt.fill_between(
        future_dates, 
        predictions - margin, 
        predictions + margin, 
        color='#FFCDD2', 
        alpha=0.5, 
        label='Intervalo de Confianza (95%)'
    )
    
    plt.title("Proyección y Tendencia de Volumen de Tráfico Diario (Sysmon Telemetry)", fontsize=14, fontweight='bold', color='#1A237E')
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Eventos Diarios", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    
    plot_proyeccion_path = os.path.join(OUTPUT_DIR, "plot_proyeccion_trafico.png")
    plt.savefig(plot_proyeccion_path, dpi=150)
    plot_proyeccion_public_path = os.path.join(PUBLIC_DIR, "plot_proyeccion_trafico.png")
    plt.savefig(plot_proyeccion_public_path, dpi=150)
    plt.close()
    logger.info(f"Guardado gráfico de proyección en: {plot_proyeccion_path}")
    
    # Preparar el dataframe de proyección para exportar
    df_projection = pd.DataFrame({
        "Fecha": future_dates,
        "Proyección_Eventos": np.round(predictions).astype(int),
        "Límite_Inferior_95": np.round(predictions - margin).astype(int),
        "Límite_Superior_95": np.round(predictions + margin).astype(int)
    })
    
    return daily_events, df_projection, coef

def export_to_excel(df_red, df_dns, daily_events, df_projection):
    """Exporta los datasets estructurados y el modelo predictivo a un libro Excel (.xlsx)."""
    excel_path = os.path.join(OUTPUT_DIR, "reporte_analisis_exploratorio.xlsx")
    logger.info(f"Guardando reporte estructurado de análisis exploratorio en Excel: {excel_path}")
    
    # Usar pandas ExcelWriter
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Pestaña 1: Resumen de Métricas
        resumen_df = pd.DataFrame({
            "Métrica": [
                "Total Eventos Red Registrados",
                "Total Solicitudes DNS Registradas",
                "Promedio Eventos Diarios",
                "Proceso más Activo",
                "Puerto más Utilizado",
                "País Destino con mayor flujo"
            ],
            "Valor": [
                len(df_red),
                len(df_dns),
                round(daily_events['eventos'].mean(), 2),
                df_red["proceso"].mode()[0],
                f"Puerto {df_red['puerto_destino'].mode()[0]}",
                df_red["pais_destino"].mode()[0]
            ]
        })
        resumen_df.to_excel(writer, sheet_name="Resumen Métricas", index=False)
        
        # Pestaña 2: Proyecciones Predictivas
        df_projection.to_excel(writer, sheet_name="Proyección 7 Días", index=False)
        
        # Pestaña 3: Histórico de Volumen Diario
        daily_events_export = daily_events.copy()
        daily_events_export.columns = ["Fecha", "Eventos_Registrados", "Dia_Index"]
        daily_events_export.to_excel(writer, sheet_name="Histórico Diario", index=False)
        
        # Pestaña 4: Distribución de Procesos
        proc_dist = df_red["proceso"].value_counts().reset_index()
        proc_dist.columns = ["Proceso", "Conexiones"]
        proc_dist.to_excel(writer, sheet_name="Uso de Aplicaciones", index=False)

    logger.info("Libro Excel exportado correctamente.")

def export_to_json(df_red, df_dns, df_projection, coef):
    """Guarda un resumen del análisis en formato JSON para consumo en la API o Next.js."""
    json_path = os.path.join(OUTPUT_DIR, "datos_analisis.json")
    logger.info(f"Guardando datos agregados en formato JSON: {json_path}")
    
    # Top países
    top_paises = df_red["pais_destino"].value_counts().head(5).to_dict()
    # Top procesos
    top_proc = df_red["proceso"].value_counts().head(5).to_dict()
    # Puertos
    top_ports = df_red["puerto_destino"].value_counts().head(5).to_dict()
    
    data = {
        "fecha_analisis": datetime.now().isoformat(),
        "total_registros_red": len(df_red),
        "total_registros_dns": len(df_dns),
        "resumen_infraestructura": {
            "top_paises": top_paises,
            "top_procesos": top_proc,
            "top_puertos": top_ports
        },
        "modelo_predictivo": {
            "coeficiente_pendiente": coef[0],
            "coeficiente_interseccion": coef[1],
            "ecuacion": f"Eventos = {coef[0]:.4f} * Dia_Index + {coef[1]:.4f}",
            "proyecciones": [
                {
                    "fecha": row["Fecha"].strftime("%Y-%m-%d"),
                    "proyeccion": int(row["Proyección_Eventos"]),
                    "limite_inferior": int(row["Límite_Inferior_95"]),
                    "limite_superior": int(row["Límite_Superior_95"])
                }
                for _, row in df_projection.iterrows()
            ]
        }
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Archivo JSON generado con éxito.")

def main():
    logger.info("=== Iniciando Proceso de Análisis Exploratorio y Predictivo (EDA) ===")
    
    # 1. Intentar cargar datos reales o generar mock
    df_red, df_dns = extract_data_from_db()
    if df_red is None:
        df_red, df_dns = generate_mock_data()
        
    # 2. Ejecutar EDA (Gráficos)
    perform_eda(df_red, df_dns)
    
    # 3. Modelado Predictivo
    daily_events, df_projection, coef = perform_prediction(df_red)
    
    # 4. Exportar a Excel
    export_to_excel(df_red, df_dns, daily_events, df_projection)
    
    # 5. Exportar a JSON
    export_to_json(df_red, df_dns, df_projection, coef)
    
    logger.info("=== Proceso de Análisis Exploratorio y Predictivo Finalizado con Éxito ===")

if __name__ == "__main__":
    main()
