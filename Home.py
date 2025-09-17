import streamlit as st
import requests
import pandas as pd

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7'
URL_THINGSPEAK = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}'

# --- Función para obtener los datos más recientes ---
@st.cache_data(ttl=60)
def get_latest_data():
    try:
        response = requests.get(URL_THINGSPEAK_FEEDS)
        response.raise_for_status()
        data = response.json()
        if 'feeds' in data and len(data['feeds']) > 0:
            last_entry = data['feeds'][-1]
            return {
                "Caudal": last_entry.get('field1'),
                "Cloro": last_entry.get('field2'),
                "Nivel": last_entry.get('field3'),
                "Altura": last_entry.get('field4'),
                "Presion": last_entry.get('field5'),
                "Temperatura": last_entry.get('field6'),
                "Humedad": last_entry.get('field7'),
                "Alarmas": last_entry.get('field8')
            }
    except Exception as e:
        st.error(f"Error al obtener datos de ThingSpeak: {e}")
    return None

# --- Diseño de la página ---
st.set_page_config(
    page_title="Inicio - Acueducto",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Sistema de Monitoreo del Acueducto")
st.markdown("Dashboard interactivo para visualizar los datos en tiempo real y el histórico del proyecto de monitoreo del acueducto Municipio Samaniego")

st.markdown("---")

# --- Imagen del Acueducto ---
# Reemplaza la URL de la imagen con la que tengas en tu repositorio de GitHub
st.image("https://raw.githubusercontent.com/jbetancourtromo/proyectoacueductoiot/main/assets/acueducto.png",
         caption="Proyecto de Ingeniería Mecatrónica: Acueducto Ovejas-Tangua", use_column_width=True)


st.markdown("---")

# --- Valores de los sensores en tiempo real ---
st.header("📈 Valores de los sensores en la última lectura")

sensor_data = get_latest_data()
if sensor_data:
    cols = st.columns(4)
    cols[0].metric("Caudal (L/min)", f"{float(sensor_data['Caudal']):.2f}" if sensor_data['Caudal'] else "N/D")
    cols[1].metric("Cloro (ppm)", f"{float(sensor_data['Cloro']):.2f}" if sensor_data['Cloro'] else "N/D")
    cols[2].metric("Nivel (%)", f"{float(sensor_data['Nivel']):.2f}" if sensor_data['Nivel'] else "N/D")
    cols[3].metric("Altura (m)", f"{float(sensor_data['Altura']):.2f}" if sensor_data['Altura'] else "N/D")
    
    col_temp, col_hum, col_pres = st.columns(3)
    col_temp.metric("Temperatura (°C)", f"{float(sensor_data['Temperatura']):.2f}" if sensor_data['Temperatura'] else "N/D")
    col_hum.metric("Humedad (%)", f"{float(sensor_data['Humedad']):.2f}" if sensor_data['Humedad'] else "N/D")
    col_pres.metric("Presión (bar)", f"{float(sensor_data['Presion']):.2f}" if sensor_data['Presion'] else "N/D")

else:
    st.warning("No se pudieron cargar los datos de los sensores. Por favor, verifica la conexión y que el canal de ThingSpeak tenga datos.")