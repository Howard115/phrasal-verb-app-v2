import streamlit as st
import requests
# Authentication handling
def handle_auth():
    is_authenticated = 'token' in st.context.cookies
    st.sidebar.title("Login")
    
    if not is_authenticated:
        if st.sidebar.button("Login with Google"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/login">', 
                       unsafe_allow_html=True)
    else:
        if st.sidebar.button("Logout"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/logout">', 
                       unsafe_allow_html=True)

def get_random_phrasal_verb():
    response = requests.get("http://localhost:8000/phrasal-verbs/random")
    return response.json()

def display_phrasal_verb(data):
    if data:
        st.write(f"**Phrasal Verb:** {data['phrasal_verb']}")
        st.write(f"**Meaning:** {data['meaning']}")
        st.write(f"**Example:** {data['example']}")

# Initialize session state
if 'phrasal_verbs' not in st.session_state:
    st.session_state.phrasal_verbs = {f'data{i+1}': None for i in range(3)}

# Handle authentication
handle_auth()

# Create columns and display phrasal verbs
columns = st.columns(3)
for i, col in enumerate(columns, 1):
    with col:
        if st.button(f"Phrasal Verb {i}"):
            st.session_state.phrasal_verbs[f'data{i}'] = get_random_phrasal_verb()
        display_phrasal_verb(st.session_state.phrasal_verbs[f'data{i}'])
        