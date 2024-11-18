import streamlit as st
import requests


# State Management
class SessionState:
    @staticmethod
    def init():
        if "phrasal_verbs" not in st.session_state:
            st.session_state.phrasal_verbs = [None] * 3
        if "story" not in st.session_state:
            st.session_state.story = None


# API Handlers
class APIHandler:
    BASE_URL = "http://localhost:8000"

    @staticmethod
    def save_api_key(api_key: str):
        response = requests.post(
            f"{APIHandler.BASE_URL}/api-keys",
            json={"api_key": api_key},
            cookies=st.context.cookies,
        )
        return response

    @staticmethod
    def delete_api_key():
        return requests.delete(
            f"{APIHandler.BASE_URL}/api-keys", cookies=st.context.cookies
        )

    @staticmethod
    def generate_story(phrasal_verbs):
        return requests.post(
            f"{APIHandler.BASE_URL}/phrasal-verbs/generate-story",
            json={"phrasal_verbs": phrasal_verbs},
            cookies=st.context.cookies,
        )

    @staticmethod
    def get_random_phrasal_verb():
        response = requests.get(f"{APIHandler.BASE_URL}/phrasal-verbs/random")
        return response.json()

    @staticmethod
    def save_favorite_story(phrasal_verbs, story):
        return requests.post(
            f"{APIHandler.BASE_URL}/phrasal-verbs/favorites",
            json={"phrasal_verbs": phrasal_verbs, "story": story},
            cookies=st.context.cookies,
        )

    @staticmethod
    def get_favorites():
        return requests.get(
            f"{APIHandler.BASE_URL}/phrasal-verbs/favorites", cookies=st.context.cookies
        )

    @staticmethod
    def delete_favorite(favorite_id: int):
        return requests.delete(
            f"{APIHandler.BASE_URL}/phrasal-verbs/favorites/{favorite_id}",
            cookies=st.context.cookies,
        )


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
    def render_auth_sidebar():
        with st.sidebar:
            st.title("Login")
            is_authenticated = "token" in st.context.cookies

            if not is_authenticated:
                st.button(
                    "Login with Google",
                    on_click=lambda: st.markdown(
                        '<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/login">',
                        unsafe_allow_html=True,
                    ),
                )
            else:
                st.button(
                    "Logout",
                    on_click=lambda: st.markdown(
                        '<meta http-equiv="refresh" content="0;url=http://localhost:8000/auth/logout">',
                        unsafe_allow_html=True,
                    ),
                )
