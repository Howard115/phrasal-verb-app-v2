import streamlit as st
import requests

is_authenticated = 'token' in st.context.cookies

# Add at the beginning of the file
if not is_authenticated:
    st.error("Please log in to view your favorite stories")
    st.stop()

class APIHandler:
    BASE_URL = "http://localhost:8000"

    @staticmethod
    def get_favorites():
        return requests.get(
            f"{APIHandler.BASE_URL}/phrasal-verbs/favorites",
            cookies=st.context.cookies
        )

# Add custom CSS
st.markdown("""
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
""", unsafe_allow_html=True)

# Fetch and display favorites automatically
response = APIHandler.get_favorites()
if response.status_code == 200:
    favorites = response.json()
    for favorite in favorites:
        with st.expander(f"Favorite Story {favorite['id']}"):
            st.markdown('<div class="pv-title">Phrasal Verbs:</div>', unsafe_allow_html=True)
            for pv in favorite['phrasal_verbs']:
                st.markdown(f"""
                    <div class="pv-item">
                        <strong>{pv['phrasal_verb']}</strong>: {pv['meaning']}
                        <div class="pv-example">Example: {pv['example']}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('**Story:**', unsafe_allow_html=True)
            # Convert markdown bold syntax to HTML span with custom class
            story_text = favorite['story'].replace('**', '<span class="highlighted-pv">', 1)
            while '**' in story_text:
                story_text = story_text.replace('**', '</span>', 1)
                if '**' in story_text:
                    story_text = story_text.replace('**', '<span class="highlighted-pv">', 1)
            st.markdown(story_text, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Failed to fetch favorites")
    