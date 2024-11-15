import streamlit as st
import requests
from datetime import datetime
import jwt

# Initialize token in session state if not present
if 'token' not in st.session_state:
    st.session_state.token = None

# Check if token is in query parameters and store it
if 'token' in st.query_params:
    st.session_state.token = st.query_params['token']
    # Remove token from URL to avoid exposing it
    st.query_params.clear()

# Check authentication state from session
is_authenticated = st.session_state.token is not None

st.sidebar.title("Login")
if not is_authenticated:
    login_button = st.sidebar.button("Login with Google")
    if login_button:
        # Redirect to backend login endpoint
        st.markdown(f'<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/login">', unsafe_allow_html=True)
else:
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        # Clear token from session state
        st.session_state.token = None
        # Redirect to backend logout endpoint 
        st.markdown(f'<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/logout">', unsafe_allow_html=True)
print(st.session_state.token)


def get_random_phrasal_verb():
    headers = {}
    if st.session_state.token:
        headers['Authorization'] = f'Bearer {st.session_state.token}'
    response = requests.get("http://localhost:8000/phrasal-verbs/random", headers=headers)
    return response.json()

# Initialize phrasal_verbs in session state if it doesn't exist
if 'phrasal_verbs' not in st.session_state:
    st.session_state.phrasal_verbs = {
        'data1': None,
        'data2': None,
        'data3': None
    }

# Create three columns
col1, col2, col3 = st.columns(3)

# Add buttons and display logic for each column
with col1:
    button1 = st.button("Phrasal Verb 1")
    if button1:
        st.session_state.phrasal_verbs['data1'] = get_random_phrasal_verb()
    if st.session_state.phrasal_verbs['data1']:
        st.write(f"**Phrasal Verb:** {st.session_state.phrasal_verbs['data1']['phrasal_verb']}")
        st.write(f"**Meaning:** {st.session_state.phrasal_verbs['data1']['meaning']}")
        st.write(f"**Example:** {st.session_state.phrasal_verbs['data1']['example']}")

with col2:
    button2 = st.button("Phrasal Verb 2")
    if button2:
        st.session_state.phrasal_verbs['data2'] = get_random_phrasal_verb()
    if st.session_state.phrasal_verbs['data2']:
        st.write(f"**Phrasal Verb:** {st.session_state.phrasal_verbs['data2']['phrasal_verb']}")
        st.write(f"**Meaning:** {st.session_state.phrasal_verbs['data2']['meaning']}")
        st.write(f"**Example:** {st.session_state.phrasal_verbs['data2']['example']}")

with col3:
    button3 = st.button("Phrasal Verb 3")
    if button3:
        st.session_state.phrasal_verbs['data3'] = get_random_phrasal_verb()
    if st.session_state.phrasal_verbs['data3']:
        st.write(f"**Phrasal Verb:** {st.session_state.phrasal_verbs['data3']['phrasal_verb']}")
        st.write(f"**Meaning:** {st.session_state.phrasal_verbs['data3']['meaning']}")
        st.write(f"**Example:** {st.session_state.phrasal_verbs['data3']['example']}")



