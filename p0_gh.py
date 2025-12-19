import streamlit as st
from openai import OpenAI
import pandas as pd

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.text_input("Contraseña:", type="password", on_change=password_entered, key="password")
        return False
    
    if not st.session_state["authenticated"]:
        st.text_input("Contraseña:", type="password", on_change=password_entered, key="password")
        st.error("Contraseña incorrecta")
        return False
    
    return True

if check_password():
    st.title("Análisis de datos con IA")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Cargar datos
df = pd.read_csv("datosprueba.csv", sep=";")

# Mostrar los datos
st.subheader("Datos disponibles")
st.dataframe(df)

# Input del usuario
pregunta = st.text_input("Pregunta sobre los datos:")

if pregunta:
    # Incluir los datos en el prompt
    prompt = f"""Aquí tienes unos datos de ventas:

{df.to_string()}

Pregunta del usuario: {pregunta}

Responde de forma concisa basándote en los datos."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    st.write(response.choices[0].message.content)

