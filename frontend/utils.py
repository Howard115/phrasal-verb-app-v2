import streamlit as st
import requests
from streamlit_cookies_controller import CookieController
import os
from dotenv import load_dotenv

load_dotenv()

cookie_controller = CookieController()

BACKEND_URL = os.getenv("BACKEND_URL", "https://phr-backend.hnd1.zeabur.app")


# State Management
class SessionState:
    @staticmethod
    def init():
        if "phrasal_verbs" not in st.session_state:
            st.session_state.phrasal_verbs = [None] * 3
        if "story" not in st.session_state:
            st.session_state.story = None
        if "token" in st.query_params:
            cookie_controller.set("token", st.query_params["token"])
            st.query_params.clear()
            


# API Handlers
class APIHandler:
    BACKEND_URL = BACKEND_URL

    @staticmethod
    def save_api_key(api_key: str):
        response = requests.post(
            f"{APIHandler.BACKEND_URL}/api-keys",
            json={"api_key": api_key},
            cookies=cookie_controller.getAll(),
        )
        return response

    @staticmethod
    def delete_api_key():
        return requests.delete(
            f"{APIHandler.BACKEND_URL}/api-keys", cookies=cookie_controller.getAll()
        )

    @staticmethod
    def generate_story(phrasal_verbs):
        return requests.post(
            f"{APIHandler.BACKEND_URL}/phrasal-verbs/generate-story",
            json={"phrasal_verbs": phrasal_verbs},
            cookies=cookie_controller.getAll()
        )

    @staticmethod
    def get_random_phrasal_verb():
        response = requests.get(f"{APIHandler.BACKEND_URL}/phrasal-verbs/random")
        return response.json()

    @staticmethod
    def save_favorite_story(phrasal_verbs, story):
        return requests.post(
            f"{APIHandler.BACKEND_URL}/phrasal-verbs/favorites",
            json={"phrasal_verbs": phrasal_verbs, "story": story},
            cookies=cookie_controller.getAll(),
        )

    @staticmethod
    def get_favorites():
        return requests.get(
            f"{APIHandler.BACKEND_URL}/phrasal-verbs/favorites", cookies=cookie_controller.getAll()
        )

    @staticmethod
    def delete_favorite(favorite_id: int):
        return requests.delete(
            f"{APIHandler.BACKEND_URL}/phrasal-verbs/favorites/{favorite_id}",
            cookies=cookie_controller.getAll(),
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
            is_authenticated = "token" in cookie_controller.getAll()

            if not is_authenticated:
                st.button(
                    "Login with Google",
                    on_click=lambda: st.markdown(
                        f'<meta http-equiv="refresh" content="0;url={BACKEND_URL}/auth/login">',
                        unsafe_allow_html=True,
                    ),
                )
            else:
                def handle_logout():
                    cookie_controller.remove("token")
                    st.markdown(
                        f'<meta http-equiv="refresh" content="0;url={BACKEND_URL}/auth/logout">',
                        unsafe_allow_html=True,
                    )
                
                st.button("Logout", on_click=handle_logout)
