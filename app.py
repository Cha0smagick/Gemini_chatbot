import streamlit as st
import google.generativeai as genai

# Inicializar Streamlit
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

# Configurar la API key de Gemini
genai.configure(api_key='your_gemini_api_key')  # Reemplazar con tu clave de API de Gemini

# Seleccionar el modelo Gemini
select_model = st.sidebar.selectbox("Selecciona el modelo", ["gemini-pro", "gemini-pro-vision"])

# Inicializar la sesión de chat
chat = genai.GenerativeModel(select_model).start_chat(history=[])

# Definir función para obtener respuesta del modelo Gemini
def get_response(messages):
    response = chat.send_message(messages, stream=True)
    return response

# Interfaz de usuario Streamlit
st.title("Gemini Chatbot")
st.sidebar.title("Configuración de Gemini")

# Historial del chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

messages = st.session_state["messages"]

# Mostrar mensajes del historial
if messages:
    for message in messages:
        role, parts = message.values()
        st.chat_message(role.lower()).markdown(parts[0])

# Entrada del usuario
user_input = st.text_input("Tú:", key="user_input")

# Enviar mensaje del usuario al modelo Gemini
if st.button("Enviar"):
    if user_input:
        messages.append({"role": "user", "parts": [user_input]})
        response = get_response(user_input)

        # Mostrar respuesta del modelo solo una vez
        res_text = ""
        for chunk in response:
            res_text += chunk.text
        st.chat_message("assistant").markdown(res_text)

        messages.append({"role": "model", "parts": [res_text]})

# Actualizar historial de mensajes en la sesión de Streamlit
st.session_state["messages"] = messages
