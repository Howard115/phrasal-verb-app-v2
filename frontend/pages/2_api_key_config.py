import streamlit as st
from utils import APIHandler, UI

st.set_page_config(
    page_title="API Key Configuration",
    page_icon="🔑",
    layout="wide"
)

# Render auth sidebar
UI.render_auth_sidebar()

# Check authentication status
is_authenticated = 'token' in st.context.cookies

if not is_authenticated:
    st.error("Please login first to access this page")
    st.stop()

st.title("🔑 OpenAI API Key Configuration")
st.write("Configure your OpenAI API key to enable story generation.")

st.text_input("Enter your OpenAI API key", type="password", key="api_key_input")
col1, col2 = st.columns(2)
with col1:
    st.button("Save API Key", on_click=lambda: save_api_key())
with col2:
    st.button("Delete API Key", on_click=lambda: delete_api_key())

def save_api_key():
    api_key = st.session_state.api_key_input
    response = APIHandler.save_api_key(api_key)
    if response.status_code == 200:
        st.success(response.json().get("message", "API key saved successfully"))
    else:
        st.error("Failed to save API key")

def delete_api_key():
    response = APIHandler.delete_api_key()
    if response.status_code == 200:
        st.success(response.json().get("message", "API key deleted successfully"))
    else:
        st.error("Failed to delete API key")