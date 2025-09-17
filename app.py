import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'TU_READ_API_KEY' # Opcional si el canal es público
URL_THINGSPEAK = f'httpsapi.thingspeak.comchannels{CHANNEL_ID}feeds.json'
# Si tu canal es privado, usa
# URL_THINGSPEAK = f'httpsapi.thingspeak.comchannels{CHANNEL_ID}feeds.jsonapi_key={READ_API_KEY}'

# --- Función para obtener los últimos datos ---
@st.cache_data(ttl=60) # Cacha los datos por 60 segundos para evitar llamadas repetitivas
def fetch_thingspeak_data()
    try
        response = requests.get(URL_THINGSPEAK)
        data = response.json()
        
        # Mapea los datos de los campos a nombres de sensores
        last_entry = data['feeds'][-1]
        sensor_data = {
            Caudal last_entry['field1'],
            Cloro last_entry['field2'],
            Nivel last_entry['field3'],
            Altura last_entry['field4'],
            Presion last_entry['field5'],
            Temperatura last_entry['field6'],
            Humedad last_entry['field7'],
            Alarmas last_entry['field8'],
        }
        return sensor_data, data['feeds']

    except Exception as e
        st.error(fError al obtener datos de ThingSpeak {e})
        return None, None
        
# --- Llama a la función y obtiene los datos ---
sensor_data, historical_data = fetch_thingspeak_data()

# --- Diseño de la página ---
st.set_page_config(layout="wide")
st.title("💧 Monitoreo del Acueducto Ovejas-Tangua")
st.markdown("---")

# --- Sección 1: Datos en Tiempo Real (KPIs) ---
st.header("📈 Valores Actuales de Sensores")
if sensor_data:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Caudal (L/min)", f"{float(sensor_data['Caudal']):.2f}")
    with col2:
        st.metric("Cloro (ppm)", f"{float(sensor_data['Cloro']):.2f}")
    with col3:
        st.metric("Nivel (%)", f"{float(sensor_data['Nivel']):.2f}")
    with col4:
        st.metric("Altura (m)", f"{float(sensor_data['Altura']):.2f}")
    with col5:
        st.metric("Presión (bar)", f"{float(sensor_data['Presion']):.2f}")
    
    # Muestra las alarmas
    st.subheader("Estado de Alarmas")
    alarm_value = int(sensor_data['Alarmas'])
    # Puedes usar una lógica para decodificar la máscara de bits
    if alarm_value > 0:
        st.error("🚨 ¡ATENCIÓN! Alarma activada.")
    else:
        st.success("✅ Sistema en estado normal.")
st.markdown("---")

# --- Sección 2: Análisis Histórico (Gráficos) ---
st.header("📊 Análisis Histórico de Datos")
if historical_data:
    df = pd.DataFrame(historical_data)
    df.rename(columns={
        'created_at': 'Fecha y Hora',
        'field1': 'Caudal', 'field2': 'Cloro', 'field3': 'Nivel',
        'field4': 'Altura', 'field5': 'Presion', 'field6': 'Temperatura',
        'field7': 'Humedad', 'field8': 'Alarmas'
    }, inplace=True)
    df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'])

    # Creación del gráfico interactivo con Plotly
    fig = px.line(df, x='Fecha y Hora', y=['Caudal', 'Nivel', 'Presion'],
                  title='Evolución de Parámetros del Acueducto',
                  labels={'value': 'Valor', 'variable': 'Parámetro'})
    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# --- Sección 3: Galería del Proyecto ---
st.header("📸 Galería del Proyecto")
st.image("https://raw.githubusercontent.com/jbetancourtromo/proyectoacueductoiot/main/assets/acueducto.png")
st.caption("Diagrama del sistema de monitoreo en Wokwi.")