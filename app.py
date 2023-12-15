import streamlit as st
import re
import google.generativeai as genai
from IPython.display import display, Markdown

# TERMINATOR

error_flag = False  # Global variable to track error display

def clean_text(text):
    # Clean punctuation and special characters using regular expressions
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

def generate_response(cleaned_input, model):
    global error_flag  # Use the global error_flag variable

    try:
        # Generate response using the model
        response = model.generate_content(cleaned_input, stream=True)

        # Display the generated response
        full_response = ""
        for chunk in response:
            full_response += chunk.text

        return full_response

    except Exception as e:
        error_message = str(e)
        if "text must be a valid text with maximum 5000 character" in error_message and not error_flag:
            error_response = ("The question you are asking may go against Google GEMINI policies: WiseOracle"
                              "Please reformulate your question without forbidden topics or ask something else. "
                              "For more information, see: https://policies.google.com/terms/generative-ai/use-policy "
                             )
            st.error(error_response)
            error_flag = True  # Set the error_flag to True after displaying the error message
            return error_response
        else:
            error_response = f"Error: {error_message}\nSorry, I am an artificial intelligence that is still in development and is in alpha phase. At the moment, I cannot answer your question properly, but in the future, I will be able to do so."
            st.error(error_response)
            return error_response

def main():
    st.title("WiseOracle")
    genai.configure(api_key='AIzaSyCezVerubEzQc9JHz3V8hofpAlSIJXGxFQ')  # Replace with your Gemini API key

    # Choose the Gemini model
    model = genai.GenerativeModel('gemini-pro')

    st.write("Ask Anything! Powered by Google GEMINI")

    # User input
    user_input = st.text_input("Question:")

    if st.button("Get answer"):
        # Clean the user input of special characters
        cleaned_input = clean_text(user_input)

        # Exit if the cleaned text is empty
        if not cleaned_input:
            st.warning("Invalid input. Please try again.")
            st.stop()

        # Additional information about INIF
        additional_info = (
            "If you want to collaborate with the project, subscribe on Hugging Face or GitHub\n"
            "If you want to donate, please donate in Bitcoin: 3KcF1yrY44smTJpVW68m8dw8q64kPtzvtX"
        )

        # Add the command to act as an INIF informative chatbot
        bot_command = (
            "I am an informative data analyst chatbot named WiseOracle, working for you as an assistant. "
            "If you have questions about anything, feel free to ask."
            f"\n\n{additional_info}"
        )

        # Generate the response
        full_response = generate_response(bot_command + cleaned_input, model)

        # Display the generated response
        st.success(full_response)

if __name__ == "__main__":
    main()
