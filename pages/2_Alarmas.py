import streamlit as st
import requests
import pandas as pd
import base64

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7' # ¡Pega aquí tu Read API Key!
URL_THINGSPEAK_LATEST = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}'

st.title("💧 Sistema de Monitoreo del Acueducto - Samaniego")
st.markdown("Programa Talento Tech 2025 - Proyecto Acueducto IoT -James Betancourt R -Christian Gaucales ")

# --- Función para obtener el estado de alarma ---
@st.cache_data(ttl=60)
def get_alarm_status():
    """Obtiene el último valor de la máscara de alarmas (field8)."""
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
st.markdown("Verifica el estado actual del sistema de alarmas con indicadores visuales.")
st.markdown("---")

# --- Lógica de alarmas y botones circulares ---
alarm_value = get_alarm_status()

# Diccionario para mapear bits a nombres de alarma
alarm_map = {
    1: "Caudal",
    2: "Cloro",
    4: "Nivel",
    8: "Altura",
    16: "Presión"
}

st.subheader("Indicadores de Alarma")

if alarm_value != -1:
    cols = st.columns(len(alarm_map))

    for i, (bit, name) in enumerate(alarm_map.items()):
        is_active = (alarm_value & bit) > 0
        color = "red" if is_active else "green"
        status_text = "Activa" if is_active else "Inactiva"
        
        with cols[i]:
            # CSS para el botón circular
            st.markdown(
                f"""
                <style>
                .circle-button {{
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    background-color: {color};
                    border: 2px solid #333;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    margin: auto;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # HTML para el botón y el texto
            st.markdown(
                f"""
                <div class="circle-button">
                    <p style="color:white; font-weight:bold; font-size:12px; line-height:1.2;">{name}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"<p style='text-align:center; font-weight:bold; font-size:14px; margin-top:10px;'>{status_text}</p>", unsafe_allow_html=True)
else:
    st.warning("No se pudo obtener el estado de las alarmas.")

st.markdown("---")

if alarm_value > 0:
    st.error("🚨 ¡ATENCIÓN! Alarma activada. Posibles problemas detectados.")
    st.warning("Verifica los sensores con el indicador rojo para más detalles.")
else:
    st.success("✅ Sistema en estado normal. No se han detectado alarmas.")


