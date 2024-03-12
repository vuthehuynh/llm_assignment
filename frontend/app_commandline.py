# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
from settings import settings
import os 

if settings.MODE == "debug":
    HOST = 'localhost'
else:
    HOST = 'backend'

def main_commandline():

    st.markdown("""
    ###### Command lists    
    - `set_user_id <user_id>`: Set the user ID to `<user_id>`.
    - `upload_file <file_path>`: Upload the file located at `<file_path>`.
    - `query <query_info>`: Upload the file located at `<file_path>`.
    """)

    ## Command line 
    st.markdown("--- ")
    command_line = st.text_input("Command line")
    

    command_data = command_line.split(" ")
    if len(command_data) == 0:
        st.write("Please enter commands set_user_id, upload_file, reply")
    # st.write(f"Processing {command_line}")
    if st.button("Run"):
        if "upload_file" in command_line:
            file_path = command_data[-1]
            if os.path.exists(file_path):
                st.write("File exists")
                with open(file_path, "rb") as f:
                    file_content = f.read()
                filename = os.path.basename(file_path)
                if file_content is not None:
                    files = {'file': (filename, file_content, 'application/pdf')}
                    response = requests.post(f"http://{HOST}:{settings.FRONENT_PORT}/upload_file", files=files)
                    st.session_state["filename"] = filename
                    if response.status_code == 200:
                        st.success("File successfully uploaded to the server.")
                    else:
                        st.error("Failed to upload the file.")
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

            user_input = command_data[-1]
            data = {
               'user_id': (None, user_id),
               'prompt': (None, user_input),
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