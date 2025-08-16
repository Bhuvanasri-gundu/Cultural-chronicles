"""
Cache Manager - Cultural Chronicles

This module provides ultra-fast caching for data operations to ensure
5-second loading times and responsive user experience.
"""

import streamlit as st
import pandas as pd
import logging
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache configuration for low network optimization
CACHE_TTL = 3600  # 1 hour cache TTL for low network
LONG_CACHE_TTL = 7200  # 2 hours for static data
SEARCH_CACHE_SIZE = 100  # Cache up to 100 recent searches

@st.cache_resource(ttl=CACHE_TTL)
def get_fast_data_manager():
    """
    Get cached data manager instance for ultra-fast access
    
    Returns:
        DataManager: Cached data manager instance
    """
    try:
        from utils.data_manager import DataManager
        dm = DataManager()
        logger.info("Data manager cached successfully")
        return dm
    except Exception as e:
        logger.error(f"Failed to cache data manager: {str(e)}")
        return None

@st.cache_data(ttl=LONG_CACHE_TTL)
def get_cached_statistics() -> Dict[str, Any]:
    """
    Get cached archive statistics for ultra-fast dashboard loading
    
    Returns:
        dict: Cached statistics data
    """
    try:
        dm = get_fast_data_manager()
        if dm:
            stats = dm.get_statistics()
            logger.info("Statistics cached successfully")
            return stats
        else:
            return {"total_stories": 0, "unique_languages": 0, "stories_with_images": 0, "recent_languages": []}
    except Exception as e:
        logger.error(f"Failed to cache statistics: {str(e)}")
        return {"total_stories": 0, "unique_languages": 0, "stories_with_images": 0, "recent_languages": []}

@st.cache_data(ttl=CACHE_TTL)
def get_cached_all_stories() -> pd.DataFrame:
    """
    Get cached all stories data for ultra-fast browsing
    
    Returns:
        pandas.DataFrame: Cached stories data
    """
    try:
        dm = get_fast_data_manager()
        if dm:
            stories = dm.get_all_stories()
            logger.info(f"Cached {len(stories)} stories successfully")
            return stories
        else:
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to cache all stories: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_TTL)
def get_cached_recent_stories(limit: int = 5) -> pd.DataFrame:
    """
    Get cached recent stories for fast dashboard display
    
    Args:
        limit: Number of recent stories to retrieve
        
    Returns:
        pandas.DataFrame: Cached recent stories data
    """
    try:
        dm = get_fast_data_manager()
        if dm:
            stories = dm.get_recent_stories(limit=limit)
            logger.info(f"Cached {len(stories)} recent stories successfully")
            return stories
        else:
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to cache recent stories: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_TTL)
def get_cached_search_results(query: str, search_type: str = "all") -> Optional[pd.DataFrame]:
    """
    Get cached search results for ultra-fast search experience
    
    Args:
        query: Search query string
        search_type: Type of search ('all', 'title', 'content', 'language')
        
    Returns:
        pandas.DataFrame or None: Cached search results
    """
    try:
        dm = get_fast_data_manager()
        if dm:
            results = dm.search_stories(query, search_type)
            logger.info(f"Cached search results for '{query}': {len(results)} matches")
            return results
        else:
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Failed to cache search results: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=LONG_CACHE_TTL)
def get_cached_filter_options() -> Dict[str, list]:
    """
    Get cached filter options for fast filter population
    
    Returns:
        dict: Cached filter options
    """
    try:
        stories_df = get_cached_all_stories()
        if not stories_df.empty:
            filter_options = {
                'languages': sorted(stories_df['detected_language'].dropna().unique().tolist()),
                'categories': sorted(stories_df['category'].dropna().unique().tolist()),
                'story_types': sorted(stories_df['story_type'].dropna().unique().tolist()),
                'regions': sorted(stories_df['region'].dropna().unique().tolist()),
                'communities': sorted(stories_df['community'].dropna().unique().tolist())
            }
            logger.info("Filter options cached successfully")
            return filter_options
        else:
            return {
                'languages': [],
                'categories': [],
                'story_types': [],
                'regions': [],
                'communities': []
            }
    except Exception as e:
        logger.error(f"Failed to cache filter options: {str(e)}")
        return {
            'languages': [],
            'categories': [],
            'story_types': [],
            'regions': [],
            'communities': []
        }

def clear_all_caches():
    """
    Clear all Streamlit caches to force fresh data loading
    """
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
        logger.info("All caches cleared successfully")
    except Exception as e:
        logger.error(f"Failed to clear caches: {str(e)}")

def warm_up_caches():
    """
    Warm up caches by pre-loading commonly accessed data
    """
    try:
        logger.info("Warming up caches...")
        
        # Pre-load data manager
        get_fast_data_manager()
        
        # Pre-load statistics
        get_cached_statistics()
        
        # Pre-load all stories
        get_cached_all_stories()
        
        # Pre-load recent stories
        get_cached_recent_stories()
        
        # Pre-load filter options
        get_cached_filter_options()
        
        logger.info("Cache warm-up completed successfully")
        
    except Exception as e:
        logger.error(f"Cache warm-up failed: {str(e)}")

# Cache invalidation helpers
def invalidate_story_caches():
    """
    Invalidate caches when new stories are added
    """
    try:
        # Clear specific caches that depend on story data
        get_cached_statistics.clear()
        get_cached_all_stories.clear()
        get_cached_recent_stories.clear()
        get_cached_filter_options.clear()
        
        logger.info("Story caches invalidated successfully")
        
    except Exception as e:
        logger.error(f"Failed to invalidate story caches: {str(e)}")

def get_cache_stats():
    """
    Get cache statistics for monitoring and debugging
    
    Returns:
        dict: Cache statistics
    """
    try:
        # This is a placeholder for cache statistics
        # Streamlit doesn't provide direct cache statistics
        return {
            "cache_status": "active",
            "ttl_seconds": CACHE_TTL,
            "last_warmed": "on_app_start"
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {str(e)}")
        return {"cache_status": "error", "error": str(e)}
