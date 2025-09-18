import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7' # ¡Pega aquí tu Read API Key!
URL_THINGSPEAK_CSV = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}'

st.title("💧 Sistema de Monitoreo del Acueducto - Samaniego")
st.markdown("Programa Talento Tech 2025 - Proyecto Acueducto IoT -James Betancourt R -Christian Gaucales ")

# --- Función para obtener los datos históricos de ThingSpeak en CSV ---
@st.cache_data(ttl=3600)
def get_historical_csv(start_date, end_date):
    try:
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        url_with_range = f"{URL_THINGSPEAK_CSV}&start={start_date_str}&end={end_date_str}"
        response = requests.get(url_with_range)
        response.raise_for_status()
        
        from io import StringIO
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Opcional: renombrar las columnas para mayor claridad
        df.rename(columns={
            'created_at': 'Fecha y Hora', 'field1': 'Caudal (L/min)', 'field2': 'Cloro (ppm)',
            'field3': 'Nivel (%)', 'field4': 'Altura (m)', 'field5': 'Presion (bar)',
            'field6': 'Temperatura (°C)', 'field7': 'Humedad (%)', 'field8': 'Alarmas'
        }, inplace=True)
        
        return df
    except Exception as e:
        st.error(f"Error al descargar datos: {e}")
    return pd.DataFrame()

# --- Diseño de la página ---
st.title("📥 Descarga de Datos Históricos")
st.markdown("Selecciona un rango de fechas para visualizar y descargar los datos completos en formato CSV.")
st.markdown("---")

# Selectores de fecha para el rango
col_start, col_end = st.columns(2)
with col_start:
    start_date = st.date_input("Fecha de inicio:", datetime.now().date() - timedelta(days=7))
with col_end:
    end_date = st.date_input("Fecha de fin:", datetime.now().date())

# Cargar y mostrar los datos
if st.button("Cargar Datos Históricos"):
    with st.spinner("Cargando datos..."):
        historical_df = get_historical_csv(datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.max.time()))
        
        if not historical_df.empty:
            st.success(f"Datos cargados. {len(historical_df)} registros encontrados.")
            st.dataframe(historical_df, use_container_width=True)
            
            # Botón de descarga CSV
            st.download_button(
                label="Descargar datos en CSV",
                data=historical_df.to_csv(index=False).encode('utf-8'),
                file_name=f"datos_acueducto_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
        else:

            st.warning("No se encontraron datos para el rango de fechas seleccionado.")
