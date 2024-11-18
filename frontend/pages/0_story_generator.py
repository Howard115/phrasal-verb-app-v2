import streamlit as st
from utils import SessionState, APIHandler, UI

st.set_page_config(page_title="Story Generator", page_icon="📝", layout="wide")


def get_random_phrasal_verb(index: int):
    st.session_state.phrasal_verbs[index] = APIHandler.get_random_phrasal_verb()
    st.session_state.story = None


def generate_story():
    response = APIHandler.generate_story(st.session_state.phrasal_verbs)
    if response.status_code == 200:
        st.session_state.story = response.json().get("story")
    else:
        st.error(
            "Failed to generate story. Make sure you have stored your OpenAI API key."
        )


def save_favorite():
    response = APIHandler.save_favorite_story(
        st.session_state.phrasal_verbs, st.session_state.story
    )
    if response.status_code == 200:
        st.success("Story saved to favorites!")
    else:
        st.error("Failed to save story to favorites")


SessionState.init()
UI.render_auth_sidebar()

st.title("📝 Story Generator")
st.write("Generate creative stories using random phrasal verbs!")

columns = st.columns(3)
for i, col in enumerate(columns):
    with col:
        st.button(f"Phrasal Verb {i+1}", on_click=get_random_phrasal_verb, args=(i,))
        UI.display_phrasal_verb_entry(st.session_state.phrasal_verbs[i])

st.button(
    "Generate Story",
    on_click=generate_story,
    disabled=not all(st.session_state.phrasal_verbs),
)

if st.session_state.story:
    st.write("**Generated Story:**")
    st.write(st.session_state.story)
    st.button(
        "Save to Favorites", on_click=save_favorite, disabled=not st.session_state.story
    )
