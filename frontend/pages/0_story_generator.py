import streamlit as st
from utils import SessionState, APIHandler, UI
import re

st.set_page_config(page_title="Story Generator", page_icon="📝", layout="wide")

# Add custom CSS styling to match favorite stories page
st.markdown(
    """
<style>
.pv-title {
    color: #0f52ba;
    font-size: 18px;
    margin-bottom: 10px;
}
.pv-item {
    margin: 10px 0;
    padding-left: 15px;
    border-left: 3px solid #0f52ba;
}
.pv-example {
    color: #666;
    font-style: italic;
    margin-left: 15px;
}
.highlighted-pv {
    color: #0f52ba;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)


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


def highlight_uppercase_words(text):
    return re.sub(r'\b(?!I\b)[A-Z]+\b', lambda m: f'<span style="color: #0f52ba;">{m.group(0).lower()}</span>', text)


SessionState.init()
UI.render_auth_sidebar()

st.title("📝 Story Generator")
st.write("Generate creative stories using random phrasal verbs!")

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
                    <strong>{pv['phrasal_verb']}</strong>: {pv['meaning']}
                    <div class="pv-example">Example: {example}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.button(
    "Generate Story",
    on_click=generate_story,
    disabled=not all(st.session_state.phrasal_verbs),
)

if st.session_state.story:
    st.write("**Generated Story:**")
    # Convert markdown bold syntax to HTML span with custom class
    story_text = st.session_state.story.replace("**", '<span class="highlighted-pv">', 1)
    while "**" in story_text:
        story_text = story_text.replace("**", "</span>", 1)
        if "**" in story_text:
            story_text = story_text.replace("**", '<span class="highlighted-pv">', 1)
    st.markdown(story_text, unsafe_allow_html=True)
    
    st.button(
        "Save to Favorites", on_click=save_favorite, disabled=not st.session_state.story
    )

st.write(st.session_state.phrasal_verbs)