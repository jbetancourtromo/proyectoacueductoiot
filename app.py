import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- Configuración de ThingSpeak ---
CHANNEL_ID = '3071480'
# Si tu canal es privado, añade tu Read API Key aquí:
# READ_API_KEY = 'IHA53391H4BEBFJ7'
URL_THINGSPEAK = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json'
# Si el canal es privado, la URL debe incluir la clave:
# URL_THINGSPEAK = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}'

# --- Función para obtener los últimos datos ---
@st.cache_data(ttl=60) # Cacha los datos por 60 segundos
def fetch_thingspeak_data():
    """
    Obtiene los datos más recientes del canal de ThingSpeak y los organiza.
    """
    try:
        response = requests.get(URL_THINGSPEAK)
        response.raise_for_status()  # Lanza una excepción para errores HTTP
        data = response.json()
        
        # Mapea los datos de los campos a nombres de sensores
        last_entry = data['feeds'][-1]
        sensor_data = {
            "Caudal": last_entry['field1'],
            "Cloro": last_entry['field2'],
            "Nivel": last_entry['field3'],
            "Altura": last_entry['field4'],
            "Presion": last_entry['field5'],
            "Temperatura": last_entry['field6'],
            "Humedad": last_entry['field7'],
            "Alarmas": last_entry['field8'],
        }
        return sensor_data, data['feeds']

    except requests.exceptions.RequestException as e:
        st.error(f"Error de red al conectar con ThingSpeak: {e}")
        return None, None
    except (KeyError, IndexError) as e:
        st.error(f"Error al procesar los datos recibidos. Asegúrate de que el canal tiene datos: {e}")
        return None, None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")
        return None, None

# --- Diseño de la página ---
st.set_page_config(
    page_title="Monitoreo Acueducto Ovejas-Tangua",
    page_icon="💧",
    layout="wide"
)

# --- Título principal y descripción ---
st.title("💧 Sistema de Monitoreo del Acueducto")
st.markdown("Dashboard interactivo para visualizar los datos en tiempo real y el histórico del proyecto de monitoreo del acueducto Ovejas-Tangua.")

# --- Llama a la función y obtiene los datos ---
sensor_data, historical_data = fetch_thingspeak_data()

st.markdown("---")

## **📈 Datos en Tiempo Real**

if sensor_data:
    st.write("Valores de los sensores en la última lectura:")
    
    # Crea un contenedor para las métricas
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Caudal (L/min)", f"{float(sensor_data['Caudal']):.2f}")
        with col2:
            st.metric("Cloro (ppm)", f"{float(sensor_data['Cloro']):.2f}")
        with col3:
            st.metric("Nivel (%)", f"{float(sensor_data['Nivel']):.2f}")
        with col4:
            st.metric("Presión (bar)", f"{float(sensor_data['Presion']):.2f}")
        with col5:
            st.metric("Temperatura (°C)", f"{float(sensor_data['Temperatura']):.2f}")
    
    # Sección para las alarmas
    st.subheader("Estado de Alarmas")
    alarm_value = int(float(sensor_data['Alarmas']))
    
    if alarm_value > 0:
        st.error("🚨 ¡ATENCIÓN! Alarma activada. Posibles problemas detectados.")
        # Opcional: decodifica los bits de la máscara de alarma para mostrar qué alarmas están activas
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
    st.warning("No se pudieron cargar los datos de los sensores. Por favor, verifica la conexión.")

st.markdown("---")

## **📊 Histórico de Datos y Tendencias**

if historical_data:
    df = pd.DataFrame(historical_data)
    
    # Renombra y limpia el DataFrame
    df.rename(columns={
        'created_at': 'Fecha y Hora',
        'field1': 'Caudal', 'field2': 'Cloro', 'field3': 'Nivel',
        'field4': 'Altura', 'field5': 'Presion', 'field6': 'Temperatura',
        'field7': 'Humedad', 'field8': 'Alarmas'
    }, inplace=True)
    df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'])
    
    # Convierte las columnas a valores numéricos, gestionando posibles errores
    for col in ['Caudal', 'Cloro', 'Nivel', 'Altura', 'Presion', 'Temperatura', 'Humedad', 'Alarmas']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    df.dropna(inplace=True)

    # Selector de datos
    sensor_options = ['Caudal', 'Cloro', 'Nivel', 'Altura', 'Presion', 'Temperatura', 'Humedad']
    selected_sensors = st.multiselect("Selecciona los sensores para el gráfico:", sensor_options, default=['Caudal', 'Nivel'])

    if selected_sensors:
        fig = px.line(df, x='Fecha y Hora', y=selected_sensors,
                      title='Evolución de Parámetros del Acueducto',
                      labels={'value': 'Valor', 'variable': 'Parámetro'},
                      markers=True)
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Por favor, selecciona al menos un sensor para visualizar los datos históricos.")
else:
    st.info("No hay datos históricos disponibles para mostrar en el gráfico.")

st.markdown("---")

## **📸 Galería del Proyecto**
st.subheader("Proyecto Acueducto -Talento Tech")
st.write("Diagrama de los componentes del sistema y su conexión.")
# Cambia esta URL a la ruta de tu imagen en tu repositorio de GitHub
st.image("https://raw.githubusercontent.com/jbetancourtromo/proyectoacueductoiot/main/assets/acueducto.png",
         caption="Diagrama de flujo del sistema de monitoreo IoT", use_column_width=True)

st.write("Recuerda reemplazar 'TU_USUARIO' y 'TU_REPO' con tus datos de GitHub.")
