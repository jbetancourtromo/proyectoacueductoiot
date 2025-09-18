import streamlit as st
import requests
import pandas as pd
import base64

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7' # ¡Pega aquí tu Read API Key!
URL_THINGSPEAK_LATEST = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds/last.json?api_key={READ_API_KEY}'

st.title("💧 Sistema de monitoreo acueducto - Samaniego")
st.markdown("Programa Talento Tech 2025 - Proyecto Acueducto IoT -James Betancourt R -Christian Gaucales ")

# --- Función para obtener el estado de alarma ---
@st.cache_data(ttl=60)
def get_alarm_status():
    """Obtiene el último valor de la máscara de alarmas (field8)."""
    try:
        response = requests.get(URL_THINGSPEAK_LATEST)
        response.raise_for_status()
        data = response.json()
        # Asegúrate de que el valor sea numérico antes de convertirlo a entero
        alarm_value = data.get('field8', '0')
        return int(float(alarm_value))
    except Exception as e:
        st.error(f"Error al obtener estado de alarmas: {e}")
    return -1

# --- Estilos CSS para los botones circulares ---
# Estos estilos se inyectan en la página
st.markdown("""
    <style>
    .circle-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    .circle-button {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        color: white;
        font-weight: bold;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: background-color 0.3s ease;
    }
    .circle-button.active {
        background-color: #e74c3c; /* Rojo para alarma activa */
    }
    .circle-button.inactive {
        background-color: #2ecc71; /* Verde para alarma inactiva */
    }
    .circle-text {
        font-size: 14px;
        line-height: 1.2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Mapeo de bits a nombres de alarma ---
alarm_map = {
    1: "Caudal",
    2: "Cloro",
    4: "Nivel",
    8: "Presión",
    16: "Temperatura"
}

# --- Diseño de la página ---
st.title("🔔 Estado de Alarmas")
st.markdown("Verifica el estado actual del sistema de alarmas con indicadores visuales.")
st.markdown("---")

alarm_value = get_alarm_status()

if alarm_value != -1:
    st.subheader("Indicadores de Alarma")
    
    # Renderiza los botones usando HTML/CSS
    html_content = '<div class="circle-container">'
    
    for bit, name in alarm_map.items():
        is_active = (alarm_value & bit) > 0
        status_class = "active" if is_active else "inactive"
        status_text = "Activa" if is_active else "Inactiva"
        
        html_content += f"""
        <div style="text-align:center; margin:10px;">
            <div class="circle-button {status_class}">
                <span class="circle-text">{name}</span>
            </div>
            <p style='margin-top:5px; font-weight:bold;'>{status_text}</p>
        </div>
        """
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)

else:
    st.warning("No se pudo obtener el estado de las alarmas.")

st.markdown("---")

if alarm_value > 0:
    st.error("🚨 ¡ATENCIÓN! Se ha detectado una alarma. Los indicadores rojos señalan el problema.")
else:
    st.success("✅ Sistema en estado normal. No se han detectado alarmas.")
      

