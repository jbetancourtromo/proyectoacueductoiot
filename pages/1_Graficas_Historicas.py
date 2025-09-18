import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
READ_API_KEY = 'IHA53391H4BEBFJ7' # ¡Pega aquí tu Read API Key!
URL_THINGSPEAK_FEEDS = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=2000' # Obtiene hasta 2000 puntos

st.title("💧 Sistema de Monitoreo del Acueducto - Samaniego")

# --- Función para obtener los datos históricos ---
@st.cache_data(ttl=3600) # Cacha los datos por 1 hora
def get_historical_data():
    try:
        response = requests.get(URL_THINGSPEAK_FEEDS)
        response.raise_for_status()
        data = response.json()
        if 'feeds' in data:
            return pd.DataFrame(data['feeds'])
    except Exception as e:
        st.error(f"Error al obtener datos históricos: {e}")
    return pd.DataFrame()

# --- Diseño de la página ---
st.title("📊 Gráficas Históricas")
st.markdown("Visualiza la evolución de los datos de los sensores a lo largo del tiempo.")
st.markdown("---")

df_historico = get_historical_data()

if not df_historico.empty:
    df_historico.rename(columns={
        'created_at': 'Fecha y Hora',
        'field1': 'Caudal', 'field2': 'Cloro', 'field3': 'Nivel',
        'field4': 'Altura', 'field5': 'Presion', 'field6': 'Temperatura',
        'field7': 'Humedad'
    }, inplace=True)
    df_historico['Fecha y Hora'] = pd.to_datetime(df_historico['Fecha y Hora'])
    
    for col in ['Caudal', 'Cloro', 'Nivel', 'Altura', 'Presion', 'Temperatura', 'Humedad']:
        df_historico[col] = pd.to_numeric(df_historico[col], errors='coerce')
    df_historico.dropna(inplace=True)

    # Selector de sensores
    sensor_options = ['Caudal', 'Cloro', 'Nivel', 'Altura', 'Presion', 'Temperatura', 'Humedad']
    selected_sensors = st.multiselect("Selecciona los sensores para el gráfico:", sensor_options, default=['Caudal', 'Nivel'])

    if selected_sensors:
        fig = px.line(df_historico, x='Fecha y Hora', y=selected_sensors,
                      title='Evolución de Parámetros del Acueducto',
                      labels={'value': 'Valor', 'variable': 'Parámetro'},
                      markers=True)
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Por favor, selecciona al menos un sensor para visualizar los datos históricos.")
else:

    st.warning("No se pudieron cargar datos históricos. Inténtalo de nuevo más tarde.")
