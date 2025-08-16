"""
Data Manager - Cultural Chronicles (Fixed)

This module handles all database operations for story management including
CRUD operations, search functionality, and statistics generation.
"""

import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError
from utils.database import get_database_connection, Story
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_, func

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Handles all database operations for cultural stories"""
    
    def __init__(self):
        """Initialize the data manager with database connection"""
        try:
            self.engine = get_database_connection()
            self.Session = sessionmaker(bind=self.engine)
            logger.info("DataManager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DataManager: {str(e)}")
            raise
    
    def save_story(self, story_data):
        """
        Save a new story to the database
        
        Args:
            story_data (dict): Dictionary containing story information
            
        Returns:
            bool: True if successful, False otherwise
        """
        session = self.Session()
        try:
            # Create new story object
            story = Story(
                title=story_data.get('title'),
                original_text=story_data.get('original_text'),
                translated_text=story_data.get('translated_text'),
                detected_language=story_data.get('detected_language'),
                category=story_data.get('category'),
                region=story_data.get('region'),
                community=story_data.get('community'),
                story_type=story_data.get('story_type'),
                language_hint=story_data.get('language_hint'),
                image_path=story_data.get('image_path')
            )
            
            session.add(story)
            session.commit()
            logger.info(f"Successfully saved story: {story_data.get('title')}")
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error saving story: {str(e)}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Unexpected error saving story: {str(e)}")
            return False
        finally:
            session.close()
    
    def _format_timestamp(self, timestamp):
        """Helper method to safely format timestamp"""
        try:
            return timestamp.isoformat() if timestamp is not None else None
        except (AttributeError, TypeError):
            return None
    
    def get_all_stories(self):
        """
        Retrieve all stories from the database
        
        Returns:
            pandas.DataFrame: DataFrame containing all stories
        """
        session = self.Session()
        try:
            stories = session.query(Story).order_by(Story.timestamp.desc()).all()
            
            # Convert to DataFrame
            data = []
            for story in stories:
                data.append({
                    'id': story.id,
                    'title': story.title,
                    'original_text': story.original_text,
                    'translated_text': story.translated_text,
                    'detected_language': story.detected_language,
                    'category': story.category,
                    'region': story.region,
                    'community': story.community,
                    'story_type': story.story_type,
                    'language_hint': story.language_hint,
                    'image_path': story.image_path,
                    'timestamp': self._format_timestamp(story.timestamp)
                })
            
            return pd.DataFrame(data)
            
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving stories: {str(e)}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Unexpected error retrieving stories: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def search_stories(self, query, search_type="all"):
        """
        Search stories based on query and search type
        
        Args:
            query (str): Search query
            search_type (str): Type of search - 'all', 'title', 'content', 'language'
            
        Returns:
            pandas.DataFrame: DataFrame containing matching stories
        """
        session = self.Session()
        try:
            # Build search query based on type
            query_lower = query.lower()
            
            if search_type == "title":
                stories = session.query(Story).filter(
                    func.lower(Story.title).contains(query_lower)
                ).order_by(Story.timestamp.desc()).all()
            elif search_type == "content":
                stories = session.query(Story).filter(
                    func.lower(Story.original_text).contains(query_lower)
                ).order_by(Story.timestamp.desc()).all()
            elif search_type == "language":
                stories = session.query(Story).filter(
                    func.lower(Story.detected_language).contains(query_lower)
                ).order_by(Story.timestamp.desc()).all()
            else:  # search_type == "all"
                stories = session.query(Story).filter(
                    or_(
                        func.lower(Story.title).contains(query_lower),
                        func.lower(Story.original_text).contains(query_lower),
                        func.lower(Story.detected_language).contains(query_lower),
                        func.lower(Story.category).contains(query_lower),
                        func.lower(Story.region).contains(query_lower),
                        func.lower(Story.community).contains(query_lower)
                    )
                ).order_by(Story.timestamp.desc()).all()
            
            # Convert to DataFrame
            data = []
            for story in stories:
                data.append({
                    'id': story.id,
                    'title': story.title,
                    'original_text': story.original_text,
                    'translated_text': story.translated_text,
                    'detected_language': story.detected_language,
                    'category': story.category,
                    'region': story.region,
                    'community': story.community,
                    'story_type': story.story_type,
                    'language_hint': story.language_hint,
                    'image_path': story.image_path,
                    'timestamp': self._format_timestamp(story.timestamp)
                })
            
            return pd.DataFrame(data)
            
        except SQLAlchemyError as e:
            logger.error(f"Database error searching stories: {str(e)}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Unexpected error searching stories: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def get_recent_stories(self, limit=5):
        """
        Get recent stories from the database
        
        Args:
            limit (int): Number of recent stories to retrieve
            
        Returns:
            pandas.DataFrame: DataFrame containing recent stories
        """
        session = self.Session()
        try:
            stories = session.query(Story).order_by(Story.timestamp.desc()).limit(limit).all()
            
            # Convert to DataFrame
            data = []
            for story in stories:
                data.append({
                    'id': story.id,
                    'title': story.title,
                    'original_text': story.original_text,
                    'detected_language': story.detected_language,
                    'category': story.category,
                    'region': story.region,
                    'timestamp': self._format_timestamp(story.timestamp)
                })
            
            return pd.DataFrame(data)
            
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving recent stories: {str(e)}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Unexpected error retrieving recent stories: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def get_statistics(self):
        """
        Get archive statistics
        
        Returns:
            dict: Dictionary containing various statistics
        """
        session = self.Session()
        try:
            # Total stories
            total_stories = session.query(Story).count()
            
            # Unique languages
            unique_languages = session.query(Story.detected_language).distinct().count()
            
            # Stories with images
            stories_with_images = session.query(Story).filter(Story.image_path.isnot(None)).count()
            
            # Recent languages (last 10 stories)
            recent_stories = session.query(Story.detected_language)\
                .order_by(Story.timestamp.desc())\
                .limit(10).all()
            
            recent_languages = list(set([story[0] for story in recent_stories if story[0]]))
            
            return {
                'total_stories': total_stories,
                'unique_languages': unique_languages,
                'stories_with_images': stories_with_images,
                'recent_languages': recent_languages
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving statistics: {str(e)}")
            return {'total_stories': 0, 'unique_languages': 0, 'stories_with_images': 0, 'recent_languages': []}
        except Exception as e:
            logger.error(f"Unexpected error retrieving statistics: {str(e)}")
            return {'total_stories': 0, 'unique_languages': 0, 'stories_with_images': 0, 'recent_languages': []}
        finally:
            session.close()
    
    def get_story_by_id(self, story_id):
        """
        Get a specific story by ID
        
        Args:
            story_id (int): ID of the story to retrieve
            
        Returns:
            dict or None: Story data if found, None otherwise
        """
        session = self.Session()
        try:
            story = session.query(Story).filter(Story.id == story_id).first()
            
            if story:
                return {
                    'id': story.id,
                    'title': story.title,
                    'original_text': story.original_text,
                    'translated_text': story.translated_text,
                    'detected_language': story.detected_language,
                    'category': story.category,
                    'region': story.region,
                    'community': story.community,
                    'story_type': story.story_type,
                    'language_hint': story.language_hint,
                    'image_path': story.image_path,
                    'timestamp': self._format_timestamp(story.timestamp)
                }
            
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving story {story_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving story {story_id}: {str(e)}")
            return None
        finally:
            session.close()