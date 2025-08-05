"""
Browse Stories Page - Cultural Chronicles

This module handles the story browsing interface with advanced filtering,
sorting, and pagination capabilities for exploring the cultural heritage archive.
"""

import streamlit as st
import pandas as pd
import os
from utils.data_manager import DataManager

def show_browse_stories():
    """Display the story browsing interface with filters and pagination"""
    
    st.markdown('<div class="section-header"><h2>📚 Browse Cultural Stories</h2></div>', unsafe_allow_html=True)
    
    # Initialize data manager
    try:
        dm = DataManager()
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        return
    
    # Get all stories for filtering
    try:
        all_stories = dm.get_all_stories()
        if all_stories.empty:
            st.info("📭 No stories found in the archive. Be the first to submit a story!")
            if st.button("➕ Submit Your Story", type="primary"):
                st.switch_page("pages/submit_story.py")
            return
    except Exception as e:
        st.error(f"❌ Failed to load stories: {str(e)}")
        return
    
    # Filters Section
    st.markdown('<div class="section-header"><h3>🔍 Filters</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Language filter
        languages = ['All'] + sorted(all_stories['detected_language'].dropna().unique().tolist())
        selected_language = st.selectbox("🌍 Language", languages)
    
    with col2:
        # Category filter
        categories = ['All'] + sorted(all_stories['category'].dropna().unique().tolist())
        selected_category = st.selectbox("📂 Category", categories)
    
    with col3:
        # Story type filter
        story_types = ['All'] + sorted(all_stories['story_type'].dropna().unique().tolist())
        selected_story_type = st.selectbox("📖 Story Type", story_types)
    
    with col4:
        # Region filter
        regions = ['All'] + sorted(all_stories['region'].dropna().unique().tolist())
        selected_region = st.selectbox("🗺️ Region", regions)
    
    # Sort options
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        sort_by = st.selectbox(
            "📊 Sort by",
            ["Recent", "Title", "Language", "Category", "Region"]
        )
    
    with col2:
        sort_order = st.selectbox("📈 Order", ["Descending", "Ascending"])
    
    with col3:
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.rerun()
    
    # Apply filters
    filtered_stories = all_stories.copy()
    
    if selected_language != 'All':
        filtered_stories = filtered_stories[filtered_stories['detected_language'] == selected_language]
    
    if selected_category != 'All':
        filtered_stories = filtered_stories[filtered_stories['category'] == selected_category]
    
    if selected_story_type != 'All':
        filtered_stories = filtered_stories[filtered_stories['story_type'] == selected_story_type]
    
    if selected_region != 'All':
        filtered_stories = filtered_stories[filtered_stories['region'] == selected_region]
    
    # Apply sorting
    if sort_by == "Recent":
        sort_column = 'timestamp'
    elif sort_by == "Title":
        sort_column = 'title'
    elif sort_by == "Language":
        sort_column = 'detected_language'
    elif sort_by == "Category":
        sort_column = 'category'
    else:  # Region
        sort_column = 'region'
    
    ascending = sort_order == "Ascending"
    if isinstance(filtered_stories, pd.DataFrame):
        filtered_stories = filtered_stories.sort_values(by=sort_column, ascending=ascending, na_position='last')
    
    # Display results count
    total_stories = len(filtered_stories)
    st.markdown(f"### 📊 Found {total_stories} stories")
    
    if total_stories == 0:
        st.info("🔍 No stories match your filter criteria. Try adjusting the filters.")
        return
    
    # Pagination
    stories_per_page = 5
    total_pages = (total_stories - 1) // stories_per_page + 1
    
    # Get current page from query parameters or default to 1
    try:
        current_page = int(st.query_params.get("page", "1"))
        current_page = max(1, min(current_page, total_pages))
    except (ValueError, TypeError):
        current_page = 1
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        new_page = st.number_input(
            f"Page (1-{total_pages})",
            min_value=1,
            max_value=total_pages,
            value=current_page,
            key="page_input"
        )
        if new_page != current_page:
            st.query_params.page = str(new_page)
            st.rerun()
    
    # Calculate pagination bounds
    start_idx = (current_page - 1) * stories_per_page
    end_idx = start_idx + stories_per_page
    page_stories = filtered_stories.iloc[start_idx:end_idx]
    
    # Display stories
    for idx, (_, story) in enumerate(page_stories.iterrows()):
        with st.expander(
            f"📖 {story['title']} ({story['detected_language']}) - {story.get('category', 'Unknown')}", 
            expanded=idx == 0  # Expand first story by default
        ):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Story content
                st.markdown("**📝 Original Story:**")
                st.write(story['original_text'])
                
                # Translation if available
                if pd.notna(story.get('translated_text')) and story['translated_text'].strip():
                    st.markdown("**🌐 English Translation:**")
                    st.write(story['translated_text'])
                
                # Metadata
                metadata_items = []
                if pd.notna(story.get('region')):
                    metadata_items.append(f"🗺️ **Region:** {story['region']}")
                if pd.notna(story.get('community')):
                    metadata_items.append(f"👥 **Community:** {story['community']}")
                if pd.notna(story.get('story_type')):
                    metadata_items.append(f"📂 **Type:** {story['story_type']}")
                
                if metadata_items:
                    st.markdown(" | ".join(metadata_items))
            
            with col2:
                # Story details card
                st.markdown(f'<div class="stat-card" style="margin: 0.2rem 0; padding: 0.5rem; text-align: left;"><strong>🌍 Language:</strong><br>{story["detected_language"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stat-card" style="margin: 0.2rem 0; padding: 0.5rem; text-align: left;"><strong>📂 Category:</strong><br>{story.get("category", "Unknown")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="stat-card" style="margin: 0.2rem 0; padding: 0.5rem; text-align: left;"><strong>📅 Date:</strong><br>{story.get("timestamp", "Unknown")[:10]}</div>', unsafe_allow_html=True)
                
                # Display image if available
                if pd.notna(story.get('image_path')) and story['image_path']:
                    if os.path.exists(story['image_path']):
                        st.image(story['image_path'], caption="Cultural Image", width=200)
                    else:
                        st.caption("🖼️ Image not found")
    
    # Pagination controls
    if total_pages > 1:
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if current_page > 1:
                if st.button("⏮️ First", key=f"first_page_{current_page}", use_container_width=True):
                    st.query_params.page = "1"
                    st.rerun()
            else:
                st.empty()
        
        with col2:
            if current_page > 1:
                if st.button("◀️ Previous", key=f"prev_page_{current_page}", use_container_width=True):
                    st.query_params.page = str(current_page - 1)
                    st.rerun()
            else:
                st.empty()
        
        with col3:
            st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)
        
        with col4:
            if current_page < total_pages:
                if st.button("Next ▶️", key=f"next_page_{current_page}", use_container_width=True):
                    st.query_params.page = str(current_page + 1)
                    st.rerun()
            else:
                st.empty()
        
        with col5:
            if current_page < total_pages:
                if st.button("Last ⏭️", key=f"last_page_{current_page}", use_container_width=True):
                    st.query_params.page = str(total_pages)
                    st.rerun()
            else:
                st.empty()
    
    # Summary statistics at bottom
    st.markdown("---")
    st.markdown("### 📊 Browse Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Filtered Stories", total_stories)
    
    with col2:
        unique_languages = filtered_stories['detected_language'].nunique()
        st.metric("🌍 Languages", int(unique_languages))
    
    with col3:
        unique_categories = filtered_stories['category'].nunique()
        st.metric("📂 Categories", int(unique_categories))
    
    with col4:
        stories_with_images = filtered_stories['image_path'].notna().sum()
        st.metric("🖼️ With Images", stories_with_images)
    

