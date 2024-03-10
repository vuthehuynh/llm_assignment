# streamlit_app.py

import streamlit as st
import requests
import pandas as pd

def main():
    st.title("File Upload and Text Input")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded file contents:")
        st.write(df)

    # Text input
    user_input = st.text_input("Enter question")
    pdf_path = st.text_input("Enter manual path")


    if st.button("Send to Flask"):
        data = {
               'prompt': (None, user_input),
                'pdf_path': (None, pdf_path)
        }
        response = send_to_flask(data)
        st.write(f"Flask response: {response}")

def send_to_flask(data):
    # Replace with your Flask backend URL
    # flask_url = 'http://localhost:8686/generate_response'
    # flask_url = 'http://localhost:5000/generate_response'
    # flask_url = 'http://0.0.0.0:5000/generate_response'
    flask_url = 'http://backend:5000/generate_response'

    try:
        # response = requests.post(flask_url, json={"data": data})
        response = requests.post(flask_url, files=data)

        if response.status_code == 200:
            print("Response received successfully:")
            # print(response.json())
            return response.json()["generated_response"]
        else:
            print("Error: Failed to receive response. Status code:", response.status_code)
            return "I am not sure"
    except requests.RequestException as e:
        return f"Error communicating with Flask: {e}"


if __name__ == "__main__":
    main()