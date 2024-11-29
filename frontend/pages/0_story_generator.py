import streamlit as st
from utils import SessionState, APIHandler, UI
import re

st.set_page_config(page_title="Story Generator", page_icon="📝", layout="wide")

def highlight_uppercase_words(text):
    return re.sub(r'\b(?!I\b)[A-Z]+\b', lambda m: f'<span style="color: #0f52ba;">{m.group(0).lower()}</span>', text)

def get_random_phrasal_verb(index: int):
    st.session_state.phrasal_verbs[index] = APIHandler.get_random_phrasal_verb()
    st.session_state.story = None

def generate_story():
    response = APIHandler.generate_story(st.session_state.phrasal_verbs)
    if response.status_code == 200:
        st.session_state.story = response.json().get("story")
    else:
        st.error("Failed to generate story. Make sure you have stored your OpenAI API key.")

def save_favorite():
    response = APIHandler.save_favorite_story(
        st.session_state.phrasal_verbs, st.session_state.story
    )
    if response.status_code == 200:
        st.success("Story saved to favorites!")
    else:
        st.error("Failed to save story to favorites")

def main():
    SessionState.init()
    UI.render_auth_sidebar()
    UI.apply_common_styles()

    st.title("📝 Story Generator")
    st.write("Generate creative stories using random phrasal verbs!")

    # Display phrasal verb buttons and entries
    columns = st.columns(3)
    for i, col in enumerate(columns):
        with col:
            st.button(f"Phrasal Verb {i+1}", on_click=get_random_phrasal_verb, args=(i,))
            if st.session_state.phrasal_verbs[i]:
                pv = st.session_state.phrasal_verbs[i]
                example = highlight_uppercase_words(pv['example'])
                st.markdown(
                    f"""
                    <div class="pv-item">
                        <strong>{pv['phrasal_verb']}</strong><span style="color : #EFFF4B"> : </span> {pv['meaning']}
                        <div class="pv-example">Example<span style="color: #EFFF4B"> : </span> {example}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Generate story button
    st.button(
        "Generate Story",
        on_click=generate_story,
        disabled=not all(st.session_state.phrasal_verbs),
    )

    # Display generated story
    if st.session_state.story:
        st.write("**Generated Story:**")
        story_text = UI.format_story_text(st.session_state.story)
        st.markdown(story_text, unsafe_allow_html=True)
        
        st.button(
            "Save to Favorites", 
            on_click=save_favorite, 
            disabled=not st.session_state.story
        )

if __name__ == "__main__":
    main()
