import streamlit as st
import requests

# State Management
class SessionState:
    @staticmethod
    def init():
        if 'phrasal_verbs' not in st.session_state:
            st.session_state.phrasal_verbs = [None] * 3
        if 'story' not in st.session_state:
            st.session_state.story = None

# API Handlers
class APIHandler:
    BASE_URL = "http://localhost:8000"

    @staticmethod
    def save_api_key(api_key: str):
        response = requests.post(
            f"{APIHandler.BASE_URL}/api-keys",
            json={"api_key": api_key},
            cookies=st.context.cookies
        )
        return response

    @staticmethod
    def delete_api_key():
        return requests.delete(
            f"{APIHandler.BASE_URL}/api-keys",
            cookies=st.context.cookies
        )

    @staticmethod
    def generate_story(phrasal_verbs):
        return requests.post(
            f"{APIHandler.BASE_URL}/phrasal-verbs/generate-story",
            json={"phrasal_verbs": phrasal_verbs},
            cookies=st.context.cookies
        )

    @staticmethod
    def get_random_phrasal_verb():
        response = requests.get(f"{APIHandler.BASE_URL}/phrasal-verbs/random")
        return response.json()

    @staticmethod
    def save_favorite_story(phrasal_verbs, story):
        return requests.post(
            f"{APIHandler.BASE_URL}/phrasal-verbs/favorites",
            json={
                "phrasal_verbs": phrasal_verbs,
                "story": story
            },
            cookies=st.context.cookies
        )

# Callbacks
class Callbacks:
    @staticmethod
    def login():
        st.markdown('<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/login">', 
                   unsafe_allow_html=True)

    @staticmethod
    def logout():
        st.markdown('<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/logout">', 
                   unsafe_allow_html=True)

    @staticmethod
    def save_api_key():
        api_key = st.session_state.api_key_input
        response = APIHandler.save_api_key(api_key)
        if response.status_code == 200:
            st.sidebar.success(response.json().get("message", "API key saved successfully"))
        else:
            st.sidebar.error("Failed to save API key")

    @staticmethod
    def delete_api_key():
        response = APIHandler.delete_api_key()
        if response.status_code == 200:
            st.sidebar.success(response.json().get("message", "API key deleted successfully"))
        else:
            st.sidebar.error("Failed to delete API key")

    @staticmethod
    def generate_story():
        response = APIHandler.generate_story(st.session_state.phrasal_verbs)
        if response.status_code == 200:
            st.session_state.story = response.json().get("story")
        else:
            st.error("Failed to generate story. Make sure you have stored your OpenAI API key.")

    @staticmethod
    def get_random_phrasal_verb(index: int):
        st.session_state.phrasal_verbs[index] = APIHandler.get_random_phrasal_verb()
        st.session_state.story = None

    @staticmethod
    def save_favorite():
        response = APIHandler.save_favorite_story(
            st.session_state.phrasal_verbs,
            st.session_state.story
        )
        if response.status_code == 200:
            st.success("Story saved to favorites!")
        else:
            st.error("Failed to save story to favorites")

# UI Components
class UI:
    @staticmethod
    def display_phrasal_verb_entry(phrasal_verb_entry):
        if not phrasal_verb_entry:
            return
        st.write(f"**Phrasal Verb:** {phrasal_verb_entry.get('phrasal_verb', '')}")
        st.write(f"**Meaning:** {phrasal_verb_entry.get('meaning', '')}")
        st.write(f"**Example:** {phrasal_verb_entry.get('example', '')}")

    @staticmethod
    def render_sidebar():
        with st.sidebar:
            st.title("Login")
            is_authenticated = 'token' in st.context.cookies
            
            if not is_authenticated:
                st.button("Login with Google", on_click=Callbacks.login)
            else:
                st.button("Logout", on_click=Callbacks.logout)
            
            st.title("OpenAI API Key")
            st.text_input("Enter your OpenAI API key", type="password", key="api_key_input")
            st.button("Save API Key", on_click=Callbacks.save_api_key)
            st.button("Delete API Key", on_click=Callbacks.delete_api_key)

    @staticmethod
    def render_main_content():
        columns = st.columns(3)
        for i, col in enumerate(columns):
            with col:
                st.button(f"Phrasal Verb {i+1}", 
                         on_click=Callbacks.get_random_phrasal_verb, 
                         args=(i,))
                UI.display_phrasal_verb_entry(st.session_state.phrasal_verbs[i])
        
        st.button("Generate Story", 
                 on_click=Callbacks.generate_story,
                 disabled=not all(st.session_state.phrasal_verbs))
        
        if st.session_state.story:
            st.write("**Generated Story:**")
            st.write(st.session_state.story)
            st.button("Save to Favorites", 
                     on_click=Callbacks.save_favorite,
                     disabled=not st.session_state.story)

def main():
    SessionState.init()
    UI.render_sidebar()
    UI.render_main_content()

if __name__ == "__main__":
    main()
