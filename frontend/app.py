import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date
import api_service  # <--- Importamos nuestra lógica separada

# 1. Configuración Inicial
st.set_page_config(page_title="Revisión de vuelos", layout="wide")

# 2. Cargar Estilos (CSS)
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- CABECERA ---
c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    st.markdown("<h1 style='text-align: center;'>Revisión de vuelos</h1>", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
col_izq, col_der = st.columns([1, 1.5], gap="large")

# === COLUMNA IZQUIERDA: INPUTS ===
with col_izq:
    st.write("### Datos del Vuelo")
    
    aerolinea = st.text_input("AEROLINEA", value="Airline")
    origen = st.text_input("ORIGEN", value="Origin")
    destino = st.text_input("DESTINO", value="Destination")
    fecha = st.date_input("FECHA", value=date(2026, 1, 1), format="DD/MM/YYYY")
    
    st.write("")
    
    consultar = st.button("Consultar")

# === LÓGICA DE INTERACCIÓN ===
# Valores por defecto para el gráfico (cuando arranca la app)
probabilidad_retraso = 0
resultado_texto = "Pendiente"

if consultar:
    with st.spinner("Consultando IA..."):
        # Llamamos a nuestro archivo de lógica separado
        respuesta = api_service.obtener_prediccion(aerolinea, origen, destino, fecha)
        
        if "error" in respuesta:
            st.error(respuesta["error"])
        else:
            # Procesar respuesta exitosa
            st.success("¡Análisis completado!")
            probabilidad_retraso = respuesta.get("probabilidad", 0) * 100
            resultado_texto = respuesta.get("prevision", "Desconocido")

# === COLUMNA DERECHA: VISUALIZACIÓN ===
with col_der:
    # Preparar datos para el gráfico
    # Si no se ha consultado, mostramos valores por defecto o ceros
    if consultar:
        prob_puntual = 100 - probabilidad_retraso
    else:
        # Valores de ejemplo para que se vea bonito al inicio (como en tu imagen)
        probabilidad_retraso = 0
        prob_puntual = 100

    df = pd.DataFrame({
        'Categoría': ['Posibilidad salir en hora', 'Posibilidad de retraso'],
        'Porcentaje': [prob_puntual, probabilidad_retraso]
    })
    
    # Gráfico
    fig = px.pie(df, values='Porcentaje', names='Categoría', hole=0.6,
                 color='Categoría',
                 color_discrete_map={
                     'Posibilidad salir en hora': '#4DD0E1',
                     'Posibilidad de retraso': '#64E9DE'
                 })
    
    fig.update_traces(textinfo='none', hoverinfo='label+percent', 
                      marker=dict(line=dict(color='#ffffff', width=2)))
    
    fig.update_layout(
        showlegend=False,
        height=350,
        margin=dict(t=30, b=0, l=0, r=0),
        annotations=[dict(text=f'{prob_puntual:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)  
    
    # Resultado numérico
    st.markdown("<h4 style='text-align: center; margin: 0; padding: 0;'>Previsión del Modelo</h4>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 3rem; margin: 0; padding: 0;'>{resultado_texto}</h1>", unsafe_allow_html=True)