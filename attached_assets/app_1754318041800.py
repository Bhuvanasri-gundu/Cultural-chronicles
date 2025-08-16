"""
Cultural Chronicles - Main Application Module

This is the main entry point for the Cultural Chronicles web application.
It handles navigation, page routing, and core functionality for preserving
India's cultural heritage through digital storytelling.

Author: Cultural Chronicles Team
Date: January 2025
"""

import os
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Set environment configuration
os.environ["STREAMLIT_HOME"] = os.path.abspath(".")

# Set page config
st.set_page_config(
    page_title="Cultural Chronicles - Heritage Archive",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data directories
os.makedirs("data", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Initialize fast cached components for 5-second loading
@st.cache_resource
def initialize_fast_app():
    """Initialize app resources with aggressive caching for ultra-fast loading"""
    from utils.cache_manager import get_fast_data_manager
    
    # Get cached data manager
    data_manager = get_fast_data_manager()
    
    # Load sample data only if needed (cached check)
    if data_manager:
        try:
            stories = data_manager.get_all_stories()
            if stories.empty:
                from sample_data import create_sample_data
                create_sample_data()
        except Exception as e:
            print(f"Sample data loading skipped: {e}")
    
    return data_manager

# Get ultra-fast cached data manager
data_manager = initialize_fast_app()

# Navigation menu
def main():
    """
    Main application function that handles navigation and page routing.
    
    This function sets up the Streamlit page configuration, applies custom CSS styling,
    creates the navigation menu, and routes users to the appropriate page based on
    their selection.
    """
    # Add custom CSS for better styling and consistent theme
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>📚 Cultural Chronicles</h1><p>Preserving India\'s Oral and Cultural Heritage</p></div>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🌟 Navigation")
        selected = option_menu(
            "Heritage Hub",
            ["Home", "Submit Story", "Browse Stories", "Search"],
            icons=["house-heart", "journal-plus", "book-half", "search-heart"],
            menu_icon="gems",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "#FF6B35", "font-size": "20px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#FF6B35"},
            }
        )
    
    if selected == "Home":
        show_home()
    elif selected == "Submit Story":
        from pages.submit_story import show_submit_story
        show_submit_story()
    elif selected == "Browse Stories":
        from pages.browse_stories import show_browse_stories
        show_browse_stories()
    elif selected == "Search":
        show_search()

def show_home():
    st.markdown('<div class="feature-card"><h2>🏠 Welcome to Cultural Chronicles</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🌟 About Our Archive</h3>
        <p>Cultural Chronicles is a multilingual storytelling archive dedicated to preserving India's rich oral and cultural heritage. 
        Our platform empowers communities to share their folk tales, traditions, and cultural stories in their native languages.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check AI availability and show appropriate message
        try:
            from models.ai_handler import TRANSFORMERS_AVAILABLE
            ai_available = TRANSFORMERS_AVAILABLE
        except ImportError:
            ai_available = False
        
        if ai_available:
            ai_features_text = """
            <div class="feature-card">
            <h3>🤖 AI-Powered Features</h3>
            <ul>
            <li><strong>Advanced Language Detection</strong>: Deep learning models identify the language of your story</li>
            <li><strong>Smart Translation</strong>: Stories are automatically translated to English using transformer models</li>
            <li><strong>Story Classification</strong>: AI categorizes stories by genre and cultural themes</li>
            <li><strong>Multilingual Support</strong>: Support for various Indian languages and scripts</li>
            </ul>
            </div>
            """
        else:
            ai_features_text = """
            <div class="feature-card">
            <h3>🤖 Smart Features</h3>
            <ul>
            <li><strong>Pattern-Based Language Detection</strong>: System identifies common Indian languages</li>
            <li><strong>Story Classification</strong>: Intelligent categorization by cultural themes</li>
            <li><strong>Multilingual Support</strong>: Support for various Indian languages and scripts</li>
            <li><strong>Cultural Preservation</strong>: Stories are organized and preserved for future generations</li>
            </ul>
            </div>
            """
        
        st.markdown(ai_features_text, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h3>📖 How It Works</h3>
        <ol>
        <li><strong>Share Your Story</strong>: Submit folk tales, traditions, or cultural stories in your native language</li>
        <li><strong>Add Context</strong>: Upload optional images of rituals, events, or local settings</li>
        <li><strong>AI Processing</strong>: Our AI models detect language, translate, and categorize your story</li>
        <li><strong>Preserve Heritage</strong>: Your story becomes part of our growing cultural archive</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card"><h3>📊 Archive Statistics</h3></div>', unsafe_allow_html=True)
        
        try:
            from utils.cache_manager import get_cached_statistics
            stats = get_cached_statistics()  # Use ultra-fast cached statistics
        except Exception as e:
            st.error(f"Unable to load statistics: {str(e)}")
            stats = {"total_stories": 0, "unique_languages": 0, "stories_with_images": 0, "recent_languages": []}
        
        st.markdown(f'<div class="stat-card"><h2>{stats.get("total_stories", 0)}</h2><p>Total Stories</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card"><h2>{stats.get("unique_languages", 0)}</h2><p>Languages Detected</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card"><h2>{stats.get("stories_with_images", 0)}</h2><p>Stories with Images</p></div>', unsafe_allow_html=True)
        
        if stats.get('recent_languages'):
            st.markdown('<div class="feature-card"><h4>🌍 Recent Languages</h4></div>', unsafe_allow_html=True)
            for lang in stats.get('recent_languages', [])[:5]:
                st.markdown(f'<div class="stat-card" style="margin: 0.3rem 0; text-align: left; padding: 0.5rem;"><span style="font-size: 16px;">🗣️ {lang}</span></div>', unsafe_allow_html=True)

def show_search():
    st.markdown('<div class="feature-card"><h2>🔍 Search Stories</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("🔎 Search stories by title, content, or language...", placeholder="Enter your search terms here")
    
    with col2:
        search_type = st.selectbox("📂 Search in:", ["All", "Title", "Content", "Language"])
    
    if search_query:
        try:
            from utils.cache_manager import get_cached_search_results
            results = get_cached_search_results(search_query, search_type.lower())  # Use ultra-fast cached search
            
            if results is not None and not results.empty:
                st.success(f"🎯 Found {len(results)} stories matching '{search_query}'")
                
                for _, story in results.iterrows():
                    with st.expander(f"📖 {story['title']} ({story['detected_language']})", expanded=False):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown("**📝 Original Story:**")
                            st.write(story['original_text'][:300] + "..." if len(story['original_text']) > 300 else story['original_text'])
                            
                            if pd.notna(story.get('translated_text')):
                                st.markdown("**🌐 English Translation:**")
                                st.write(story['translated_text'][:300] + "..." if len(story['translated_text']) > 300 else story['translated_text'])
                        
                        with col2:
                            st.markdown(f'<div class="stat-card" style="margin: 0.2rem 0; padding: 0.5rem; text-align: left;"><strong>🌍 Language:</strong> {story["detected_language"]}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="stat-card" style="margin: 0.2rem 0; padding: 0.5rem; text-align: left;"><strong>📂 Category:</strong> {story.get("category", "Unknown")}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="stat-card" style="margin: 0.2rem 0; padding: 0.5rem; text-align: left;"><strong>📅 Date:</strong> {story.get("timestamp", "Unknown")[:10]}</div>', unsafe_allow_html=True)
                            
                            if pd.notna(story.get('image_path')) and os.path.exists(story['image_path']):
                                st.image(story['image_path'], width=150)
            else:
                st.info("🔍 No stories found matching your search criteria. Try different keywords or search type.")
        except Exception as e:
            st.error(f"❌ Search failed: {str(e)}")
            st.info("💡 Please try again or contact support if the issue persists.")

if __name__ == "__main__":
    main()
