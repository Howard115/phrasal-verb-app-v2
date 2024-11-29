import streamlit as st
from utils import APIHandler, UI, cookie_controller
import re

st.set_page_config(page_title="Favorite Stories", page_icon="⭐", layout="wide")

def highlight_uppercase_words(text):
    return re.sub(r'\b(?!I\b)[A-Z]+\b', lambda m: f'<span class="blue-word">{m.group(0).lower()}</span>', text)

def delete_favorite(favorite_id: int):
    response = APIHandler.delete_favorite(favorite_id)
    if response.status_code == 200:
        st.session_state.refresh_favorites = True
    else:
        st.error("Failed to delete story")

def display_favorite_story(favorite):
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        expander = st.expander(f"Favorite Story {favorite['id']}")
    with col2:
        st.button(
            "🗑️",
            key=f"delete_{favorite['id']}",
            on_click=delete_favorite,
            args=(favorite["id"],),
            help="Delete this story",
        )

    with expander:
        st.markdown('<div class="pv-title">Phrasal Verbs:</div>', unsafe_allow_html=True)
        for pv in favorite["phrasal_verbs"]:
            st.markdown(
                f"""
                <div class="pv-item">
                    <strong>{pv['phrasal_verb']}</strong><span style="color : #EFFF4B"> : </span> {pv['meaning']}
                    <div class="pv-example">Example<span style="color: #EFFF4B"> : </span> {highlight_uppercase_words(pv['example'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("**Story:**", unsafe_allow_html=True)
        story_text = UI.format_story_text(favorite["story"])
        st.markdown(story_text, unsafe_allow_html=True)

def main():
    # Initialize session state for refresh tracking
    if "refresh_favorites" not in st.session_state:
        st.session_state.refresh_favorites = False

    # Render auth sidebar and apply styles
    UI.render_auth_sidebar()
    UI.apply_common_styles()

    is_authenticated = "token" in cookie_controller.getAll()

    if not is_authenticated:
        st.error("Please log in to view your favorite stories")
        st.stop()

    st.title("⭐ My Favorite Stories")

    # Check if we need to refresh after a deletion
    if st.session_state.refresh_favorites:
        st.session_state.refresh_favorites = False
        st.rerun()

    # Fetch and display favorites
    response = APIHandler.get_favorites()
    if response.status_code == 200:
        favorites = response.json()
        for favorite in favorites:
            display_favorite_story(favorite)
    else:
        st.error("Failed to fetch favorites")

if __name__ == "__main__":
    main()
