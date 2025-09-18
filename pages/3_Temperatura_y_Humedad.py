import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7' # ¡Pega aquí tu Read API Key!
URL_THINGSPEAK_LATEST = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}'

st.title("💧 Sistema de monitoreo acueducto - Samaniego")
st.markdown("Programa Talento Tech 2025 - Proyecto Acueducto IoT -James Betancourt R -Christian Gaucales ")

# --- Función para obtener los últimos datos ---
@st.cache_data(ttl=60)
def get_latest_data_gauges():
    try:
        response = requests.get(URL_THINGSPEAK_LATEST)
        response.raise_for_status()
        data = response.json()
        return {
            "Temperatura": float(data.get('field6')),
            "Humedad": float(data.get('field7'))
        }
    except Exception as e:
        st.error(f"Error al obtener datos para los medidores: {e}")
    return None

# --- Diseño de la página ---
st.title("🌡️ Temperatura y Humedad")
st.markdown("Visualización de las últimas lecturas de temperatura y humedad .")
st.markdown("---")

sensor_data = get_latest_data_gauges()

if sensor_data:
    temp_val = sensor_data["Temperatura"]
    hum_val = sensor_data["Humedad"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Temperatura (°C)")
        fig_temp = go.Figure(go.Indicator(
            mode="gauge+number",
            value=temp_val,
            title={'text': "Temperatura"},
            gauge={'axis': {'range': [None, 50]},
                   'bar': {'color': "green"},
                   'steps': [
                       {'range': [0, 20], 'color': "lightblue"},
                       {'range': [20, 35], 'color': "lightgreen"},
                       {'range': [35, 50], 'color': "salmon"}
                   ]}
        ))
        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        st.subheader("Humedad (%)")
        fig_hum = go.Figure(go.Indicator(
            mode="gauge+number",
            value=hum_val,
            title={'text': "Humedad"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkblue"},
                   'steps': [
                       {'range': [0, 40], 'color': "red"},
                       {'range': [40, 70], 'color': "yellow"},
                       {'range': [70, 100], 'color': "lightgreen"}
                   ]}
        ))
        st.plotly_chart(fig_hum, use_container_width=True)
else:

    st.warning("No se pudieron cargar los datos de temperatura y humedad.")


