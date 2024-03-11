# streamlit_app.py

import streamlit as st
import requests
import pandas as pd

DEBUG = True
if DEBUG:
    HOST = 'localhost'
else:
    HOST = 'backend'

def main():
    

    # For upload file pdf to server though api /upload_file which is defined in server/simple_server.py
    st.title("File Upload and Text Input")
    user_id = st.text_input("User ID")
    streamlit_pdf = st.file_uploader("Upload a CSV file", type=["pdf"])
    if streamlit_pdf is not None:
        # For demonstration, assuming server expects multipart/form-data
        files = {'file': (streamlit_pdf.name, streamlit_pdf, 'application/pdf')}
        response = requests.post(f"http://{HOST}:5000/upload_file", files=files)

        if response.status_code == 200:
            st.success("File successfully uploaded to the server.")
        else:
            st.error("Failed to upload the file.")

    # Text input
    user_input = st.text_input("Enter question")

    ### Todo
    # pdf_path = st.text_input("Enter manual path")
    # if st.button("Send to Flask"):
    #     data = {
    #            'prompt': (None, user_input),
    #             'pdf_path': (None, pdf_path)
    #     }
    #     response = send_to_flask(data)
    #     st.write(f"Flask response: {response}")
    
    # Call the langchain to process the information and return response
    if st.button("Query"):
                
        data = {
               'user_id': (None, user_id),
               'prompt': (None, user_input),
                'pdf_path': (None, streamlit_pdf.name)
        }
        response, user_history = send_to_flask(data)
        st.write(f"{response}")

        st.write(f"History of {user_id}:{user_history}")


def send_to_flask(data):
    # Replace with your Flask localhost URL
    # flask_url = 'http://localhost:8686/generate_response'
    # flask_url = 'http://localhost:5000/generate_response'
    # flask_url = 'http://0.0.0.0:5000/generate_response'
    flask_url = f'http://{HOST}:5000/generate_response'

    try:
        # response = requests.post(flask_url, json={"data": data})
        response = requests.post(flask_url, files=data)

        if response.status_code == 200:
            print("Response received successfully:")
            # print(response.json())
            return response.json()["generated_response"], response.json()["user_history"]
        else:
            print("Error: Failed to receive response. Status code:", response.status_code)
            return "I am not sure", "I am not sure"
    except requests.RequestException as e:
        return f"Error communicating with Flask: {e}"


if __name__ == "__main__":
    main()