import streamlit as st
from PIL import Image
import textwrap
import google.generativeai as genai

# Function to display formatted Markdown text
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to generate content using Gemini API
def generate_gemini_content(prompt, model_name='gemini-pro-vision', image=None):
    model = genai.GenerativeModel(model_name)
    if not image:
        st.warning("Por favor, agrega una imagen para usar el modelo gemini-pro-vision.")
        return None

    response = model.generate_content([prompt, image])
    return response

# Streamlit app
def main():
    st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
    st.title("Gemini Chatbot")
    st.sidebar.title("Configuración de Gemini")

    # Configurar la API key de Gemini (reemplazar con tu clave de API de Gemini)
    genai.configure(api_key='your_google_api_key')

    # Seleccionar el modelo Gemini
    select_model = st.sidebar.selectbox("Selecciona el modelo", ["gemini-pro", "gemini-pro-vision"])

    # Inicializar la sesión de chat
    chat = genai.GenerativeModel(select_model).start_chat(history=[])

    # Definir función para obtener respuesta del modelo Gemini
    def get_response(messages):
        response = chat.send_message(messages, stream=True)
        return response

    # Historial del chat
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    messages = st.session_state["messages"]

    # Mostrar mensajes del historial
    if messages:
        for message in messages:
            role, parts = message.values()
            if role.lower() == "user":
                st.markdown(f"Tú: {parts[0]}")
            elif role.lower() == "model":
                st.markdown(f"Assistant: {to_markdown(parts[0])}")

    # Entrada del usuario
    user_input = st.text_input("Tú:")

    # Enviar mensaje del usuario al modelo Gemini
    if st.button("Enviar"):
        if user_input:
            messages.append({"role": "user", "parts": [user_input]})
            response = get_response(user_input)

            # Mostrar respuesta del modelo solo una vez
            res_text = ""
            for chunk in response:
                res_text += chunk.text

            st.markdown(f"Assistant: {to_markdown(res_text)}")
            messages.append({"role": "model", "parts": [res_text]})

    # Actualizar historial de mensajes en la sesión de Streamlit
    st.session_state["messages"] = messages

    # Set the model to 'gemini-pro-vision'
    model_name = 'gemini-pro-vision'

    # Get user input prompt
    prompt = st.text_area("Ingresa tu mensaje para Gemini Vision Pro:")

    # Get optional image input
    image_file = st.file_uploader("Sube una imagen (si aplica):", type=["jpg", "jpeg", "png"])

    # Display image if provided
    if image_file:
        st.image(image_file, caption="Imagen subida", use_column_width=True)

    # Generate content on button click
    if st.button("Generar Contenido"):
        st.markdown("### Contenido Generado:")
        if not image_file:
            st.warning("Por favor, proporciona una imagen para el modelo gemini-pro-vision.")
        else:
            image = Image.open(image_file)
            response = generate_gemini_content(prompt, model_name=model_name, image=image)

            # Display the generated content in Markdown format if response is available
            if response:
                if response.candidates:
                    parts = response.candidates[0].content.parts
                    generated_text = parts[0].text if parts else "No se generó contenido."
                    st.markdown(to_markdown(generated_text))
                else:
                    st.warning("No se encontraron candidatos en la respuesta.")

if __name__ == "__main__":
    main()
