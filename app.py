import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai
import re
import textwrap
from IPython.display import display, Markdown

# TERMINATOR

error_flag = False  # Global variable to track error display

def clean_text(text):
    # Clean punctuation and special characters using regular expressions
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

def translate_text(text, target_language='en'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translation = translator.translate(text)
    return translation

def generate_response(cleaned_input, model):
    global error_flag  # Use the global error_flag variable

    try:
        # Generate response using the model
        response = model.generate_content(cleaned_input, stream=True)

        # Display the generated response
        full_response = ""
        for chunk in response:
            full_response += chunk.text

        # Translate the response to Spanish without modifying it
        translated_output = translate_text(full_response, target_language='es')

        return translated_output

    except Exception as e:
        error_message = str(e)
        if "text must be a valid text with maximum 5000 character" in error_message and not error_flag:
            error_response = ("La pregunta que está realizando puede que vaya en contra de las políticas de Google Bard e INIF. "
                              "Por favor, reformule su pregunta sin temas no permitidos o pregunte algo diferente. "
                              "Para más información consulte: https://policies.google.com/terms/generative-ai/use-policy "
                              "o www.inif.com.co/laura-chatbot/use-policy")
            st.error(error_response)
            error_flag = True  # Set the error_flag to True after displaying the error message
            return error_response
        else:
            error_response = f"Error: {error_message}\nDisculpa, soy una inteligencia artificial que aún se encuentra en desarrollo y está en fase alfa. En este momento no puedo responder a tu pregunta adecuadamente, pero en el futuro seré capaz de hacerlo."
            st.error(error_response)
            return error_response

def main():
    st.title("Chatbot INIF - TERMINATOR")
    genai.configure(api_key='y')  # Replace with your Gemini API key

    # Choose the Gemini model
    model = genai.GenerativeModel('gemini-pro')

    st.write("Bienvenido al Chatbot informativo del Instituto Nacional de Investigación y Prevención del Fraude (INIF).")

    # User input
    user_input = st.text_input("Pregunta:")

    if st.button("Obtener Respuesta"):
        # Translate the question to English
        translated_input = translate_text(user_input, target_language='en')

        # Clean the translated text of special characters
        cleaned_input = clean_text(translated_input)

        # Exit if the cleaned text is empty
        if not cleaned_input:
            st.warning("Texto ingresado no válido. Inténtalo de nuevo.")
            st.stop()

        # Additional information about INIF
        additional_info = (
            "Trabajamos para empresarios y colaboradores de cualquier industria que buscan combatir el fraude que impacta negativamente la reputación y la economía de sus organizaciones y del país.\n"
            "Somos una empresa privada que trabaja con la industria bancaria y aseguradora."
        )

        # Add the command to act as an INIF informative chatbot
        bot_command = (
            "I am an informative data analyst chatbot named TERMINATOR, working for the National Institute of Fraud Research and Prevention (INIF), dedicated to fraud prevention and mitigation. "
            "If you have questions related to fraud or prevention, feel free to ask. For inquiries about other topics, I'll redirect you to the fraud prevention context."
            f"\n\n{additional_info}"
            "\n\nContact Information for INIF:"
            "\nPhone: +57 317 638 94 71"
            "\nEmail: atencionalcliente@inif.com.co"
            "\n\nOur Mission:"
            "\nTo be the most reliable engine of knowledge, research, and information in Colombia, capable of preventing and combating fraud through synergy between our team and companies."
            "\n\nOur Vision:"
            "\nTo lead the construction of a more honest culture, allowing us to progress as a society."
        )

        # Generate the response
        translated_output = generate_response(bot_command + cleaned_input, model)

        # Display the generated response in green or red based on the content
        if "La pregunta que está realizando puede que vaya en contra de las políticas de Google Bard e INIF." in translated_output:
            st.error(translated_output)
        else:
            st.success(translated_output)

if __name__ == "__main__":
    main()
