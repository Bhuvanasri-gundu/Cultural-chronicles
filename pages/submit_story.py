"""
Submit Story Page - Cultural Chronicles

This module handles the story submission interface where users can:
- Enter story details (title and content)
- Upload cultural images
- Provide additional metadata (region, community, story type)
- Submit stories for AI processing and database storage
"""

import streamlit as st
import os
from datetime import datetime
from utils.data_manager import DataManager
from utils.image_handler import handle_image_upload
from models.ai_handler import detect_language, classify_story

def show_submit_story():
    """Display the story submission form with all required fields and validation"""
    
    st.markdown('<div class="section-header"><h2>📝 Submit Your Cultural Story</h2></div>', unsafe_allow_html=True)
    
    # Initialize data manager
    try:
        dm = DataManager()
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        st.info("💡 Please check your database configuration and try again.")
        return
    
    # Story Details Section
    st.markdown('<div class="section-header"><h3>📖 Story Details</h3></div>', unsafe_allow_html=True)
    
    with st.form("story_submission_form", clear_on_submit=True):
        # Title input
        title = st.text_input(
            "📚 Story Title *",
            placeholder="Enter the title of your cultural story...",
            help="Provide a descriptive title for your story"
        )
        
        # Content input
        content = st.text_area(
            "📝 Story Content *",
            placeholder="Share your cultural story, folk tale, tradition, or recipe in your preferred language...",
            height=200,
            help="Write your story in any Indian language or English. Our AI will detect the language automatically."
        )
        
        # Language hint
        language_hint = st.selectbox(
            "🌍 Language Hint (Optional)",
            ["Auto-detect", "Hindi", "Telugu", "Tamil", "Malayalam", "Kannada", "Bengali", 
             "Gujarati", "Punjabi", "Odia", "English", "Other"],
            help="Help our AI by providing a language hint (optional)"
        )
        
        # Add Images Section
        st.markdown('<div class="section-header"><h3>🖼️ Add Images</h3></div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "📷 Upload Cultural Image (Optional)",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
            help="Upload an image related to your story (festivals, rituals, food, etc.)"
        )
        
        # Image preview
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Image Preview", width=300)
        
        # Additional Information Section
        st.markdown('<div class="section-header"><h3>ℹ️ Additional Information</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            region = st.text_input(
                "🗺️ Region/State",
                placeholder="e.g., Kerala, Punjab, Bengal...",
                help="Specify the geographical region associated with this story"
            )
            
            story_type = st.selectbox(
                "📂 Story Type",
                ["Folk Tale", "Legend", "Tradition", "Festival", "Recipe", 
                 "Historical Account", "Religious Story", "Song", "Other"],
                help="Select the type of cultural content"
            )
        
        with col2:
            community = st.text_input(
                "👥 Community/Culture",
                placeholder="e.g., Bengali, Tamil, Tribal...",
                help="Specify the community or cultural group"
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "🚀 Submit Story",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # Validate required fields
            if not title.strip():
                st.error("❌ Please provide a story title")
                return
            
            if not content.strip():
                st.error("❌ Please provide story content")
                return
            
            # Show processing message
            with st.spinner("🤖 Processing your story with AI..."):
                try:
                    # Handle image upload
                    image_path = None
                    if uploaded_file is not None:
                        image_path = handle_image_upload(uploaded_file)
                        if not image_path:
                            st.warning("⚠️ Image upload failed, but story will be saved without image")
                    
                    # AI Processing
                    detected_language = detect_language(
                        content, 
                        language_hint if language_hint != "Auto-detect" else None
                    )
                    
                    category = classify_story(content, title)
                    
                    # Prepare story data
                    story_data = {
                        'title': title.strip(),
                        'original_text': content.strip(),
                        'translated_text': None,  # TODO: Add translation functionality
                        'detected_language': detected_language,
                        'category': category,
                        'region': region.strip() if region.strip() else None,
                        'community': community.strip() if community.strip() else None,
                        'story_type': story_type,
                        'language_hint': language_hint if language_hint != "Auto-detect" else None,
                        'image_path': image_path,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Save to database
                    if dm.save_story(story_data):
                        st.success("🎉 Story submitted successfully!")
                        st.balloons()
                        
                        # Show processing results
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"🔍 **Detected Language:** {detected_language}")
                            st.info(f"📂 **Category:** {category}")
                        with col2:
                            if image_path:
                                st.info("📷 **Image:** Uploaded successfully")
                            st.info(f"📅 **Saved:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                        
                        # Clear cache to reflect new data
                        st.cache_resource.clear()
                        
                        # Suggest next actions
                        st.markdown("### 🎯 What's Next?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("📚 Browse All Stories", use_container_width=True):
                                st.switch_page("pages/browse_stories.py")
                        with col2:
                            if st.button("🔍 Search Stories", use_container_width=True):
                                st.switch_page("app.py")  # This will redirect to search
                        
                    else:
                        st.error("❌ Failed to save story. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error processing story: {str(e)}")
                    st.info("💡 Please check your input and try again.")

    # Help section
    with st.expander("ℹ️ Need Help?", expanded=False):
        st.markdown("""
        ### 📖 Submission Guidelines
        
        **Story Content:**
        - Share authentic cultural stories, folk tales, traditions, or recipes
        - Write in your preferred Indian language or English
        - Include cultural context and significance
        
        **Images:**
        - Upload relevant cultural images (festivals, rituals, food, etc.)
        - Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP
        - Images will be automatically optimized
        
        **Cultural Sensitivity:**
        - Respect cultural traditions and communities
        - Ensure you have permission to share cultural content
        - Provide accurate information about cultural practices
        
        **AI Processing:**
        - Our AI automatically detects the language of your story
        - Stories are categorized by cultural themes
        - All content is preserved in its original form
        """)
    
    # Show recent submissions
    try:
        recent_stories = dm.get_recent_stories(limit=3)
        if not recent_stories.empty:
            st.markdown("### 📖 Recent Submissions")
            for _, story in recent_stories.iterrows():
                with st.container():
                    st.markdown(f"**{story['title']}** ({story['detected_language']}) - {story['timestamp'][:10]}")
                    st.caption(f"Category: {story.get('category', 'Unknown')} | Region: {story.get('region', 'Unknown')}")
    except Exception:
        pass  # Silently ignore if recent stories can't be loaded
