# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
from settings import settings
from pathlib import Path 
import os 

if settings.MODE == "debug":
    HOST = 'localhost'
else:
    HOST = 'backend'

def main_commandline():

    st.markdown("""
    ###### Command lists    
    - `set_user_id <user_id>`: Set the user ID to `<user_id>`.
    - `upload_file: Start uploading the file.
    - `query <query_info>`: Upload the file located at `<file_path>`.
    """)

    ## Command line 
    st.markdown("--- ")
    if not "file_upload_visibility" in st.session_state:
        file_upload_visibility = False
    else:
        file_upload_visibility = True
        file_upload_visibility = st.session_state["file_upload_visibility"]

    # st.write(file_upload_visibility)
    my_expander = st.expander("Expander", expanded=file_upload_visibility)
    with my_expander:
        streamlit_pdf = st.file_uploader("Upload a PDF user manual", type=["pdf"])
    command_line = st.text_input("Command line")
    

    command_data = command_line.split(" ")
    if len(command_data) == 0:
        st.write("Please enter commands set_user_id, upload_file, reply")
    
    if streamlit_pdf is not None:
        # For demonstration, assuming server expects multipart/form-data
        files = {'file': (streamlit_pdf.name, streamlit_pdf, 'application/pdf')}
        response = requests.post(f"http://{HOST}:{settings.FRONENT_PORT}/upload_file", files=files)
        if response.status_code == 200:
            st.success("File successfully uploaded to the server.")
            st.session_state["filename"] = streamlit_pdf.name
        else:
            st.error("Failed to upload the file.")

    if st.button("Run"):
        if "upload_file" in command_line:
            st.session_state["file_upload_visibility"] = True
            st.session_state["streamlit_pdf"] = streamlit_pdf
            st.rerun()
        elif "set_user_id" in command_line:
            user_id = command_data[-1]
            st.session_state["user_id"] = user_id
            st.write(f"User ID {user_id} has been set")
        elif "query" in command_line:
            if "filename" in st.session_state:
                filename = st.session_state["filename"]
            else:
                st.write("Please upload file first")
                return
            if "user_id" in st.session_state:
                user_id = st.session_state["user_id"]
            else:
                st.write("Use default user_id 1")
                user_id = "1"
                st.session_state["user_id"] = user_id

            user_input = command_line.split("query")
            data = {
               'user_id': (None, user_id),
               'prompt': (None, user_input[1]),
               'pdf_path': (None, filename)
            }
            response, user_history = send_to_flask(data)
            st.write(f"{response}")


def send_to_flask(data):
    flask_url = f'http://{HOST}:{settings.FRONENT_PORT}/chat'
    try:
        response = requests.post(flask_url, files=data)
        if response.status_code == 200:
            print("Response received successfully:")
            return response.json()["generated_response"], response.json()["user_history"]
        else:
            print("Error: Failed to receive response. Status code:", response.status_code)
            return "I am not sure", "I am not sure"
    except requests.RequestException as e:
        return f"Error communicating with Flask: {e}"

if __name__ == "__main__":
    main()