import streamlit as st
from app_webui import main_webui 
from app_commandline import main_commandline
with st.sidebar:
    st.title("Navigation")
    selection = st.radio("", ["Home", "Web UI Mode", "Commandline Mode"])
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if selection == "Home":
    st.title("Home Page")
    st.write("Welcome to the LLM app!")
    st.session_state.page = 'main'
elif selection == "Web UI Mode":
    st.title("Web UI Mode")
    st.session_state.page = 'app_webui'
    main_webui()
elif selection == "Commandline Mode":
    st.title("Commandline Mode")
    st.session_state.page = 'app_commandline'
    main_commandline()