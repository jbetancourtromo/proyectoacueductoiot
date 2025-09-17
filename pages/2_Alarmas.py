import streamlit as st
import requests
import pandas as pd

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7' # ¡Pega aquí tu Read API Key!
URL_THINGSPEAK_LATEST = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}'

# --- Función para obtener el estado de alarma ---
@st.cache_data(ttl=60)
def get_alarm_status():
    try:
        response = requests.get(URL_THINGSPEAK_LATEST)
        response.raise_for_status()
        data = response.json()
        return int(float(data.get('field8', 0)))
    except Exception as e:
        st.error(f"Error al obtener estado de alarmas: {e}")
    return -1

# --- Diseño de la página ---
st.title("🔔 Estado de Alarmas")
st.markdown("Verifica el estado actual del sistema de alarmas.")
st.markdown("---")

alarm_value = get_alarm_status()

if alarm_value != -1:
    if alarm_value > 0:
        st.error("🚨 ¡ATENCIÓN! Alarma activada. Posibles problemas detectados.")
        
        alarm_messages = []
        if (alarm_value & 1) > 0: alarm_messages.append("Alarma de Caudal")
        if (alarm_value & 2) > 0: alarm_messages.append("Alarma de Cloro")
        if (alarm_value & 4) > 0: alarm_messages.append("Alarma de Nivel")
        if (alarm_value & 8) > 0: alarm_messages.append("Alarma de Altura")
        if (alarm_value & 16) > 0: alarm_messages.append("Alarma de Presión")
        
        st.warning("Alarmas activas: " + ", ".join(alarm_messages))
    else:
        st.success("✅ Sistema en estado normal. No se han detectado alarmas.")
else:
    st.warning("No se pudo obtener el estado de alarmas.")