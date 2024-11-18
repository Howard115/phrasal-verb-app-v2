import streamlit as st
from utils import SessionState, UI

st.set_page_config(
    page_title="Phrasal Verb Learning App", page_icon="📚", layout="wide"
)


SessionState.init()
UI.render_auth_sidebar()

st.title("📚 Welcome to Phrasal Verb Learning App")

st.markdown(
    """
Welcome to your interactive phrasal verb learning journey! This app helps you master English phrasal verbs through creative storytelling.

### 📝 Available Features:

1. **Story Generator**: Create unique stories using random phrasal verbs
2. **Favorite Stories**: Review and manage your saved stories
3. **Settings**: Configure your API key and preferences

Choose a section from the sidebar to get started!
"""
)

with st.expander("ℹ️ How to use this app"):
    st.markdown(
        """
    1. Start with the Story Generator to practice with random phrasal verbs
    2. Save interesting stories to your favorites for later review
    3. Configure your API key in the settings if needed
    """
    )
